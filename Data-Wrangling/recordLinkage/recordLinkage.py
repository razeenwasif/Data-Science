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

# conda run -n rapids-25.08 python3 recordLinkage.py

# --- Setup Logging ---
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

# =============================================================================
# Main program execution
# =============================================================================
def main():
    # Variable names for loading datasets
    datasetA_name = 'datasets/clean-A-10000.csv'
    datasetB_name = 'datasets/clean-B-10000.csv'
    truthfile_name = 'datasets/clean-true-matches-10000.csv'

    # The list of tuples (comparison function, attribute name in record A,
    # attribute name in record B)
    approx_comp_funct_list = [(comparison.jaccard_comp, 'first_name', 'first_name'),
                              (comparison.dice_comp, 'middle_name', 'middle_name'),
                              (comparison.jaro_winkler_comp, 'last_name', 'last_name'),
                              (comparison.edit_dist_sim_comp, 'suburb', 'suburb'),
                              (comparison.exact_comp, 'state', 'state'),
                             ]

    attr_list = ['first_name', 'middle_name', 'last_name', 'gender', 'birth_date', 'street_address', 'suburb', 'postcode', 'state', 'phone']

    # =============================================================================
    # Step 1: Load the two datasets from CSV files
    start_time = time.time()

    recA_dict = loadDataset.load_data_set(datasetA_name, 'rec_id', attr_list)
    recB_dict = loadDataset.load_data_set(datasetB_name, 'rec_id', attr_list)
    true_match_set = loadDataset.load_truth_data(truthfile_name)

    loading_time = time.time() - start_time
    logging.info(f"Data loading took {loading_time:.3f} seconds.")

    # -----------------------------------------------------------------------------
    # Step 2: Block the datasets
    start_time = time.time()

    recA_gdf = cudf.DataFrame.from_dict(recA_dict, orient='index')
    recB_gdf = cudf.DataFrame.from_dict(recB_dict, orient='index')

    canopy_attr_list = ['first_name', 'last_name']
    T1 = 0.8 # Loose Threshold (distance)
    T2 = 0.4 # Tight Threshold (distance)
    blockA_dict = blocking.canopy_clustering(recA_gdf, canopy_attr_list, T1, T2)
    blockB_dict = blocking.canopy_clustering(recB_gdf, canopy_attr_list, T1, T2)

    blocking_time = time.time() - start_time
    logging.info(f"Data blocking took {blocking_time:.3f} seconds.")
    blocking.printBlockStatistics(blockA_dict, blockB_dict)

    # -----------------------------------------------------------------------------
    # Step 3: Compare the candidate pairs
    start_time = time.time()

    sim_vec_dict = comparison.compareBlocks(blockA_dict, blockB_dict, \
                                            recA_gdf, recB_gdf, \
                                            approx_comp_funct_list)

    comparison_time = time.time() - start_time
    logging.info(f"Data comparison took {comparison_time:.3f} seconds.")

    # -----------------------------------------------------------------------------
    # Step 4: Classify the candidate pairs
    start_time = time.time()

    class_match_set, class_nonmatch_set = \
               classification.supervisedMLClassify(sim_vec_dict, true_match_set)

    classification_time = time.time() - start_time
    logging.info(f"Data classification took {classification_time:.3f} seconds.")

    # -----------------------------------------------------------------------------
    # Step 5: Evaluate the classification
    num_comparisons = len(sim_vec_dict)
    all_comparisons = len(recA_dict) * len(recB_dict)
    cand_rec_id_pair_list = sim_vec_dict.keys()

    evaluation.evaluate_blocking(cand_rec_id_pair_list, true_match_set, num_comparisons, all_comparisons)
    evaluation.evaluate_linkage(class_match_set, class_nonmatch_set, true_match_set, all_comparisons)

    linkage_time = loading_time + blocking_time + comparison_time + classification_time
    logging.info(f'Total runtime required for linkage: {linkage_time:.3f} sec')

    # -----------------------------------------------------------------------------
    # Step 6: Save the linkage result
    saveLinkResult.save_linkage_set('matches.csv', class_match_set)

if __name__ == "__main__":
    main()

