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

def supervisedMLClassify(sim_vectors_gdf, true_match_set, n_estimators=5):
    """A classifier method based on a supervised machine learning technique
     (random forest) which learns from the given similarity vectors and the
     true match status set provided.

     The approach works as follows:
     1) Create the matrix of features (similarity vectors) and class labels
        (true matches and true non-matches)
     2) Train a random forest classifier on the training data.
     3) For each record pair and its similarity vector, predict its class
        (match or non-match).

     Parameter Description:
       sim_vectors_gdf : A cuDF DataFrame with record pairs and their similarity
                         vectors.
       true_match_set : Set of true matches (record identifier pairs)
       n_estimators   : The number of trees in the forest.
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

    # --- Create a smaller, balanced sample for training to avoid memory issues ---
    
    # Separate true matches and non-matches from the full dataset
    match_mask = (y == 1)
    X_matches = X[match_mask]
    y_matches = y[match_mask]
    
    X_non_matches = X[~match_mask]

    # We will use all true matches for training, and sample the non-matches
    n_matches = len(X_matches)
    # Create a larger sample of non-matches to help the classifier learn
    n_non_match_sample = min(len(X_non_matches), n_matches * 5)

    print(f'  Creating a training sample with all {n_matches} matches and' + \
          f' {n_non_match_sample} non-matches.')
    sys.stdout.flush()

    X_non_match_sample = X_non_matches.sample(n=n_non_match_sample, random_state=42)
    y_non_match_sample = y.loc[X_non_match_sample.index]

    # Combine to form the final sampled dataset for training/testing
    X_sampled = cudf.concat([X_matches, X_non_match_sample])
    y_sampled = cudf.concat([y_matches, y_non_match_sample])

    # Split the SMALLER, SAMPLED dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_sampled, y_sampled, \
                                                    test_size=0.33, \
                                                    random_state=42)

    print('  Number of training records: %d' % len(X_train))
    print('  Number of testing records: %d' % len(X_test))
    print('')
    sys.stdout.flush()

    # Initialize and train the classifier
    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate the classifier on the sampled test set
    accuracy = clf.score(X_test, y_test)
    print('  Classifier accuracy on sampled test set: %.3f' % accuracy)
    print('')
    sys.stdout.flush()

    # Classify all record pairs
    predictions = clf.predict(X)
    
    # Vectorized result collection
    #
    predictions_series = cudf.Series(predictions)
    match_mask = predictions_series == 1

    match_pairs = rec_pairs[match_mask]
    non_match_pairs = rec_pairs[~match_mask]

    class_match_set = set(map(tuple, match_pairs.to_pandas().to_records(index=False)))
    class_nonmatch_set = set(map(tuple, non_match_pairs.to_pandas().to_records(index=False)))

    print('  Classified %d record pairs as matches and %d as non-matches' % \
        (len(class_match_set), len(class_nonmatch_set)))
    print('')
    sys.stdout.flush()

    return class_match_set, class_nonmatch_set

# -----------------------------------------------------------------------------

# End of program.


