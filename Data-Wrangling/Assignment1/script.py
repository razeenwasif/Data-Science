import numpy as np 
import pandas as pd
import json

# Load dataset 
file_path = "./data/data_wrangling_medical_2025_u7283652.csv"
df = pd.read_csv(file_path)

# Helper: rounder
rnd = lambda x: float(np.round(x, 2))

# Inspect dataset
print(df.head())
df.info()

# Select relevant columns
missingness_df = df[['postcode', 'phone', 'email']].copy()

# Create 0-1 missingness pattern (1=present, 0=missing)
pattern_df = missingness_df.notnull().astype(int)

# Count frequency of each unique missingness pattern
pattern_summary = pattern_df.value_counts().reset_index(name='count')

print("Missingness Pattern Table:"'\n', pattern_summary)

# -------------------------
# Q2: Correlations
# -------------------------
print("\n" + "="*50)
print("Q2: Correlations")
print("="*50)

# (a) BMI vs age_at_consultation (numeric-numeric): Pearson correlation
bmi_age_corr = df[['bmi', 'age_at_consultation']].dropna()
corr_bmi_age = bmi_age_corr['bmi'].corr(bmi_age_corr['age_at_consultation'], method='pearson')
print(f"Pearson Correlation (BMI vs Age): {rnd(corr_bmi_age)}")

# (b) state vs "valid marital status": use Cramér's V for categorical-categorical
# Define valid marital statuses by inspecting existing distinct values (lowercased, stripped).
marital_unique = df['marital_status'].astype(str).str.strip().str.lower().unique().tolist()

# Define a conservative valid set (common statuses)
valid_status_set = {
    'single', 'married', 'divorced', 'widowed', 'separated', 'de facto', 'defacto', 'married-de-facto',
    'in relationship', 'engaged', 'never married', 'not-married', 'civil union', 'partnered', 'not married'
}

# Flag valid marital status (non-empty and in valid set)
marital_norm = df['marital_status'].astype(str).str.strip().str.lower().replace({'': np.nan})
is_valid_marital = marital_norm.isin(valid_status_set)

# Build contingency table only for rows with valid marital status and non-missing state
state_valid = df.loc[is_valid_marital & df['state'].notna(), ['state', 'marital_status']].copy()
state_valid['state'] = state_valid['state'].astype(str).str.strip().str.upper()
state_valid['marital_status'] = state_valid['marital_status'].astype(str).str.strip().str.lower()

ct = pd.crosstab(state_valid['state'], state_valid['marital_status'])

# Compute chi-squared statistic manually
observed = ct.values
n = observed.sum()
row_sums = observed.sum(axis=1, keepdims=True)
col_sums = observed.sum(axis=0, keepdims=True)
expected = row_sums @ col_sums / n

# Avoid divisions by zero in chi2 where expected == 0
with np.errstate(divide='ignore', invalid='ignore'):
    chi2 = np.nansum((observed - expected) ** 2 / np.where(expected == 0, np.nan, expected))

k = min(observed.shape[0] - 1, observed.shape[1] - 1)
cramers_v = np.sqrt(chi2 / (n * k)) if k > 0 else np.nan
print(f"Cramér's V (State vs Valid Marital Status): {rnd(cramers_v)}")

# -------------------------
# Q3: Data Quality Dimensions
# -------------------------
print("\n" + "="*50)
print("Q3: Data Quality Dimensions")
print("="*50)
# (a) Completeness: proportion of non-missing values
def completeness(series):
    return series.notna().mean() * 100

comp_middle_name = completeness(df['middle_name'])
comp_email = completeness(df['email'])
print(f"Completeness - middle_name: {rnd(comp_middle_name)}%")
print(f"Completeness - email: {rnd(comp_email)}%")

# (b) Validity:
# - weight valid: assume plausible adult human weights in kg [30, 300]; consider non-missing weights
def validity_weight(series):
    non_missing = series.dropna()
    valid = non_missing.between(30, 300, inclusive='both')
    return (valid.mean() * 100, int(valid.sum()), int(non_missing.shape[0]))

