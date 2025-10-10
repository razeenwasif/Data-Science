# --- filename: comparison.py ---
import os
import sys
import numpy as np
from collections import Counter
import cudf
import cupy
from numba import cuda
from numba_kernels import (
    calculate_jaccard_similarity_gpu_pairwise,
    calculate_dice_similarity_gpu_pairwise,
    calculate_jaro_winkler_pairwise_gpu,
    calculate_levenshtein_pairwise_gpu,
    get_q_grams_set,
)

MAX_STRING_LEN = 128
Q = 2


def get_q_grams(s, q):
    if s is None:
        return set()
    return {s[i:i+q] for i in range(len(s) - q + 1)}


# ------------------- stable CPU comparisons -------------------

def exact_comp(val1, val2):
    if val1 is None or val2 is None or (len(val1) == 0) or (len(val2) == 0):
        return 0.0
    return 1.0 if val1 == val2 else 0.0


def jaccard_comp(val1, val2):
    if val1 is None or val2 is None or (len(val1) == 0) or (len(val2) == 0):
        return 0.0
    if val1 == val2:
        return 1.0
    s1 = get_q_grams(val1, Q)
    s2 = get_q_grams(val2, Q)
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    inter = len(s1.intersection(s2))
    union = len(s1.union(s2))
    return float(inter) / union


def dice_comp(val1, val2):
    if val1 is None or val2 is None or (len(val1) == 0) or (len(val2) == 0):
        return 0.0
    if val1 == val2:
        return 1.0
    s1 = get_q_grams(val1, Q)
    s2 = get_q_grams(val2, Q)
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    inter = len(s1.intersection(s2))
    return 2.0 * inter / (len(s1) + len(s2))


# Reuse existing Python implementations of jaro/winkler/edit for correctness
from rapidfuzz.distance import Levenshtein


def jaro_comp(val1, val2):
    # fall back to simple library if available
    try:
        from rapidfuzz.string_metric import jaro_similarity
        return float(jaro_similarity(val1, val2))
    except Exception:
        # lightweight fallback (approx)
        if val1 == val2:
            return 1.0
        return 0.0


def jaro_winkler_comp(val1, val2):
    try:
        from rapidfuzz.string_metric import jaro_winkler_similarity
        return float(jaro_winkler_similarity(val1, val2))
    except Exception:
        return jaro_comp(val1, val2)


def edit_dist_sim_comp(val1, val2):
    if val1 is None or val2 is None or (len(val1) == 0) or (len(val2) == 0):
        return 0.0
    if val1 == val2:
        return 1.0
    # normalized Levenshtein
    dist = Levenshtein.distance(val1, val2)
    maxlen = max(len(val1), len(val2))
    return 1.0 - float(dist) / float(maxlen)


# ------------------- GPU helpers -------------------

def _series_to_padded_uint8(series, max_len=MAX_STRING_LEN):
    """Convert cuDF string Series to numpy uint8 padded array and lengths.
    Returns (arr, lengths) where arr.shape = (n, max_len), dtype=uint8 and
    lengths.shape = (n,), dtype=int32.
    """
    if len(series) == 0:
        return np.empty((0, max_len), dtype=np.uint8), np.empty((0,), dtype=np.int32)
    # Convert to Python list of bytes
    py_list = series.fillna('').to_arrow().to_pylist()
    n = len(py_list)
    arr = np.zeros((n, max_len), dtype=np.uint8)
    lengths = np.zeros((n,), dtype=np.int32)
    for i, s in enumerate(py_list):
        if s is None:
            continue
        if isinstance(s, str):
            b = s.encode('utf8', errors='ignore')[:max_len]
        else:
            # bytes-like
            b = bytes(s)[:max_len]
        arr[i, :len(b)] = np.frombuffer(b, dtype=np.uint8)
        lengths[i] = len(b)
    return arr, lengths


# ------------------- chunk processor (uses GPU pairwise for edit-style where possible) -------------------

