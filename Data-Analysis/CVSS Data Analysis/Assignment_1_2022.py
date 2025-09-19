# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# <h1 align='center'> COMP2420/COMP6420 - Introduction to Data Management,<br/> Analysis and Security</h1>
#
# <h1 align='center'> Assignment - 1 (2022)</h1>
#
# -----
#
# |**Maximum Marks**         |**100**
# |--------------------------|--------
# |  **Weight**              |  **15% of the Total Course Grade**
# |  **Submission deadline** |  **TBA**
# |  **Submission mode**     |  **Electronic, Using GitLab**
# |  **Penalty**             |  **100% after the deadline**
#
#
# ## Learning Outcomes
# The following learning outcomes apply to this piece:
# - **LO3** - Demonstrate basic knowledge and understanding of descriptive and predictive data analysis methods, optimization and search, and knowledge representation.
# - **LO4** - Formulate and extract descriptive and predictive statistics from data
# - **LO5** - Analyse and interpret results from descriptive and predictive data analysis
# - **LO6** - Apply their knowledge to a given problem domain and articulate potential data analysis problems
#
#
# ## Submission
#
# You need to submit the following items:
# - The notebook `Assignment_1_2022_uXXXXXXX.ipynb` (where uXXXXXXX is your uid) 
# - A completed `statement-of-originality.md`, found in the root of the forked gitlab repo.
#
# Submissions are performed by pushing to your forked GitLab assignment repository. For a refresher on forking and cloning repositories, please refer to `Lab 1`. Issues with your Git repo (with the exception of a CECS/ANU wide Gitlab failure) will not be considered as grounds for an extension. You will also need to add your details below. Any variation of this will result in a `zero mark`.
#
# ***** 
#
# ### Notes:
#
# * It is strongly advised to read the whole assignment before attempting it and have at least a cursory glance at the dataset in order to gauge the requirements and understand what you need to do as a bigger picture.
# * Backup your assignment to your Gitlab repo often. 
# * Extra reading and research will be required. Make sure you include all references in your Statement of Originality. If this does not occur, at best marks will be deduced. Otherwise, academic misconduct processes will be followed.
# * For answers requiring free form written text, use the designated cells denoted by `YOUR WRITTEN ANSWER HERE` -- double click on the cell to write inside them.
# * For all coding questions please write your code after the comment `YOUR CODE HERE`. Remember to document your code using comments and doc strings as appropriate.
# * In the process of testing your code, you can insert more cells or use print statements for debugging, but when submitting your file remember to remove these cells and calls respectively. You are welcome to add additional cells to the final submission, provided they add value to the overall piece.
# * You will be marked on **correctness** and **readability** of your code, if your marker can't understand your code your marks may be deducted.
# * Comment your code.
# * Before submitting, restart the kernel in Jupyter Lab and re-run all cells before submitting your code. This will ensure the namespace has not kept any old variables, as these won't come across in submission and your code will not run. Without this, you could lose a significant number of marks.
#
# *****
#
# Credit: This assignment is based on previous work by Alex Niven in COMP2420/6420.  We thank Alex for allowing us to use his work and build on it.

# %% [markdown]
# ### Enter your Student ID below:

# %% [raw]
# u7283652

# %% [markdown]
# ******
# ## Context
# You have been hired as a data scientist on a cybersecurity consulting team.  Your team has been tasked with advising government on the risk and impact of recent cybersecurity threats. 
#
# ### What is cybersecurity and why do we care?
#
# “Cybersecurity is the practice of protecting critical systems and sensitive information from digital attacks” (IBM,2022).  Attackers normally target vulnerabilities in software and hardware systems in order to either bring down a system or steal sensitive or personal information.  Common cyber threats include malware, phishing, ransomware and distributed denial of service (DDoS).  You can read more about cyber threats on [the Australian Cyber Security Centre web page](https://www.cyber.gov.au/acsc/individuals-and-families/threats).  
#
# Cyber-attacks can have significant negative impact to individuals, businesses and society at large.  They can lead to loss of privacy and money, cause disruption in key services and even cause death (some examples are given in [this article on impact of cyber-attacks here](https://www.securitymagazine.com/articles/96337-the-real-world-impacts-of-cyberattacks)).  Moreover, dealing with cyber-attacks is expensive.  IBM reports that the cost of a data breach in 2020 was USD $3.85 million globally (IBM, 2022).  
#
#
# ### How could you start your underlying investigation?
#
# As a data scientist, you need to understand what problem you are trying to solve first.  In this particular case, you are trying to assess the risk and impact of recent cybersecurity threats.  In order to do so, you need to know what are those threats and have a method to carry out this assessment.  Where can you find this information?  There are various sources you could draw from.  To get started, your team has identified a few relevant systems for your investigation as described next.
#
# #### The Common Vulnerability and Exposures (CVE) system
# The CVE system is like a database that holds a number of the publicly known vulnerabilities that exist for software. It is the de-facto identifying system for publicly exposed vulnerabilities in systems, used by big tech companies such as  Apple, Microsoft, Google, Red Hat, etc. The CVE is a schema that allows the consistent storing of information regarding vulnerabilities.  More reading on the CVE is [here](https://www.cve.org/)
#
# The CVE system was developed by [The MITRE Corporation](https://www.mitre.org/) almost 20 years ago, and is now the de-facto system for providing identifiers for vulnerabilities in various systems. 
#
# CVE defines a vulnerability as, _"A weakness in the computational logic (e.g., code) found in software and hardware components that, when exploited, results in a negative impact to confidentiality, integrity, or availability"._ A CVE can affect multiple products and multiple software versions of a product.
#
# However, the CVE system alone is incomplete, and extended by organisations such as the **National Vulnerability Database (NVD)**.
#
# #### The Common Weakness Enumeration (CWE) system
# There is another related system to CVE called the [Common Weakness Enumeration (CWE)](https://cwe.mitre.org), also developed by MITRE. CWE categorises types of software vulnerabilities whereas CVE is just a list of currently known vulnerabilities regarding specific systems and products (Camacho, 2021) .  Each CWE identifier is related to a specific type of weakness which will have its own unique characteristics, rather than specific instances of vulnerabilities within products or systems. 
# The CWE's are broadly viewed in three categories:
# - [by Software Development](https://cwe.mitre.org/data/definitions/699.html)
# - [by Hardware Design](https://cwe.mitre.org/data/definitions/1194.html)
# - [by Research Concepts](https://cwe.mitre.org/data/definitions/1000.html)
#
# #### The Common Vulnerability Scoring System (CVSS)
# CVSS is the de-facto scoring system for determining the impacts of vulnerabilities in the CVE system.  It is developed and maintained by the [National Vulnerability Database (NVD)](https://nvd.nist.gov).  All vulnerabilities in the NVD have been assigned a CVE identifier. Developed by the Forum of Incident Response and Security Teams (FIRST), the CVSS system is now in its 3<sup>rd</sup> major iteration (version 3).
#
# ### The Assignment Dataset: based on the Common Vulnerability Scoring System (CVSS) data
# The assignment dataset is derived from a subset of the Common Vulnerability Scoring System (CVSS) data for the year 2020 available from the [National Vulnerability Database (NVD)](https://nvd.nist.gov). 
#
# Note that while over 1000 CWE identifiers exist, only a small subset will be present within our dataset. This is due to the NVD using their own subset of them, which can be found on the [NVD website](https://nvd.nist.gov/vuln/categories).
#
# We have further filtered the 2020 CVSS dataset by retaining only the records that relate to the Software Development viewpoint. In our dataset, each unique CVE is mapped to one or more CWE's and is given a vulnerability score that is assigned by the CVSS scoring system. 
#
#
#
# ### What should I do next? 
# Good question! Now that you have some background, you can work with the given CVE-based dataset as a starting point to explore a number of questions to help in your investigation.  You can draw on your python, data analysis and basic machine learning skills to work towards the goal that your team has been tasked with.
#
#
# *****
#
# References
#
# IBM. 2022. What is Cybersecurity? | IBM. [online] Available at: [https://www.ibm.com/au-en/topics/cybersecurity](https://www.ibm.com/au-en/topics/cybersecurity). (Accessed 3 March 2022).
#
# Camacho, R. 2021.  All about CWE: Common Weakness Enumeration. Parasoft. [https://www.parasoft.com/blog/what-is-cwe/#:~:text=In%20short%3A%20the%20difference%20between,regarding%20specific%20systems%20and%20products.](https://www.parasoft.com/blog/what-is-cwe/#:~:text=In%20short%3A%20the%20difference%20between,regarding%20specific%20systems%20and%20products.)

