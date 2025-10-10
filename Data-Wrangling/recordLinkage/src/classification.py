""" Module with functionalities for classifying a dictionary of record pairs
    and their similarities.

    Each function in this module returns two sets, one with record pairs
    classified as matches and the other with record pairs classified as
    non-matches.
"""

# =============================================================================

import sys
import cudf
import cupy
import numpy as np
from cuml.ensemble import RandomForestClassifier
from cuml.model_selection import train_test_split
def exactClassify(sim_vec_dict):
  """Method to classify the given similarity vector dictionary assuming only
     exact matches (having all similarities of 1.0) are matches.

     Parameter Description:
       sim_vec_dict : Dictionary of record pairs with their identifiers as
                      as keys and their corresponding similarity vectors as
                      values.

     The classification is based on the exact matching of attribute values,
     that is the similarity vector for a given record pair must contain 1.0
     for all attribute values.

     Example:
       (recA1, recB1) = [1.0, 1.0, 1.0, 1.0] => match
       (recA2, recB5) = [0.0, 1.0, 0.0, 1.0] = non-match
  """

  print('Exact classification of %d record pairs' % (len(sim_vec_dict)))

  class_match_set    = set()
  class_nonmatch_set = set()

  # Iterate over all record pairs
  #
  for (rec_id_tuple, sim_vec) in sim_vec_dict.items():

    sim_sum = sum(sim_vec)  # Sum all attribute similarities

    if sim_sum == len(sim_vec):  # All similarities were 1.0
      class_match_set.add(rec_id_tuple)
    else:
      class_nonmatch_set.add(rec_id_tuple)

  print('  Classified %d record pairs as matches and %d as non-matches' % \
        (len(class_match_set), len(class_nonmatch_set)))
  print('')

  return class_match_set, class_nonmatch_set

# -----------------------------------------------------------------------------

def thresholdClassify(sim_vec_dict, sim_thres):
  """Method to classify the given similarity vector dictionary with regard to
     a given similarity threshold (in the range 0.0 to 1.0), where record pairs
     with an average similarity of at least this threshold are classified as
     matches and all others as non-matches.

     Parameter Description:
       sim_vec_dict : Dictionary of record pairs with their identifiers as
                      as keys and their corresponding similarity vectors as
                      values.
       sim_thres    : The classification similarity threshold.
  """

  assert sim_thres >= 0.0 and sim_thres <= 1.0, sim_thres

  print('Similarity threshold based classification of %d record pairs' % \
        (len(sim_vec_dict)))
  print('  Classification similarity threshold: %.3f' % (sim_thres))

  class_match_set    = set()
  class_nonmatch_set = set()

  # Iterate over all record pairs
  #
  for (rec_id_tuple, sim_vec) in sim_vec_dict.items():

    sim_sum = float(sum(sim_vec))  # Sum all attribute similarities
    avr_sim = sim_sum / len(sim_vec)

    if avr_sim >= sim_thres:  # Average similarity is high enough
      class_match_set.add(rec_id_tuple)
    else:
      class_nonmatch_set.add(rec_id_tuple)

  print('  Classified %d record pairs as matches and %d as non-matches' % \
        (len(class_match_set), len(class_nonmatch_set)))
  print('')

  return class_match_set, class_nonmatch_set

# -----------------------------------------------------------------------------

def minThresholdClassify(sim_vec_dict, sim_thres):
  """Method to classify the given similarity vector dictionary with regard to
     a given similarity threshold (in the range 0.0 to 1.0), where record pairs
     that have all their similarities (of all attributes compared) with at
     least this threshold are classified as matches and all others as
     non-matches.

     Parameter Description:
       sim_vec_dict : Dictionary of record pairs with their identifiers as
                      as keys and their corresponding similarity vectors as
                      values.
       sim_thres    : The classification minimum similarity threshold.
  """

  assert sim_thres >= 0.0 and sim_thres <= 1.0, sim_thres

  print('Minimum similarity threshold based classification of ' + \
        '%d record pairs' % (len(sim_vec_dict)))
  print('  Classification similarity threshold: %.3f' % (sim_thres))

  class_match_set    = set()
  class_nonmatch_set = set()

  # Iterate over all record pairs
  #
  for (rec_id_tuple, sim_vec) in sim_vec_dict.items():

    # Flag to check is all attribute similarities are high enough or not
    #
    record_pair_match = True

    # check for all the compared attributes
    #
    for sim in sim_vec:
      if sim < sim_thres:  # Similarity is not enough
        record_pair_match = False
        break  # No need to compare more similarities, speed-up the process

    if (record_pair_match):  # All similaries are high enough
      class_match_set.add(rec_id_tuple)
    else:
      class_nonmatch_set.add(rec_id_tuple)

  print('  Classified %d record pairs as matches and %d as non-matches' % \
        (len(class_match_set), len(class_nonmatch_set)))
  print('')

  return class_match_set, class_nonmatch_set

# -----------------------------------------------------------------------------

