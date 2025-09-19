
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
        """Merges the two datasets on SSN."""
        if self.df_education is None or self.df_medical is None:
            self.load_data()
        
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

    def run_full_process(self):
        """Runs the entire data wrangling and analysis process."""
        self.merge_datasets()
        self.correct_values()
        self.save_merged_data()