# %% [markdown]
# **********
# ## Data Description
# We have a sizable dataset to give you (in the form of 2 files), so it is wise to consider your code in terms of complexity to ensure it doesn't take 30 minutes to run a single line. 
#
# The below tables provide an outline of the data, broken down into the columns of the dataset features. 
#
# ###  The CVSS data table
# | Column Name    | Description    |
# | :------------- | :------------- |
# | cve_id         | The CVE identifier for the vulnerability |
# | assigner       | The entity who assigned the CVE |
# | description     | A description of the vulnerability |
# | cwe_ids         | The CWE identifiers of the vulnerability. Note that there can be multiple cwe_id's attached to one cve_id |
# | refs            | url links to the initial postings of the vulnerability |
# | ref_names       | other information which provide more reference about the CVE |
# | ref_sources     | other information which provide more reference about the CVE |
# | ref_tags        | other information which provide more reference about the CVE |
# | v3_attackVector | CVSSv3 field, identifier for how the vulnerability would be used in an attack |
# | v3_attackComplexity | CVSSv3 field, identifier for the difficulty of performing an attack using the vulnerability |
# | v3_privilegesRequired | CVSSv3 field, an identifier for the privileges required in the system to use the vulnerability successfully |
# | v3_userInteraction | CVSSv3 field, an identifier for whether a user needs to actively interact for the vulnerability to be exploited or not |
# | v3_scope | CVSSv3 field, an identifier for whether the scope of an item changes when using the vulnerability. e.g: whether a regular user becomes a superuser. |
# | v3_confidentialityImpact | CVSSv3 field, identifier for the impact upon the confidentiality of information in the product/service after using the vulnerability |
# | v3_integrityImpact | CVSSv3 field, identifier for the impact upon the integrity of information in the product/service after using the vulnerability |
# | v3_availabilityImpact | CVSSv3, field, identifier for the impact upon the availability of information in the product/service after using the vulnerability |
# | v3_exploitabilityScore | The Exploitability Score is a sub score of the CVSS Base Score |
# | v3_impactScore | The Impact Score is a sub score of the CVSS Base Score |
# | v3_baseScore | The CVSS score (out of 10) given to the vulnerability based on CVSS v3.1 |
# | v3_baseSeverity | A textual representation of the numeric Base Score|
#
# We only use the Base Metrics out of the [CVSS Metrics](https://www.first.org/cvss/v3-1/media/MetricGroups.svg). While there are additional metrics that can be applied, most are variants. Therefore, we will use the base metrics. The column names starting with 'v3_' are CVSS v3.1 metrics. Refer to the specification document  [CVSSv3.1 Guide](https://www.first.org/cvss/v3.1/specification-document) for more information on the metrics. 
#
# **Note:** While this dataset has 20 columns, the data in the last four columns have been purposely omitted (see Question 2 of the Assignment).

# %% [markdown]
# ###  The CVE to Configurations mapping table
# | Column Name    | Description    |
# | :------------- | :------------- |
# | cve_id         | The CVE identifier for the vulnerability |
# | vendor         | The name of the vendor who produces the product |
# | product_name   | The name of the affected product       |
# | version        | List of the affected product versions |
#
# Recall that a CVE can affect multiple products and multiple software versions of a product.

# %% [markdown]
# *******************
# ## Package Imports

# %%
# Common Imports
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
plt.style.use('seaborn')
# # %matplotlib inline

# %%
# Import additional modules here as required
# It is unlikely that you would need any additional modules, however we had added space here just in case you feel 
#     extras are required. Note that justification as to WHY you are using them MUST be provided.
#
# Note that only modules in the standard Anaconda distribution are allowed. If you need to install it manually, it is not an accepted package.
#
#
from sklearn.linear_model import LogisticRegression 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import timeit
import math
from math import sqrt
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import StandardScaler
from pylab import rcParams
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold # Scikit-learn K-Folds cross-validator
from sklearn.model_selection import cross_val_score # evaluating cross-validator performance
k_fold = KFold(n_splits=10, shuffle=True, random_state=0) # KFold configuration      
from sklearn.pipeline import Pipeline
# explicitly require this experimental feature
from sklearn.experimental import enable_halving_search_cv # noqa
# now you can import normally from model_selection
from sklearn.model_selection import HalvingGridSearchCV  # GridSearch

# %% [markdown]
# ****
# ## Q1: Loading and Processing the Data
# Your first step in any data analysis and visualisation task is to load the data and make it usable. Note that the data consists of various types (Categorical, Numerical, Text, etc.). Also the dataset may not be perfect; it may contain missing data or invalid values at some places. It would be wise to perform some pre-processing to make the data easier to work with. 
#
# #### (Q1.a) You need to load the following two files available in the './data' folder into a suitable data structure:
# - cvss_dataset.csv
# - cve_configurations_mapping.csv
#
# Please write out the code you would use to load those files and the code you would use to perform some pre-processing. (2 marks)
#
# #### (Q1.b)You also need to briefly outline your steps and justify your decisions. 
# This is an open-ended question, and marks will be awarded for logical processing of data. (3 marks)
#
# **HINTS** -
# * You might need to split some columns into two or combine two columns into one to make them more useful from an analysis point-of-view.
# * You might need to rename some columns.
# * It may be worth recoding the CVSS data to the numerical values required for Q2.
# * You are welcome to drop unwanted columns (but don't remove or impute values for the last four columns as you will be asked to recreate these columns in Q2)
# * If you wish, you may combine the data available in both files.
#
# <span style= 'float: right;'><b>[5 marks]</b></span>

# %%
# %%time
# YOUR CODE HERE (Q1.a)
# Loading the two files
fileName1 = "./data/cve_configurations_mapping.csv"
fileName2 = "./data/cvss_dataset.csv"

# Create dataframe of csv files
try:
    cve_df = pd.read_csv(fileName1)
except OSError:
    print("Could not read file:",fileName1)
except FileNotFoundError:
    print(f"file {fileName1} not found")

try:
    cvss_df = pd.read_csv(fileName2)
except OSError:
    print("Could not read file:",fileName2)
except FileNotFoundError:
    print(f"file {fileName2} not found")

# Joining the two dataframes into one
data_df = pd.merge(cve_df, cvss_df, on="cve_id")

# check for null
print("These columns have Nan: ", data_df.columns[data_df.isna().any()].tolist())

# Replacing categorical column's nan with mode 
# (https://www.geeksforgeeks.org/pandas-filling-nan-in-categorical-data/)
cols = ['version', 'ref_names', 'ref_sources']
data_df[cols] = data_df[cols].fillna(data_df.mode().iloc[0])

# Converting categorical data to numerical
# Create a dict of the categorical values to be replaced by the numeric values
# The values are taken from the CVSSv3.1 specification document
numeric_replace = {"v3_attackVector": {"NETWORK":0.85, "ADJACENT_NETWORK":0.62, "LOCAL":0.55, "PHYSICAL":0.2},
                   "v3_attackComplexity": {"LOW":0.77, "HIGH":0.44},
                   "v3_scope": {"UNCHANGED":0.0, "CHANGED":1.0},
                   "v3_userInteraction": {"NONE":0.85, "REQUIRED":0.62},
                   "v3_confidentialityImpact": {"HIGH":0.56, "LOW":0.22, "NONE":0},
                   "v3_integrityImpact": {"HIGH":0.56, "LOW":0.22, "NONE":0},
                   "v3_availabilityImpact": {"HIGH":0.56, "LOW":0.22, "NONE":0},
                   "v3_privilegesRequired": {"NONE":0.85, "LOW":0.0, "HIGH":1.0}}

# Replace the values
data_df = data_df.replace(numeric_replace)

# use apply and lambda for better efficiency
# Low = 0, High = 1
def encode_privileges(v3_scope, v3_privilegesRequired):
    '''
    This function encodes categories in privileges required
    input: float, object
    output: float
    '''
    if v3_scope == 0.0 and v3_privilegesRequired == 0.0:
        return float(0.62)
    elif v3_scope == 1.0 and v3_privilegesRequired == 0.0:
        return float(0.68)
    elif v3_scope == 0.0 and v3_privilegesRequired == 1.0:
        return float(0.27)
    elif v3_scope == 1.0 and v3_privilegesRequired == 1.0:
        return float(0.5)
    
data_df['v3_privilegesRequired'] = data_df.apply(lambda row: encode_privileges(row['v3_scope'], row['v3_privilegesRequired']), axis=1)
# The nan values would be the None label which is 0.85 numerically
data_df['v3_privilegesRequired'] = data_df['v3_privilegesRequired'].fillna(0.85)


# check whether the dtype have been converted to numeric
# print("the data types in the dataset are as follows:\n", data_df.dtypes, "\n")

# Check if there are any more null values except the last four.
print("After pre-processing, these columns have Nan: ", data_df.columns[data_df.isna().any()].tolist())

# Check for duplicate rows. Drop any duplicates
print("There are",data_df.duplicated().sum(),"duplicated rows")

# data_df.to_csv('joined.csv')

data_df.describe()


