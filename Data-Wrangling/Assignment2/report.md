checkcodes: 87ab424b / 462b43a24f17

## Task 1 (3 marks): 
Generate two strings of numbers based on your ANU ID (excluding the first character ‘u’):
– s1 is the string ‘123’ concatenated with the first four digits of your ANU ID.
– s2 is the string ‘123’ concatenated with the last four digits of your ANU ID. Include any leading zeros.
For example, if your ANU ID is u9800765 then s1 = ‘1239800’ and s2 = ‘1230765’
Now manually calculate the following similarities between these two strings and include in your assignment both your workings (equations or edit matrices) as well as the final results for:
1. The Dice coefficient similarity based on unigrams (q = 1).
2. The Jaccard similarity based on bigrams (q = 2).
3. The bag distance similarity
4. The Levenshtein edit distance between the two strings, assuming a cost of 2 for substitutions, cost of 1 for inserts,
and cost of 1 for deletes.
5. In a couple of sentences, explain the relationship between the bag distance and the edit distance.
Round the final numerical results to two decimal places. For sub-task 4 you must show the full edit matrix as your workings.

### Answers:
my ANU ID: u7283652
string 1 = 1237283
string 2 = 1233652

1. Dice coefficient of s1 and s2 based on unigrams.
    * s1_{q=1}: '1' '2' '3' '7' '8' (must be sets after extracting unigrams)
    * s2_{q=1}: '1' '2' '3' '6' '5'
    matching_window = floor(max(7,7) / 2) - 1 = 2
    dice_sim = 2 * len(s1_{q=1} & s2_{q=2}) / (len(s1_{q=1}) + len(s2_{q=2}))
    dice_sim = 2 * 3 / (5 + 5) = 6 / 10 = 0.60

2. Jaccard similarity based on bigrams 
    * s1_{q=2}: '12' '23' '37' '72' '28' '83'
    * s2_{q=2}: '12' '23' '33' '36' '65' '52'
    matching_window = floor(max(6, 6) / 2) - 1 = 2 
    dice_jacc = 2 / (6 + 6 - 2) = 0.20

3. Bag distance similarity 
    * s1_{bag} = {1, 2, 3, 7, 2, 8, 3}
    * s2_{bag} = {1, 2, 3, 3, 6, 5, 2}
    dist_{bag} = max(|x - y|, |y - x|) = max({7,8}, {6,5}) = 2 
    sim_bag = 1.0 - (2 / max(len(s1), len(s2))) = 1.0 - 2/7 = 0.71

4. The Levenshtein edit distance between the two strings, assuming a cost of 2 for substitutions, cost of 1 for inserts and cost of 1 for deletes.
                     
                    |s1| if |s2| = 0 
