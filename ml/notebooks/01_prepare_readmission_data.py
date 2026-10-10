import os
import sys

import numpy as np
import pandas as pd


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

sys.path.append(PROJECT_ROOT)


# =========================================================
# DATABASE CONNECTION
# =========================================================

from python.utils.db_connection import get_engine


# =========================================================
# CONFIGURATION
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
# LOAD DATA FROM MYSQL
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
# BASIC VALIDATION
# =========================================================

print("\nColumns available:")

print(
    df.columns.tolist()
)


print("\nMissing values:")

print(
    df.isnull().sum()
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
# CHECK INVALID ADMISSION DATES
# =========================================================

invalid_admission_dates = df[
    df["admission_date"].isna()
].shape[0]


if invalid_admission_dates > 0:

    raise ValueError(
        f"Found {invalid_admission_dates} invalid "
        "admission dates."
    )


# =========================================================
# SORT DATA CHRONOLOGICALLY
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
# FEATURE ENGINEERING
# =========================================================

print("\nCreating historical admission features...")


# ---------------------------------------------------------
# Number of previous admissions
# ---------------------------------------------------------

df["previous_admissions"] = (
    df.groupby("patient_id")
      .cumcount()
)


# ---------------------------------------------------------
# Previous admission date
# ---------------------------------------------------------

df["previous_admission_date"] = (
    df.groupby("patient_id")[
        "admission_date"
    ].shift(1)
)


# ---------------------------------------------------------
# Days since previous admission
# ---------------------------------------------------------

df["days_since_previous_admission"] = (
    df["admission_date"]
    - df["previous_admission_date"]
).dt.days


# ---------------------------------------------------------
# First admission flag
# ---------------------------------------------------------

df["is_first_admission"] = (
    df["previous_admissions"] == 0
).astype(int)


# ---------------------------------------------------------
# Handle first admissions
# ---------------------------------------------------------

df["days_since_previous_admission"] = (
    df["days_since_previous_admission"]
    .fillna(-1)
)


# =========================================================
# CREATE SYNTHETIC READMISSION TARGET
# =========================================================
#
# IMPORTANT:
#
# This project uses synthetic/de-identified healthcare
# data. The original dataset does not contain a real
# observed 30-day readmission outcome.
#
# Therefore, we create a synthetic target for demonstrating
# the machine-learning workflow.
#
# This model must NOT be described as a clinically validated
# readmission prediction system.
# =========================================================

print("\nCreating synthetic readmission target...")


rng = np.random.default_rng(42)


# ---------------------------------------------------------
# Calculate synthetic risk score
# ---------------------------------------------------------

risk_score = (

    0.30
    * (
        df["previous_admissions"] > 0
    ).astype(int)

    +

    0.20
    * (
        df["previous_admissions"] >= 2
    ).astype(int)

    +

    0.15
    * (
        df["abnormal_lab_count"] >= 2
    ).astype(int)

    +

    0.10
    * (
        df["diagnosis_count"] >= 3
    ).astype(int)

    +

    0.10
    * (
        df["treatment_count"] >= 3
    ).astype(int)

    +

    0.10
    * (
        df["patient_age"] >= 65
    ).astype(int)

    +

    0.05
    * (
        df["admission_type"] == "Emergency"
    ).astype(int)
)


# ---------------------------------------------------------
# Add controlled randomness
# ---------------------------------------------------------

random_component = rng.random(
    len(df)
)


# ---------------------------------------------------------
# Generate target
# ---------------------------------------------------------

df["readmitted_30d"] = (
    random_component < risk_score
).astype(int)


# =========================================================
# SELECT ML FEATURES
# =========================================================

features = [

    # Patient demographics
    "patient_age",
    "gender",
    "city",
    "insurance_type",

    # Admission information
    "admission_type",
    "admission_source",
    "department_name",

    # Patient history
    "previous_admissions",
    "days_since_previous_admission",

    # Clinical indicators
    "diagnosis_count",
    "treatment_count",
    "lab_test_count",
    "abnormal_lab_count",

    # Target
    "readmitted_30d"
]


ml_df = df[
    features
].copy()


# =========================================================
# REMOVE INVALID RECORDS
# =========================================================

ml_df = ml_df[
    ml_df["patient_age"].notna()
].copy()


# =========================================================
# FINAL DATA VALIDATION
# =========================================================

print("\nChecking ML dataset...")

print(
    f"Final records: {len(ml_df):,}"
)


# Check missing values

missing_values = (
    ml_df.isnull().sum()
)


if missing_values.sum() > 0:

    print(
        "\nMissing values detected:"
    )

    print(
        missing_values[
            missing_values > 0
        ]
    )

else:

    print(
        "No missing values found."
    )


# =========================================================
# TARGET VALIDATION
# =========================================================

target_counts = (
    ml_df["readmitted_30d"]
    .value_counts()
    .sort_index()
)


target_percentages = (
    ml_df["readmitted_30d"]
    .value_counts(
        normalize=True
    )
    .sort_index()
    .mul(100)
    .round(2)
)


# =========================================================
# SAVE DATASET
# =========================================================

output_file = os.path.join(
    OUTPUT_DIR,
    "readmission_ml_dataset.csv"
)


ml_df.to_csv(
    output_file,
    index=False
)


# =========================================================
# FINAL REPORT
# =========================================================

print("\n")
print("=" * 60)
print("READMISSION ML DATASET")
print("=" * 60)


print(
    f"\nTotal records: {len(ml_df):,}"
)


print(
    "\nTarget distribution:"
)

print(
    target_counts
)


print(
    "\nTarget percentage:"
)

print(
    target_percentages
)


print(
    "\nFeature columns:"
)

for column in ml_df.columns:

    print(
        f" - {column}"
    )


print(
    "\nData types:"
)

print(
    ml_df.dtypes
)


print(
    "\nDataset saved to:"
)

print(
    output_file
)


print(
    "\nReadmission dataset preparation "
    "completed successfully."
)