# %% [raw]
# # YOUR WRITTEN ANSWER HERE (Q1.b)
# Combined the two datasets into one to make it easier to work with
#
# Replaced Nan values in the categorical columns according to Frequent Categorical Imputation with the assumption that missing values are likely to be the majority of the values present.
# With this approach the benefit is that its a simple method to implement for categorical variables however it distorts the relation of the most frequent label. Another disadvantage to this method is that having a lot of null values may bias the prediction if replacing with mode, however using the isnull().sum() function, it was seen that compared to the total sample size, approx. 0.006% of the data were null.
# Reference: (https://medium.com/analytics-vidhya/ways-to-handle-categorical-column-missing-data-its-implementations-15dc4a56893)
#
# The v3 categorical values were replaced by their corresponding numerical value taken from the CVSSv3.1 documentation inorder to be able to calculate the base score for later.
#
# Check for any duplicates to reduce complexity. There were no duplicates in the data.

# %% [markdown]
# ******
# ## Q2: Recreating Missing Data
# While the dataset that has been provided is thorough, you may have already noticed that the last four columns (i.e. 'v3_exploitabilityScore', 'v3_impactScore', 'v3_baseScore', 'v3_baseSeverity) are empty. These are related to the CVSSv3.1 base score and are well documented in the specification documents  [CVSSv3.1 Guide](https://www.first.org/cvss/v3.1/specification-document) and [CVSS calculator](https://www.first.org/cvss/calculator/3.1).
#
# Your task is as follows:
#
# #### (Q2.a) Implement a **CVSSv3.1** Base Score calculator and recalculate values for the last four columns for each applicable entry in the dataset. (5 marks) 
#
# #### (Q2.b) Explain how you performed the calculations. Provide the [Equations](https://www.first.org/cvss/v3-1/media/EquationsDiagram.svg) that you used. (5 marks)
#
# <span style= 'float: right;'><b>[10 marks]</b></span>
#
# <br><br>
# **Additional Questions for COMP6420 students: [worth extra 5 marks]** 
#
# #### (Q2.c) Please explain how would you validate that your calculations are correct? (3 marks)
#
# #### (Q2.d) Provide some evidence that you have validated your calculations. (2 marks)

# %%
# Helper Functions
def Roundup (i):
    '''
    This function roundsup numbers. This implementation of the function
    was provided in the CVSSv3.1 documentation. The only adjustment made to
    the function was replacing round_to_nearest_integer with python's 
    in-built round().
    '''
    int_input = round(i * 100000)
    if (int_input % 10000) == 0:
        return int_input / 100000.0
    else:
        return (math.floor(int_input / 10000) + 1) / 10.0



# %%
# %%time
# YOUR CODE HERE
# Create a function and apply that function to the dataframe to calculate the missing values

# turn off SettingWithCopyWarning
pd.options.mode.chained_assignment = None # defualt='warn'

# approach: create a dataframe of only v3_confidentialityImpact, v3_integrityImpact
# and v3_availabilityImpact. perform calculation on the dataframe. create a new column
# called ISS and fill the column with the calculated values using numpy vectorization.
def ISS_score(v3_confidentialityImpact, v3_integrityImpact, v3_availabilityImpact):
    '''
    This function takes in confidentialty, integrity and availability impacts
    to calculate a ISS score.
    input: float, float, float
    output: float
    '''
    ISS = 1 - ((1 - v3_confidentialityImpact) * 
               (1 - v3_integrityImpact) * 
               (1 - v3_availabilityImpact))
    
    return ISS
# create ISS coulm and fill with ISS scores
data_df['ISS'] = np.vectorize(ISS_score)(data_df['v3_confidentialityImpact'], 
                                         data_df['v3_integrityImpact'], 
                                         data_df['v3_availabilityImpact'])

# Fill in the missing columns
# calculate Impact score
def impactScore(ISS, v3_scope):
    '''
    This function calculates the impact score using the ISS score and scope
    input: float, float
    output: float
    '''
    if v3_scope == 0:
        impact_score = 6.42 * ISS
    elif v3_scope == 1:
        impact_score = 7.52 * (ISS - 0.029) - 3.25 * (ISS - 0.02)**15
    return impact_score

# replace nan values in impact score column with calculated values
data_df['v3_impactScore'] = np.vectorize(impactScore)(data_df['ISS'],
                                                 data_df['v3_scope'])
# calculate exploitability score
def exploitScore(v3_attackVector, v3_attackComplexity, v3_privilegesRequired, v3_userInteraction):
    '''
    This function calculates the exploitability score using the 
    attackVector, attackComplexity, privilegesRequired, UserInteraction
    input: float, float, float, float
    output: float
    '''
    exp_score = 8.22 * v3_attackVector * v3_attackComplexity * v3_privilegesRequired * v3_userInteraction
    return exp_score

# replace nan values in exploitability score with calculated values
data_df['v3_exploitabilityScore'] = np.vectorize(exploitScore)(data_df['v3_attackVector'],
                                                           data_df['v3_attackComplexity'],
                                                           data_df['v3_privilegesRequired'],
                                                           data_df['v3_userInteraction'])
# calculate Base score
def baseScore(v3_impactScore, v3_exploitabilityScore, v3_scope):
    '''
    This function calculates the base score through the help of roundup function,
    The parameters are the impact, exploitability and scope.
    input: float, float, float
    output: float
    '''
    if v3_impactScore <= 0:
        return 0
    elif v3_scope == 0:
        return Roundup(min((v3_impactScore + v3_exploitabilityScore), 10))
    elif v3_scope == 1:
        return Roundup(min(1.08 * (v3_impactScore + v3_exploitabilityScore), 10))

# replace nan values in exploitability score with calculated values
data_df['v3_baseScore'] = np.vectorize(baseScore)(data_df['v3_impactScore'],
                                             data_df['v3_exploitabilityScore'],
                                             data_df['v3_scope'])

# calculate base severity
# 1 is lowest, 5 is highest
def base_severity_rating(v3_baseScore):
    '''
    This function assigns a severity rating depending on the base score
    input: float
    output: string
    '''
    pass
    if v3_baseScore == 0:
        return 1
    elif 0.1 <= v3_baseScore <= 3.9:
        return 2
    elif 4.0 <= v3_baseScore <= 6.9:
        return 3
    elif 7.0 <= v3_baseScore <= 8.9:
        return 4
    elif 9.0 <= v3_baseScore <= 10.0:
        return 5
      
# replace nan values in base severity
data_df['v3_baseSeverity'] = np.vectorize(base_severity_rating)(data_df['v3_baseScore'])

# create a csv
# data_df.to_csv('filled_df.csv')

# Check if there are any more null values.
print("After filling missing values, these columns have Nan: ", data_df.columns[data_df.isna().any()].tolist())


# %% [raw]
# # YOUR WRITTEN ANSWER HERE
# To perform the calculations, the equations that were needed were provided by the CVSS documentation.
# The equations were:

# %% [markdown]
# ![alt text](CVSS_equations.png "CVSS_equations")

# %% [raw]
# Too calculate each of the missing variables, functions were created according to the equations to fill in the values.
# Then using numpy vectorization, all the columns were filled with the calculated values, row by row. Numpy vectorisation was 
# used because it proved to be significantly faster than using apply with lambda.
#
# Resources:
# [1] https://stackoverflow.com/questions/52673285/performance-of-pandas-apply-vs-np-vectorize-to-create-new-column-from-existing-c

# %%
data_df.describe()

# %% [markdown]
# ******
# ## Q3: Data Exploration
# In this question you are asked to explore the given data and present information in a suitable manner. You are required to present the information both visually (using plots) and using descriptive statistics. 

# %%
# %%time
# Base score distribution.
sns.set(rc = {'figure.figsize':(20,8)})
sns.histplot(data_df['v3_baseScore'], bins=15, kde=True)
plt.show()

# Boxplot representation
sns.catplot(x='v3_baseScore', kind='box', data=data_df, height=3, aspect=3, orient="h")
plt.show()

print("The histogram and box plot shows that most base scores are between 7 to 8 and 9 to 10 which indicates in 2020 there were high severity cases")



# %%
# %%time
# # Boxplot categorical values (product_name) Most frequent products and their base scores

data_product = {'product_name': data_df['product_name'],
               'v3_baseScore': data_df['v3_baseScore']}
df_product = pd.DataFrame(data_product)

top_10_products = df_product['product_name'].value_counts()[:10].index.tolist()
# ['debian_linux', 'android', 'fedora', 'leap', 'chrome', 'mac_os_x', 'iphone_os', 'tvos', 'watchos', 'sdx55_firmware']

product_dict = {'debian_linux': df_product.loc[df_product['product_name']=='debian_linux', 'v3_baseScore'],
                'android': df_product.loc[df_product['product_name']=='android', 'v3_baseScore'],
                'fedora': df_product.loc[df_product['product_name']=='fedora', 'v3_baseScore'],
                'leap': df_product.loc[df_product['product_name']=='leap', 'v3_baseScore'],
                'chrome': df_product.loc[df_product['product_name']=='chrome', 'v3_baseScore'],
                'mac_os_x': df_product.loc[df_product['product_name']=='mac_os_x', 'v3_baseScore'],
                'iphone_os': df_product.loc[df_product['product_name']=='iphone_os', 'v3_baseScore'],
                'tvos': df_product.loc[df_product['product_name']=='tvos', 'v3_baseScore'],
                'watchos': df_product.loc[df_product['product_name']=='watchos', 'v3_baseScore'],
                'sdx55_firmware': df_product.loc[df_product['product_name']=='sdx55_firmware', 'v3_baseScore']}

