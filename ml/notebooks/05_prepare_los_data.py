import os
import sys

import pandas as pd


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

sys.path.append(PROJECT_ROOT)


# =========================================================
# DATABASE CONNECTION
# =========================================================

from python.utils.db_connection import get_engine


# =========================================================
# OUTPUT DIRECTORY
# =========================================================

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "ml",
    "outputs"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# =========================================================
# LOAD DATA
# =========================================================

print("\nLoading admission analytics data...")

engine = get_engine()

query = """
SELECT *
FROM vw_admission_analytics
ORDER BY patient_id, admission_date
"""

df = pd.read_sql(
    query,
    engine
)

print(
    f"Loaded {len(df):,} admission records."
)


# =========================================================
# CONVERT DATE COLUMNS
# =========================================================

date_columns = [
    "admission_date",
    "date_of_birth",
    "discharge_date"
]

for column in date_columns:

    df[column] = pd.to_datetime(
        df[column],
        errors="coerce"
    )


# =========================================================
# SORT DATA
# =========================================================

df = df.sort_values(
    by=[
        "patient_id",
        "admission_date"
    ]
).reset_index(
    drop=True
)


# =========================================================
# PREVIOUS ADMISSION FEATURES
# =========================================================

df["previous_admissions"] = (
    df.groupby("patient_id")
      .cumcount()
)


df["previous_admission_date"] = (
    df.groupby("patient_id")[
        "admission_date"
    ].shift(1)
)


df["days_since_previous_admission"] = (
    df["admission_date"]
    - df["previous_admission_date"]
).dt.days


df["days_since_previous_admission"] = (
    df["days_since_previous_admission"]
    .fillna(-1)
)


# =========================================================
# SELECT FEATURES
# =========================================================

features = [

    # Demographics
    "patient_age",
    "gender",
    "city",
    "insurance_type",

    # Admission
    "admission_type",
    "admission_source",
    "department_name",

    # Historical utilization
    "previous_admissions",
    "days_since_previous_admission",

    # Clinical activity
    "diagnosis_count",
    "treatment_count",
    "lab_test_count",
    "abnormal_lab_count",

    # Target
    "length_of_stay"
]


los_df = df[
    features
].copy()


# =========================================================
# REMOVE INVALID TARGETS
# =========================================================

los_df = los_df[
    los_df["length_of_stay"].notna()
].copy()


los_df = los_df[
    los_df["length_of_stay"] > 0
].copy()


# =========================================================
# VALIDATION
# =========================================================

print("\nChecking dataset...")

print(
    f"Final records: {len(los_df):,}"
)


print("\nMissing values:")

print(
    los_df.isnull().sum()
)


print("\nLength-of-stay statistics:")

print(
    los_df["length_of_stay"].describe()
)


# =========================================================
# SAVE DATASET
# =========================================================

output_file = os.path.join(
    OUTPUT_DIR,
    "los_ml_dataset.csv"
)


los_df.to_csv(
    output_file,
    index=False
)


# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n")
print("=" * 60)
print("LENGTH-OF-STAY ML DATASET")
print("=" * 60)


print(
    f"\nTotal records: {len(los_df):,}"
)


print(
    "\nAverage LOS:"
)

print(
    f"{los_df['length_of_stay'].mean():.2f} days"
)


print(
    "\nMinimum LOS:"
)

print(
    f"{los_df['length_of_stay'].min()} days"
)


print(
    "\nMaximum LOS:"
)

print(
    f"{los_df['length_of_stay'].max()} days"
)


print(
    "\nDataset saved to:"
)

print(
    output_file
)


print(
    "\nLength-of-stay dataset preparation completed successfully."
)