edits.lev(s1, s2) { |s2| if |s1| = 0 
                    lev (tail(s1), tail(s2))  if s1[0] = s2[0]
                            { lev(tail(a), b) 
                    1 + min { lev(a, tail(b))  otherwise
                            { lev(tail(a), tail(b))

if s1_{i} = s2_{j} then d_{ij} = replace

| replace | insert |
| delete  | pick the min of three

|   | ε | 1 | 2 | 3 | 7 | 2 | 8 | 3 |
----|---|----------------------------
| ε | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 1 | 1 | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| 2 | 2 | 1 | 0 | 1 | 2 | 3 | 4 | 5 |
| 3 | 3 | 2 | 1 | 0 | 1 | 2 | 3 | 4 |
| 3 | 4 | 3 | 2 | 1 | 2 | 3 | 4 | 3 |
| 6 | 5 | 4 | 3 | 2 | 3 | 4 | 5 | 4 |
| 5 | 6 | 5 | 4 | 3 | 4 | 5 | 6 | 5 |
| 2 | 7 | 6 | 5 | 4 | 5 | 4 | 5 | 6 |

Levenshtein distance = 6

5. In a coupe of sentences, explain the relationship between the bag distance and the edit distance.
    * The bag distance is a lower bound for edit distance, meaning the bag distance between two strings will always be less than or equal to their edit distance. Bag distance is also computationally less expensive.


## Task 2 (Dataset merging) (maximum of 200 words for both as one):

1. How many unique SSNs occurred in common in both data sets? How many occurred only in the medical data set, and how many occurred only in the education data set?
    * common in both data sets: 15956
    * only in medical: 4044
    * only in education: 3267

2. If there were records that only occurred in a single data set, describe whether you decieded to delete or retain them in the final merged data set, and explain / justify why.
    * I chose to retain them to ensure the most comprehensive analysis possible and to prevent premature data loss. By keeping all records, we can analyze the entire population available and it also provides the flexibilty to investigate the characteristics of individuals who appear in only one of the datasets.

## Task 3 (Missing and Incorrect Values):

1. Following the missing patterns table we discussed in the labs and used in Assignment 1, find the combination of three attributes with the highest number of missing values (i.e. the three-attribute combinations with the largest numbers of records with missing values) in (a) education data set, and (b) your merged dataset. Provide the attribute names and the corresponding number of records with missing values in each of these data sets.

	* **(a) Education Dataset:**
		*   The combination of three attributes with the highest number of missing values is `('occupation', 'salary', 'credit_card_number')`.
		*   There are **239** records where all three of these attributes are missing.
	* **(b) Merged Dataset:**
		*   The combination of three attributes with the highest number of missing values is also `('occupation', 'salary', 'credit_card_number')`.
		*   In the merged dataset, there are **4283** records where all three of these attributes are missing.

2. What are the two attributes with the highest number of missing values (individually) in your merged data set? For
these attributes, either:
– consider if you can impute these missing values. If so describe the approach you have taken to impute
missing values, and justify why you have taken this approach; or
– if you decided you cannot impute missing values in an attribute then describe and justify why you have not
done any imputation.

	* The two attributes with the highest number of missing values in the merged dataset (after resolving inconsistencies) are:
		1.  `salary`: 7,034 missing values
		2.  `marital_status`: 5,843 missing values
	* **Handling of `salary` missing values:**
		*   **Decision:** Missing values in `salary` are primarily a result of the cleaning process, where salaries below $10,000 were replaced with `NaN`.
		*   **Justification:** This approach was taken to remove unrealistic and potentially erroneous salary entries that would skew statistical analysis. By treating these as missing, we ensure that any analysis involving salary is based on realistic income levels. No further imputation was performed as these `NaN`s represent intentionally excluded data points.
	* **Handling of `marital_status` missing values:**
		*   **Decision:** I decided **not to impute** the missing values for `marital_status`.
		*   **Justification:** `marital_status` is a categorical variable, and without additional information or a clear pattern, imputing these values (e.g., with the mode) could introduce bias or incorrect assumptions into the dataset. It is safer to leave these values as missing, allowing downstream analysis to handle them appropriately (e.g., by excluding them or treating 'missing' as its own category if appropriate for the analysis).

3. Describe what incorrect or impossible values you found in attributes in your merged data set, and provide how many
such incorrect or impossible values are there for each attribute. Also describe why you believe these values are
impossible or incorrect.

	*   **Negative `weight`:**
		*   **Count:** 2,161 records.
		*   **Reason:** A person's weight cannot be a negative value. This is a clear data entry or measurement error.
	*   **Negative `salary`:**
		*   **Count:** 2,996 records.
		*   **Reason:** A salary cannot be a negative amount. This indicates a data error.
	*   **Incorrectly Calculated `bmi`:**
		*   **Count:** 2,161 records.
		*   **Reason:** The Body Mass Index (BMI) is calculated from height and weight. In these records, the stored `bmi` value is inconsistent with the `height` and `weight` values, often because the weight is negative.

4. Describe how you dealt with the incorrect or impossible values identified in your merged data set (for example
correcting them in some way or another).

	*   **For Negative `weight`:**
		*   **Action:** I will take the absolute value of the weight to make it positive.
		*   **Justification:** It is highly probable that the negative sign is a data entry error and the magnitude of the value is correct. This approach corrects the error while preserving the data.
	*   **For Negative `salary`:**
		*   **Action:** I will take the absolute value of the salary.
		*   **Justification:** Similar to weight, a negative salary is illogical. Taking the absolute value is the most reasonable correction under the assumption that the number is correct, just with the wrong sign.
	*   **For Incorrectly Calculated `bmi`:**
		*   **Action:** After correcting the negative weights, I will recalculate the `bmi` for all records using the formula: `BMI = weight (kg) / (height (m))^2`. The existing `bmi` column will be updated with these new, correct values.
		*   **Justification:** Since BMI is a derived value, recalculating it is the only way to ensure it is accurate and consistent with the source `height` and `weight` data.

## Task 4 (Duplicate and Inconsistent Records)

### Duplicate Records

I identified duplicate SSNs within the education dataset using drop_duplicates(subset=['ssn'], keep='last').

Action Taken: I retained the last occurrence of each SSN and dropped all earlier duplicates.

Justification: Keeping the last record ensures that the most recent or updated information is preserved. This reduces the chance of using outdated data for a given individual, which is crucial for an analysis of education, employment, and health.

### Inconsistencies Between Datasets

The script identified the following attributes with inconsistencies
  between records with the same SSN, along with the number of
  inconsistent records for each:

   * last_name: 37
   * gender: 1580
   * street_address: 6716
   * suburb: 6625
   * postcode: 5274
   * state: 2851
   * phone: 1921
   * email: 1508

  How these inconsistencies were dealt with:

  The wrangler.py script resolves these inconsistencies by creating
  a new, unified column for each common attribute in the merged
  dataset. For each attribute, it prioritizes the value from the
  education dataset. Specifically, if a value exists in the
  education dataset for a given SSN, that value is selected for the
  merged column. If the value is missing in the education dataset
  but present in the medical dataset, the medical dataset's value is
   used. If both are missing, the merged column will contain a null
  value. After this resolution, the original separate columns (e.g.,
   first_name_edu and first_name_med) are dropped.

  Justification for the approach:

  The code implements a "prefer education dataset" strategy for resolving
  inconsistencies in common attributes. This decision is supported by a
  data quality assessment focusing on missing values in the original
  datasets. For critical contact information attributes such as
  `postcode`, `phone`, and `email`, the education dataset exhibits
  significantly higher completeness (fewer missing values) compared to
  the medical dataset. For instance, the education dataset has 21 missing
  postcodes compared to 4010 in the medical dataset; 1990 missing phone
  numbers versus 7921; and 2028 missing emails versus 5985.

  While the medical dataset showed higher completeness for some address
  components like `street_address`, `suburb`, and `state`, the overall
  superiority of the education dataset in key identifying and contact
  fields makes it a more reliable primary source for these attributes.
  This pragmatic choice establishes a consistent rule for conflict
  resolution, ensuring that the merged dataset benefits from the more
  complete information where it matters most for individual identification
  and contact. In a real-world scenario, such a preference would also
  be driven by formal data authority designations or specific business
  rules.


## Task 5 (Other Data Cleaning):

Here are the four additional data cleaning and transformation tasks I performed:

### 1. Standardized Date and Timestamp Columns

*   **Action:** I converted the `birth_date`, `employment_timestamp`, and `consultation_timestamp` columns from their original `object` (text) format into proper `datetime` objects.
*   **Justification:** This data type correction is fundamental for enabling accurate, time-based calculations. It allows for the verification of age, analysis of time-lapsed between employment and health consultations, and general trend analysis, all of which are crucial for exploring the links between education, employment, and health.
*   **Result:** The columns were successfully converted, as shown by the script output, changing their data type from `object` to `datetime64[ns]` and `datetime64[ns, UTC]`.

### 2. Cleaned Invalid Salary Data

*   **Action:** I analyzed the `salary` column and identified a large number of records with invalid data, including negative values and zeros. I implemented a cleaning step to replace any salary below a realistic threshold of $10,000 with `NaN` (Not a Number).
*   **Justification:** Including these invalid salaries in any analysis would heavily skew the results (e.g., the mean income). By treating them as missing data, we get a more accurate and reliable understanding of the relationship between realistic income levels and health outcomes. 
*   **Result:** This action affected 5,264 records. The minimum salary in the dataset was raised from -9999.0 to 10009.0, and the mean salary shifted from a skewed $56,164 to a more representative $85,590.

### 3. Standardized `education` Categories

*   **Action:** I inspected the `education` column and found multiple variations for the same education level (e.g., `certificate-i`, `certificate-ii`, `certificate-iii`, `certificate-iv`). I consolidated these into a single, consistent set of categories (e.g., `certificate`).
*   **Justification:** This standardization is essential for any statistical analysis involving education. It prevents the data for a single education level from being split across multiple categories, thereby increasing the validity and statistical power of the analysis.
*   **Result:** The various certificate levels were grouped into one `certificate` category, and other levels were simplified (e.g., `bachelor-degree` to `bachelor`), resulting in a cleaner, more usable feature.

### 4. Engineered `bmi_category` Feature

*   **Action:** I created a new categorical column, `bmi_category`, by grouping the numerical `bmi` values into four standard health categories: 'Underweight' (<18.5), 'Normal' (18.5-24.9), 'Overweight' (25-29.9), and 'Obese' (>=30).
*   **Justification:** For analyzing health outcomes, these standard BMI categories are often more powerful and interpretable than the continuous BMI values. This feature engineering step creates a more direct and clinically relevant variable for exploring the link between lifestyle factors and health status.
*   **Result:** A new `bmi_category` column was successfully added to the dataset, with the records distributed across the four health categories (e.g., 8,861 'Obese', 4,869 'Normal', etc.).

	*   **For Negative `weight`:**
		*   **Action:** I will take the absolute value of the weight to make it positive.
		*   **Justification:** It is highly probable that the negative sign is a data entry error and the magnitude of the value is correct. This approach corrects the error while preserving the data.
	*   **For Negative `salary`:**
		*   **Action:** I will take the absolute value of the salary.
		*   **Justification:** Similar to weight, a negative salary is illogical. Taking the absolute value is the most reasonable correction under the assumption that the number is correct, just with the wrong sign.
	*   **For Incorrectly Calculated `bmi`:**
		*   **Action:** After correcting the negative weights, I will recalculate the `bmi` for all records using the formula: `BMI = weight (kg) / (height (m))^2`. The existing `bmi` column will be updated with these new, correct values.
		*   **Justification:** Since BMI is a derived value, recalculating it is the only way to ensure it is accurate and consistent with the source `height` and `weight` data.  