df_product = pd.DataFrame(data = product_dict)
# fill missing values
df_product.fillna(df_product.mean())

# Plotting
sns.boxplot(x='variable', y='value', data=pd.melt(df_product), palette="Set3")
plt.title("Most occuring products and their base score")
plt.show()
print("Most products had a high mean base score")


# %% [markdown]
# #### (Q3.a)
# There is an unverified claim made that most of the CVEs reported in 2020 were of MEDIUM Severity.  How would you check that claim and present the conclusion? Please explain your approach and implement it in code.
# <span style= 'float: right;'><b>[5 marks]</b></span>

# %%
# %%time
# YOUR CODE HERE
# 3 is medium
rating_dict = {'CRITICAL': 5, 'HIGH': 4, 'MEDIUM': 3, 'LOW': 2, 'NONE': 1}
mode_severity = data_df['v3_baseSeverity'].mode().tolist()[0]
rating = [k for k, v in rating_dict.items() if v==mode_severity]
print(f"Most of the CVE's reported in 2020 had a severity of {mode_severity} which is {rating}")

# Plot a histogram to show the mode which would be the middle bar
rcParams['figure.figsize'] = 22, 8
sns.histplot(data=data_df, x='v3_baseSeverity', kde=True, bins=10)
plt.show()
print("As shown is the graph, 4 (HIGH) has the highest count")



# %% [raw]
# # YOUR WRITTEN ANSWER HERE
# As the whole dataset is of 2020's, this claim can be easily checked by returning the mode of the base severity column. If the mode happens to be 3 then most of the reported CVE's would be of MEDIUM severity.
# In this case the mode is 4 which is HIGH. Therefore the claim is not true.

# %% [markdown]
# #### (Q3.b)
# What are the top 5 CWEs that are mentioned in the data? Why did you present this information in the way you chose?
# <span style= 'float: right;'><b>[5 marks]</b></span>

# %%
# %%time
# YOUR CODE HERE
# top 5 occuring CWES
top_5_cwe = data_df['cwe_ids'].value_counts()[:5].index.tolist()
print(f'The top 5 most occurring cwe ids are: \033[4m \033[1m{top_5_cwe}\033[0m \033[0m')

# %%
# %%time
# top 5 CWES by base score
data_df_copy = data_df.copy()
data_df_copy = data_df_copy.sort_values(by='v3_baseScore', ascending=False)
data_df_copy = data_df_copy['cwe_ids']
top_5_cwe_basescore = data_df_copy.unique()[:5]
print(F"The top 5 cwes by base score in-order is:\033[4m \033[1m{top_5_cwe_basescore}\033[0m \033[0m")

# %% [raw]
# # YOUR WRITTEN ANSWER HERE
# Assuming top 5 CWEs means the CWEs that occur the most, this can be found using value_counts()
# If top 5 CWEs means by base score then that can be found by grouping by CWE_id and sorting by base score.
# I have provided answers to both cases just in case.
#

# %% [markdown]
# #### (Q3.c)
# Google products are commonly used.  Your team wants to know how cyber-threats are affecting google users.  Find all the CVEs associated with the Vendor google and present the distribution of CVSS Base Scores for google in a suitable manner.  Please also explain your steps.
# <span style= 'float: right;'><b>[5 marks]</b></span>

# %%
# YOUR CODE HERE
# find all cves associated with google
google_cves = data_df[data_df['vendor']=='google']
google_cves = google_cves['cve_id']
pd.set_option('display.max_rows', None)
google_cves.head()

# %%
# %%time
# show distribution of base score for google
google_baseScore = data_df.loc[data_df['vendor']=='google', 'v3_baseScore']
pd.reset_option('display.max_rows', None)
print(f"The mean base score for google is: \033[4m \033[1m{google_baseScore.mean()}\033[0m \033[0m, indicating high cyber threats")
print("Most to least occuring basescore for google: ",google_baseScore.value_counts().index.tolist())

# Plot
sns.histplot(data=google_baseScore, bins=5, kde=True)
plt.title("distribution of base score for google")
print("From the most to least occuring list, it's seen that 8.8 and 9.8 occurs a lot which is represented in the histogram")

# %% [raw]
# # YOUR WRITTEN ANSWER HERE
# To find all CVEs associated with google, I filtered the vendor column where google was located and stored the resulting series into a variable.
# Then I only selected the cve_id column and presented that.
#
# To find the distribution of google's base scores I chose an histogram to display the result using seaborn's histplot because histogram's are typically best for showing distribution plots.
# From the plot it can be seen that a lot of google's base scores are approximately in the 8 - 9 range which shows google had been affected quite alot in 2020.

# %% [markdown]
# #### (Q3.d)
# Find the top 5 vendors that are most affected (i.e. that has most number of rows in the configurations table) and present the distribution of CVSS Base scores for these top 5 vendors using a suitable visualization.  Please also explain your steps.
# <span style= 'float: right;'><b>[10 marks]</b></span>

# %%
# %%time
# YOUR CODE HERE
# # Boxplot Most frequent vendors and their base scores
data_vendor = {'vendor': data_df['vendor'],
               'v3_baseScore': data_df['v3_baseScore']}
df_vendor = pd.DataFrame(data_vendor)

# get top 5 most frequent values
top_5_vendors = df_vendor['vendor'].value_counts()[:5].index.tolist()
# ['qualcomm', 'intel', 'netgear', 'apple', 'oracle']

vendors = ['qualcomm', 'intel', 'netgear', 'apple', 'oracle']
# filtering dataframe so only the top 5 are present
res_df_vendor = df_vendor[df_vendor['vendor'].isin(vendors)]

# check for missing values
res_df_vendor.isnull().any()

# Plotting
sns.catplot(x='vendor', y='v3_baseScore', data=res_df_vendor, kind='box', palette="Set3", height=6, aspect=1.5)
plt.title("Most occuring vendors and their base score")
plt.show()
print("From the graph it can be seen that the vendors that have the most frequent vulnerabilites in their systems, most of them were of medium to high severity")

# %% [raw]
# # YOUR WRITTEN ANSWER HERE
# First I created new dataframe with only the vendor and baseScore column to make operations easier. 
# To do this, I created a dict with the column names as keys and values of that column from the original dataframe. Then I turned the dict into a dataframe.
# From there, I used value_counts() to get the top 5 vendor. Then I created a list of the top 5 vendor and using the isin() function, filtered the dataframe and stored the result into 
# a new dataframe such that the new one only has rows including the top 5 vendors.
# To visllaise the distribution, I used box catplot from seaborn as it allows categorical values on the x axis. Boxplot makes it easier to see the distribution of base score for each vendor.

# %% [markdown]
# ******
# ## Q4: Identifying Data Analysis Problems
# ### CVEs and real world issues
#
# We mentioned that dataset is from 2020 and we have only given you the records that relate to the Software Development viewpoint. Do you remember any major software vulnerabilities that came to light in 2020? [This article](https://securityintelligence.com/posts/top-10-cybersecurity-vulnerabilities-2020/) claims that the top 2 vulnerabilities that were found in 2020 are;
# - CVE-2020-8515: Draytek Vigor Command Injection
# - CVE-2020-5722: HTTP: Grandstream UCM6200 SQL Injection
#
# However, there may be various viewpoints. For e.g.: [this article](https://blog.detectify.com/2020/12/30/top-10-critical-cves-added-in-2020/) mentions another 10 CVE's. 
#
# Your task is as follows:
# #### (Q4.a)
# - Find and present the vulnerabilities that are mentioned in the above two articles in the given dataset in a tabular format. You may not find all the 12 CVE's. What are possible reasons for this? (5 marks)
# - Examine the properties of the CVEs that you found above. (At a minimum you should consider the data available in the './data/cvss_dataset.csv' file). Present a justification as to why some of the given CVEs may have been considered a _"large"_ bug? This should include references to the amount of damage a vulnerability caused, or could have potentially caused. (5 marks)
#
# <span style= 'float: right;'><b>[10 marks]</b></span>
#
# <br><br>
# **Additional question for COMP6420 students: [worth extra 10 marks]**
# #### (Q4.b)
# - If you were given the task of identifying the top-10 most critical CVEs in the given data, how would you tackle the problem? Give a brief list of initial analysis you would perform. (7 marks)
#
# - How would you go about implemention your proposed approach? (3 marks)
#
# References are highly recommended for this question (both parts a and b) so that you can evidence your argument. **DO NOT** forget to list your references, including in your statement of originality document.  **Please note that failure to reference or improper referencing constitute a case for plagiarism which can have serious consequences for you.  So make sure you use references appropriately.  Please familiarise yourself with the university's [academic integrity rules here](https://www.anu.edu.au/students/academic-skills/academic-integrity) if you have not done so already**.

