
from wrangler import DataWrangler

EDUCATION_DATASET = "/home/r10x8596/Github/Data-Science/Data-Wrangling/Assignment2/data/data_wrangling_education_2025_u7283652.csv"
MEDICAL_DATASET = "/home/r10x8596/Github/Data-Science/Data-Wrangling/Assignment2/data/data_wrangling_medical_2025_u7283652.csv"
MERGED_DATASET = "/home/r10x8596/Github/Data-Science/Data-Wrangling/Assignment2/data/data_wrangling_merged_2025_u7283652.csv"

def main():
    """Main function to run the data wrangling process."""
    
    # Initialize the wrangler
    wrangler = DataWrangler(EDUCATION_DATASET, MEDICAL_DATASET, MERGED_DATASET)

    # Run the main processing pipeline
    wrangler.run_full_process()

    # --- Perform and print analysis as done in previous scripts ---

    print("\n" + "="*50)
    print("TASK 3 ANALYSIS RESULTS")
    print("="*50 + "\n")

    # Part 1: Missing Combinations
    print("--- Part 1: Attribute Combinations with Missing Values ---")
    combo_edu, count_edu = wrangler.find_missing_combinations(dataset_name='education')
    print(f"In education dataset, top combination is {combo_edu} with {count_edu} missing records.")
    
    combo_merged, count_merged = wrangler.find_missing_combinations(dataset_name='merged')
    print(f"In merged dataset, top combination is {combo_merged} with {count_merged} missing records.")

    # Part 2: Top Missing Attributes
    print("\n--- Part 2: Top Two Attributes with Missing Values ---")
    top_two_missing = wrangler.find_top_missing_attributes()
    print(top_two_missing)
    print("\nJustification: As noted in report.md, these attributes (phone_med, email_med) are unique identifiers and should not be imputed, as it would mean fabricating data.")

if __name__ == "__main__":
    main()