weight_valid_pct, weight_valid_n, weight_nonmiss_n = validity_weight(df['weight'])
print(f"\nValidity - weight: {rnd(weight_valid_pct)}% ({weight_valid_n} of {weight_nonmiss_n} non-missing values are valid)")

# - email valid: contains '@'; only consider non-empty (non-null and non-empty string) emails
email_series = df['email'].astype(str)
non_empty_email_mask = email_series.str.strip().ne('') & df['email'].notna()
emails_non_empty = email_series[non_empty_email_mask]
valid_email_mask = emails_non_empty.str.contains('@', regex=False)
email_valid_pct = valid_email_mask.mean() * 100
email_valid_n = int(valid_email_mask.sum())
email_nonempty_n = int(emails_non_empty.shape[0])
print(f"Validity - email: {rnd(email_valid_pct)}% ({email_valid_n} of {email_nonempty_n} non-empty values are valid)")

# (c) Uniqueness for first name: fraction of records with a unique first_name among non-missing
first_nonmiss = df['first_name'].dropna().astype(str).str.strip()
first_counts = first_nonmiss.value_counts()
unique_records = first_counts[first_counts == 1].sum()
uniq_firstname_pct = (unique_records / first_nonmiss.shape[0]) * 100
print(f"\nUniqueness - first_name: {rnd(uniq_firstname_pct)}%")

# (d) Consistency between age_at_consultation and birth_date for valid age values
# Parse dates; use only date part of consultation_timestamp (ignore time/timezone completely)
birth = pd.to_datetime(df['birth_date'], errors='coerce').dt.date

# Keep only the date portion before 't' if present
consult_date_str = df['consultation_timestamp'].astype(str).str.split('t', n=1, expand=True)[0]
consult_date = pd.to_datetime(consult_date_str, errors='coerce').dt.date

# Compute age in years at consultation: floor difference in days / 365.2425
# (Use exact year calculation based on months/days by comparing month/day to account for birthdays)
def calc_age_on( birth_dates, consult_dates):
    b = pd.to_datetime(pd.Series(birth_dates), errors='coerce')
    c = pd.to_datetime(pd.Series(consult_dates), errors='coerce')
    years = c.dt.year - b.dt.year
    before_bday = ( (c.dt.month < b.dt.month) | ((c.dt.month == b.dt.month) & (c.dt.day < b.dt.day)) )
    years_adjusted = years - before_bday.astype(int)
    return years_adjusted

computed_age = calc_age_on(birth, consult_date)

# Valid ages: non-negative integers
age_valid_mask = df['age_at_consultation'].notna() & (df['age_at_consultation'] >= 0)
# Rows with both dates valid
dates_valid_mask = pd.to_datetime(pd.Series(birth), errors='coerce').notna() & pd.to_datetime(pd.Series(consult_date), errors='coerce').notna()

consistency_mask_domain = age_valid_mask & dates_valid_mask

computed_age_filtered = computed_age[consistency_mask_domain]
reported_age_filtered = df.loc[consistency_mask_domain, 'age_at_consultation']

# Now, ensure they are compared element-wise by value after aligning
# (or if they are already series from a common filtered index, this is fine)
# If computed_age has a different index, reset both:
consistency_equals = (computed_age_filtered.reset_index(drop=True) == reported_age_filtered.reset_index(drop=True))

consistency_pct = consistency_equals.mean() * 100 if consistency_mask_domain.any() else np.nan
consistency_n = int(consistency_equals.sum()) if consistency_mask_domain.any() else 0
consistency_den = int(consistency_equals.shape[0]) if consistency_mask_domain.any() else 0
print(f"\nConsistency - age vs birth_date: {rnd(consistency_pct)}% ({consistency_n} of {consistency_den} records are consistent)")

