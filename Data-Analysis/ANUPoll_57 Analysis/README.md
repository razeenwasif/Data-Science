## ANU Poll 57 Data Mining and Analysis

This repository contains R scripts and a report detailing a comprehensive data mining and analysis project performed on the ANU Poll 57 dataset. The project explores various data mining techniques, including association mining, classification (Logistic Regression, Decision Trees, SVM, Neural Networks), regression (Regression Trees, Neural Networks), and clustering (K-Means).

## Project Overview

The primary goal of this project is to analyze the ANU Poll 57 data, which captures Australian citizens' opinions on important and topical issues, particularly the Australian Constitutional Referendum on the Aboriginal and Torres Strait Islander Voice to Parliament. The analysis aims to understand public sentiment, identify demographic influences, and explore relationships between opinions and demographics.

## Files in this Repository

    ANUPoll_57_Analysis.R: This script focuses on initial data exploration, cleaning, correlation analysis, and association mining. It identifies factors associated with respondents' satisfaction with the country's future (variable A1).

    ANUPoll_57_Classification.R: This script implements and evaluates various classification models (Logistic Regression, Decision Trees, SVM, Neural Networks) to predict how people voted in the referendum (variable RB1). It includes hyperparameter tuning and performance evaluation using confusion matrices and ROC curves.

    ANUPoll_57_Clustering.R: This script performs K-Means clustering on selected demographic variables (RD7_a to RD7_e) to identify distinct groups within the dataset. It includes methods for determining the optimal number of clusters and interpreting cluster characteristics.

    ANUPoll_57_Regression.R: This script builds and evaluates regression models (Regression Trees and Neural Networks) to predict the weight_final_ref variable, which represents demographic weighting. It includes hyperparameter tuning and performance metrics like RMSE, R-Squared, and MAE.

    comp3425_assignment2_v2.pdf: This PDF outlines the assignment brief for COMP3425 Data Mining S1 2024, providing the context and requirements for the project.

    report.pdf: This is the final project report, detailing the methodology, results, and discussion for each data mining task. It includes qualitative summaries, model evaluations, and interpretations of findings.

## Analysis Highlights

    Data Cleaning: Comprehensive handling of missing values and removal of irrelevant columns.

    Correlation Analysis: Examination of pairwise correlations between key variables to understand relationships.

    Association Mining: Discovery of interesting association rules related to public satisfaction with the country's future, with a focus on interpreting their objective and subjective significance.

    Classification: Development and comparison of multiple classification models to predict referendum voting behavior, highlighting the strengths and weaknesses of each approach.

    Regression: Implementation of regression models to predict demographic weighting, with a focus on model selection and optimization.

    Clustering: Identification of distinct respondent groups based on their opinions on specific social and political statements.

## Setup and Usage

To run the R scripts, you will need to have R and RStudio installed, along with the following R packages:

    ggplot2

    Hmisc

    corrplot

    arules

    party

    GGally

    arulesViz

    dplyr

    tidymodels

    caret

    rpart

    pROC

    rpart.plot

    tree

    e1071

    kernlab

    neuralnet

    tidyverse

    vip

    RColorBrewer

    factoextra

    cluster

    gridExtra

You can install these packages in R using install.packages("package_name").

    Download the Dataset: The project uses the 02_ANUPoll_57_CSV_100150_general.csv dataset. Ensure this file is placed in the same directory as your R scripts, or update the setwd() and filename variables in each R script to point to the correct location of your data.

    Run the R Scripts: Execute each .R script in RStudio. The scripts are designed to perform data loading, cleaning, model training, and evaluation.

    Review the Report: Refer to report.pdf for detailed explanations, results, and interpretations of the analysis performed by the R scripts.