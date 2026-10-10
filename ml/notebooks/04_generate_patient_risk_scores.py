import os
import sys

import joblib
import pandas as pd
import numpy as np


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
# DIRECTORIES
# =========================================================

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "ml",
    "outputs"
)

MODEL_DIR = os.path.join(
    PROJECT_ROOT,
    "ml",
    "models"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# =========================================================
# LOAD DATA
# =========================================================

print("\nLoading admission dataset...")

input_file = os.path.join(
    OUTPUT_DIR,
    "readmission_ml_dataset.csv"
)

df = pd.read_csv(
    input_file
)

print(
    f"Loaded {len(df):,} admission records."
)


# =========================================================
# LOAD RANDOM FOREST MODEL
# =========================================================

print("\nLoading Random Forest model...")

model_file = os.path.join(
    MODEL_DIR,
    "random_forest.joblib"
)

model = joblib.load(
    model_file
)

print(
    "Random Forest model loaded successfully."
)


# =========================================================
# PREPARE FEATURES
# =========================================================

TARGET = "readmitted_30d"

X = df.drop(
    columns=[TARGET]
)


# =========================================================
# GENERATE READMISSION PROBABILITY
# =========================================================

print(
    "\nGenerating readmission probabilities..."
)


probabilities = model.predict_proba(
    X
)[:, 1]


df["readmission_probability"] = (
    probabilities
)


# =========================================================
# CONVERT PROBABILITY TO PERCENTAGE
# =========================================================

df["readmission_probability_pct"] = (
    df["readmission_probability"] * 100
).round(2)


# =========================================================
# CREATE RISK CATEGORY
# =========================================================
#
# These thresholds are project/demo thresholds.
# They are NOT clinically validated thresholds.
# =========================================================

def assign_risk_category(probability):

    if probability < 0.30:

        return "Low"

    elif probability < 0.60:

        return "Medium"

    else:

        return "High"


df["risk_category"] = (
    df["readmission_probability"]
    .apply(assign_risk_category)
)


# =========================================================
# CREATE PATIENT-LEVEL SUMMARY
# =========================================================
#
# A patient can have multiple admissions.
#
# For the Patient 360 dashboard we want one row per patient.
#
# We use the most recent admission for the current risk
# snapshot.
# =========================================================


# ---------------------------------------------------------
# Load original admission information
# ---------------------------------------------------------

print(
    "\nLoading admission details..."
)


from python.utils.db_connection import get_engine


engine = get_engine()


query = """
SELECT
    admission_id,
    patient_id,
    admission_date,
    doctor_name,
    department_name,
    outcome,
    length_of_stay,
    total_bill,
    insurance_covered,
    patient_paid
FROM vw_admission_analytics
"""

admission_details = pd.read_sql(
    query,
    engine
)


# ---------------------------------------------------------
# Convert admission date
# ---------------------------------------------------------

admission_details["admission_date"] = (
    pd.to_datetime(
        admission_details["admission_date"],
        errors="coerce"
    )
)


# =========================================================
# MERGE ML RESULTS WITH ADMISSION DETAILS
# =========================================================

# The ML dataset currently doesn't contain admission_id,
# so we align records by their original ordering through
# a fresh query using the same patient/date ordering.

print(
    "\nPreparing patient risk dataset..."
)


query_full = """
SELECT
    admission_id,
    patient_id,
    admission_date
FROM vw_admission_analytics
ORDER BY patient_id, admission_date
"""

admission_keys = pd.read_sql(
    query_full,
    engine
)


admission_keys["admission_date"] = (
    pd.to_datetime(
        admission_keys["admission_date"],
        errors="coerce"
    )
)


# The ML preparation script used exactly this ordering.
# Therefore, the row count and ordering should match.

if len(admission_keys) != len(df):

    raise ValueError(
        "Admission key count does not match ML dataset."
    )


df.insert(
    0,
    "admission_id",
    admission_keys["admission_id"].values
)

df.insert(
    1,
    "patient_id",
    admission_keys["patient_id"].values
)

df.insert(
    2,
    "admission_date",
    admission_keys["admission_date"].values
)


# =========================================================
# MERGE ADDITIONAL ADMISSION INFORMATION
# =========================================================

df = df.merge(
    admission_details,
    on=[
        "admission_id",
        "patient_id",
        "admission_date"
    ],
    how="left",
    suffixes=(
        "",
        "_detail"
    )
)


# =========================================================
# SORT BY PATIENT AND DATE
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
# GET MOST RECENT ADMISSION PER PATIENT
# =========================================================

patient_risk = (
    df
    .groupby(
        "patient_id",
        as_index=False
    )
    .tail(1)
    .copy()
)


# =========================================================
# SELECT PATIENT 360 RISK COLUMNS
# =========================================================

patient_risk = patient_risk[
    [
        "patient_id",
        "admission_id",
        "admission_date",

        "patient_age",
        "gender",
        "city",
        "insurance_type",

        "admission_type",
        "admission_source",
        "department_name",

        "previous_admissions",
        "days_since_previous_admission",

        "diagnosis_count",
        "treatment_count",
        "lab_test_count",
        "abnormal_lab_count",

        "readmission_probability",
        "readmission_probability_pct",
        "risk_category",

        "doctor_name",
        "outcome",
        "length_of_stay",

        "total_bill",
        "insurance_covered",
        "patient_paid"
    ]
].copy()


# =========================================================
# SAVE ADMISSION-LEVEL RISK DATASET
# =========================================================

admission_output = os.path.join(
    OUTPUT_DIR,
    "admission_risk_scores.csv"
)


df.to_csv(
    admission_output,
    index=False
)


# =========================================================
# SAVE PATIENT-LEVEL RISK DATASET
# =========================================================

patient_output = os.path.join(
    OUTPUT_DIR,
    "patient_risk_scores.csv"
)


patient_risk.to_csv(
    patient_output,
    index=False
)


# =========================================================
# DISPLAY RISK DISTRIBUTION
# =========================================================

print("\n")
print("=" * 60)
print("PATIENT RISK DISTRIBUTION")
print("=" * 60)


print(
    patient_risk[
        "risk_category"
    ].value_counts()
)


print("\nRisk percentages:")


print(
    patient_risk[
        "risk_category"
    ]
    .value_counts(
        normalize=True
    )
    .mul(100)
    .round(2)
)


# =========================================================
# DISPLAY HIGH-RISK PATIENTS
# =========================================================

print("\n")
print("=" * 60)
print("SAMPLE HIGH-RISK PATIENTS")
print("=" * 60)


high_risk = (
    patient_risk[
        patient_risk["risk_category"] == "High"
    ]
    .sort_values(
        "readmission_probability",
        ascending=False
    )
    .head(10)
)


display_columns = [
    "patient_id",
    "patient_age",
    "previous_admissions",
    "abnormal_lab_count",
    "diagnosis_count",
    "treatment_count",
    "readmission_probability_pct",
    "risk_category"
]


print(
    high_risk[
        display_columns
    ].to_string(
        index=False
    )
)


# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n")
print("=" * 60)
print("PATIENT RISK SCORING COMPLETED")
print("=" * 60)


print(
    "\nAdmission-level risk file:"
)

print(
    admission_output
)


print(
    "\nPatient-level risk file:"
)

print(
    patient_output
)


print(
    "\nTotal unique patients:"
)

print(
    f"{len(patient_risk):,}"
)


print(
    "\nPatient risk scoring completed successfully."
)