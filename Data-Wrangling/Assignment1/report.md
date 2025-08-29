87ab424b / ad0084dd9cb5

Task 1:
1. 
a. Two new data quality challenges that have arisen since the Rahm and Do paper's publication are the unstructured data deluge and the integrity of data from the Internet of Things (IoT).  

Unstructured data, which can include emails, customer support transcripts, and social media posts, now accounts for the majority of all data. This data is inherently "messy" and "chaotic," lacking the predefined formats that traditional data cleaning methods rely on. As a result, sensitive information can remain unprotected, and AI models trained on this data may produce flawed predictions and decisions. 

The second major issue is the volume and velocity of IoT data. Traditional systems designed for batch processing "falter when faced with live data streams," leading to a new set of problems. Inconsistent, outdated, or inaccurate readings from faulty sensors can lead to misleading insights and costly mistakes, requiring a shift to continuous, real-time data validation.   

b. Yes, the problems identified in the Rahm and Do paper remain highly relevant today. While the paper was written over two decades ago, its foundational taxonomy for data quality problems is still applicable, especially for issues that arise from integrating data from different sources. The core issues they identified, such as duplicated records, naming conflicts, and structural conflicts, have not disappeared but have become magnified in complexity and scale by the modern data ecosystem.  

The influx of data from a multitude of channels, including cloud storage and real-time streams, makes duplicate entries and inconsistencies an inevitable challenge. Similarly, the paper's focus on schema-level issues like naming and structural conflicts is more critical than ever, given the widespread use of microservices and APIs from independent developers, each with their own naming conventions and data formats. Therefore, the paper's framework is not a historical artifact but a foundational set of principles that requires modern solutions to address a far more complex reality.  


2. When serving as a data wrangler for the Australian Bureau of Statistics (ABS), three key aspects would need to be considered when integrating census data. First, the process of linking data across different census years, known as inter-census linkage, would require careful management of linkage errors. Records might be incorrectly matched ("false links") or contain inconsistencies due to reporting or processing errors, which can distort longitudinal analysis if not meticulously managed.  

Second, handling self-reported and politically sensitive data, particularly for Aboriginal and Torres Strait Islander peoples, presents a unique challenge. The ABS uses a "Standard Indigenous Question" based on 'origin,' and an individual's self-identification can change over time due to non-demographic factors. A data wrangler must account for these nuances and ensure that any changes in population counts are not solely interpreted as demographic shifts, as this could lead to misguided policy decisions.  

Finally, ensuring coherence and standardization across different data collections is crucial. The census is a full population count, but other ABS datasets, like the Labour Force Survey, may use different sampling or collection methodologies. This can render datasets "not strictly comparable" and necessitate careful data transformations and documentation of any methodological discrepancies to prevent flawed conclusions.   

Task 2:
L = [25, 11, 40, 17, 17, 41, 21, 31, 46, 26, 86, 74, 100, 28, 15, 97, 72, 83, 65, 2]

L-sorted = [2, 11, 15, 17, 17, 21, 25, 26, 28, 31, 40, 41, 46, 65, 72, 74, 83, 86, 97, 100]

a. Mean and Standard deviation calculation
Mean = Sum of all numbers / count of numbers = 897/20 = 44.85 
Std = 30.13349

b. Median and median absolute deviation
Median = 35.5
MAD = 19.5

c. Mode 
mode = 17

d. Based on the mode, median, and mean values, the distribution is right-skewed. Since Mean > Median > Mode, the distribution has a longer tail on the right side.

Task 3:
Bin 1: [2, 11, 15, 17, 17, 21, 25, 26, 28, 31]
Bin 2: [40, 41, 46, 65, 72, 74, 83, 86, 97, 100]

1. equal depth with two bins and smoothed by bin median
    Median of bin 1 is 19.0 
    Median of bin 2 is 73.0 

    smoothed_bin_1 = [19, 19, 19, 19, 19, 19, 19, 19, 19, 19] 
    smoothed_bin_2 = [73, 73, 73, 73, 73, 73, 73, 73, 73, 73]

2. equal width with three bins and smoothed by bin mean
    The min is 2 and max is 100 so range is 100-2=98. With three equal-width bins, the width of each bin is 98/3 approx. 32.67 
    The bin boundaries are:
        * Bin 1: [2, 34.67)
        * Bin 2: [34.67, 67.33)
        * Bin 3: [67.33, 100]

    sort the numbers into respective bins:
    * Bin 1: [2, 11, 15, 17, 17, 21, 25, 26, 28, 31]
    * Bin 2: [40, 41, 46, 65]
    * Bin 3: [72, 74, 83, 86, 97, 100]

    smoothed by bin mean:
    * Bin 1: [19.3, 19.3, 19.3, 19.3, 19.3, 19.3, 19.3, 19.3, 19.3, 19.3]
    * Bin 2: [48, 48, 48, 48]
    * Bin 3: [85.33, 85.33, 85.33, 85.33, 85.33, 85.33]

