# ============================================================================
# Record linkage software for the COMP3430/COMP8430 Data Wrangling course, 
# 2025.
# Version 1.0
#
# Copyright (C) 2025 the Australian National University and
# others. All Rights Reserved.
#
# =============================================================================

"""Testng module for debugging record linkage functions.

   This module calls the necessary modules to perform the functionalities of
   the record linkage process.
"""

# =============================================================================
# Import necessary modules (Python standard modules first, then other modules)

import sys

import loadDataset
import blocking
import comparison
import classification
import evaluation

def testBlocking(test_case_dict, solution_dict, blk_attr_list, rl_function, 
                 rl_function_str):
  """Method to test different blocking techniques as implemented in the
     blocking module. Both phoneticBlocking and slkBlocking functions 
     are tested here.

     Parameter Description:
       test_case_dict  : Dictionary of test cases.
       solution_dict   : Dictionary of solutions for the test cases.
       blk_attr_list   : Selected attributes to be blocked.
       rl_function     : Record linkage function.
       rl_function_str : Record linkage function name.
  """

  test_status = 'success'
  if(rl_function_str == 'phoneticBlocking'):
    block_dict = rl_function(test_case_dict, blk_attr_list)
  elif(rl_function_str == 'slkBlocking'):
    block_dict = rl_function(test_case_dict, blk_attr_list[0], blk_attr_list[1],
                            blk_attr_list[2], blk_attr_list[3])
  
  res_dict = {}
  for blck_val, rec_id_list in block_dict.items():
    for rec_id in rec_id_list:
      res_dict[rec_id] = blck_val
  
  wrong_val_list = []
  for rec_id, blck_val in res_dict.items():
    corr_val = solution_dict[rec_id]
    if(corr_val != blck_val):
      wrong_val_list.append((test_case_dict[rec_id], corr_val, blck_val))

  if(len(wrong_val_list) > 0):
    test_status = 'fail'

    print ('Test cases FAILED!')
    print ()
    for test_val, corr_ans, wrng_ans in wrong_val_list:
      print ('  - Testing value:          %s' %test_val)
      print ('  - Correct blocking value: %s' %corr_ans)
      print ('  - Wrong blocking value:   %s' %wrng_ans)
      print ()

  else:
    print ('Test cases SUCCESSFUL!')
    print ()
  
  return test_status

#---------------------------------------------------------------------------------
def testComparison(test_case_dict, solution_dict, rl_function):
  """Method to test different comparison techniques as implemented in the
     comparison module. All comparison functions are tested here.

     Parameter Description:
       test_case_dict  : Dictionary of test cases.
       solution_dict   : Dictionary of solutions for the test cases.
       rl_function     : Record linkage function.
  """

  test_status = 'success'

  wrong_val_list = []
  for rec_id, val_pair in test_case_dict.items():
    calc_sim_val = rl_function(val_pair[0], val_pair[1])
    calc_sim_val = round(calc_sim_val, 5)
    corr_sim_val = solution_dict[rec_id]
    if(corr_sim_val != calc_sim_val):
      wrong_val_list.append((test_case_dict[rec_id], corr_sim_val, calc_sim_val))
  
  if(len(wrong_val_list) > 0):
    test_status = 'fail'
    
    print ('\nTest case FAILED!\n')
    for test_val, corr_ans, wrng_ans in wrong_val_list:
      print ('  - Testing value pair:       %s' %str(test_val))
      print ('  - Correct similarity value: %s' %corr_ans)
      print ('  - Wrong similarity value:   %s' %wrng_ans)
      print ()

  else:
    print ('\nTest case SUCCESSFUL!\n')

#---------------------------------------------------------------------------------
def testClassification(test_case_dict, solution_dict, rl_function, rl_function_str,
                       sim_threshold, weight_vec=None):
  """Method to test different classification techniques as implemented in the
     classification module. All classification functions are tested here.

     Parameter Description:
       test_case_dict  : Dictionary of test cases.
       solution_dict   : Dictionary of solutions for the test cases.
       blk_attr_list   : Selected attributes to be blocked.
       rl_function     : Record linkage function.
       rl_function_str : Record linkage function name.
       sim_threshold   : Similarity threshold for classification.
       weight_vec      : Vector of weights assigned for each attribute.
  """
  
  test_status = 'success'

  if(rl_function_str == 'exactClassify'):
    match_set, nonmatch_set = rl_function(test_case_dict)
  elif(rl_function_str in ['thresholdClassify', 'minThresholdClassify']):
    match_set, nonmatch_set = rl_function(test_case_dict, sim_threshold)
  elif(rl_function_str == 'weightedSimilarityClassify'):
    match_set, nonmatch_set = rl_function(test_case_dict, weight_vec, sim_threshold)

  wrong_val_list = []
  for rec_pair in test_case_dict.keys():
    if(rec_pair in match_set):
      if(solution_dict[rec_pair] != 'm'):
        wrong_val_list.append((rec_pair, solution_dict[rec_pair], 'm'))
    elif(rec_pair in nonmatch_set):
      if(solution_dict[rec_pair] != 'u'):
        wrong_val_list.append((rec_pair, solution_dict[rec_pair], 'u'))
    else:
      wrong_val_list.append((rec_pair, solution_dict[rec_pair], 'none'))

  if(len(wrong_val_list) > 0):
    test_status = 'fail'
    
    print ('\nUsed similarity threshold: %.2f' %sim_threshold)
    print ('Test case FAILED!\n')
    for test_val, corr_ans, wrng_ans in wrong_val_list:
      print ('  - Testing record pair:      %s' %str(test_val))
      print ('  - Correct matching class:   %s' %corr_ans)
      print ('  - Wrong non-matching class: %s' %wrng_ans)
      print ()

  else:
    print ('\nUsed similarity threshold: %.2f' %sim_threshold)
    print ('Test case SUCCESSFUL!\n')

