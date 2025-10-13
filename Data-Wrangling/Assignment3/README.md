# Record Linkage GPU Pipeline

## Overview
This project implements a GPU-accelerated record linkage workflow that loads two person-level datasets, blocks records to curtail comparisons, computes similarity vectors, classifies matches with a cuML-based random forest, evaluates metrics, and writes the predicted matches to `out/matches.csv`. The code is organised inside `src/` with modular steps you can customise for different linkage scenarios.

## Prerequisites
- NVIDIA GPU with a supported CUDA driver (CUDA 12.x as exported in `conda_env.txt`).
- Conda (Miniconda/Anaconda) to manage the RAPIDS stack.
- Datasets formatted as CSV files containing the attributes referenced in `recordLinkage.py`.

### Environment setup
```bash
# create an environment matching the exported stack
conda create -n rapids-rl --file conda_env.txt
conda activate rapids-rl
```
If you need a leaner environment, start from `rapidsai` nightly packages that match your CUDA version and add dependencies listed in the spec file (cuDF, cuML, cuGraph, FAISS, CuPy, rapidfuzz, numba, etc.).

## Repository layout
- `src/recordLinkage.py` – entry point orchestrating the six pipeline stages.
- `src/config.py` – high-level knobs (logging, q-gram length, GPU toggle, classifier size).
- `src/blocking.py` – blocking strategies, including ANN-based candidate generation.
- `src/comparison.py` – similarity functions with GPU and CPU implementations.
- `src/classification.py` – cuML random forest training, threshold selection, and scoring.
- `src/evaluation.py` – blocking and linkage quality metrics.
- `src/saveLinkResult.py` – writes the match set to CSV.
- `src/datasets/` – default CSV inputs supplied for the assignment.
- `out/` – pipeline output directory (`matches.csv` is created here).

## Running the pipeline
```bash
python src/recordLinkage.py assignment_datasets
```
The positional argument selects a dataset preset. The following presets are predefined inside `recordLinkage.py`:
- `assignment_datasets` (default if omitted)
- `clean_100000`
- `little-dirty_100000`
- `very-dirty_100000`

Each preset maps to three CSV files (`datasetA`, `datasetB`, and `truthfile`). To add new data, extend the `dataset_configs` dictionary with your own key and file paths.

## Core settings to tweak
### `src/config.py`
- `Q_GRAM_LENGTH` – length of q-grams for Jaccard/Dice similarities. Higher values tighten comparisons but require more exact matches.
- `ML_N_ESTIMATORS` – number of trees in the cuML random forest. Increase for better recall at the cost of GPU memory and runtime.
- `LOG_LEVEL` / `LOG_FORMAT` – standard Python logging settings used across modules.
- `USE_GPU_COMPARISON` – disable to force CPU comparisons (useful for development without a GPU). GPU kernels fall back to CPU automatically on failure, but explicit disable keeps everything on host.

### Blocking controls (`src/recordLinkage.py`)
- `partition_attr` and `ann_attrs` determine the blocking scheme. Adjust attribute lists to better capture your domain (e.g., include postcode for geographic clustering).
- `K_NEIGHBORS` and `ann_sim_threshold` define the ANN search breadth. Larger `k` and lower thresholds trade runtime for recall.
- Dataset-specific overrides are applied before candidate generation. Add your own category or tweak the per-category values to balance speed and quality.

### Comparison controls (`src/recordLinkage.py` and `src/comparison.py`)
- `approx_comp_funct_list` defines which similarity function is applied to each attribute. You can add/remove tuples or swap in CPU-only helpers from `comparison.py`.
- `attr_list` controls which columns are loaded from the CSV files. Keep it in sync with your data schema.
- To change GPU memory usage, adjust `MAX_STRING_LEN` in `comparison.py` for long text fields.

