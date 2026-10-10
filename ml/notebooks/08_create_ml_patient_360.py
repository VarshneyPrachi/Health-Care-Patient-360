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
# DIRECTORIES
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
# LOAD PATIENT RISK DATA
# =========================================================

print("\nLoading patient risk data...")

risk_file = os.path.join(
    OUTPUT_DIR,
    "patient_risk_scores.csv"
)

risk_df = pd.read_csv(
    risk_file
)

print(
    f"Loaded {len(risk_df):,} patient risk records."
)


# =========================================================
# LOAD LOS PREDICTIONS
# =========================================================

print("\nLoading LOS predictions...")

los_file = os.path.join(
    OUTPUT_DIR,
    "los_predictions.csv"
)

los_df = pd.read_csv(
    los_file
)

print(
    f"Loaded {len(los_df):,} LOS prediction records."
)


# =========================================================
# CONVERT DATES
# =========================================================

risk_df["admission_date"] = pd.to_datetime(
    risk_df["admission_date"],
    errors="coerce"
)

los_df["admission_date"] = pd.to_datetime(
    los_df["admission_date"],
    errors="coerce"
)


# =========================================================
# KEEP ONLY REQUIRED LOS COLUMNS
# =========================================================

los_columns = [
    "admission_id",
    "patient_id",
    "predicted_length_of_stay",
    "prediction_error_days",
    "absolute_prediction_error_days",
    "predicted_los_category"
]


los_subset = los_df[
    los_columns
].copy()


# =========================================================
# MERGE RISK + LOS
# =========================================================

print(
    "\nCombining ML outputs..."
)


ml_patient_360 = risk_df.merge(
    los_subset,
    on=[
        "admission_id",
        "patient_id"
    ],
    how="left"
)


# =========================================================
# VALIDATION
# =========================================================

print(
    "\nValidating merged dataset..."
)


print(
    f"Total records: {len(ml_patient_360):,}"
)


missing_los = (
    ml_patient_360[
        "predicted_length_of_stay"
    ]
    .isna()
    .sum()
)


print(
    f"Records missing LOS prediction: {missing_los:,}"
)


# =========================================================
# REMOVE DUPLICATES
# =========================================================

duplicates = (
    ml_patient_360[
        "patient_id"
    ]
    .duplicated()
    .sum()
)


print(
    f"Duplicate patient records: {duplicates:,}"
)


# =========================================================
# SORT
# =========================================================

ml_patient_360 = ml_patient_360.sort_values(
    by=[
        "readmission_probability",
        "patient_id"
    ],
    ascending=[
        False,
        True
    ]
).reset_index(
    drop=True
)


# =========================================================
# ROUND NUMERIC COLUMNS
# =========================================================

numeric_columns = [
    "readmission_probability",
    "readmission_probability_pct",
    "predicted_length_of_stay",
    "prediction_error_days",
    "absolute_prediction_error_days"
]


for column in numeric_columns:

    if column in ml_patient_360.columns:

        ml_patient_360[column] = (
            ml_patient_360[column]
            .round(2)
        )


# =========================================================
# SAVE FINAL DATASET
# =========================================================

output_file = os.path.join(
    OUTPUT_DIR,
    "ml_patient_360.csv"
)


ml_patient_360.to_csv(
    output_file,
    index=False
)


# =========================================================
# SUMMARY
# =========================================================

print("\n")
print("=" * 60)
print("ML PATIENT 360 DATASET")
print("=" * 60)


print(
    f"\nTotal patients: "
    f"{len(ml_patient_360):,}"
)


print(
    "\nRisk distribution:"
)

print(
    ml_patient_360[
        "risk_category"
    ].value_counts()
)


print(
    "\nPredicted LOS distribution:"
)

print(
    ml_patient_360[
        "predicted_los_category"
    ].value_counts()
)


print(
    "\nAverage readmission probability:"
)

print(
    f"{ml_patient_360['readmission_probability_pct'].mean():.2f}%"
)


print(
    "\nAverage predicted LOS:"
)

print(
    f"{ml_patient_360['predicted_length_of_stay'].mean():.2f} days"
)


# =========================================================
# DISPLAY SAMPLE
# =========================================================

print("\n")
print("=" * 60)
print("SAMPLE ML PATIENT 360 RECORDS")
print("=" * 60)


display_columns = [
    "patient_id",
    "patient_age",
    "gender",
    "insurance_type",
    "department_name",
    "previous_admissions",
    "abnormal_lab_count",
    "readmission_probability_pct",
    "risk_category",
    "length_of_stay",
    "predicted_length_of_stay",
    "predicted_los_category"
]


print(
    ml_patient_360[
        display_columns
    ]
    .head(10)
    .to_string(
        index=False
    )
)


# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n")
print("=" * 60)
print("ML PATIENT 360 CREATION COMPLETED")
print("=" * 60)


print(
    "\nFinal dataset:"
)

print(
    output_file
)


print(
    "\nML Patient 360 dataset completed successfully."
)