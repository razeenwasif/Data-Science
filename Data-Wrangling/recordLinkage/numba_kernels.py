import numpy as np
from numba import cuda

Q = 2

def get_q_grams_set(s):
    if s is None:
        return set()
    return {s[i:i+Q] for i in range(len(s) - Q + 1)}

@cuda.jit
def jaccard_similarity_kernel(set1_arr, set2_arr, result_arr):
    """
    CUDA kernel to calculate Jaccard similarity between two sets.
    Assumes set1_arr and set2_arr are sorted arrays of unique integers.
    This kernel calculates the similarity for a single pair of sets.
    """
    # Get the global thread ID
    idx = cuda.grid(1)

    # This kernel is designed for a single pair of sets, so idx should be 0
    # For pairwise similarity across many sets, the kernel would need to be
    # structured differently to handle multiple pairs.
    if idx == 0:
        len1 = set1_arr.shape[0]
        len2 = set2_arr.shape[0]

        intersection_count = 0
        union_count = 0

        i, j = 0, 0
        while i < len1 and j < len2:
            if set1_arr[i] == set2_arr[j]:
                intersection_count += 1
                i += 1
                j += 1
            elif set1_arr[i] < set2_arr[j]:
                i += 1
            else:
                j += 1
        
        union_count = len1 + len2 - intersection_count

        if union_count > 0:
            result_arr[0] = intersection_count / union_count
        else:
            result_arr[0] = 1.0 # Both sets are empty, consider them identical

def calculate_jaccard_similarity_gpu(set1, set2):
    """
    Calculates the Jaccard similarity between two sets using Numba CUDA.
    """
    # Convert sets to sorted numpy arrays of hashes
    arr1 = np.array(sorted([hash(s) for s in set1]), dtype=np.int64)
    arr2 = np.array(sorted([hash(s) for s in set2]), dtype=np.int64)

    # Allocate device memory for input and output
    d_arr1 = cuda.to_device(arr1)
    d_arr2 = cuda.to_device(arr2)
    d_result = cuda.device_array(1, dtype=np.float32)

    # Configure the kernel launch
    threadsperblock = 1
    blockspergrid = 1

    # Launch the kernel
    jaccard_similarity_kernel[blockspergrid, threadsperblock](d_arr1, d_arr2, d_result)

    # Copy the result back to the host
    result = d_result.copy_to_host()
    return result[0]

@cuda.jit
def jaccard_similarity_pairwise_kernel(arr1, arr2, result_arr):
    """
    CUDA kernel to calculate Jaccard similarity between two 2D arrays of sets.
    Each row is a sorted set of integers, padded with -1.
    """
    i = cuda.grid(1)
    if i >= arr1.shape[0]:
        return

    # Find the intersection
    intersection_count = 0
    j, k = 0, 0
    while j < arr1.shape[1] and k < arr2.shape[1]:
        val1 = arr1[i, j]
        val2 = arr2[i, k]

        if val1 == -1 or val2 == -1:
            break

        if val1 == val2:
            intersection_count += 1
            j += 1
            k += 1
        elif val1 < val2:
            j += 1
        else:
            k += 1
    
    # Find the lengths of the sets
    len1 = 0
    for j in range(arr1.shape[1]):
        if arr1[i, j] != -1:
            len1 += 1
        else:
            break
            
    len2 = 0
    for j in range(arr2.shape[1]):
        if arr2[i, j] != -1:
            len2 += 1
        else:
            break

    union_count = len1 + len2 - intersection_count

    if union_count > 0:
        result_arr[i] = intersection_count / union_count
    else:
        result_arr[i] = 1.0

def calculate_jaccard_similarity_gpu_pairwise(sets1, sets2):
    """
    Calculates the Jaccard similarity for pairs of sets using Numba CUDA.
    """
    
    max_len = 0
    for s in sets1:
        max_len = max(max_len, len(s))
    for s in sets2:
        max_len = max(max_len, len(s))
        
    arr1 = np.full((len(sets1), max_len), -1, dtype=np.int64)
    arr2 = np.full((len(sets2), max_len), -1, dtype=np.int64)
    
    for i, s in enumerate(sets1):
        arr1[i, :len(s)] = np.array(sorted([hash(q) for q in s]), dtype=np.int64)

    for i, s in enumerate(sets2):
        arr2[i, :len(s)] = np.array(sorted([hash(q) for q in s]), dtype=np.int64)
        
    d_arr1 = cuda.to_device(arr1)
    d_arr2 = cuda.to_device(arr2)
    d_result = cuda.device_array(len(sets1), dtype=np.float32)
    
    threadsperblock = 256
    blockspergrid = (len(sets1) + (threadsperblock - 1)) // threadsperblock
    
    jaccard_similarity_pairwise_kernel[blockspergrid, threadsperblock](d_arr1, d_arr2, d_result)
    
    return d_result.copy_to_host()
