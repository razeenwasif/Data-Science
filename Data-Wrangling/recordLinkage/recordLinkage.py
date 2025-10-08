# =============================================================================
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
import cudf

# conda run -n rapids-25.08 python3 recordLinkage.py

# =============================================================================
# Variable names for loading datasets

datasetA_name = 'datasets/clean-A-1000.csv'
datasetB_name = 'datasets/clean-B-1000.csv'
truthfile_name = 'datasets/clean-true-matches-1000.csv'

# datasetA_name = 'datasets/comp3430_comp8430-rl-additional-datasets/very-dirty-A-100000.csv'
# datasetB_name = 'datasets/comp3430_comp8430-rl-additional-datasets/very-dirty-B-100000.csv'
# truthfile_name = 'datasets/comp3430_comp8430-rl-additional-datasets/very-dirty-true-matches-100000.csv'

headerA_line   = True
headerB_line   = True

rec_idA_col = 0
rec_idB_col = 0

attr_list = ['first_name', 'middle_name', 'last_name', 'gender', 'birth_date', 'street_address', 'suburb', 'postcode', 'state', 'phone']

# The list of tuples (comparison function, attribute name in record A,
# attribute name in record B)
#
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

start_time = time.time()

recA_gdf = cudf.DataFrame.from_dict(recA_dict, orient='index')
recB_gdf = cudf.DataFrame.from_dict(recB_dict, orient='index')

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
                                        recA_gdf, recB_gdf, \
                                        approx_comp_funct_list)

comparison_time = time.time() - start_time

# -----------------------------------------------------------------------------
# Step 4: Classify the candidate pairs

start_time = time.time()

class_match_set, class_nonmatch_set = \
           classification.supervisedMLClassify(sim_vec_dict, true_match_set)

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