# %% [raw]
# CVE-2020-12720, CVE-2020-5902, CVE-2020-15506, CVE-2020-14882, CVE-2020-14750, CVE-2020-17530, CVE-2020-2551, CVE-2020-13379, CVE-2020-1147, CVE-2020-8209, 

# %% [raw]
# CVE-2019-19871, CVE-2018-20062, CVE-2006-1547, CVE-2012-0391, CVE-2014-6271, CVE-2019-0708, CVE-2020-8515, CVE-2018-13382, CVE-2018-13379, CVE-2018-11776, CVE-2020-5722

# %%
# YOUR CODE HERE
pd.set_option('display.max_columns', None)
# Check if the CVE mentioned in the articles are in the dataset
# leave out duplicates using set
cve_set = {'CVE-2020-12720',' CVE-2020-5902', 'CVE-2020-15506', 'CVE-2020-14882', 'CVE-2020-14750', 'CVE-2020-17530', 'CVE-2020-2551', 'CVE-2020-13379', 'CVE-2020-1147', 'CVE-2020-8209', 
            'CVE-2019-19871', 'CVE-2018-20062', 'CVE-2006-1547', 'CVE-2012-0391', 'CVE-2014-6271', 'CVE-2019-0708', 'CVE-2020-8515', 'CVE-2018-13382', 'CVE-2018-13379', 'CVE-2018-11776', 'CVE-2020-5722'}

# filtering the dataframe
res_df = data_df[data_df['cve_id'].isin(cve_set)]

print(f"Of the CVEs from the articles, only these were present in the dataset: \033[4m \033[1m{res_df['cve_id'].unique()}\033[0m \033[0m")
res_df


# %% [raw]
# # YOUR WRITTEN ANSWER HERE
# Some possibilites for why not all the CVE from the article are present in the data set might be because no information were provided, were failed to provide, or were chosen not to provide for these cves.
# Due to all/most of these CVEs affecting large organisations such as apache and oracle, and all these CVEs have a critical base severity rating with a score of 9.8 which shows they caused a lot of damage, is likely why they were considered to be a "large" bug/problem.
# From the dataset it can be seen that these CVE's required no user interaction, no privileges, low attack complexity and high confidentiality, inetgrity and availability impacts therefore these CVEs were very exploitable and the nature of their severity earned them critical base scores. 
# A large factor as to why these CVEs were so severe was because all of them are SQL injection and incorrect access control vulnerabilities.
# CVE-2020-17530 which affected both oracle (multiple times) and apache for example was exploited by attackers to perform remote code execution by forcing the Apache Struts framework to perform double evaluation. Attackers were able to execute system commands by sending specially crafted HTTP requests [Ref 6].
# SQL injection attacks are one of the most prevalent and dangerous web application vulnerabilities [Ref 7]. The impact SQL injection can have on a business is extensive. A successful attack may result in unauthorized viewing of user lists, deletion of entire tables and in certain cases the attacker gaining administrative rights to a database, all of which are highly detrimental to a business [Ref 8].
# That's why these four CVEs from this dataset were a significant problem when they emerged.
#

# %% [markdown]
# ******
# ## Q5: Data Analysis
# In this section, you will be provided a question or statement that you are required to prove/disprove. For each question, you are to provide a statement outlining your answer, using evidence from the dataset as your justification. You are expected to draw upon not only your visualisation skills, but also your hypothesis testing skills where required. That means you expected to justify your answer based on both statistical and visual evidence.
#
# Don't forget to state any assumptions you make in the questions in order to clarify your argument.
#
# Use the following as a guide to assess the statements given below:
# - How would you assess the given statement? 
# - What kinds of statistical tests are appropriate to validate the statement? Justify your selection.
# - How would you present the information related to the statement in a graphical manner?
# - What is your answer to the statement? Why do you say so?
#
# **Hint:** You are not expected to build Machine Learning models to answer this question. 

# %% [markdown]
# #### (Q5.a)
# #### Statement: "The sum of the two sub scores (i.e. the Exploitability sub-score and the Impact sub-score) is a 'good' predictor for the Base Score."
#
# After implementing the **CVSSv3.1** Base Score calculator in Question 2, you may recall that the Base Score is derived from two sub scores (i.e. the Exploitability sub-score and the Impact sub-score). For simplicity, let us explore whether we can get a 'good' estimate for the Base Score just by simply adding up the Exploitability sub-score and the Impact sub-score. 
#
# [5 marks for code implementation, 5 marks for written response]
# <span style= 'float: right;'><b>[10 marks]</b></span>

# %% [raw]
# Hypothesis test
# Null hypothesis: The sum of Exploitability-score and Impact-score is not a good predictor for the Base Score.
# Alternate hypothesis: The sum of Exploitability-score and Impact-score a good predictor for the Base Score.

# %%
# %%time
pd.reset_option('display.max_columns', None)
def plot_correlation_heatmap(data):
    '''
    plot correlation's matrix to explore dependency between features 
    '''
    # Looking for correlations in the data set
    corr_matrix = data_df.corr()
    # Generating a heatmap of the correlation matrix
    plt.figure(figsize=(16, 8))
    heatmap = sns.heatmap(data_df.corr()[['v3_baseScore']].sort_values(by='v3_baseScore', ascending=False), vmin=-1, vmax=1, annot=True);
    heatmap.set_title('Features Correlating with base score')
    plt.show()  
plot_correlation_heatmap(data_df)
print("From the heatmap , it can be seen that base score has strong correlations with base severity(which is a given), ISS, impact score, explotability score and availability impact")



# %%
# %%time
# To reduce wall time, I only took a sample of the dataframe (20000 rows out of ~50000) which still returned a similar graph
def plot_scatter_matrix(data):
    # plotting a scatter matrix of a few promising attributes
    attributes = ["v3_baseScore", "v3_impactScore", "v3_exploitabilityScore", "v3_baseSeverity"]
    rcParams['figure.figsize'] = 28, 6
    sns.pairplot(data_df[attributes].sample(20000), diag_kind='kde', hue='v3_baseSeverity')
plot_scatter_matrix(data_df)
print("Higher base severity number indicates higher severity rating")

# %%
# %%time
y = data_df['v3_baseScore']
x = data_df['v3_impactScore']

fig = plt.figure(figsize=(30,6))
ax2 = fig.add_subplot(122)
plt.scatter(x, y, alpha=0.2, edgecolors='black', c='purple')
sns.regplot(x=x, y=y)
plt.xlabel("v3_impactScore")
plt.ylabel('v3_baseScore')
plt.title("Relationship between impact score and base score")

print("It can be clearly seen that there is a sort of a upward trend and the points are not too dispersed.")
plt.show()

# %% [raw]
# Multiple Linear Regression model:

# %%
# %%time
# Copy of original data
data_df_copy = data_df.copy()

# Select features
X1 = np.array(data_df_copy[['v3_exploitabilityScore', 'v3_impactScore']]) # Feature variables
y1 = np.array(data_df_copy['v3_baseScore'])                               # Target variables

# Instantiate Standard scaler
scaler = StandardScaler()
X1 = scaler.fit_transform(X1)

# Split the dataset
X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, train_size=0.8, random_state=42)

# Instantiate Linear Regression
mlr = LinearRegression()

# Create a pipeline for multiple linear regression
pipe_mlr = Pipeline(steps=[('scaler',StandardScaler()),
                           ('mlr',LinearRegression())])

MLR_model = pipe_mlr.fit(X1_train, y1_train)

# Predict
y1_pred = np.around(MLR_model.predict(X1_test), 1)
print("Actual values:", y1_test[0:5])
print(f'MLR model predictions {y1_pred[0:5]}')
print("The predicted values using exploitability score and impact score are very similar to the actual values")
print(" ")

# check the test score and training score of your model
MLR_score = MLR_model.score(X1_test, y1_test)
print(f'R-squared (score) of multiple linear regression model is \033[4m \033[1m{MLR_score}\033[0m \033[0m, indicating very high correlation')

# %%
# %%time
fig = plt.figure(figsize=(16,6))
plt.scatter(y1_test, y1_pred, alpha=0.5, color = 'black')
plt.vlines(y1_test, y1_pred, color='r', ymax=y1_test)
plt.title("Multiple linear regression test model")
plt.xlabel("True Values")
plt.ylabel("Predictions")

# add the regression line 
# code from Lab04
sns.regplot(x=y1_test, y=y1_pred, line_kws={"color": "red"})

plt.show()

# %%
# %%time
# Add up both exploitability and impact score columns and store in a new colume
# compare with base score column
data_df_copy = data_df.copy()
data_df_copy['exp+impact'] = data_df_copy.apply(lambda x: x['v3_impactScore'] + x['v3_exploitabilityScore'], axis=1).round(1)

