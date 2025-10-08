import code
import os 
import numpy as np
import sys 
from collections import Counter
import cudf
import cugraph
import cupy
from numba_kernels import calculate_jaccard_similarity_gpu_pairwise, calculate_dice_similarity_gpu_pairwise, get_q_grams_set
from numba import cuda
from rapidfuzz import fuzz
from rapidfuzz.distance import Levenshtein

MAX_STRING_LEN = 256


@cuda.jit
def gpu_jaro_winkler(s1, s2, out):
    i = cuda.grid(1)
    if i < s1.shape[0]:
        out[i] = jaro_winkler_similarity_kernel(s1[i], s2[i])

@cuda.jit
def gpu_levenshtein(s1, s2, out):
    i = cuda.grid(1)
    if i < s1.shape[0]:
        out[i] = levenshtein_similarity_kernel(s1[i], s2[i])


def get_char_vocab(s1, s2):
    """Create a character vocabulary from two series of strings."""
    chars = set()
    for s in s1.to_pandas():
        chars.update(s)
    for s in s2.to_pandas():
        chars.update(s)
    char_to_int = {char: i for i, char in enumerate(chars)}
    return char_to_int

def strings_to_char_arrays(s, char_to_int):
    """Convert a series of strings to a 2D numpy array of character indices."""
    num_strings = len(s)
    char_arrays = np.zeros((num_strings, MAX_STRING_LEN), dtype=np.int32)
    for i, string in enumerate(s.to_pandas()):
        for j, char in enumerate(string):
            if j < MAX_STRING_LEN:
                char_arrays[i, j] = char_to_int[char]
    return char_arrays