### Classification controls (`src/classification.py`)
- `supervisedMLClassify` accepts `n_estimators` and `threshold_offset`. The main script already passes `threshold_offset` based on dataset category—modify that logic if you introduce new presets.
- Ratio and depth grids (`ratio_candidates`, `depth_candidates`) govern hyper-parameter search. Expand these lists to explore additional model sizes.
- To use a deterministic split, change the `random_state` values inside the sampling routines.

### Output and evaluation
- Results are written by default to `out/matches.csv`. Pass a different path to `saveLinkResult.save_linkage_set` if you want separate runs.
- Blocking and linkage metrics print to stdout. Redirect to a log file if you want persistent audit trails (`python src/recordLinkage.py ... | tee run.log`).

## Adding new datasets
1. Place your CSVs under `src/datasets/` (or another path of your choosing).
2. Ensure record IDs and attribute names match the expectations in `attr_list`. Columns are converted to lowercase on load.
3. Update `dataset_configs` with the new key and file paths.
4. Optionally add a new `dataset_category` to drive specialised blocking thresholds or classifier offsets.

## Troubleshooting
- **CUDA out of memory** – reduce ANN `K_NEIGHBORS`, increase filtering thresholds, or disable GPU comparisons to fall back on CPU.
- **Missing RAPIDS libraries** – rebuild the environment from `conda_env.txt` or install the specific packages (`conda install -n rapids-rl -c rapidsai -c conda-forge cudf cuml cupy faiss-gpu`).
- **Slow CPU runs** – set `USE_GPU_COMPARISON=True` and verify the environment is activated on a GPU-enabled host.

## Example workflow
```bash
conda activate rapids-rl
python src/recordLinkage.py clean_100000
```
Adjust `LOG_LEVEL` in `src/config.py` if you need more verbose logs during the run. After completion, inspect `out/matches.csv` and the logged precision/recall metrics to validate linkage quality. Iterate on the blocking and comparison settings as described above to meet your specific data quality and runtime targets.

## Further Reading

### Library documentation
- RAPIDS cuDF documentation: https://docs.rapids.ai/api/cudf/stable/
- RAPIDS cuML documentation (RandomForest, TF-IDF, ANN utilities): https://docs.rapids.ai/api/cuml/stable/
- CuPy user guide: https://docs.cupy.dev/en/stable/
- Numba CUDA programming guide: https://numba.readthedocs.io/en/stable/cuda/index.html
- FAISS GPU reference: https://faiss.ai/
- RapidFuzz API reference: https://rapidfuzz.github.io/rapidfuzz/

### GPU-accelerated record linkage & entity resolution
- Y. Jiang, P. Christen, U. Rahm, “Scaling blocking for record linkage on multi-core and GPU processors,” *The VLDB Journal* 26, 811–835 (2017). https://doi.org/10.1007/s00778-016-0440-4
- NVIDIA Developer Blog, “Accelerating Entity Resolution with RAPIDS,” highlights GPU-accelerated record linkage workflows using cuDF and cuML. https://developer.nvidia.com/blog/accelerating-entity-resolution-with-rapids/
- RAPIDS notebooks-contrib, “Record Linkage with RAPIDS cuDF and cuML,” end-to-end GPU pipeline example. https://github.com/rapidsai/notebooks-contrib/blob/main/intermediate_notebooks/rapids_record_linkage.ipynb

### Custom GPU kernels with Numba
- NVIDIA Developer Blog, “CUDA Python: Using Numba to Accelerate Python,” walkthrough of writing and optimizing custom CUDA kernels in Python. https://developer.nvidia.com/blog/cuda-python-numba/
- S. K. Lam, A. Pitrou, S. Seibert, “Numba: A LLVM-based Python JIT compiler,” *Proceedings of the Second Workshop on the LLVM Compiler Infrastructure in HPC*, 2015. https://doi.org/10.1145/2833157.2833162
- RAPIDS documentation on user-defined functions with Numba (applies to custom kernels executed inside cuDF): https://docs.rapids.ai/api/cudf/stable/udf/intro/
