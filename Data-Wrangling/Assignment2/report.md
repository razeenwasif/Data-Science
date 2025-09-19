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
		*   There are **251** records where all three of these attributes are missing.
	* **(b) Merged Dataset:**
		*   The combination of three attributes with the highest number of missing values is also `('occupation', 'salary', 'credit_card_number')`.
		*   In the merged dataset, there are **4295** records where all three of these attributes are missing.

2. What are the two attributes with the highest number of missing values (individually) in your merged data set? For
these attributes, either:
– consider if you can impute these missing values. If so describe the approach you have taken to impute
missing values, and justify why you have taken this approach; or
– if you decided you cannot impute missing values in an attribute then describe and justify why you have not
done any imputation.

	* The two attributes with the highest number of missing values in the merged dataset are:
		1.  `phone_med`: 11,485 missing values
		2.  `email_med`: 9,493 missing values
	* **Decision:** I decided **not to impute** the missing values for these two attributes.
	* **Justification:**
		*   Phone numbers and email addresses are unique personal identifiers. There is no reliable or logical method to guess or generate these values. Standard imputation techniques like mean, median, or mode are irrelevant for this type of data.
		*   Attempting to impute these values would be an act of data fabrication, as any generated value would almost certainly be incorrect. This would compromise the integrity of the dataset and add no value to the analysis.
		*   It is far better to acknowledge that the contact information is unknown than to populate the field with a false one.

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

