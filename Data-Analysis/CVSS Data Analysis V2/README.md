## CVSS Data Analysis: Unsupervised Learning for Vulnerability Assessment

This repository contains the analysis for a data mining project focused on applying unsupervised learning techniques to the Common Vulnerability Scoring System (CVSS) dataset. The goal is to cluster software vulnerabilities based on their CVSS metrics, providing a structured approach for a cybersecurity procurement team to make risk-based decisions.

## Project Overview

The project leverages the CVSSv3.1 specification to transform raw vulnerability data into a format suitable for clustering. By grouping similar vulnerabilities, the analysis aims to identify distinct "severity levels" or profiles that can inform procurement strategies without relying on pre-calculated scores.

## Files in this Repository

    Clustering Data Analysis Assignment.ipynb: The main Jupyter Notebook containing all the Python code for data loading, preprocessing, feature engineering, scaling, dimensionality reduction (PCA), K-Means clustering, and visualization.

    report.pdf (or similar, if you generate one): The detailed report summarizing the methodology, results, and interpretations of the clustering analysis. (Note: This README assumes you will generate a PDF report based on the analysis in the notebook).

    CVSS_data_complete.csv: The dataset used for this analysis (assumed to be present in the same directory or specified path).

## Analysis Highlights

The Clustering Data Analysis Assignment.ipynb notebook covers the following key steps:

    Data Loading & Initial Inspection: Loading the CVSS_data_complete.csv dataset and checking for missing values.

    Missing Value Handling: Dropping rows with NaN values (though the provided snippet suggests no such values were found initially).

    Feature Engineering & Recoding: Transforming categorical CVSSv3.1 metrics (e.g., Attack Vector, Attack Complexity, User Interaction, Scope, Privileges Required, Impact metrics) into numerical representations as per the CVSSv3.1 specification.

    Data Scaling: Applying StandardScaler to normalize the numerical features, ensuring equal contribution to the clustering algorithm.

    Dimensionality Reduction (PCA): Reducing the data to 2 principal components for effective visualization of clusters.

    K-Means Clustering: Implementing the K-Means algorithm to group vulnerabilities.

    Optimal k Determination: Using the Elbow Method to identify and justify the optimal number of clusters.

    Cluster Visualization: Plotting the 2D PCA-reduced data with points colored by their assigned cluster, along with cluster centroids, to visually interpret the groupings.

## Setup and Usage

To run this analysis, you will need a Python environment with Jupyter Notebook and the following libraries installed:

    pandas

    numpy

    scikit-learn (for StandardScaler, PCA, KMeans)

    matplotlib

    seaborn

You can install these libraries using pip:

pip install pandas numpy scikit-learn matplotlib seaborn jupyter

### Running the Analysis

    Clone the Repository:

    git clone <repository-url>
    cd <repository-name>

    Place the Dataset: Ensure CVSS_data_complete.csv is in the same directory as the Jupyter Notebook, or update the file path in the notebook accordingly.

    Launch Jupyter Notebook:

    jupyter notebook

    Open the Notebook: In the Jupyter interface, open Clustering Data Analysis Assignment.ipynb and run all cells.

The notebook will execute the entire analysis pipeline, from data loading to cluster visualization.