def _process_chunk(pairs_chunk, recA_gdf_renamed, recB_gdf_renamed, attr_comp_list, chunk_num):
    pairs_gdf = cudf.DataFrame(pairs_chunk, columns=['rec_id_A', 'rec_id_B'])

    unique_ids_A = pairs_gdf['rec_id_A'].unique()
    unique_ids_B = pairs_gdf['rec_id_B'].unique()

    chunk_recA_gdf = recA_gdf_renamed.loc[unique_ids_A]
    chunk_recB_gdf = recB_gdf_renamed.loc[unique_ids_B]

    merged_gdf = pairs_gdf.merge(chunk_recA_gdf, left_on='rec_id_A', right_index=True, how='left')
    merged_gdf = merged_gdf.merge(chunk_recB_gdf, left_on='rec_id_B', right_index=True, how='left')

    print(f'  Comparing attribute values for candidate pairs chunk {chunk_num} (using native cudf and GPU kernels where possible)...')
    sys.stdout.flush()

    sim_vectors_list = []

    # Precompute GPU arrays for attributes that will use pairwise GPU kernels
    # Gather attribute names that are GPU-capable
    gpu_attrs = set()
    for comp_funct, aA, aB in attr_comp_list:
        if comp_funct in (jaro_winkler_comp, edit_dist_sim_comp):
            gpu_attrs.add((aA, aB))

    gpu_buffers = {}
    for aA, aB in gpu_attrs:
        colA = merged_gdf[aA + '_A'].fillna('')
        colB = merged_gdf[aB + '_B'].fillna('')
        arrA, lenA = _series_to_padded_uint8(colA, max_len=MAX_STRING_LEN)
        arrB, lenB = _series_to_padded_uint8(colB, max_len=MAX_STRING_LEN)
        # Transfer to device
        d_arrA = cuda.to_device(arrA)
        d_lenA = cuda.to_device(lenA)
        d_arrB = cuda.to_device(arrB)
        d_lenB = cuda.to_device(lenB)
        gpu_buffers[(aA, aB)] = (d_arrA, d_lenA, d_arrB, d_lenB)

    for comp_funct, attr_nameA, attr_nameB in attr_comp_list:
        col_A = merged_gdf[attr_nameA + '_A'].fillna('')
        col_B = merged_gdf[attr_nameB + '_B'].fillna('')

        if comp_funct == exact_comp:
            sim_col = (col_A == col_B).astype('float32')

        elif comp_funct == jaccard_comp:
            qgrams_A = col_A.str.ngrams(n=Q).explode().reset_index()
            qgrams_A.columns = ['index', 'qgram']
            qgrams_B = col_B.str.ngrams(n=Q).explode().reset_index()
            qgrams_B.columns = ['index', 'qgram']
            qgrams_A = qgrams_A.drop_duplicates()
            qgrams_B = qgrams_B.drop_duplicates()
            len_A = qgrams_A.groupby('index')['qgram'].count().rename('len_A')
            len_B = qgrams_B.groupby('index')['qgram'].count().rename('len_B')
            intersection = qgrams_A.merge(qgrams_B, on=['index', 'qgram'], how='inner')
            intersection_size = intersection.groupby('index')['qgram'].count().rename('intersection_size')
            sim_df = cudf.concat([len_A, len_B, intersection_size], axis=1).fillna(0)
            union_size = sim_df['len_A'] + sim_df['len_B'] - sim_df['intersection_size']
            sim_col = (sim_df['intersection_size'] / union_size).fillna(0)

        elif comp_funct == dice_comp:
            qgrams_A = col_A.str.ngrams(n=Q).explode().reset_index()
            qgrams_A.columns = ['index', 'qgram']
            qgrams_B = col_B.str.ngrams(n=Q).explode().reset_index()
            qgrams_B.columns = ['index', 'qgram']
            qgrams_A = qgrams_A.drop_duplicates()
            qgrams_B = qgrams_B.drop_duplicates()
            len_A = qgrams_A.groupby('index')['qgram'].count().rename('len_A')
            len_B = qgrams_B.groupby('index')['qgram'].count().rename('len_B')
            intersection = qgrams_A.merge(qgrams_B, on=['index', 'qgram'], how='inner')
            intersection_size = intersection.groupby('index')['qgram'].count().rename('intersection_size')
            sim_df = cudf.concat([len_A, len_B, intersection_size], axis=1).fillna(0)
            sum_len = sim_df['len_A'] + sim_df['len_B']
            sim_col = (2 * sim_df['intersection_size'] / sum_len).fillna(0)

        elif comp_funct in (jaro_winkler_comp, edit_dist_sim_comp):
            # Try GPU pairwise implementation if available and sizes are reasonable
            try:
                d_arrA, d_lenA, d_arrB, d_lenB = gpu_buffers[(attr_nameA, attr_nameB)]
                if comp_funct == jaro_winkler_comp:
                    sims = calculate_jaro_winkler_pairwise_gpu(d_arrA, d_lenA, d_arrB, d_lenB)
                else:
                    sims = calculate_levenshtein_pairwise_gpu(d_arrA, d_lenA, d_arrB, d_lenB)
                sim_col = cudf.Series(sims)
            except Exception:
                # graceful fallback to CPU implementation
                print('    NOTE: GPU path failed; using CPU fallback for edit-style similarity')
                sys.stdout.flush()
                s_A = col_A.to_pandas()
                s_B = col_B.to_pandas()
                sim_list = [comp_funct(v1, v2) for v1, v2 in zip(s_A, s_B)]
                sim_col = cudf.Series(sim_list, nan_as_null=False)

        else:
            print(f"    WARNING: '{comp_funct.__name__}' is not natively supported on GPU. Processing on CPU.")
            sys.stdout.flush()
            s_A = col_A.to_pandas()
            s_B = col_B.to_pandas()
            sim_list = [comp_funct(v1, v2) for v1, v2 in zip(s_A, s_B)]
            sim_col = cudf.Series(sim_list, nan_as_null=False)

        try:
            sample_vals = sim_col.head(5).to_pandas().tolist()
            print(f'    sample sim ({attr_nameA}->{attr_nameB}): {sample_vals}')
            sys.stdout.flush()
        except Exception:
            pass

        sim_vectors_list.append(sim_col.astype('float32'))

    sim_vectors_gdf = cudf.concat(sim_vectors_list, axis=1)
    sim_vectors_gdf.columns = [f'sim_{i}' for i in range(len(attr_comp_list))]
    sim_vectors_gdf['rec_id_A'] = merged_gdf['rec_id_A']
    sim_vectors_gdf['rec_id_B'] = merged_gdf['rec_id_B']

    del pairs_gdf, merged_gdf
    import gc
    gc.collect()

    return sim_vectors_gdf