3. equal width with four bins and smoothed by bin boundaries 
    98/4 = 24.5 so bin boundaries are:
    * Bin 1: [2, 26.5)
    * Bin 2: [26.5, 51.0)
    * Bin 3: [51.0, 75.5)
    * Bin 4: [75.5, 100]

    sort the numbers into respective bins:
    * Bin 1: [2, 11, 15, 17, 17, 21, 25, 26]
    * Bin 2: [28, 31, 40, 41, 46]
    * Bin 3: [65, 72, 74]
    * Bin 4: [83, 86, 97, 100]

    smoothed list:
    * Bin 1: [2, 2, 26.5, 26.5, 26.5, 26.5, 26.5, 26.5]
    * Bin 2: [26.5, 26.5, 51, 51, 51]
    * Bin 3: [75.5, 75.5, 75.5] 
    * Bin 4: [75.5, 75.5, 100, 100]

4. equal depth with four bins and smoothed by bin boundaries
    * Bin 1: [2, 11, 15, 17, 17]
    * Bin 2: [21, 25, 26, 28, 31]
    * Bin 3: [40, 41, 46, 65, 72]
    * Bin 4: [74, 83, 86, 97, 100]

    smoothed bins:
    * Bin 1: [2, 17, 17, 17, 17]
    * Bin 2: [21, 21, 21, 31, 31]
    * Bin 3: [40, 40, 40, 72, 72]
    * Bin 4: [74, 74, 74, 100, 100]

Task 4:

### 1. Provide the missingness patterns of values for the three attributes: postcode, phone, and email. You should provide the 0-1 missing value pattern table.
| postcode | phone | email | count |
| -------- | ----- | ----- | ----- |
| 1        | 1     | 1     | 6774  |
| 1        | 0     | 1     | 4442  |
| 1        | 1     | 0     | 2891  |
| 1        | 0     | 0     | 1883  |
| 0        | 1     | 1     | 1690  |
| 0        | 0     | 1     | 1109  |
| 0        | 1     | 0     | 724   |
| 0        | 0     | 0     | 487   |


### 2. Calculate the correlation between the attributes (a) BMI and age_at_consultation and (b) state and valid marital_status.
(a) BMI vs age_at_consultation
    * Correlation value: 0.25 
    * Method: Pearson correlation 
    * Why this method: both attributes are continuous numeric variables measured on an interval scale; Pearson quantifies linear association.

(b) State vs valid marital_status
    * Correlation value: 0.03
    * Method: Cramer's V (based on χ² from the contingency table; n=9490 valid pairs)
    * Why this method: both variables are nominal categorical, so Cramér’s V is appropriate for strength of association without assuming ordering. (“Valid” marital statuses considered: single, married, divorced, widowed, separated, de facto/defacto/de-facto, civil union, partnered, engaged, in relationship, never married, not married; case/spacing normalized.)

### 3. For the following attributes, calculate numerical values for the following data quality dimensions:
    (a) Completeness for middle_name and email (consider these attributes individually)
        - Completeness 
            * middle_name: 89.78%
            * email: 70.08%
            * How it was calculated: count of non-null values divided by total rows 

    (b) Validity for weight and email (with a valid email containing the @ symbol. Only consider non empty email values for the calculation)
        - Weight: 86.26% (17253 of 20000 non-missing values are valid), using a plausible range 30-300kg on non-missing weights only.
        - Email: 85.04% (11919 of 14015 non-empty values are valid), where validity is presence of "@" and denominator = non-empty emails only (trimmed, non-null).
        - How it was calculated: for each attribute, valid_count / applicable_records

    (c) Uniqueness for first_name 
        - 11.61%. Calculated by getting proportion of records whose first_name occurs exactly once among non-missing first names.

    (d) Consistency between age_at_consultation and birth_date (for valid age values)
        - 48.29%. Calculated by parsing consultation date from consultation_timestamp using only the date part before "t" (ignoring timezone). Then compute age in full years on that date from birth_date. Lastly, compare to recorded age_at_consultation for all rows with valid dates and non-negative age where they exactly match.