# =============================================================================
# Main programme
# =============================================================================

# Command line arguments
rl_module = sys.argv[1].lower() # Testing module
rl_function_str = sys.argv[2] # Testing function

assert rl_module in ['blocking', 'comparison', 'classification', 'evaluation'], \
    'Invalid record linkage module provided'

if(rl_module == 'blocking'):
  assert rl_function_str in ['phoneticBlocking', 'slkBlocking'], \
    'Invalid blocking function provided'
elif(rl_module == 'comparison'):
  assert rl_function_str in ['jaccard_comp', 'dice_comp', 'jaro_comp', 
  'jaro_winkler_comp', 'bag_dist_sim_comp', 'edit_dist_sim_comp'], \
    'Invalid comparison function provided'
elif(rl_module == 'classification'):
  assert rl_function_str in ['exactClassify', 'thresholdClassify', 
  'minThresholdClassify', 'weightedSimilarityClassify', 'supervisedMLClassify'], \
    'Invalid classification function provided'
else:
  assert rl_function_str in ['accuracy', 'precision', 'recall', 'specificity', 
  'fmeasure', 'reduction_ratio', 'pairs_completeness', 'pairs_quality'], \
    'Invalid evaluation function provided'

rl_function = getattr(eval(rl_module), rl_function_str)

print ('\nRunning tests for %s function in %s module' %(rl_function_str, rl_module))

# -----------------------------------------------------------------------------
# Test cases for bocking module

if(rl_function_str == 'phoneticBlocking'): # Soundex blocking
  blk_attr_list = [0]

  blk_dict_test_case1 = {'rec1': ['Brian'], 'rec2': ['Peter'], 'rec3': ['Anushka'], 
  'rec4': ['Graham']}
  solution_dict1 = {'rec1': 'b650', 'rec2': 'p360', 'rec3': 'a520', 'rec4': 'g650'}

  blk_dict_test_case2 = {'rec1': ['Smith'], 'rec2': ['Miller'], 'rec3': ['Vidanage'], 
  'rec4': ['Williams']}
  solution_dict2 = {'rec1': 's530', 'rec2': 'm460', 'rec3': 'v352', 'rec4': 'w452'}

  test_status1 = testBlocking(blk_dict_test_case1, solution_dict1, blk_attr_list, 
                              rl_function, rl_function_str)
  test_status2 = testBlocking(blk_dict_test_case2, solution_dict2, blk_attr_list, 
                              rl_function, rl_function_str)

elif(rl_function_str == 'slkBlocking'): # SLK blocking
  blk_attr_list = [1, 0, 2, 3]
  blk_dict_test_case = {'rec1': ['Brian', 'Schmidt', '24/02/1967', 'm'], 
                        'rec2': ['Hugh', 'Jackman', '12/10/1968', ''],
                        'rec3': ['Jess', 'Li', '', 'f']
                        }
  solution_dict = {'rec1': 'chiri240219671', 'rec2': 'acmug121019689', 
                    'rec3': 'i22es010119002', }

  test_status = testBlocking(blk_dict_test_case, solution_dict, blk_attr_list, 
                              rl_function, rl_function_str)

# -----------------------------------------------------------------------------
# Test cases for comparison module