# find the difference between exp+impact and base score columns to see how much the values differ by
data_df_copy['diff'] = data_df_copy.apply(lambda x: x['v3_baseScore'] - x['exp+impact'], axis=1)
# find the mean of diff
print(f"The mean of the differences between baseScore and exp+impact is: \033[4m \033[1m{data_df_copy['diff'].mean()}\033[0m \033[0m ")
data_df_copy

# %%
hypothesis = np.array(data_df_copy['exp+impact'])
actual = np.array(data_df_copy['v3_baseScore'])

hypothesis_mean = np.mean(data_df_copy['exp+impact'])
actual_mean = np.mean(data_df_copy['v3_baseScore'])
print(f'hypothesis mean: {hypothesis_mean}')
print(f'actual mean: {actual_mean}')

hypothesis_std = np.std(data_df_copy['exp+impact'])
actual_std = np.std(data_df_copy['v3_baseScore'])
print(f'hypothesis standard deviation: {hypothesis_std}')
print(f'actual standard deviation: {actual_std}')

# Call hypothesis function
t, p = stats.ttest_ind(hypothesis, actual)
print("p-value:", p)

if p < 0.05:
    print("we reject null hypothesis")
else:
    print("we fail to reject null hypothesis")

# %% [raw]
# # YOUR WRITTEN ANSWER HERE
# From the correlation heatmap and scatter matrices plotted implemented in above, it can be seen the exploitability and impact scores have quite a high correlation with base score. Exploitability score having a correlation of 0.67 and impact score having a correlation of 0.74 which signifies them being a pretty good predictor for the base score.
# From adding up the exploitability and impact score columns we can see that the resulting scores are very similar to the actual base scores. They only differ by about 0.1.
# Also the Machine learning models showed that exploitability and impact scores were able to predict the base scores to very close extent.
#
# From these results, we can conclude that exploitability and impact scores are good predictors for base scores.

# %% [markdown]
# #### (Q5.b):
#
# #### Statement: "The entries which require both LOW/None privileges AND LOW attack complexity have a higer CVSS Base Score."
#
# In this question we are looking at the relationship beetween some of the categorial data that is present in our dataset and our response variable. 
#
# [5 marks for code implementation, 5 marks for written response]        
# <span style= 'float: right;'><b>[10 marks]</b></span>

# %% [raw]
# Hypothesis Test
# null hypothesis: The entries which require both LOW/None privileges AND LOW attack complexity have a higer CVSS Base Score.
# alternate hypothesis: The entries which require both LOW/None privileges AND LOW attack complexity doesn't have a higer CVSS Base Score.

# %%
# %%time
# filtering the dataframe
privs = [0.85, 0.62, 0.68]
attackComp = [0.77]
result_df = data_df[data_df['v3_privilegesRequired'].isin(privs)]
result_df2 = result_df[result_df['v3_attackComplexity'].isin(attackComp)]
pd.set_option('display.max_columns', None)
# Find the mean base score on these conditions
mean_baseScore = result_df2['v3_baseScore'].mean()

# Compare with the mean base score of original data
original_mean_baseScore = data_df['v3_baseScore'].mean()

print(f'The original mean base score is {original_mean_baseScore}, compared to the low/none privileges and low attack complexity mean base score {mean_baseScore},')
print("which shows that there isn't a significant difference.")

# Plot some distribution graphs
rcParams['figure.figsize'] = 28, 6
sns.histplot(data=result_df2, x='v3_baseScore', bins=10, kde=True, color='orange', label='low attack and low/none privileges')

# Original
sns.histplot(data=data_df, x='v3_baseScore', bins=10, kde=True, label='original')
plt.legend()

print("As seen in the histogram, both datasets have equal number of high base scores")

# %%
hypothesis = np.array(result_df2['v3_baseScore'])
actual = np.array(data_df['v3_baseScore'])

hypothesis_mean = np.mean(result_df2['v3_baseScore'])
actual_mean = np.mean(data_df['v3_baseScore'])
print(f'hypothesis mean: {hypothesis_mean}')
print(f'actual mean: {actual_mean}')

hypothesis_std = np.std(result_df2['v3_baseScore'])
actual_std = np.std(data_df['v3_baseScore'])
print(f'hypothesis standard deviation: {hypothesis_std}')
print(f'actual standard deviation: {actual_std}')

# Call hypothesis function
t, p = stats.ttest_ind(hypothesis, actual)
print("p-value:", p)

if p < 0.05:
    print("we reject null hypothesis")
else:
    print("we fail to reject null hypothesis")

# %% [raw]
# # YOUR WRITTEN ANSWER HERE
# After performing a hypothesis test, looking at the means and doing some visualisation, it can be concluded that the null hypothesis is not true.
# The difference in mean base score between the two is only about ~0.2, which is quite insignificant. Using the histogram plot, it can be seen that
# both cases have same number of high base scores which shows low privileges and attack complexity don't have a significant effect on base scores.
# Therefore the entries which require both LOW/None privileges AND LOW attack complexity doesn't have a higer CVSS Base Score.

# %% [markdown]
# ******
# ## Q6: Classification

# %% [markdown]
# Now you are asked to build a classification model to predict the Threat level (Base Severity) of a vulnerability. 
#
# Your task is as follows:
# #### (Q6.a): Train a classification model to predict Threat level (Base Severity). You are able to choose any variables in the dataset, except of course the Base Scores, Sub Scores and Base Severity. (10 marks)
# #### (Q6.b): Why did you implement this particular model? What are the advantages and limitations of this type of model? (2 marks)
# #### (Q6.c): What are your considerations in implementing the training/testing split? Why did you make this choice? (2 marks)
# #### (Q6.d): Briefly explain your training considerations (including iterations, hyper-parameters and variable selection). (2 marks)
# #### (Q6.e):  How did you perform testing and validation? Which metrics were used in the validation? (2 marks)
# #### (Q6.f): After running your experiment, provide a written answer highlighting your results and the outcome of your work. (2 marks)
#
# <span style= 'float: right;'><b>[20 marks]</b></span>

# %% [raw]
# Since Base Severity is of multiclass, KNN should be the correct choice to implement. I'll compare it to Logistic Regression to see which one performs better.

# %% [markdown]
# ### Logistic Regression: ###

# %%
# %%time
# YOUR CODE HERE
# Creating a copy of the original to preserve the original data
data_df_copy = data_df.copy()

# Scaling the data
scaler = StandardScaler()

# Features to use:
# ['v3_attackVector', 'v3_attackComplexity', 'v3_privilegesRequired', 
#  'v3_userInteraction', 'v3_scope', 'v3_confidentialityImpact', 'v3_integrityImpact','v3_availabilityImpact']

# columns to scale
cols = ['v3_attackVector', 'v3_attackComplexity',
        'v3_privilegesRequired', 'v3_userInteraction', 'v3_scope',
        'v3_confidentialityImpact', 'v3_integrityImpact','v3_availabilityImpact']
data_df_copy[cols] = scaler.fit_transform(data_df_copy[cols])

data_df_copy = data_df_copy.drop(['cve_id', 'version', 'assigner',
       'description', 'cwe_ids', 'refs', 'ref_names', 'ref_sources',
       'ref_tags', 'v3_exploitabilityScore', 'v3_impactScore',
       'v3_baseScore', 'ISS', 'vendor', 'product_name'], axis=1)

# Selecting the features
# X will be every column except last (severity)
X = data_df_copy.iloc[:, :-1].values  # feature variables
y = data_df_copy.iloc[:, -1].values   # target variables

# Check if properly scaled
print("The mean of X is:", X.mean())
print("The standard deviation of X is:", X.std())

# %%
# %%time
# Splitting the data
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

#(Balancing) check whether the data set is balanced or not
# i.e the output classes in the training set are equally represented. 
# value_counts() func can be used to calc the number of records
# in each output class
print (X_train.shape,",", y_train.shape)
print (X_test.shape,",", y_test.shape)

def check_set_balance():
    if X_train.shape[0] == y_train.shape[0] and X_test.shape[0] == y_test.shape[0]:
        print("the training sets and testing sets are balanced")
    else :
        print("the sets are not balanced")
check_set_balance()

# %%
# %%time
import warnings
warnings.filterwarnings("ignore") 
# Using SKlearn's GridSearchCV for hyperparameter tuning

# First I will try Logistic Regression and see it's performance
# Instantiate the model
logreg = LogisticRegression()

# Logistic Regression requires two parameters 'C' and 'penalty' to be optimised by GridSearchCV [Ref: 1]
C = np.logspace(-4, 4, 50)
# all solvers use either none or l2. some don't use l1.
penalty = ['none', 'l2']
# sag and saga are better for larger datasets and handles multiclass problems
solver = ['sag', 'saga']

# Create a dict of hyperparameters
hyperparameters = dict(logreg__C=C,
                       logreg__penalty=penalty,
                       logreg__solver=solver)

# Creating a pipeline for better work flow
pipe = Pipeline(steps=[('scaler',StandardScaler()),
                       ('logreg',logreg)]) 

# Instantiate GridSearchCV and pass in the parameters and cross_validation of 5 folds
# halvingGridSearch = HalvingGridSearchCV(pipe, hyperparameters, n_jobs=-1, min_resources="exhaust", factor=3, random_state=42, cv=5)

