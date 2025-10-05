
import pandas as pd
import numpy as np
from itertools import combinations

class DataWrangler:
    """A class to handle the data wrangling process for the assignment."""

    def __init__(self, education_file, medical_file, merged_file):
        """Initializes the DataWrangler with file paths."""
        self.education_file = education_file
        self.medical_file = medical_file
        self.merged_file = merged_file
        self.df_education = None
        self.df_medical = None
        self.df_merged = None

    def load_data(self):
        """Loads the education and medical datasets."""
        print("Loading datasets...")
        self.df_education = pd.read_csv(self.education_file)
        self.df_medical = pd.read_csv(self.medical_file)
        print("Datasets loaded successfully.")

    def merge_datasets(self):
        """Merges the two datasets on SSN, after removing duplicates from the source files."""
        if self.df_education is None or self.df_medical is None:
            self.load_data()
        
        # De-duplicate the education dataset, keeping the last record
        self.df_education.drop_duplicates(subset=['ssn'], keep='last', inplace=True)

        print("Merging datasets...")
        self.df_merged = pd.merge(self.df_education, self.df_medical, on='ssn', how='outer', suffixes=('_edu', '_med'))
        print("Datasets merged successfully.")

    def find_missing_combinations(self, dataset_name='merged', num_attributes=3):
        """Finds the top combination of attributes with missing values."""
        if dataset_name == 'merged':
            df = self.df_merged
        elif dataset_name == 'education':
            df = self.df_education
        else:
            raise ValueError("Invalid dataset name. Choose 'merged' or 'education'.")

        cols = df.columns
        max_missing_count = 0
        top_combination = None

        for combo in combinations(cols, num_attributes):
            missing_count = df[list(combo)].isnull().all(axis=1).sum()
            if missing_count > max_missing_count:
                max_missing_count = missing_count
                top_combination = combo

        return top_combination, max_missing_count

    def find_top_missing_attributes(self, num_attributes=2):
        """Finds the top individual attributes with missing values."""
        missing_counts = self.df_merged.isnull().sum()
        return missing_counts.sort_values(ascending=False).head(num_attributes)

    def find_internal_duplicates(self):
        """Finds and reports on duplicate SSNs within each source dataset."""
        if self.df_education is None or self.df_medical is None:
            self.load_data()

        edu_duplicates = self.df_education[self.df_education.duplicated(subset=['ssn'], keep=False)]
        med_duplicates = self.df_medical[self.df_medical.duplicated(subset=['ssn'], keep=False)]

        num_edu_duplicates = len(edu_duplicates['ssn'].unique())
        num_med_duplicates = len(med_duplicates['ssn'].unique())

        print(f"Found {num_edu_duplicates} SSNs with duplicate records in the education dataset.")
        print(f"Found {num_med_duplicates} SSNs with duplicate records in the medical dataset.")

        return edu_duplicates, med_duplicates

    def assess_dataset_quality(self):
        """Assesses data quality by comparing missing values in common attributes between datasets."""
        if self.df_education is None or self.df_medical is None:
            self.load_data()

        common_cols = ['first_name', 'middle_name', 'last_name', 'gender', 'birth_date', 'street_address', 'suburb', 'postcode', 'state', 'phone', 'email']
        quality_assessment = {}

        print("\n--- Data Quality Assessment (Missing Values) ---")
        for col in common_cols:
            missing_edu = self.df_education[col].isnull().sum()
            missing_med = self.df_medical[col].isnull().sum()
            quality_assessment[col] = {'education_missing': missing_edu, 'medical_missing': missing_med}
            print(f"  {col}: Education Missing = {missing_edu}, Medical Missing = {missing_med}")
        print("--------------------------------------------------")
        return quality_assessment

    def find_inconsistencies(self):
        """Finds and counts inconsistencies between common columns."""
        common_cols = ['first_name', 'middle_name', 'last_name', 'gender', 'birth_date', 'street_address', 'suburb', 'postcode', 'state', 'phone', 'email']
        inconsistencies = {}

        # Get the records that are present in both datasets
        inner_merged = self.df_merged[self.df_merged['rec_id_edu'].notna() & self.df_merged['rec_id_med'].notna()]

        for col in common_cols:
            col_edu = col + '_edu'
            col_med = col + '_med'
            
            # Find where the values are different, but both are non-null
            mismatch = inner_merged[inner_merged[col_edu].notna() & inner_merged[col_med].notna() & (inner_merged[col_edu] != inner_merged[col_med])]
            inconsistencies[col] = mismatch['ssn'].nunique()

        return inconsistencies

    def resolve_inconsistencies(self):
        """Resolves inconsistencies by preferring the education dataset."""
        print("Resolving inconsistencies...")
        common_cols = ['first_name', 'middle_name', 'last_name', 'gender', 'birth_date', 'street_address', 'suburb', 'postcode', 'state', 'phone', 'email']

        for col in common_cols:
            col_edu = col + '_edu'
            col_med = col + '_med'
            # Coalesce the columns, preferring the _edu version
            self.df_merged[col] = self.df_merged[col_edu].fillna(self.df_merged[col_med])
            # Drop the old columns
            self.df_merged.drop(columns=[col_edu, col_med], inplace=True)
        
        print("Inconsistencies resolved.")

    def run_full_process(self):
        """Runs the entire data wrangling and analysis process."""
        self.merge_datasets()
        self.resolve_inconsistencies()
        self.correct_values()
        self.save_merged_data()

    def correct_values(self):
        """Corrects the identified incorrect values in the merged dataset."""
        print("Correcting values...")
        # Correct negative weights and salaries
        self.df_merged['weight'] = self.df_merged['weight'].abs()
        self.df_merged['salary'] = self.df_merged['salary'].abs()
        print("Corrected negative weights and salaries.")

        # Recalculate BMI
        valid_hw = self.df_merged['height'].notna() & self.df_merged['weight'].notna()
        self.df_merged.loc[valid_hw, 'bmi'] = self.df_merged.loc[valid_hw, 'weight'] / (self.df_merged.loc[valid_hw, 'height'] / 100)**2
        print("Recalculated BMI.")
        print("Value correction complete.")

    def save_merged_data(self):
        """Saves the cleaned merged dataframe to a CSV file."""
        print(f"Saving cleaned data to {self.merged_file}...")
        self.df_merged.to_csv(self.merged_file, index=False)
        print("Data saved successfully.")

    def convert_to_datetime(self):
        """Converts date and timestamp columns to datetime objects."""
        print("Converting date/timestamp columns...")
        date_cols = ['birth_date', 'employment_timestamp', 'consultation_timestamp']
        for col in date_cols:
            self.df_merged[col] = pd.to_datetime(self.df_merged[col], errors='coerce')
        print("Date/timestamp conversion complete.")

    def clean_salary(self, threshold=10000):
        """Replaces salaries below a threshold with NaN."""
        print(f"Cleaning salary data... Replacing salaries below {threshold} with NaN.")
        low_salary_count = self.df_merged[self.df_merged['salary'] < threshold].shape[0]
        self.df_merged.loc[self.df_merged['salary'] < threshold, 'salary'] = np.nan
        print(f"Replaced {low_salary_count} records with low salaries.")

    def standardize_education(self):
        """Standardizes the education column to consistent values."""
        print("Standardizing education column...")
        # Example mapping - this would be built based on initial analysis
        education_mapping = {
            'bachelor-degree': 'bachelor',
            'graduate-diploma': 'graduate-diploma',
            'graduate-certificate': 'graduate-certificate',
            'certificate-iv': 'certificate-iv',
            'master-degree': 'master',
            'doctoral-degree': 'doctorate'
            # Add other mappings as needed based on value_counts()
        }
        # For now, a simple standardization: extract the first part of the hyphenated string
        self.df_merged['education'] = self.df_merged['education'].str.split('-').str[0]
        print("Education column standardized.")

    def create_bmi_category(self):
        """Creates a BMI category column from the BMI values."""
        print("Creating BMI category...")
        bins = [0, 18.5, 25, 30, np.inf]
        labels = ['Underweight', 'Normal', 'Overweight', 'Obese']
        self.df_merged['bmi_category'] = pd.cut(self.df_merged['bmi'], bins=bins, labels=labels, right=False)
        print("BMI category created.")

    def run_full_process(self):
        """Runs the entire data wrangling and analysis process."""
        self.merge_datasets()
        self.resolve_inconsistencies()
        self.correct_values()
        self.save_merged_data()
