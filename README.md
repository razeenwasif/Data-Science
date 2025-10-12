# Machine Learning and Data Science Portfolio

A curated collection of coursework, experiments, and reports covering the data science pipeline—from exploratory analysis and predictive modelling through to large-scale data wrangling and relational database design. Projects live in self-contained folders that include source code, datasets, and supporting documentation.

## Repository Structure

| Directory | Focus |
|-----------|-------|
| `Data-Analysis` | R- and Python-based analytical studies, including clustering, classification, regression, and interactive reporting. |
| `Data-Wrangling` | Data cleaning, feature engineering, and record linkage pipelines implemented with Python scripts and notebooks. |
| `Relational Database` | SQL coursework, schema design artefacts, and reference material for relational systems and SQLite. |

Each subdirectory often contains its own `README.md`, reports, and assignment briefs that provide project-specific context.

## Featured Projects

- **ANU Poll 57 Data Mining (`Data-Analysis/ANUPoll_57 Analysis`)**: R scripts that walk through association mining, supervised learning, regression, and clustering to interpret national survey responses; includes a comprehensive final report and scripted visualisations.
- **CVSS Vulnerability Analysis (`Data-Analysis/CVSS Data Analysis*`)**: Companion Python notebooks, scripts, and HTML dashboards for analysing CVSS vulnerability data with statistical modelling and interactive exploration.
- **Record Linkage Pipeline (`Data-Wrangling/recordLinkage`)**: End-to-end entity matching workflow featuring configurable blocking strategies, similarity scoring kernels (CPU/GPU), and evaluation utilities.
- **Data Wrangling Assignments (`Data-Wrangling/Assignment1–3`)**: Reproducible pipelines for auditing, transforming, and validating large datasets, accompanied by written reports and generated plots.
- **SQLite Coursework (`Relational Database/SQLite Assignment` & `Introduction to SQLite`)**: Jupyter notebooks, ER diagrams, and practice databases that demonstrate schema exploration, SQL querying, and database analysis.

## Getting Started

Most folders are standalone; review the local README or report first. Common setup steps include:

- **Python environments** (for data wrangling and CVSS projects):
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt  # if provided
  ```
- **R projects** (for ANU Poll analysis): Install R/RStudio and the libraries listed in the project README (e.g., `tidyverse`, `caret`, `arules`, `neuralnet`, `factoextra`, `cluster`).
- **SQLite notebooks**: Launch Jupyter (`jupyter notebook`) or VS Code, and ensure SQLite binaries are available if you wish to run queries outside the notebooks.

## Data and Reports

- Datasets (CSV/SQLite) are stored alongside the scripts that consume them; many are large, so version control is configured to keep them locally.
- PDF and Markdown reports summarise methodology and findings for most assignments—use them for a quick narrative overview before diving into code.

## Contributing & Extensions

This repository documents academic work and experimentation. If you fork or build upon these projects:

- Preserve dataset confidentiality requirements from the original assignments.
- Add environment files (`requirements.txt`, `environment.yml`, or `renv.lock`) when introducing new dependencies.
- Prefer reproducible scripts/notebooks and document any manual preprocessing in the relevant README.
