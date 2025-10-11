"""Main script for performing record linkage on two datasets.

This script orchestrates the entire record linkage workflow, which consists of
the following steps:

1.  **Data Loading**: Loads two datasets (A and B) and a truth file containing
    known matches from CSV files.
2.  **Blocking**: Reduces the number of candidate pairs by grouping records into
    blocks based on shared characteristics. This implementation uses a multi-pass
    approach, combining phonetic and simple blocking methods.
3.  **Comparison**: Computes similarity vectors for the candidate pairs generated
    in the blocking step. This is done on the GPU for performance.
4.  **Classification**: Uses a supervised machine learning model (Random Forest) to
    classify candidate pairs as matches or non-matches based on their
    similarity vectors.
5.  **Evaluation**: Assesses the quality of the linkage by comparing the results
    against the ground truth data, calculating metrics for both the blocking and
    classification steps.
6.  **Save Results**: Saves the final set of matched pairs to a CSV file.
"""

import argparse
import time
import logging
import loadDataset
import blocking
import comparison
import classification
import evaluation
import cudf
import saveLinkResult
from config import LOG_LEVEL, LOG_FORMAT

# conda run -n rapids-rl python src/recordLinkage.py very-dirty_100000

# --- Setup Logging ---
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

# =============================================================================
# Main program execution
# =============================================================================
def main():
    """Main program execution.

    Orchestrates the record linkage workflow from data loading to evaluation and
    saving the final results.
    """
    parser = argparse.ArgumentParser(description='GPU-based record linkage pipeline.')
    parser.add_argument(
        'dataset',
        nargs='?',
        default='clean_100000',
        help='Dataset preset to use (e.g. -clean_100000, -very-dirty_100000, clean_100000).',
    )
    args = parser.parse_args()

    dataset_key = args.dataset.lstrip('-').lower()
    dataset_configs = {
        'clean_100000': {
            'datasetA_name': './datasets/comp3430_comp8430-rl-additional-datasets/clean-A-100000.csv',
            'datasetB_name': './datasets/comp3430_comp8430-rl-additional-datasets/clean-B-100000.csv',
            'truthfile_name': './datasets/comp3430_comp8430-rl-additional-datasets/clean-true-matches-100000.csv',
        },
        'very-dirty_100000': {
            'datasetA_name': './datasets/comp3430_comp8430-rl-additional-datasets/very-dirty-A-100000.csv',
            'datasetB_name': './datasets/comp3430_comp8430-rl-additional-datasets/very-dirty-B-100000.csv',
            'truthfile_name': './datasets/comp3430_comp8430-rl-additional-datasets/very-dirty-true-matches-100000.csv',
        },
    }
    if dataset_key not in dataset_configs:
        available = ', '.join(sorted(dataset_configs.keys()))
        raise ValueError(f'Unknown dataset preset "{dataset_key}". Available options: {available}')

    datasetA_name = dataset_configs[dataset_key]['datasetA_name']
    datasetB_name = dataset_configs[dataset_key]['datasetB_name']
    truthfile_name = dataset_configs[dataset_key]['truthfile_name']

    # The list of tuples (comparison function, attribute name in record A,
    # attribute name in record B)
    # Prefer GPU-enabled comparison functions to keep large batches on device.
    approx_comp_funct_list = [
        (comparison.jaccard_comp_gpu, 'first_name', 'first_name'),
        (comparison.dice_comp_gpu, 'middle_name', 'middle_name'),
        (comparison.jaro_winkler_comp_gpu, 'last_name', 'last_name'),
        (comparison.levenshtein_comp_gpu, 'street_address', 'street_address'),
        (comparison.levenshtein_comp_gpu, 'suburb', 'suburb'),
        (comparison.exact_comp, 'state', 'state'),
        (comparison.gender_comp, 'gender', 'gender'),
        (comparison.date_digits_comp, 'birth_date', 'birth_date'),
        (comparison.postcode_exact_comp, 'postcode', 'postcode'),
        (comparison.phone_suffix_comp, 'phone', 'phone'),
    ]

    attr_list = ['first_name', 'middle_name', 'last_name', 'gender', 'birth_date', 'street_address', 'suburb', 'postcode', 'state', 'phone']

    # =============================================================================
    # Step 1: Load the two datasets from CSV files
    start_time = time.time()

    recA_gdf = loadDataset.load_data_set(datasetA_name, 'rec_id', attr_list)
    recB_gdf = loadDataset.load_data_set(datasetB_name, 'rec_id', attr_list)
    true_match_set = loadDataset.load_truth_data(truthfile_name)

    loading_time = time.time() - start_time
    logging.info(f"Data loading took {loading_time:.3f} seconds.")

    # -----------------------------------------------------------------------------
    # Step 2: Block the datasets
    start_time = time.time()

    # --- Partitioning Pass: simple blocking on state ---
    logging.info('Partitioning datasets by state...')
    partition_attr = ['state']
    state_blocks_A = blocking.simpleBlocking(recA_gdf, partition_attr)
    state_blocks_B = blocking.simpleBlocking(recB_gdf, partition_attr)

    all_candidate_pairs_list = []

    # --- ANN Candidate Generation within each partition ---
    logging.info('Running ANN candidate generation within each state partition...')
    ann_attrs = ['first_name', 'last_name', 'suburb']
    K_NEIGHBORS = 25

    # Get a set of common state keys to iterate over
    common_states = set(state_blocks_A.keys()) & set(state_blocks_B.keys())

    for i, state_key in enumerate(common_states):
        logging.info(f'  Processing partition {i+1}/{len(common_states)}: {state_key}')

        rec_ids_A = state_blocks_A[state_key]
        rec_ids_B = state_blocks_B[state_key]

        # Filter main GDFs to get records for the current state
        temp_gdf_A = recA_gdf.loc[rec_ids_A]
        temp_gdf_B = recB_gdf.loc[rec_ids_B]

        # Generate candidate pairs for the partition using ANN search
        partition_pairs_gdf = blocking.ann_candidate_generation(temp_gdf_A, temp_gdf_B, k=K_NEIGHBORS, blk_attr_list=ann_attrs)
        all_candidate_pairs_list.append(partition_pairs_gdf)

    # Combine candidate pairs from all partitions
    candidate_pairs_gdf = cudf.concat(all_candidate_pairs_list, ignore_index=True)
    candidate_pairs_gdf = candidate_pairs_gdf.drop_duplicates()
    
    logging.info(f"Total candidate pairs generated from ANN blocking: {len(candidate_pairs_gdf)}")

    blocking_time = time.time() - start_time
    logging.info(f"Data blocking took {blocking_time:.3f} seconds.")
    # Note: printBlockStatistics is not applicable to the new pair-based approach

    # -----------------------------------------------------------------------------
    # Step 3: Compare the candidate pairs
    start_time = time.time()

    sim_vectors_gdf = comparison.compare_pairs(candidate_pairs_gdf, recA_gdf, recB_gdf, \
                                               approx_comp_funct_list)

    dataset_category = 'clean' if 'clean-' in datasetA_name else \
                       'very_dirty' if 'very-dirty-' in datasetA_name else \
                       'unknown'

    def _apply_high_precision_filters(sim_vectors):
        """Prune candidate pairs that lack agreement on high-signal identifiers."""
        required_cols = {
            'sim_postcode',
            'sim_phone',
            'sim_birth_date',
            'sim_gender',
            'sim_first_name',
            'sim_last_name',
            'sim_street_address',
            'sim_suburb',
        }
        if sim_vectors.empty:
            return sim_vectors

        available_cols = set(sim_vectors.columns)
        if not required_cols.issubset(available_cols):
            logging.warning('Precision filters skipped (missing columns: %s)',
                            ', '.join(sorted(required_cols - available_cols)))
            return sim_vectors

        first_col = sim_vectors['sim_first_name']
        last_col = sim_vectors['sim_last_name']
        postcode_col = sim_vectors['sim_postcode']
        suburb_col = sim_vectors['sim_suburb']
        address_col = sim_vectors['sim_street_address']
        phone_col = sim_vectors['sim_phone']
        birth_col = sim_vectors['sim_birth_date']
        gender_col = sim_vectors['sim_gender']

        if dataset_category == 'clean':
            first_good = first_col >= 0.75
            last_good = last_col >= 0.90
            location_strong = (postcode_col >= 0.99) & (suburb_col >= 0.95)
            address_strong = address_col >= 0.90
            suburb_tight = suburb_col >= 0.97
            phone_strong = phone_col >= 0.90
            birth_strong = birth_col >= 0.99
            gender_match = gender_col >= 0.90

            keep_mask = (
                (location_strong & last_good & (first_good | address_strong | phone_strong | birth_strong | gender_match))
                | (phone_strong & last_good & (first_good | gender_match))
                | (birth_strong & last_good & (first_good | gender_match))
                | (address_strong & suburb_tight & last_good)
            )

        elif dataset_category == 'very_dirty':
            first_loose = first_col >= 0.70
            last_loose = last_col >= 0.80
            postcode_relaxed = postcode_col >= 0.95
            suburb_relaxed = suburb_col >= 0.90
            address_relaxed = address_col >= 0.82
            phone_relaxed = phone_col >= 0.85
            birth_relaxed = birth_col >= 0.99
            gender_relaxed = gender_col >= 0.95

            location_combo = postcode_relaxed & suburb_relaxed & last_loose
            phone_combo = phone_relaxed & first_loose & last_loose
            address_combo = address_relaxed & suburb_relaxed & last_loose
            birth_combo = birth_relaxed & last_loose & (first_loose | gender_relaxed)

            keep_mask = location_combo | phone_combo | address_combo | birth_combo
        else:
            postcode_match = postcode_col >= 0.99
            phone_match = phone_col >= 0.85
            birthdate_name_match = (birth_col >= 0.99) & ((first_col >= 0.70) | (last_col >= 0.80))
            address_match = (address_col >= 0.85) & (suburb_col >= 0.95)
            gender_aux = (gender_col >= 0.99) & (last_col >= 0.80)
            keep_mask = postcode_match | phone_match | birthdate_name_match | address_match | gender_aux

        filtered = sim_vectors[keep_mask]
        logging.info('Precision filters (%s) kept %d of %d candidate pairs (%.2f%%).',
                     dataset_category,
                     len(filtered), len(sim_vectors),
                     100.0 * len(filtered) / max(1, len(sim_vectors)))
        return filtered.reset_index(drop=True)

    sim_vectors_gdf = _apply_high_precision_filters(sim_vectors_gdf)

    comparison_time = time.time() - start_time
    logging.info(f"Data comparison took {comparison_time:.3f} seconds.")

    # Exit if no candidate pairs were generated
    if sim_vectors_gdf.empty:
        logging.info("No candidate pairs were generated after blocking. Exiting.")
        return

    # -----------------------------------------------------------------------------
    # Step 4: Classify the candidate pairs
    start_time = time.time()

    class_match_set, class_nonmatch_set = \
               classification.supervisedMLClassify(sim_vectors_gdf, true_match_set)

    classification_time = time.time() - start_time
    logging.info(f"Data classification took {classification_time:.3f} seconds.")

    # -----------------------------------------------------------------------------
    # Step 5: Evaluate the classification
    num_comparisons = len(sim_vectors_gdf)
    all_comparisons = len(recA_gdf) * len(recB_gdf)

    evaluation.evaluate_blocking(sim_vectors_gdf, true_match_set, num_comparisons, all_comparisons)
    evaluation.evaluate_linkage(class_match_set, class_nonmatch_set, true_match_set, all_comparisons)

    linkage_time = loading_time + blocking_time + comparison_time + classification_time
    logging.info(f'Total runtime required for linkage: {linkage_time:.3f} sec')

    # -----------------------------------------------------------------------------
    # Step 6: Save the linkage result
    saveLinkResult.save_linkage_set('./out/matches.csv', class_match_set)

if __name__ == "__main__":
    main()