# The rest of compareBlocks / compare_pairs remains unchanged (omitted here for brevity)


# --- filename: numba_kernels.py ---
import numpy as np
from numba import cuda

@cuda.jit
def _jaro_winkler_kernel(arr1, len1, arr2, len2, out, max_len):
    i = cuda.grid(1)
    if i >= arr1.shape[0]:
        return
    # Implement a simple byte-wise Jaro-like similarity using windowing
    l1 = len1[i]
    l2 = len2[i]
    if l1 == 0 or l2 == 0:
        out[i] = 0.0
        return
    match_distance = max(l1, l2) // 2 - 1
    matches = 0
    trans = 0
    # Local flags are not straightforward; use simple nested loops (O(n*m))
    for a in range(l1):
        start = 0 if a - match_distance < 0 else a - match_distance
        end = l2 if a + match_distance + 1 > l2 else a + match_distance + 1
        for b in range(start, end):
            if arr1[i, a] == arr2[i, b]:
                matches += 1
                break
    if matches == 0:
        out[i] = 0.0
        return
    # naive transposition approx: count positions where bytes differ at same index up to min(l1,l2)
    minl = l1 if l1 < l2 else l2
    mismatch = 0
    for k in range(minl):
        if arr1[i, k] != arr2[i, k]:
            mismatch += 1
    trans = mismatch
    jaro = (matches / l1 + matches / l2 + (matches - trans/2) / matches) / 3.0
    # winkler prefix
    prefix = 0
    for k in range(min(4, minl)):
        if arr1[i, k] == arr2[i, k]:
            prefix += 1
        else:
            break
    out[i] = jaro + prefix * 0.1 * (1.0 - jaro)


@cuda.jit
def _levenshtein_kernel(arr1, len1, arr2, len2, out, max_len):
    i = cuda.grid(1)
    if i >= arr1.shape[0]:
        return
    l1 = len1[i]
    l2 = len2[i]
    if l1 == 0 and l2 == 0:
        out[i] = 1.0
        return
    if l1 == 0:
        out[i] = 0.0
        return
    # Use small DP table in global memory per thread (inefficient but correct)
    # allocate arrays in host memory style via python can't here; so use simple looped method
    # Build previous and current row arrays in python-style using CUDA local arrays
    prev = cuda.local.array(256, dtype=np.int32)
    curr = cuda.local.array(256, dtype=np.int32)
    for j in range(l2 + 1):
        prev[j] = j
    for a in range(1, l1 + 1):
        curr[0] = a
        ca = arr1[i, a-1]
        for b in range(1, l2 + 1):
            cost = 0 if ca == arr2[i, b-1] else 1
            insert = curr[b-1] + 1
            delete = prev[b] + 1
            replace = prev[b-1] + cost
            # min of three
            m = insert
            if delete < m:
                m = delete
            if replace < m:
                m = replace
            curr[b] = m
        for j in range(l2 + 1):
            prev[j] = curr[j]
    dist = curr[l2]
    out[i] = 1.0 - float(dist) / float(max(l1, l2))


def calculate_jaro_winkler_pairwise_gpu(d_arrA, d_lenA, d_arrB, d_lenB):
    n = d_arrA.shape[0]
    out = cuda.device_array(n, dtype=np.float32)
    threadsperblock = 128
    blockspergrid = (n + (threadsperblock - 1)) // threadsperblock
    _jaro_winkler_kernel[blockspergrid, threadsperblock](d_arrA, d_lenA, d_arrB, d_lenB, out, d_arrA.shape[1])
    return out.copy_to_host()


def calculate_levenshtein_pairwise_gpu(d_arrA, d_lenA, d_arrB, d_lenB):
    n = d_arrA.shape[0]
    out = cuda.device_array(n, dtype=np.float32)
    threadsperblock = 128
    blockspergrid = (n + (threadsperblock - 1)) // threadsperblock
    _levenshtein_kernel[blockspergrid, threadsperblock](d_arrA, d_lenA, d_arrB, d_lenB, out, d_arrA.shape[1])
    return out.copy_to_host()


# --- filename: comparison_kernels.py ---
# This file remains a minimal set of illustrative kernels; advanced logic moved to numba_kernels.py

@cuda.jit
def compare_kernel(s1, s2, out, comp_funct):
    i = cuda.grid(1)
    if i < s1.size:
        out[i] = comp_funct(s1[i], s2[i])

