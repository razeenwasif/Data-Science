
from wrangler import DataWrangler

EDUCATION_DATASET = "/home/r10x8596/Github/Data-Science/Data-Wrangling/Assignment2/data/data_wrangling_education_2025_u7283652.csv"
MEDICAL_DATASET = "/home/r10x8596/Github/Data-Science/Data-Wrangling/Assignment2/data/data_wrangling_medical_2025_u7283652.csv"
MERGED_DATASET = "/home/r10x8596/Github/Data-Science/Data-Wrangling/Assignment2/data/data_wrangling_merged_2025_u7283652.csv"

def main():
    """Main function to run the data wrangling process."""
    
    # Initialize the wrangler
    wrangler = DataWrangler(EDUCATION_DATASET, MEDICAL_DATASET, MERGED_DATASET)

    # 1. Load and Merge
    wrangler.load_data()
    
    # Assess data quality before merging
    wrangler.assess_dataset_quality()

    wrangler.merge_datasets()

    # 2. Perform Analysis (Tasks 3 and 4 - Initial Checks)
    print("\n" + "="*50)
    print("INITIAL ANALYSIS RESULTS (Before Resolution)")
    print("="*50 + "\n")

    # Task 3 Analysis (part 1 - education dataset)
    print("--- Task 3: Missing Values (Education Dataset) ---")
    combo_edu, count_edu = wrangler.find_missing_combinations(dataset_name='education')
    print(f"In education dataset, top missing 3-attribute combination is {combo_edu} with {count_edu} records.")

    # Task 4 Analysis (Duplicates and Inconsistencies)
    print("\n--- Task 4: Duplicates and Inconsistencies ---")
    wrangler.find_internal_duplicates()
    inconsistencies = wrangler.find_inconsistencies()
    print("\nNumber of inconsistent values for common attributes:")
    for col, count in inconsistencies.items():
        print(f"  {col}: {count}")

    # 3. Resolve, Clean, and Save (Initial Cleanup)
    print("\n" + "="*50)
    print("PERFORMING INITIAL CLEANUP (Resolution)")
    print("="*50 + "\n")

    # First, resolve inconsistencies to create the final columns
    wrangler.resolve_inconsistencies()

    # 4. Perform Analysis (Tasks 3 - After Resolution)
    print("\n" + "="*50)
    print("ANALYSIS RESULTS (After Resolution)")
    print("="*50 + "\n")

    # Task 3 Analysis (part 2 - merged dataset after resolution)
    print("--- Task 3: Missing Values (Merged Dataset After Resolution) ---")
    top_two_missing = wrangler.find_top_missing_attributes()
    print(f"In merged dataset, top two missing attributes are:\n{top_two_missing}")
    combo_merged, count_merged = wrangler.find_missing_combinations(dataset_name='merged')
    print(f"In merged dataset, top missing 3-attribute combination is {combo_merged} with {count_merged} records.")

    # Now, perform Task 5 cleaning steps
    print("--- Task 5, Step 1: Converting Date Columns ---")
    print("Data types before conversion:")
    print(wrangler.df_merged[['birth_date', 'employment_timestamp', 'consultation_timestamp']].dtypes)
    wrangler.convert_to_datetime()
    print("\nData types after conversion:")
    print(wrangler.df_merged[['birth_date', 'employment_timestamp', 'consultation_timestamp']].dtypes)

    # Task 5, Step 2: Clean Salary Data
    print("\n--- Task 5, Step 2: Cleaning Salary Data ---")
    print("Salary stats before cleaning:")
    print(wrangler.df_merged['salary'].describe())
    wrangler.clean_salary()
    print("\nSalary stats after cleaning:")
    print(wrangler.df_merged['salary'].describe())

    # Task 5, Step 3: Standardize Education Column
    print("\n--- Task 5, Step 3: Standardizing Education Column ---")
    print("Education values before standardization:")
    print(wrangler.df_merged['education'].value_counts())
    wrangler.standardize_education()
    print("\nEducation values after standardization:")
    print(wrangler.df_merged['education'].value_counts())

    # Task 5, Step 4: Create BMI Category
    print("\n--- Task 5, Step 4: Creating BMI Category ---")
    wrangler.create_bmi_category()
    print("BMI category values:")
    print(wrangler.df_merged['bmi_category'].value_counts())

    # Correct other values and save
    wrangler.correct_values()
    wrangler.save_merged_data()

if __name__ == "__main__":
    main()