# -------------------------
# Q4: Benford first digit distributions
# -------------------------
print("\n" + "="*50)
print("Q4: Benford's Law Analysis")
print("="*50)

def first_digit_series(series):
    # extract first non-zero digit from absolute value (numbers only)
    s = pd.to_numeric(series, errors='coerce').dropna().astype(float).abs()
    # remove zeros
    s = s[s != 0]
    # first digit
    digits = s.astype(str).str.replace('.', '', regex=False).str.replace('e+', 'e', regex=False)
    # Use string conversion robustly by iterating numeric approach
    def first_digit(x):
        x = abs(x)
        while x >= 10:
            x //= 10
        while 0 < x < 1:
            x *= 10
        return int(str(int(x))[0])
    return s.apply(first_digit)

def benford_distribution(digits):
    counts = digits.value_counts().reindex(range(1,10), fill_value=0)
    total = counts.sum()
    pct = (counts / total * 100).round(2) if total > 0 else counts.astype(float)
    return counts, total, pct

digits_chol = first_digit_series(df['cholesterol_level'])
digits_bp = first_digit_series(df['blood_pressure'])
digits_medicare = first_digit_series(df['medicare_number'])

counts_chol, total_chol, pct_chol = benford_distribution(digits_chol)
counts_bp, total_bp, pct_bp = benford_distribution(digits_bp)
counts_medicare, total_medicare, pct_medicare = benford_distribution(digits_medicare)

# Benford theoretical distribution
benford_theory = pd.Series({d: 100 * np.log10(1 + 1/d) for d in range(1,10)}).round(2)

print("--- Cholesterol Level First Digit Distribution (%):")
print(pct_chol)
print("\n--- Blood Pressure First Digit Distribution (%):")
print(pct_bp)
print("\n--- Medicare Number First Digit Distribution (%):")
print(pct_medicare)
print("\n--- Benford's Law Theoretical Distribution (%):")
print(benford_theory)

# -------------------------
# Prepare final outputs
# -------------------------

# Prepare outputs (rounded where appropriate)
outputs = {
    "Q2": {
        "BMI_vs_Age": {"method": "Pearson correlation", "value": rnd(corr_bmi_age)},
        "State_vs_ValidMaritalStatus": {"method": "Cramér's V", "value": rnd(cramers_v), "n_pairs": int(n)}
    },
    "Q3": {
        "Completeness": {
            "middle_name_pct": rnd(comp_middle_name),
            "email_pct": rnd(comp_email)
        },
        "Validity": {
            "weight_pct": rnd(weight_valid_pct),
            "weight_counts": {"valid": weight_valid_n, "non_missing": weight_nonmiss_n},
            "email_pct": rnd(email_valid_pct),
            "email_counts": {"valid": email_valid_n, "non_empty": email_nonempty_n}
        },
        "Uniqueness": {
            "first_name_pct": rnd(uniq_firstname_pct)
        },
        "Consistency": {
            "age_vs_birthdate_pct": rnd(consistency_pct) if not np.isnan(consistency_pct) else None,
            "counts": {"consistent": consistency_n, "evaluated": consistency_den}
        }
    },
    "Q4": {
        "Benford": {
            "cholesterol": {"counts": counts_chol.to_dict(), "pct": pct_chol.to_dict(), "n": int(total_chol)},
            "blood_pressure": {"counts": counts_bp.to_dict(), "pct": pct_bp.to_dict(), "n": int(total_bp)},
            "medicare_number": {"counts": counts_medicare.to_dict(), "pct": pct_medicare.to_dict(), "n": int(total_medicare)},
            "theory_pct": benford_theory.to_dict()
        }
    },
    "Q2_helper": {
        "marital_unique_sample": marital_unique[:20]
    }
}
# --- Final Print of All Results ---
print("\n\n" + "="*50)
print("FINAL OUTPUTS DICTIONARY")
print("="*50)
# Use json.dumps for a readable, indented print of the nested dictionary
print(json.dumps(outputs, indent=2))