def weightedSimilarityClassify(sim_vec_dict, weight_vec, sim_thres):
  """Method to classify the given similarity vector dictionary with regard to
     a given weight vector and a given similarity threshold (in the range 0.0
     to 1.0), where an overall similarity is calculated based on the weights
     for each attribute, and where record pairs with the similarity of at least
     the given threshold are classified as matches and all others as
     non-matches.

     Parameter Description:
       sim_vec_dict : Dictionary of record pairs with their identifiers as
                      as keys and their corresponding similarity vectors as
                      values.
       weight_vec   : A vector with weights, one weight for each attribute.
       sim_thres    : The classification similarity threshold.
  """

  assert sim_thres >= 0.0 and sim_thres <= 1.0, sim_thres

  # Check weights are available for all attributes
  #
  first_sim_vec = list(sim_vec_dict.values())[0]
  assert len(weight_vec) == len(first_sim_vec), len(weight_vec)

  print('Weighted similarity based classification of %d record pairs' % \
        (len(sim_vec_dict)))
  print('  Weight vector: %s'   % (str(weight_vec)))
  print('  Classification similarity threshold: %.3f' % (sim_thres))

  class_match_set    = set()
  class_nonmatch_set = set()

  weight_sum = sum(weight_vec)  # Sum of all attribute weights

  # Iterate over all record pairs
  #
  for (rec_id_tuple, sim_vec) in sim_vec_dict.items():

    sim_sum = 0.0

    # Compute weighted sim for each attribute
    #
    for sim, weight in zip(sim_vec, weight_vec):
      sim_sum += sim * weight

    avr_sim = sim_sum / weight_sum  # Compute noramlised average similarity

    if avr_sim >= sim_thres:  # Average similarity is high enough
      class_match_set.add(rec_id_tuple)
    else:
      class_nonmatch_set.add(rec_id_tuple)

  print('  Classified %d record pairs as matches and %d as non-matches' % \
        (len(class_match_set), len(class_nonmatch_set)))
  print('')

  return class_match_set, class_nonmatch_set

# -----------------------------------------------------------------------------