@cuda.jit(device=True)
def jaro_winkler_similarity_kernel(s1, s2):
    """Numba CUDA kernel for Jaro-Winkler similarity."""
    len1 = len(s1)
    len2 = len(s2)

    if len1 == 0 or len2 == 0:
        return 0.0

    match_distance = (max(len1, len2) // 2) - 1

    s1_matches = cuda.local.array(MAX_STRING_LEN, dtype=np.bool_)
    s2_matches = cuda.local.array(MAX_STRING_LEN, dtype=np.bool_)

    for i in range(len1):
        s1_matches[i] = False
    for i in range(len2):
        s2_matches[i] = False

    matches = 0
    transpositions = 0

    for i in range(len1):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, len2)

        for j in range(start, end):
            if not s2_matches[j] and s1[i] == s2[j]:
                s1_matches[i] = True
                s2_matches[j] = True
                matches += 1
                break

    if matches == 0:
        return 0.0

    k = 0
    for i in range(len1):
        if s1_matches[i]:
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1

    jaro_sim = (matches / len1 + matches / len2 + (matches - transpositions // 2) / matches) / 3.0

    # Winkler modification
    prefix = 0
    for i in range(min(len1, len2, 4)):
        if s1[i] == s2[i]:
            prefix += 1
        else:
            break

    return jaro_sim + prefix * 0.1 * (1.0 - jaro_sim)

@cuda.jit(device=True)
def levenshtein_similarity_kernel(s1, s2):
    """Numba CUDA kernel for Levenshtein similarity."""
    len1 = len(s1)
    len2 = len(s2)

    if len1 == 0 or len2 == 0:
        return 0.0

    if len1 < len2:
        s1, s2 = s2, s1
        len1, len2 = len2, len1

    prev_row = cuda.local.array(MAX_STRING_LEN, dtype=np.int32)
    curr_row = cuda.local.array(MAX_STRING_LEN, dtype=np.int32)

    for i in range(len2 + 1):
        prev_row[i] = i

    for i in range(1, len1 + 1):
        curr_row[0] = i
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            curr_row[j] = min(curr_row[j - 1] + 1,
                                prev_row[j] + 1,
                                prev_row[j - 1] + cost)
        for j in range(len2 + 1):
            prev_row[j] = curr_row[j]

    return 1.0 - (curr_row[len2] / len1)






from comparison_kernels import compare_kernel

""" Module with functionalities for comparison of attribute values as well as
	record pairs. The record pair comparison function will return a dictionary
	of the compared pairs to be used for classification.
"""

Q = 2	# Value length of q-grams for Jaccard and Dice comparison function

def get_q_grams(s, q):
	return {s[i:i+q] for i in range(len(s) - q + 1)}

# =============================================================================
# First the basic functions to compare attribute values

def exact_comp(val1, val2):
	"""Compare the two given attribute values exactly, return 1 if they are the
		 same (but not both empty!) and 0 otherwise.
	"""

	# If at least one of the values is empty return 0
	#
	if val1 is None or val2 is None or (len(val1) == 0) or (len(val2) == 0):
		return 0.0

	elif (val1 != val2):
		return 0.0
	else:	# The values are the same
		return 1.0

# -----------------------------------------------------------------------------

def jaccard_comp(val1, val2):
	"""Calculate the Jaccard similarity between the two given attribute values
		 by extracting sets of sub-strings (q-grams) of length q.

		 Returns a value between 0.0 and 1.0.
	"""

	# If at least one of the values is empty return 0
	#
	if val1 is None or val2 is None or (len(val1) == 0) or (len(val2) == 0):
		return 0.0

	# If both attribute values exactly match return 1
	#
	elif (val1 == val2):
		return 1.0

	# ********* Implement Jaccard similarity function here *********

	jacc_sim = 0.0	# Replace with your code

	q_grams_val1 = get_q_grams(val1, Q) 
	q_grams_val2 = get_q_grams(val2, Q)

	# Handle cases where q_grams might be empty 
	if not q_grams_val1 and not q_grams_val2:
				return 1.0 
	if not q_grams_val1 or not q_grams_val2:
				return 0.0 

	numerator = len(q_grams_val1.intersection(q_grams_val2))
	denominator = len(q_grams_val1.union(q_grams_val2))
	jacc_sim = float(numerator) / denominator

	# ************ End of your Jaccard code *************************************

	assert jacc_sim >= 0.0 and jacc_sim <= 1.0

	return jacc_sim

def jaccard_distance(val1, val2):
  """Calculate the Jaccard distance between the two given attribute values.
  """

  return 1.0 - jaccard_comp(val1, val2)

def jaccard_comp_gpu(vals1, vals2):
    """
    Calculate the Jaccard similarity between two cuDF Series of strings on the GPU.
    """
    
    vals1_list = vals1.to_arrow().to_pylist()
    vals2_list = vals2.to_arrow().to_pylist()

    sets1 = [get_q_grams_set(s) for s in vals1_list]
    sets2 = [get_q_grams_set(s) for s in vals2_list]
    
    sims = calculate_jaccard_similarity_gpu_pairwise(sets1, sets2)
    
    return cudf.Series(sims)

# -----------------------------------------------------------------------------

def dice_comp(val1, val2):
	"""Calculate the Dice coefficient similarity between the two given attribute
		 values by extracting sets of sub-strings (q-grams) of length q.

		 Returns a value between 0.0 and 1.0.
	"""

	# If at least one of the values is empty return 0
	#
	if val1 is None or val2 is None or (len(val1) == 0) or (len(val2) == 0):
		return 0.0

	# If both attribute values exactly match return 1
	#
	elif (val1 == val2):
		return 1.0

	# ********* Implement Dice similarity function here *********

	dice_sim = 0.0	# Replace with your code

	q_grams_val1 = get_q_grams(val1, Q)
	q_grams_val2 = get_q_grams(val2, Q)
	
	if not q_grams_val1 and not q_grams_val2:
		return 1.0
	if not q_grams_val1 or not q_grams_val2:
		return 0.0
   
	numerator = 2 * len(q_grams_val1.intersection(q_grams_val2))
	denominator = len(q_grams_val1) + len(q_grams_val2)
	dice_sim = float(numerator)/denominator 

	# ************ End of your Dice code ****************************************

	assert dice_sim >= 0.0 and dice_sim <= 1.0

	return dice_sim

# -----------------------------------------------------------------------------

JARO_MARKER_CHAR = chr(1)	# Special character used in the Jaro, Winkler comp.

def jaro_comp(val1, val2):
	"""Calculate the similarity between the two given attribute values based on
		the Jaro comparison function.

		 As described in 'An Application of the Fellegi-Sunter Model of Record
		 Linkage to the 1990 U.S. Decennial Census' by William E. Winkler and Yves
		 Thibaudeau.

		 Returns a value between 0.0 and 1.0.
	"""

	# If at least one of the values is empty return 0
	#
	if (val1 == '') or (val2 == ''):
		return 0.0

	# If both attribute values exactly match return 1
	#
	elif (val1 == val2):
		return 1.0

	len1 = len(val1)	# Number of characters in val1
	len2 = len(val2)	# Number of characters in val2

	halflen = int(max(len1, len2) / 2) - 1

	assingment1 = ''	# Characters assigned in val1
	assingment2 = ''	# Characters assigned in val2

	workstr1 = val1	# Copy of original value1
	workstr2 = val2	# Copy of original value2

	common1 = 0	# Number of common characters
	common2 = 0	# Number of common characters

	for i in range(len1):	# Analyse the first string
		start = max(0, i - halflen)
		end	 = min(i + halflen + 1, len2)
		index = workstr2.find(val1[i], start, end)
		if (index > -1):		# Found common character, count and mark it as assigned
			common1 += 1
			assingment1 = assingment1 + val1[i]
			workstr2 = workstr2[:index] + JARO_MARKER_CHAR + workstr2[index+1:]

	for i in range(len2):	# Analyse the second string
		start = max(0, i - halflen)
		end	 = min(i + halflen + 1, len1)
		index = workstr1.find(val2[i], start, end)
		if (index > -1):		# Found common character, count and mark it as assigned
			common2 += 1
			assingment2 = assingment2 + val2[i]
			workstr1 = workstr1[:index] + JARO_MARKER_CHAR + workstr1[index+1:]

	if (common1 != common2):
		common1 = float(common1 + common2) / 2.0

	if (common1 == 0):		# No common characters within half length of strings
		return 0.0

	transposition = 0	# Calculate number of transpositions

	for i in range(len(assingment1)):
		if (assingment1[i] != assingment2[i]):
			transposition += 1
	transposition = transposition / 2.0

	common1 = float(common1)

	jaro_sim = 1./3.*(common1 / float(len1) + common1 / float(len2) + \
					 (common1 - transposition) / common1)

	assert (jaro_sim >= 0.0) and (jaro_sim <= 1.0), \
							'Similarity weight outside 0-1: %f' % (jaro_sim)

	return jaro_sim

# -----------------------------------------------------------------------------

def jaro_winkler_comp(val1, val2):
	"""Calculate the similarity between the two given attribute values based on
		 the Jaro-Winkler modifications.

		 Applies the Winkler modification if the beginning of the two strings is
		 the same.

		 As described in 'An Application of the Fellegi-Sunter Model of Record
		 Linkage to the 1990 U.S. Decennial Census' by William E. Winkler and Yves
		 Thibaudeau.

		 If the beginning of the two strings (up to first four characters) are the
		 same, the similarity weight will be increased.

		 Returns a value between 0.0 and 1.0.
	"""

	# If at least one of the values is empty return 0
	#
	if (val1 == '') or (val2 == ''):
		return 0.0

	# If both attribute values exactly match return 1
	#
	elif (val1 == val2):
		return 1.0

	# First calculate the basic Jaro similarity
	#
	jaro_sim = jaro_comp(val1, val2)
	if (jaro_sim == 0):
		return 0.0	# No common characters

	# ********* Implement Winkler similarity function here *********
	
	strings = [val1, val2]
	p = min(len(os.path.commonprefix(strings)), 4) # Cap prefix length at 4
	jw_sim = jaro_sim + (1 - jaro_sim) * (p/10)

	# ************ End of your Winkler code *************************************

	assert (jw_sim >= jaro_sim), 'Winkler modification is negative'
	assert (jw_sim >= 0.0) and (jw_sim <= 1.0), \
				 'Similarity weight outside 0-1: %f' % (jw_sim)

	return jw_sim

# -----------------------------------------------------------------------------
def bag(s):
	count = Counter(s)
	return count

def bag_dist_sim_comp(val1, val2):
	"""Calculate the bag distance similarity between the two given attribute
		 values.

		 Returns a value between 0.0 and 1.0.
	"""

	# If at least one of the values is empty return 0
	#
	if val1 is None or val2 is None or (len(val1) == 0) or (len(val2) == 0):
		return 0.0

	# If both attribute values exactly match return 1
	#
	elif (val1 == val2):
		return 1.0

	# ********* Implement bag similarity function here *********
	# Extra task only

	bag_sim = 0.0	# Replace with your code
	s1 = bag(val1)
	s2 = bag(val2)
	difference_size = max(len(s1.keys() - s2.keys()), len(s2.keys() - s1.keys()))
	bag_sim = 1.0 - difference_size / max(len(val1), len(val2))
	
	# ************ End of your bag distance code ********************************

	assert bag_sim >= 0.0 and bag_sim <= 1.0

	return bag_sim

# -----------------------------------------------------------------------------

def edit_dist_sim_comp(val1, val2):
	"""Calculate the edit distance similarity between the two given attribute
		 values.

		 Returns a value between 0.0 and 1.0.
	"""

	# If at least one of the values is empty return 0
	#
	if val1 is None or val2 is None or (len(val1) == 0) or (len(val2) == 0):
		return 0.0

	# If both attribute values exactly match return 1
	#
	elif (val1 == val2):
		return 1.0

	# ********* Implement edit distance similarity here *********

	# Extra task only

	edit_sim = 0.0	# Replace with your code

	# Faster if the first value is longer than the second value, so call
	# function with reversed values
	#
	if len(val1) < len(val2):
		return edit_dist_sim_comp(val2, val1)

	# Iterate through the characters in each value 
	previous_row = list(range(len(val2) + 1))  # Initialise first row in the
	# edit matrix
	for (i, ch1) in enumerate(val1):  # Loop over positions and characters
		current_row = [i + 1]  # Initialise next row in the edit matrix

		for (j, ch2) in enumerate(val2):
			insertion = previous_row[j + 1] + 1
			deletion = current_row[j] + 1
			substitution = previous_row[j]
			if (ch1 != ch2):
				substitution += 1

			# Get minimum of insert, delete and substitute
			current_row.append(min(insertion, deletion, substitution))

		previous_row = current_row  # Set previous row as current one

	edit_dist = current_row[-1]  # Lower right corner of edit matrix

	edit_sim = 1.0 - float(edit_dist) / float(max(len(val1), len(val2)))

	# ************ End of your edit distance code *******************************

	assert edit_sim >= 0.0 and edit_sim <= 1.0

	return edit_sim

# -----------------------------------------------------------------------------

# Additional comparison functions for: (extra tasks for students to implement)
# - dates
# - ages
# - phone numbers
# - emails
# etc.

# =============================================================================
# Function to compare a block

def compareBlocks(blockA_dict, blockB_dict, recA_gdf, recB_gdf, attr_comp_list):
    """Build a similarity dictionary with pair of records from the two given
     block dictionaries using a vectorized GPU approach with CPU fallback for
     unsupported functions.
    """

    print(f'Vectorizing {len(blockA_dict)} blocks from dataset A with {len(blockB_dict)} blocks from dataset B')
    sys.stdout.flush()

    # 1. Generate all candidate pairs from blocks
    pair_list = []
    for block_bkv, rec_idA_list in blockA_dict.items():
        if block_bkv in blockB_dict:
            rec_idB_list = blockB_dict[block_bkv]
            for rec_idA in rec_idA_list:
                for rec_idB in rec_idB_list:
                    pair_list.append((rec_idA, rec_idB))

    if not pair_list:
        print('  No candidate pairs found after blocking.')
        return {}
    
    pairs_gdf = cudf.DataFrame(pair_list, columns=['rec_id_A', 'rec_id_B'])
    print(f'  Generated {len(pairs_gdf)} candidate record pairs.')
    sys.stdout.flush()

    # 2. Join with attribute data
    recA_gdf_renamed = recA_gdf.add_suffix('_A')
    recB_gdf_renamed = recB_gdf.add_suffix('_B')

    merged_gdf = pairs_gdf.merge(recA_gdf_renamed, left_on='rec_id_A', right_index=True, how='left')
    merged_gdf = merged_gdf.merge(recB_gdf_renamed, left_on='rec_id_B', right_index=True, how='left')

    # 3. Apply comparisons
    print('  Comparing attribute values for candidate pairs (using native cudf and custom kernels where possible)...')
    sys.stdout.flush()
    
    sim_vectors_list = []
    
    for comp_funct, attr_nameA, attr_nameB in attr_comp_list:
        col_A_name = attr_nameA + '_A'
        col_B_name = attr_nameB + '_B'

        col_A = merged_gdf[col_A_name].fillna('')
        col_B = merged_gdf[col_B_name].fillna('')

        if comp_funct == exact_comp:
            sim_col = (col_A == col_B).astype('float32')



        elif comp_funct == jaccard_comp:
            print(f"    GPU kernel for: '{comp_funct.__name__}'")
            sys.stdout.flush()
            sets_A = col_A.to_pandas().apply(get_q_grams_set).tolist()
            sets_B = col_B.to_pandas().apply(get_q_grams_set).tolist()
            sim_array = calculate_jaccard_similarity_gpu_pairwise(sets_A, sets_B)
            sim_col = cudf.Series(sim_array)

        elif comp_funct == dice_comp:
            print(f"    GPU kernel for: '{comp_funct.__name__}'")
            sys.stdout.flush()
            sets_A = col_A.to_pandas().apply(get_q_grams_set).tolist()
            sets_B = col_B.to_pandas().apply(get_q_grams_set).tolist()
            sim_array = calculate_dice_similarity_gpu_pairwise(sets_A, sets_B)
            sim_col = cudf.Series(sim_array)


        elif comp_funct in [jaro_winkler_comp, edit_dist_sim_comp]:
            print(f"    GPU kernel for: '{comp_funct.__name__}'")
            sys.stdout.flush()

            char_to_int = get_char_vocab(col_A, col_B)

            s1_arr = strings_to_char_arrays(col_A, char_to_int)
            s2_arr = strings_to_char_arrays(col_B, char_to_int)

            d_s1 = cuda.to_device(s1_arr)
            d_s2 = cuda.to_device(s2_arr)
            d_out = cuda.device_array(len(col_A), dtype=np.float32)

            threadsperblock = 256
            blockspergrid = (len(col_A) + (threadsperblock - 1)) // threadsperblock

            if comp_funct == jaro_winkler_comp:
                gpu_jaro_winkler[blockspergrid, threadsperblock](d_s1, d_s2, d_out)
            else:
                gpu_levenshtein[blockspergrid, threadsperblock](d_s1, d_s2, d_out)

            sim_col = cudf.Series(d_out)

        else:
            print(f"    WARNING: '{comp_funct.__name__}' is not natively supported on GPU. Processing on CPU.")
            sys.stdout.flush()
            s_A = col_A.to_pandas()
            s_B = col_B.to_pandas()
            sim_list = [comp_funct(v1, v2) for v1, v2 in zip(s_A, s_B)]
            sim_col = cudf.Series(sim_list, nan_as_null=False)

        sim_vectors_list.append(sim_col)

    # 4. Assemble the final dictionary
    print('  Assembling final similarity vector dictionary...')
    sys.stdout.flush()

    sim_vectors_gdf = cudf.concat(sim_vectors_list, axis=1)
    sim_vectors_gdf.columns = [f'sim_{i}' for i in range(len(attr_comp_list))]

    sim_vectors_gdf['rec_id_A'] = merged_gdf['rec_id_A']
    sim_vectors_gdf['rec_id_B'] = merged_gdf['rec_id_B']

    sim_vec_dict = {}
    for row in sim_vectors_gdf.to_pandas().itertuples(index=False):
        key = (row.rec_id_A, row.rec_id_B)
        sim_vec_dict[key] = list(row)[:-2]

    print(f'  Compared {len(sim_vec_dict)} record pairs')
    print('')
    sys.stdout.flush()

    return sim_vec_dict
# -----------------------------------------------------------------------------

# End of program.