elif(rl_module == 'comparison'): # Comparison
  comp_dict_test_case = {'rec1': ('peter', 'peter'),
                          'rec2': ('crate', 'trace'),
                          'rec3': ('dwayne', 'dwane'),
                          'rec4': ('jones', 'johnson'),
                          'rec5': ('charlie', 'charles')
  }
  if(rl_function_str == 'jaccard_comp'):
    solution_dict = {'rec1': 1.0, 'rec2': 0.14286, 'rec3': 0.5, 'rec4': 0.25,
     'rec5': 0.5}
  elif(rl_function_str == 'dice_comp'):
    solution_dict = {'rec1': 1.0, 'rec2': 0.25, 'rec3': 0.66667, 'rec4': 0.4,
     'rec5': 0.66667}
  elif(rl_function_str == 'jaro_comp'):
    solution_dict = {'rec1': 1.0, 'rec2': 0.73333, 'rec3': 0.94444, 'rec4': 0.79048,
     'rec5': 0.90476}
  elif(rl_function_str == 'jaro_winkler_comp'):
    solution_dict = {'rec1': 1.0, 'rec2': 0.73333, 'rec3': 0.96111, 'rec4': 0.83238,
     'rec5': 0.94286}
  elif(rl_function_str == 'bag_dist_sim_comp'):
    solution_dict = {'rec1': 1.0, 'rec2': 1.0, 'rec3': 0.83333, 'rec4': 0.57143,
     'rec5': 0.85714}
  elif(rl_function_str == 'edit_dist_sim_comp'):
    solution_dict = {'rec1': 1.0, 'rec2': 0.6, 'rec3': 0.83333, 'rec4': 0.42857,
     'rec5': 0.71429}

  test_status = testComparison(comp_dict_test_case, solution_dict, rl_function)

# -----------------------------------------------------------------------------
# Test cases for classification module

elif(rl_module == 'classification'): # Classification
  sim_vec_dict = {('rec1', 'rec2'): [1.0, 1.0, 1.0, 1.0], 
                  ('rec3', 'rec4'): [1.0, 1.0, 0.0, 1.0],
                  ('rec5', 'rec6'): [0.82454, 0.6222, 0.9167, 0.7415],
                  ('rec7', 'rec8'): [0.99857, 1.0, 0.74487, 0.1454],
                  ('rec9', 'rec10'): [0.18182, 0.64, 0.45, 0.1],
  }
  
  sim_thresh_list = [0.9, 0.6, 0.3]
  weight_vec = [0.3, 0.2, 0.4, 0.1] #assuming attributes [first_name, last_name, date_of_birth, state]

  if(rl_function_str == 'exactClassify'):
    solution_dict = {('rec1', 'rec2'): 'm', ('rec3', 'rec4'): 'u', 
                     ('rec5', 'rec6'): 'u', ('rec7', 'rec8'): 'u',
                     ('rec9', 'rec10'): 'u'
    }
    test_status = testClassification(sim_vec_dict, solution_dict, rl_function,
                                   rl_function_str, sim_thresh_list[0])

  elif(rl_function_str == 'thresholdClassify'):
    solution_dict_9 = {('rec1', 'rec2'): 'm', ('rec3', 'rec4'): 'u', 
                        ('rec5', 'rec6'): 'u', ('rec7', 'rec8'): 'u',
                        ('rec9', 'rec10'): 'u'
    }
    solution_dict_6 = {('rec1', 'rec2'): 'm', ('rec3', 'rec4'): 'm', 
                        ('rec5', 'rec6'): 'm', ('rec7', 'rec8'): 'm',
                        ('rec9', 'rec10'): 'u'
    }
    solution_dict_3 = {('rec1', 'rec2'): 'm', ('rec3', 'rec4'): 'm', 
                        ('rec5', 'rec6'): 'm', ('rec7', 'rec8'): 'm',
                        ('rec9', 'rec10'): 'm'
    }
    solution_dict_list = [solution_dict_9, solution_dict_6, solution_dict_3]

    for i, sim_tresh in enumerate(sim_thresh_list):
      test_status = testClassification(sim_vec_dict, solution_dict_list[i], rl_function,
                                       rl_function_str, sim_tresh)

  elif(rl_function_str == 'minThresholdClassify'):
    solution_dict_9 = {('rec1', 'rec2'): 'm', ('rec3', 'rec4'): 'u', 
                        ('rec5', 'rec6'): 'u', ('rec7', 'rec8'): 'u',
                        ('rec9', 'rec10'): 'u'
    }
    solution_dict_6 = {('rec1', 'rec2'): 'm', ('rec3', 'rec4'): 'u', 
                        ('rec5', 'rec6'): 'm', ('rec7', 'rec8'): 'u',
                        ('rec9', 'rec10'): 'u'
    }
    solution_dict_3 = {('rec1', 'rec2'): 'm', ('rec3', 'rec4'): 'u', 
                        ('rec5', 'rec6'): 'm', ('rec7', 'rec8'): 'u',
                        ('rec9', 'rec10'): 'u'
    }
    solution_dict_list = [solution_dict_9, solution_dict_6, solution_dict_3]

    for i, sim_tresh in enumerate(sim_thresh_list):
      test_status = testClassification(sim_vec_dict, solution_dict_list[i], rl_function,
                                       rl_function_str, sim_tresh)

  elif(rl_function_str == 'weightedSimilarityClassify'):
    solution_dict = {('rec1', 'rec2'): 'm', ('rec3', 'rec4'): 'm', 
                     ('rec5', 'rec6'): 'm', ('rec7', 'rec8'): 'm',
                     ('rec9', 'rec10'): 'u'
    }

    test_status = testClassification(sim_vec_dict, solution_dict, rl_function,
                                    rl_function_str, sim_thresh_list[1], weight_vec)