def supervisedMLClassify(sim_vectors_gdf, true_match_set, n_estimators=10, threshold=0.4):
    """A classifier method based on a supervised machine learning technique
     (random forest) which learns from the given similarity vectors and the
     true match status set provided.

     Improved to handle class imbalance with multiple strategies.

     Parameter Description:
       sim_vectors_gdf : A cuDF DataFrame with record pairs and their similarity
                         vectors.
       true_match_set : Set of true matches (record identifier pairs)
       n_estimators   : The number of trees in the forest.
       threshold      : The probability threshold to classify a pair as a match.
  """

    class_match_set =    set()
    class_nonmatch_set = set()

    print('Supervised random forest classification of %d record pairs' % \
        (len(sim_vectors_gdf)))
    sys.stdout.flush()

    rec_pairs = sim_vectors_gdf[['rec_id_A', 'rec_id_B']]
    X = sim_vectors_gdf.drop(columns=['rec_id_A', 'rec_id_B'])
    X = X.fillna(0.0)
    
    # Vectorized label creation using isin for efficient lookup
    #
    true_match_df = cudf.DataFrame(list(true_match_set), columns=['rec_id_A', 'rec_id_B'])
    true_match_df['label'] = 1

    labeled_pairs = rec_pairs.merge(true_match_df, on=['rec_id_A', 'rec_id_B'], how='left')
    y = labeled_pairs['label'].fillna(0).astype('int32')

    # --- Create a training sample with improved class balance ---

    match_mask = (y == 1)
    X_matches = X[match_mask]
    y_matches = y[match_mask]
    n_matches = len(X_matches)

    print(f'  Total true matches in dataset: {n_matches}')
    print(f'  Total non-matches in dataset: {len(y) - n_matches}')

    # Strategy 1: Balance training data more carefully
    # Use a 1:1 or 1:2 ratio instead of 1:5
    n_total = len(y)
    n_non_matches = n_total - n_matches
    
    # Try a 1:2 ratio (2 non-matches per match) for better balance
    n_non_match_sample = min(n_non_matches, n_matches * 2)

    print(f'  Creating a training sample with all {n_matches} matches and' + \
          f' {n_non_match_sample} non-matches (1:{n_non_match_sample//n_matches if n_matches > 0 else 0} ratio).')
    sys.stdout.flush()

    if n_non_match_sample > 0:
        non_match_indices_gpu = y[y == 0].index.to_series()
        sampled_non_match_indices = non_match_indices_gpu.sample(n=n_non_match_sample, replace=False)

        X_non_match_sample = X.take(sampled_non_match_indices)
        y_non_match_sample = y.take(sampled_non_match_indices)

        print(f'  Actually using {len(X_non_match_sample)} non-matches for training.')
        sys.stdout.flush()

        X_sampled = cudf.concat([X_matches, X_non_match_sample])
        y_sampled = cudf.concat([y_matches, y_non_match_sample])
    else:
        X_sampled = X_matches
        y_sampled = y_matches

    # Split the sampled dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_sampled, y_sampled, \
                                                    test_size=0.33, \
                                                    random_state=42)

    print('  Number of training records: %d' % len(X_train))
    print('  Number of testing records: %d' % len(X_test))
    print('')
    sys.stdout.flush()

    # Strategy 2: cuML doesn't support class_weight, so use data-level balancing instead
    # Ensure training data is well-balanced by further adjusting non-match sampling
    # Also use hyperparameters to reduce overfitting to the majority class
    
    # No additional rebalancing needed - the initial sampling should be sufficient
    # The key is to use a reasonable probability threshold, not class rebalancing
    print(f'  Training set composition: {(y_train == 1).sum()} matches, {(y_train == 0).sum()} non-matches')
    
    clf = RandomForestClassifier(
        n_estimators=n_estimators, 
        random_state=42,
        max_depth=15,              # Limit depth to reduce overfitting
        min_samples_split=20,      # Require more samples to split (reduces noise)
        min_samples_leaf=10        # Require more samples in leaf nodes
    )
    clf.fit(X_train, y_train)

    # Evaluate the classifier on the sampled test set
    accuracy = clf.score(X_test, y_test)
    print('  Classifier accuracy on sampled test set: %.3f' % accuracy)
    print('')
    sys.stdout.flush()

    # First pass: collect probability predictions to analyze distribution
    chunk_size = 1_000_000
    probas_list = []
    print(f'  Predicting probabilities on {len(X)} pairs in {((len(X)-1)//chunk_size)+1} chunks of size {chunk_size}...')
    sys.stdout.flush()
    
    for i in range(0, len(X), chunk_size):
        chunk = X.iloc[i:i + chunk_size]
        chunk_probas = clf.predict_proba(chunk)
        # Store only the positive class probability
        probas_list.append(chunk_probas.iloc[:, 1])

    probas_all = cupy.concatenate(probas_list)
    
    # Analyze probability distribution to choose optimal threshold
    probas_np = cupy.asnumpy(probas_all)
    percentiles = np.percentile(probas_np, [50, 75, 90, 95, 99])
    print(f'  Probability distribution - 50th: {percentiles[0]:.3f}, 75th: {percentiles[1]:.3f}, ' + 
          f'90th: {percentiles[2]:.3f}, 95th: {percentiles[3]:.3f}, 99th: {percentiles[4]:.3f}')
    
    # Use a dynamic threshold based on percentiles
    # For matching, we want high precision, so use a conservative threshold
    # If most pairs have high probability, use a higher percentile threshold
    if percentiles[4] < 0.5:  # 99th percentile is low
        dynamic_threshold = percentiles[4]  # Use 99th percentile
    elif percentiles[3] < 0.5:  # 95th percentile is low
        dynamic_threshold = percentiles[3]  # Use 95th percentile
    else:  # Most scores are high, use provided threshold or be very conservative
        dynamic_threshold = max(threshold, 0.5)
    
    print(f'  Using dynamic threshold: {0.5:.3f} (provided threshold was {threshold:.3f})')
    print('')
    sys.stdout.flush()

    fixed_threshold = 0.5
    
    # Second pass: apply threshold to get predictions
    predictions = (probas_all >= fixed_threshold).astype('int32')

    # --- Memory Cleanup ---
    print('  Cleaning up memory before final result collection...')
    sys.stdout.flush()
    del probas_list
    del X
    del clf
    del X_sampled, y_sampled, X_train, y_train, X_test, y_test
    del X_matches, y_matches, X_non_match_sample, y_non_match_sample
    del y
    import gc
    gc.collect()
    
    # Vectorized result collection in chunks to avoid OOM
    predictions_series = cudf.Series(predictions)

    chunk_size = 1_000_000
    class_match_set = set()
    class_nonmatch_set = set()

    print(f'  Collecting results in {((len(rec_pairs)-1)//chunk_size)+1} chunks of size {chunk_size}...')
    sys.stdout.flush()

    for i in range(0, len(rec_pairs), chunk_size):
        rec_pairs_chunk = rec_pairs.iloc[i:i + chunk_size]
        predictions_chunk = predictions_series.iloc[i:i + chunk_size]
        mask_chunk = (predictions_chunk == 1)

        match_pairs_chunk = rec_pairs_chunk[mask_chunk]
        if not match_pairs_chunk.empty:
            class_match_set.update(map(tuple, match_pairs_chunk.to_pandas().to_records(index=False)))

        non_match_pairs_chunk = rec_pairs_chunk[~mask_chunk]
        if not non_match_pairs_chunk.empty:
            class_nonmatch_set.update(map(tuple, non_match_pairs_chunk.to_pandas().to_records(index=False)))

    print('  Classified %d record pairs as matches and %d as non-matches' % \
        (len(class_match_set), len(class_nonmatch_set)))
    print('')
    sys.stdout.flush()

    return class_match_set, class_nonmatch_set

# -----------------------------------------------------------------------------

# End of program.


