import os
import sys

import joblib
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

MODEL_DIR = os.path.join(
    PROJECT_ROOT,
    "ml",
    "models"
)


# =========================================================
# DATABASE CONNECTION
# =========================================================

from python.utils.db_connection import get_engine


# =========================================================
# LOAD LOS DATASET
# =========================================================

print("\nLoading LOS ML dataset...")

los_file = os.path.join(
    OUTPUT_DIR,
    "los_ml_dataset.csv"
)

los_df = pd.read_csv(
    los_file
)

print(
    f"Loaded {len(los_df):,} records."
)


# =========================================================
# LOAD LINEAR REGRESSION MODEL
# =========================================================

print(
    "\nLoading Linear Regression LOS model..."
)

model_file = os.path.join(
    MODEL_DIR,
    "linear_regression_los.joblib"
)

los_model = joblib.load(
    model_file
)

print(
    "LOS model loaded successfully."
)


# =========================================================
# PREPARE FEATURES
# =========================================================

TARGET = "length_of_stay"

X = los_df.drop(
    columns=[TARGET]
)


# =========================================================
# GENERATE PREDICTIONS
# =========================================================

print(
    "\nGenerating LOS predictions..."
)

predicted_los = los_model.predict(
    X
)


# =========================================================
# CLEAN PREDICTIONS
# =========================================================

los_df[
    "predicted_length_of_stay"
] = predicted_los.round(2)


# LOS cannot realistically be below one day
los_df[
    "predicted_length_of_stay"
] = (
    los_df[
        "predicted_length_of_stay"
    ]
    .clip(lower=1)
)


# =========================================================
# LOAD ADMISSION IDENTIFIERS
# =========================================================

print(
    "\nLoading admission identifiers..."
)

engine = get_engine()

query = """
SELECT
    admission_id,
    patient_id,
    admission_date
FROM vw_admission_analytics
ORDER BY patient_id, admission_date
"""

admission_keys = pd.read_sql(
    query,
    engine
)


admission_keys[
    "admission_date"
] = pd.to_datetime(
    admission_keys[
        "admission_date"
    ],
    errors="coerce"
)


# =========================================================
# VALIDATE RECORD COUNTS
# =========================================================

if len(admission_keys) != len(los_df):

    raise ValueError(
        "Admission key count does not match LOS dataset."
    )


# =========================================================
# ADD IDENTIFIERS
# =========================================================

los_df.insert(
    0,
    "admission_id",
    admission_keys[
        "admission_id"
    ].values
)

los_df.insert(
    1,
    "patient_id",
    admission_keys[
        "patient_id"
    ].values
)

los_df.insert(
    2,
    "admission_date",
    admission_keys[
        "admission_date"
    ].values
)


# =========================================================
# CALCULATE PREDICTION ERROR
# =========================================================

los_df[
    "prediction_error_days"
] = (
    los_df[
        "predicted_length_of_stay"
    ]
    - los_df[
        "length_of_stay"
    ]
).round(2)


los_df[
    "absolute_prediction_error_days"
] = (
    los_df[
        "prediction_error_days"
    ]
    .abs()
    .round(2)
)


# =========================================================
# CREATE LOS CATEGORY
# =========================================================

def categorize_los(days):

    if days <= 3:
        return "Short Stay"

    elif days <= 7:
        return "Medium Stay"

    else:
        return "Long Stay"


los_df[
    "predicted_los_category"
] = (
    los_df[
        "predicted_length_of_stay"
    ]
    .apply(categorize_los)
)


# =========================================================
# SAVE PREDICTIONS
# =========================================================

output_file = os.path.join(
    OUTPUT_DIR,
    "los_predictions.csv"
)

los_df.to_csv(
    output_file,
    index=False
)


# =========================================================
# DISPLAY SUMMARY
# =========================================================

print("\n")
print("=" * 60)
print("LOS PREDICTION SUMMARY")
print("=" * 60)


print(
    f"\nTotal admissions: {len(los_df):,}"
)


print(
    "\nActual average LOS:"
)

print(
    f"{los_df['length_of_stay'].mean():.2f} days"
)


print(
    "\nPredicted average LOS:"
)

print(
    f"{los_df['predicted_length_of_stay'].mean():.2f} days"
)


print(
    "\nAverage absolute prediction error:"
)

print(
    f"{los_df['absolute_prediction_error_days'].mean():.2f} days"
)


print(
    "\nPredicted LOS categories:"
)

print(
    los_df[
        "predicted_los_category"
    ]
    .value_counts()
)


# =========================================================
# SAMPLE PREDICTIONS
# =========================================================

print("\n")
print("=" * 60)
print("SAMPLE LOS PREDICTIONS")
print("=" * 60)


sample_columns = [
    "admission_id",
    "patient_id",
    "patient_age",
    "admission_type",
    "department_name",
    "length_of_stay",
    "predicted_length_of_stay",
    "absolute_prediction_error_days",
    "predicted_los_category"
]


print(
    los_df[
        sample_columns
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
print("LOS PREDICTION GENERATION COMPLETED")
print("=" * 60)


print(
    "\nPrediction file:"
)

print(
    output_file
)


print(
    "\nLOS prediction pipeline completed successfully."
)