from numba import cuda

@cuda.jit(device=True)
def get_q_grams_gpu(s, q, q_grams):
    for i in range(len(s) - q + 1):
        q_grams[i] = s[i:i+q]

@cuda.jit(device=True)
def jaccard_comp_gpu(s1, s2):
    # This is a simplified implementation for demonstration purposes.
    # A real implementation would need to handle memory allocation and
    # other complexities.
    if len(s1) == 0 or len(s2) == 0:
        return 0.0
    if s1 == s2:
        return 1.0

    q = 2
    q_grams1 = cuda.local.array(shape=100, dtype='<U3')
    q_grams2 = cuda.local.array(shape=100, dtype='<U3')

    get_q_grams_gpu(s1, q, q_grams1)
    get_q_grams_gpu(s2, q, q_grams2)

    intersection = 0
    for i in range(len(s1) - q + 1):
        for j in range(len(s2) - q + 1):
            if q_grams1[i] == q_grams2[j]:
                intersection += 1
                break

    union = (len(s1) - q + 1) + (len(s2) - q + 1) - intersection

    if union == 0:
        return 1.0
    else:
        return intersection / union

@cuda.jit
def compare_kernel(s1, s2, out, comp_funct):
    i = cuda.grid(1)
    if i < s1.size:
        out[i] = comp_funct(s1[i], s2[i])