# Fitting the data
# logreg_model = halvingGridSearch.fit(X_train, y_train)
# print("The best parameters are:", logreg_model.best_params_)

# %% [raw]
# Due to the Halving grid search taking quite a bit of time (around 12-15 seconds) I've commented the code out but left it in the cells
# to show my working essentially. 

# %%
# %%time
warnings.filterwarnings("default") 
# Fit best model from grid search
# Make an instance of Logistic Regression using the best parameters
# setting penalty to none gave warnings and ignored C so ls was chosen (the default)
logreg = LogisticRegression(C=1.7575106248547894, penalty='l2', max_iter=1000, solver='sag')

# Fit logistic regression
logreg_model = logreg.fit(X_train, y_train)

# Model evaluations
train_score = logreg_model.score(X_train,y_train)
test_score = logreg_model.score(X_test,y_test)

print(f"Training set score:\033[4m \033[1m{train_score}\033[0m \033[0m")
print(f"Test set score:\033[4m \033[1m{test_score}\033[0m \033[0m")
print("----------------------------------------------------------------")

coeff = logreg_model.coef_[0]
columns = np.array(['v3_attackVector', 'v3_attackComplexity', 'v3_privilegesRequired', 
                    'v3_userInteraction', 'v3_scope', 'v3_confidentialityImpact', 
                    'v3_integrityImpact','v3_availabilityImpact'])
coefficent = {x:coef for x, coef in zip(columns, coeff)}

print("Intercept :", logreg_model.intercept_)
print("Attributes' Coefficients: ", coefficent)

# %%
# %%time
y_pred = logreg_model.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Precision:",metrics.precision_score(y_test, y_pred, average='micro'))
print("Recall:",metrics.recall_score(y_test, y_pred, average='micro'))
print('----------------------------------------------------------------------')
print('Classification report')
print('----------------------------------------------------------------------')
print(classification_report(y_test, y_pred))
print('----------------------------------------------------------------------')
print("The RMSE of the model is:", sqrt(mean_squared_error(y_test, y_pred)), "indicating the logistic regression model fit the data pretty well")

# %%
# Confusion matrix
cm = metrics.confusion_matrix(y_test, y_pred)
print("CONFUSION MATRIX:")
print(cm)
print("From the number of true positives in the confusion matrix it can seen that the Logistic regression model was correctly able to classify majority of the classes.")

# %%
# %%time
## Get Labels
class_names = ['low','medium','high','critical']
# Plot confusion matrix in a beautiful manner
plt.rcParams['axes.grid'] = False 
fig = plt.figure(figsize=(16, 8))
ax= plt.subplot()
sns.heatmap(cm, annot=True, ax = ax, fmt = 'g'); 
# labels, title and ticks
ax.set_xlabel('Predicted', fontsize=20)
ax.xaxis.set_label_position('bottom')
plt.xticks(rotation=90)
ax.xaxis.set_ticklabels(class_names, fontsize = 10)
ax.xaxis.tick_bottom()

ax.set_ylabel('True', fontsize=20)
ax.yaxis.set_ticklabels(class_names, fontsize = 10)
plt.yticks(rotation=0)

plt.title('Confusion Matrix', fontsize=20)

plt.show()

# %%
# %%time
# Residual Analysis
# Error = Actualy y values - predicted y values
fig = plt.figure(figsize=(25, 8))
ax1 = fig.add_subplot(121)
plt.scatter(y_pred, y_test, alpha=0.3)
sns.regplot(x=y_pred, y=y_test, line_kws={"color": "red"})
plt.vlines(y_test, y_pred, color='r', ymax=y_test)
plt.ylabel("Actual Values")
plt.xlabel("Predicted values")
plt.title("Logistic Regression model predicted vs actual")

ax2 = fig.add_subplot(122)
residuals = y_test - y_pred
plt.scatter(y_pred, residuals, alpha=0.3)
plt.hlines(y=0, xmin=0, xmax=max(y_pred), color='red')
plt.ylabel("Residuals")
plt.xlabel("Predicted values")
plt.title("Logistic Regression Residual Plot")

plt.show()
print("From the residual plot, it can be seen that for most high base scores some dots in the positive region are far from the line indicating the model's predictions were too low.")
print("Most dots (primarily in the negative region) are close to the lines.")


# %%
print(np.isnan(y_test).any())
print(np.isnan(y_pred).any())

# %% [raw]
# Side-note: After working on later questions, for some reason the above graph got altered and a lot of dots went missing leaving only 10. Not sure of the reason behind this because there are no nan values present either.

# %% [markdown]
# ### K-Neighbors Classifier: ###

# %%
# %%time
# Creating new copy and starting fresh
data_df_copy = data_df.copy()
data_df_copy2 = data_df.copy()

# Scaling the data
scaler = StandardScaler()

# Features to use:
# ['v3_attackVector', 'v3_attackComplexity', 'v3_privilegesRequired', 
#  'v3_userInteraction', 'v3_scope', 'v3_confidentialityImpact', 'v3_integrityImpact','v3_availabilityImpact']

# columns to scale
cols = ['v3_attackVector', 'v3_attackComplexity',
        'v3_privilegesRequired', 'v3_userInteraction', 'v3_scope',
        'v3_confidentialityImpact', 'v3_integrityImpact','v3_availabilityImpact']
data_df_copy[cols] = scaler.fit_transform(data_df_copy[cols])

data_df_copy = data_df_copy.drop(['cve_id', 'version', 'assigner',
       'description', 'cwe_ids', 'refs', 'ref_names', 'ref_sources',
       'ref_tags', 'v3_exploitabilityScore', 'v3_impactScore',
       'v3_baseScore', 'ISS', 'vendor', 'product_name'], axis=1)

# Selecting the features
# X will be every column except last (severity)
X = data_df_copy.iloc[:, :-1].values  # feature variables
y = data_df_copy.iloc[:, -1].values   # target variables

# %%
# %%time
# Using SKlearn's GridSearchCV for hyperparameter tuning
# Instantiate the model
knn = KNeighborsClassifier()

# Hyperparameters to tune
hyperparameters = {'n_neighbors': np.arange(1,10),
                  'weights': ['uniform', 'distance'],
                  'metric': ['euclidean', 'manhattan']}

# Instantiate GridSearchCV and pass in the parameters and cross_validation of 5 folds
# halvingGridSearch = HalvingGridSearchCV(knn, hyperparameters, n_jobs=-1, min_resources="exhaust", factor=3, random_state=42, cv=5)

# Fitting the data
# knn_model = halvingGridSearch.fit(X_train, y_train)
# print("The best parameters are:", knn_model.best_params_)

# %% [raw]
# Due to the Halving grid search taking quite a bit of time (around 20 seconds) I've commented the code out but left it in the cells
# to show my working essentially. 

# %%
# %%time
# Splitting the data
X2_train, X2_test, y2_train, y2_test = train_test_split(X, y, train_size=0.8, random_state=42)

# fit and score the model 
knn = KNeighborsClassifier(n_neighbors=5, metric='manhattan', weights='distance')
knn_model = knn.fit(X2_train, y2_train)
# Predict
y2_pred = knn_model.predict(X2_test)

print("Training Score:", knn_model.score(X2_train, y2_train))
print("Test score: ", knn_model.score(X2_test, y2_test))
# print results
print('----------------------------------------------------------------------')
print('Classification report')
print('----------------------------------------------------------------------')
print(classification_report(y2_test, y2_pred))
print('----------------------------------------------------------------------')
print('The KNN model was able to precisely classify 3 (Medium), 4 (High) and 5 (Critical)')
print('----------------------------------------------------------------------')
print("The RMSE of the model is:", sqrt(mean_squared_error(y2_test, y2_pred)), "indicating the KNN model fit the data very well, better than Logistic Regression")

# %%
# %%time
# Confusion matrix
cm = metrics.confusion_matrix(y2_test, y2_pred)
print("CONFUSION MATRIX:")
print(cm)
print("From the number of true positives in the confusion matrix it can seen that the KNN model was correctly able to classify majority of the classes. Better than Logistic regression.")

# %%
# %%time
## Get Labels
class_names = ['low','medium','high','critical']
# Plot confusion matrix in a beautiful manner
plt.rcParams['axes.grid'] = False 
fig = plt.figure(figsize=(16, 8))
ax= plt.subplot()
sns.heatmap(cm, annot=True, ax = ax, fmt = 'g'); 
# labels, title and ticks
ax.set_xlabel('Predicted', fontsize=20)
ax.xaxis.set_label_position('bottom')
plt.xticks(rotation=90)
ax.xaxis.set_ticklabels(class_names, fontsize = 10)
ax.xaxis.tick_bottom()

ax.set_ylabel('True', fontsize=20)
ax.yaxis.set_ticklabels(class_names, fontsize = 10)
plt.yticks(rotation=0)

plt.title('KNN Confusion Matrix', fontsize=20)

