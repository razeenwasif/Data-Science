# ============================================================================
# Record linkage software for the COMP3430/COMP8430 Data Wrangling course, 
# 2025.
# Version 1.0
#
# Copyright (C) 2025 the Australian National University and
# others. All Rights Reserved.
#
# =============================================================================

"""Main module for linking records from two files.

   This module calls the necessary modules to perform the functionalities of
   the record linkage process.
"""

# =============================================================================
# Import necessary modules (Python standard modules first, then other modules)

import time

import loadDataset
import blocking
import comparison
import classification
import evaluation

# =============================================================================
# Variable names for loading datasets

# ******** Uncomment to select a pair of datasets **************

datasetA_name = 'datasets/clean-A-50.csv'
datasetB_name = 'datasets/clean-B-50.csv'

#datasetA_name = 'datasets/clean-A-1000.csv'
#datasetB_name = 'datasets/clean-B-1000.csv'

#datasetA_name = 'datasets/clean-A-10000.csv'
#datasetB_name = 'datasets/clean-B-10000.csv'

#datasetA_name = 'datasets/little-dirty-A-10000.csv'
#datasetB_name = 'datasets/little-dirty-B-10000.csv'

#datasetA_name = 'datasets/comp3430_comp8430-rl-additional-datasets/very-dirty-A-100000.csv'
#datasetB_name = 'datasets/comp3430_comp8430-rl-additional-datasets/very-dirty-B-100000.csv'


headerA_line   = True  # Dataset A header line available - True or Flase
headerB_line   = True  # Dataset B header line available - True or Flase

# Name of the corresponding file with true matching record pair

# ***** Uncomment a file name corresponding to your selected datasets *******

truthfile_name = 'datasets/clean-true-matches-50.csv'
#truthfile_name = 'datasets/clean-true-matches-1000.csv'
#truthfile_name = 'datasets/clean-true-matches-10000.csv'
#truthfile_name = 'datasets/little-dirty-true-matches-10000.csv'
#truthfile_name = 'datasets/comp3430_comp8430-rl-additional-datasets/very-dirty-true-matches-100000.csv'

# The two attribute numbers that contain the record identifiers
#
rec_idA_col = 0
rec_idB_col = 0

# The list of attributes to be used either for blocking or linking
#
# For the example data sets used in COMP8430 data wrangling in 2025:
# 
#  0: rec_id
#  1: first_name
#  2: middle_name
#  3: last_name
#  4: gender
#  5: current_age
#  6: birth_date
#  7: street_address
#  8: suburb
#  9: postcode
# 10: state
# 11: phone
# 12: email

attr_list = ['first_name', 'middle_name', 'last_name', 'gender', 'birth_date', 'street_address', 'suburb', 'postcode', 'state', 'phone']

# ******** In lab 3, explore different attribute sets for blocking ************

# The list of attributes to use for blocking (all must occur in the above
# attribute lists)
#
blocking_attr_list = ['last_name', 'gender']

# ******** In lab 4, explore different comparison functions for different  ****
# ********           attributes                                            ****

# The list of tuples (comparison function, attribute number in record A,
# attribute number in record B)
#
exact_comp_funct_list = [(comparison.exact_comp, 'first_name', 'first_name'),
                         (comparison.exact_comp, 'middle_name', 'middle_name'),
                         (comparison.exact_comp, 'last_name', 'last_name'),
                         (comparison.exact_comp, 'suburb', 'suburb'),
                         (comparison.exact_comp, 'state', 'state'),
                         ]

approx_comp_funct_list = [(comparison.jaccard_comp, 'first_name', 'first_name'),
                          (comparison.dice_comp, 'middle_name', 'middle_name'),
                          (comparison.jaro_winkler_comp, 'last_name', 'last_name'),
                          (comparison.bag_dist_sim_comp, 'street_address', 'street_address'),
                          (comparison.edit_dist_sim_comp, 'suburb', 'suburb'),
                          (comparison.exact_comp, 'state', 'state'),
                         ]

# =============================================================================
#
# Step 1: Load the two datasets from CSV files

start_time = time.time()

recA_dict = loadDataset.load_data_set(datasetA_name, 'rec_id', attr_list)
recB_dict = loadDataset.load_data_set(datasetB_name, 'rec_id', attr_list)