### 4. Calculate the distributions of the first digits (benford's law) for the attributes (a) cholesterol_level, (b) blood_pressure and (c) medicare_number. 
(a) Cholesterol level (n = 20,000)
Observed %: 1: 63.67, 2: 27.54, 3: 0.86, 4: 0.46, 5: 0.65, 6: 1.00, 7: 1.46, 8: 1.86, 9: 2.50
Benford theory %: 1: 30.10, 2: 17.61, 3: 12.49, 4: 9.69, 5: 7.92, 6: 6.69, 7: 5.80, 8: 5.12, 9: 4.58
| First Digit | Observed Count | Observed % | Benford Theory % | Difference |
|-------------|----------------|------------|------------------|------------|
| 1           | 12,734         | 63.67      | 30.10           | +33.57     |
| 2           | 5,508          | 27.54      | 17.61           | +9.93      |
| 3           | 172            | 0.86       | 12.49           | -11.63     |
| 4           | 92             | 0.46       | 9.69            | -9.23      |
| 5           | 130            | 0.65       | 7.92            | -7.27      |
| 6           | 200            | 1.00       | 6.69            | -5.69      |
| 7           | 292            | 1.46       | 5.80            | -4.34      |
| 8           | 372            | 1.86       | 5.12            | -3.26      |
| 9           | 500            | 2.50       | 4.58            | -2.08      |

Does it follow? No. It is overwhelmingly concentrated on 1 and 2 (far above Benford), likely because cholesterol values are generated within a narrow clinical range that anchors most first digits to 1–2.

(b) Blood pressure (n = 20,000)
Observed %: 1: 0.00, 2: 0.00, 3: 0.00, 4: 0.00, 5: 0.00, 6: 8.71, 7: 78.60, 8: 12.67, 9: 0.02
Does it follow? No. Systolic/diastolic-like values are typically 60–89, so first digits cluster at 7 and 8, violating the logarithmic spread Benford expects.
| First Digit | Observed Count | Observed % | Benford Theory % | Difference |
|-------------|----------------|------------|------------------|------------|
| 1           | 0              | 0.00       | 30.10           | -30.10     |
| 2           | 0              | 0.00       | 17.61           | -17.61     |
| 3           | 0              | 0.00       | 12.49           | -12.49     |
| 4           | 0              | 0.00       | 9.69            | -9.69      |
| 5           | 0              | 0.00       | 7.92            | -7.92      |
| 6           | 1,742          | 8.71       | 6.69            | +2.02      |
| 7           | 15,720         | 78.60      | 5.80            | +72.80     |
| 8           | 2,534          | 12.67      | 5.12            | +7.55      |
| 9           | 4              | 0.02       | 4.58            | -4.56      |


(c) Medicare number (n = 20,000)
Observed %: 1: 11.12, 2: 10.86, 3: 11.08, 4: 11.00, 5: 11.05, 6: 11.00, 7: 11.36, 8: 11.30, 9: 11.25
Does it follow? No. It’s ~uniform across 1–9 (common for assigned identifiers), unlike natural magnitude-spanning processes where Benford applies.
| First Digit | Observed Count | Observed % | Benford Theory % | Difference |
|-------------|----------------|------------|------------------|------------|
| 1           | 2,224          | 11.12      | 30.10           | -18.98     |
| 2           | 2,172          | 10.86      | 17.61           | -6.75      |
| 3           | 2,216          | 11.08      | 12.49           | -1.41      |
| 4           | 2,200          | 11.00      | 9.69            | +1.31      |
| 5           | 2,210          | 11.05      | 7.92            | +3.13      |
| 6           | 2,200          | 11.00      | 6.69            | +4.31      |
| 7           | 2,272          | 11.36      | 5.80            | +5.56      |
| 8           | 2,260          | 11.30      | 5.12            | +6.18      |
| 9           | 2,250          | 11.25      | 4.58            | +6.67      |

### 5. Assume you constructed a data cube representing certain clinical information contained in your generated dataset, where the three dimensions indicate the locations, disease type, and the consultation time. Briefly describe two data warehousing operations you can apply on this data cube, clearly specifying on which dimension the operation is applied, and an example for the result you may obtain.
Roll-up (Time dimension → Year to Decade): aggregate yearly counts to decade level.
Example result: total infectious disease consultations in VIC during the 2010s vs 2020s, enabling trend comparison at a coarser temporal granularity.

Slice (Disease Type dimension): fix Disease Type = “hereditary diseases” to examine a State × Year sub-cube.
Example result: a 2D matrix of hereditary disease consultations by state across years, which you could then rank to find the state with the highest average yearly hereditary disease consultations.




