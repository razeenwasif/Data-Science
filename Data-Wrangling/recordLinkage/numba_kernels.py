import numpy as np
from numba import cuda

Q = 2

def get_q_grams_set(s):
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