# Load data set of true matching pairs
#
true_match_set = loadDataset.load_truth_data(truthfile_name)

loading_time = time.time() - start_time

# -----------------------------------------------------------------------------
# Step 2: Block the datasets

import cudf

start_time = time.time()

recA_gdf = cudf.DataFrame.from_dict(recA_dict, orient='index')
recB_gdf = cudf.DataFrame.from_dict(recB_dict, orient='index')

#blockA_dict = blocking.simpleBlocking(recA_gdf, blocking_attr_list)
#blockB_dict = blocking.simpleBlocking(recB_gdf, blocking_attr_list)

canopy_attr_list = ['first_name', 'last_name']
T1 = 0.8 # Loose Threshold (distance)
T2 = 0.4 # Tight Threshold (distance)
blockA_dict = blocking.canopy_clustering(recA_gdf, canopy_attr_list, T1, T2)
blockB_dict = blocking.canopy_clustering(recB_gdf, canopy_attr_list, T1, T2)

blocking_time = time.time() - start_time

# Print blocking statistics
#
blocking.printBlockStatistics(blockA_dict, blockB_dict)

# -----------------------------------------------------------------------------
# Step 3: Compare the candidate pairs

start_time = time.time()

sim_vec_dict = comparison.compareBlocks(blockA_dict, blockB_dict, \
                                        recA_dict, recB_dict, \
                                        approx_comp_funct_list)

comparison_time = time.time() - start_time

# -----------------------------------------------------------------------------
# Step 4: Classify the candidate pairs

start_time = time.time()

# Exact matching based classification
#
# class_match_set, class_nonmatch_set = \
# classification.exactClassify(sim_vec_dict)

# *********** In lab 5, explore different similarity threshold values *********

# A supervised decision tree classifier
#
class_match_set, class_nonmatch_set = \
           classification.supervisedMLClassify(sim_vec_dict, true_match_set)

# Minimum similarity threshold based classification
#
#min_sim_threshold = 0.5
#class_match_set, class_nonmatch_set = \
#             classification.minThresholdClassify(sim_vec_dict,
#                                                 min_sim_threshold)

# A supervised decision tree classifier
#
#class_match_set, class_nonmatch_set = \
#           classification.supervisedMLClassify(sim_vec_dict, true_match_set)

classification_time = time.time() - start_time

# -----------------------------------------------------------------------------
# Step 5: Evaluate the classification

# Get the number of record pairs compared
#
num_comparisons = len(sim_vec_dict)

# Get the number of total record pairs to compared if no blocking used
#
all_comparisons = len(recA_dict) * len(recB_dict)

# Get the list of identifiers of the compared record pairs
#
cand_rec_id_pair_list = sim_vec_dict.keys()

# Blocking evaluation
#
rr = evaluation.reduction_ratio(num_comparisons, all_comparisons)
pc = evaluation.pairs_completeness(cand_rec_id_pair_list, true_match_set)
pq = evaluation.pairs_quality(cand_rec_id_pair_list, true_match_set)

print('Blocking evaluation:')
print('  Reduction ratio:    %.3f' % (rr))
print('  Pairs completeness: %.3f' % (pc))
print('  Pairs quality:      %.3f' % (pq))
print('')

# Linkage evaluation
#
linkage_result = evaluation.confusion_matrix(class_match_set,
                                             class_nonmatch_set,
                                             true_match_set,
                                             all_comparisons)

accuracy =    evaluation.accuracy(linkage_result)
precision =   evaluation.precision(linkage_result)
recall    =   evaluation.recall(linkage_result)
fmeasure  =   evaluation.fmeasure(linkage_result)

print('Linkage evaluation:')
print('  Accuracy:    %.3f' % (accuracy))
print('  Precision:   %.3f' % (precision))
print('  Recall:      %.3f' % (recall))
print('  F-measure:   %.3f' % (fmeasure))
print('')

linkage_time = loading_time + blocking_time + comparison_time + \
               classification_time
print('Total runtime required for linkage: %.3f sec' % (linkage_time))

# -----------------------------------------------------------------------------
# Step 6: Save the linkage result

import saveLinkResult
saveLinkResult.save_linkage_set('very-dirty-100000-matches.csv', class_match_set)

# -----------------------------------------------------------------------------

# End of program.