plt.show()

# %%
# %%time
# Cross validating
knn = KNeighborsClassifier(n_neighbors=5, metric='manhattan', weights='distance')
knn.fit(X2_train, y2_train)
# Predict
y2_pred = knn.predict(X2_test)
print("KNN model score:", metrics.accuracy_score(y2_test, y2_pred))

# cross-validation score
# K fold is configured to 10 from the imports cells
score = cross_val_score(knn, X2_train, y2_train, cv=k_fold, n_jobs=1, scoring='accuracy')
print("Cross validated score:", score.mean())

# %% [raw]
# # YOUR WRITTEN ANSWER HERE
# For my classification model I decided to implement the K-Neighbors classifier because it is a multi-class classifier. However, to make sure that KNN would be the better model for this dataset, I also implemented trained Logistic Regression model to compare both of their scores and determine whether my choice was correct.
# Comparing the classification model's, it seems KNN turned out to be the better classifier to classify base severity ratings which is a multiclass label. 
# This is probably due to logistic regression being a binary classifier where it would require binarized target variable (0 and 1) to perform better.
#
# I went with the standard 80% training size which would allow the model sufficient training data to be able to accurately predict on the testing set. I also set the random state to get a consistent result to be able to compare the models.
#
# For my features I selected all the variables that are used for calculating the sub scores and base scores which in turn returns us a base severity rating. Essentially all these v3 variables would be best at predicting the base severity because they contribute towards calculating the base severity.  
# For max iteration I chose 1000 which returned a high train and test score and was also computationally less expensive. For the hyperparameters I used HalvingGridSearch which is much faster than Grid Search to find the best parameters that would result in the best score and for the cross validation splitting strategy parameter, I passed in the default cv of 5 to keep time complexity to a minimum.
#
# I also used sklearn's cross_val_score to compare with HalvingGridSearch's cross validation to get an estimate of knn model's performance on new data from both cross validations. The results were very accurate and close and the difference was quite insignificant.
#
# For metrics evalutaion, Sklearn's Confusion matrix and Classification report were used. The Classification report returned the precision (accuracy of model id finding true positives) , recall (how many of the actual positives our model captures) and f1 scores (a balance between precision and recall).
#
# Summary of the results:
#
#                        | LogisticRegression | K-nearest neighbors
# ___________________________________________________________________
# Test-score             | 0.989              | 0.999
# RMSE                   | 0.101              | 0.024
#
# True-positive (low)    | 59                 | 64
# True-positive (medium) | 2117               | 2149
# True-positive (high)   | 4111               | 4162
# True-positive (crit)   | 4072               | 4085 
#
# We can see that KNN is the overall better model for this dataset with great performance. 
#
# Refs:
# [1] Reference for multi-class confusion matrix heatmap code:
#     https://stackoverflow.com/questions/65618137/confusion-matrix-for-multiple-classes-in-python
# [2] https://www.projectpro.io/recipes/optimize-hyper-parameters-of-logistic-regression-model-using-grid-search-in-python
# [3] https://www.kaggle.com/code/enespolat/grid-search-with-logistic-regression/notebook
# [4] https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html   
# [5] https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.HalvingGridSearchCV.html
# [6] https://towardsdatascience.com/cross-validation-and-grid-search-efa64b127c1b

# %% [markdown]
# ******
# ## Q7: Apply your knowledge to the problem domain
#
# The government is worried about security issues that target user involvement over the internet.  You have been asked to help identify relevant vulnerabilities that need to be prioritised for patching.  While the CVSS systems provide a good general system for determining the Threat Level (Severity) of a vulnerability, you are only concerned with weaknesses that can be exploited over a network, and require user interaction.
#
# Your task is as follows:    
# #### (Q7.a)
# - Develop and present a basic heuristic to classify the Threat Level to identify which products need patching relevant to the above given context. A heuristic is a simple set of rules or a rule of thumb (e.g. 'If the fire alarm is activated, then leave the building' or 'If there are grey clouds, bring the washing in as it might rain' ). (2 marks)
# <br>(Similar to the Q6 above, you are able to choose any variables in the dataset, except of course the Base Scores, Sub Scores and Base Severity)
# - Run your heuristic over the dataset, and add the output to each row on the dataset, under a new column named `Threat Classification`.  (5 marks)
# - Justify your use of variables and the reasoning behind your heuristic in the written section below and explain how this might be an effective solution to stopping attacks. (3 marks)
#
# <span style= 'float: right;'><b>[10 marks]</b></span>
#
# <br><br>
# **Additional question for COMP6420 students: [worth extra 10 marks]**
# #### (Q7.b)
#  - Compare your heuristic result with the actual result (threat level) (5 marks)
#  - Based on your result, how would you improve your heuristic? (no implementation is required) (5 marks)
#

# %%
# YOUR CODE HERE
pd.set_option('display.max_column', None)
# attack vector = network = 0.85
# user interaction = required = 0.62
# Create a subset of the original dataframe with only the above mentioned values
data_df_copy_heuristic = data_df.copy()
data_df_copy_heuristic = data_df_copy_heuristic[data_df_copy_heuristic['v3_attackVector'].isin([0.85])]
data_df_copy_heuristic = data_df_copy_heuristic[data_df_copy_heuristic['v3_userInteraction'].isin([0.62])]

# Drop base scores, sub scores and base severity
data_df_copy_heuristic.drop(['v3_exploitabilityScore', 'v3_impactScore', 'v3_baseScore', 
                   'ISS', 'assigner', 'description', 'refs',
                   'ref_names', 'ref_sources', 'ref_tags'], axis=1, inplace=True)
data_df_copy_heuristic


# %%
def heuristic_formula(av, ac, pr, ui, s, ci, ii, ai):
    '''
    A simple function to calculates a threat classification using a simple set of rules
    input: attackVector, attackComplexity, privilegesRequired,
           userInteraction, scope, confidentialityImpact,
           integrityImpact, availabilityImpact
    output: threat classification rating
    '''
    if s == 1:
        res = av + ac + (pr * 6) + ui + (ci + ii + ai)
    else:
        res = av + ac + (pr * 5) + ui + (ci + ii + ai)
    return res

# Create threat classification column using heuristic formula
data_df_copy_heuristic['Threat_score'] = np.vectorize(heuristic_formula)(data_df_copy_heuristic['v3_attackVector'],
                                                              data_df_copy_heuristic['v3_attackComplexity'],
                                                              data_df_copy_heuristic['v3_privilegesRequired'],
                                                              data_df_copy_heuristic['v3_userInteraction'],
                                                              data_df_copy_heuristic['v3_scope'],
                                                              data_df_copy_heuristic['v3_confidentialityImpact'],
                                                              data_df_copy_heuristic['v3_integrityImpact'],
                                                              data_df_copy_heuristic['v3_availabilityImpact'])

def Threat_classification(Threat_score):
    '''
    This function assigns a severity rating depending on the base score
    input: float
    output: string
    '''
    if 0.0 <= Threat_score <= 3.9:
        return 2
    elif 4.0 <= Threat_score <= 6.9:
        return 3
    elif 7.0 <= Threat_score <= 8.9:
        return 4
    elif 9.0 <= Threat_score <= 10.0:
        return 5
    
data_df_copy_heuristic['Threat classificaiton'] = data_df_copy_heuristic.apply(lambda row: Threat_classification(row['Threat_score']), axis=1)

# %%
# Comparing threat classification from heuristic to actual base severity
data_df_copy_heuristic['similarities'] = np.where(data_df_copy_heuristic['Threat classificaiton']==data_df_copy_heuristic['v3_baseSeverity'], data_df_copy_heuristic['Threat classificaiton'], np.nan)
print(data_df_copy_heuristic['similarities'].value_counts(),'\n')
print("The number of severity ratings corrrectly calculated by heuristic: \n0 low severity out of 10, \n2432 medium severity out of 4294, \n1472 high severity out of 1513, \n50 critical severity out of 77.")
print("\nThe heuristic implemented isn't quite accurate and has much room for improvement")

# %%
pd.reset_option('display.max_column', None)
# Find products that need patching
data_df_copy_sub = data_df_copy_heuristic[['vendor', 'product_name', 'version', 'Threat classificaiton']]
data_df_copy_sub_sorted = data_df_copy_sub.sort_values(['Threat classificaiton'], ascending = False)
data_df_copy_sub_sorted.head(10)

# %% [raw]
# According to the created heuristic, these ten products displayed above are severly vulnerable and require patching.

# %% [raw]
# # YOUR WRITTEN ANSWER HERE
# For the heuristic I've used all the v3 scores which can help calculate the threat classification
# To calculate the threat classification, I've simply used the condition that is the scope is changed, the threat would be much higher therefore multiply the privileges required by a high number such as 6.
# If the scope is unchanged then multiply privileges required by a lower number such as 5 because the threat wouldn't be as severe.
#
# This simple heuristic can give an idea of which products have severe vulnerabilities through their corresponding threat classification and require urgent patching.
