import os
import sys
import pandas as pd

from sqlalchemy import text
from sqlalchemy.types import (
    VARCHAR,
    Integer,
    DECIMAL,
    Date
)


# --------------------------------------------------
# Add project root to Python path
# --------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

sys.path.insert(0, PROJECT_ROOT)


# --------------------------------------------------
# Import database connection
# --------------------------------------------------

from python.utils.db_connection import get_engine


# --------------------------------------------------
# CSV path
# --------------------------------------------------

CSV_PATH = os.path.join(
    PROJECT_ROOT,
    "ml",
    "outputs",
    "ml_patient_360.csv"
)


# --------------------------------------------------
# Check CSV
# --------------------------------------------------

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(
        f"ML Patient 360 file not found:\n{CSV_PATH}"
    )

print("Loading ML Patient 360 dataset...")

df = pd.read_csv(CSV_PATH)

print(f"Rows loaded: {len(df)}")
print(f"Columns loaded: {len(df.columns)}")


# --------------------------------------------------
# Convert data types
# --------------------------------------------------

# Dates
if "admission_date" in df.columns:
    df["admission_date"] = pd.to_datetime(
        df["admission_date"],
        errors="coerce"
    ).dt.date


# ID columns
df["patient_id"] = df["patient_id"].astype(str)
df["admission_id"] = df["admission_id"].astype(str)


# --------------------------------------------------
# Connect to MySQL
# --------------------------------------------------

engine = get_engine()

print("Connected to MySQL successfully.")


# --------------------------------------------------
# Define MySQL column types
# --------------------------------------------------

dtype_map = {

    # IDs
    "patient_id": VARCHAR(20),
    "admission_id": VARCHAR(20),

    # Text
    "gender": VARCHAR(20),
    "city": VARCHAR(100),
    "insurance_type": VARCHAR(50),
    "admission_type": VARCHAR(50),
    "admission_source": VARCHAR(100),
    "department_name": VARCHAR(100),
    "risk_category": VARCHAR(20),
    "doctor_name": VARCHAR(100),
    "outcome": VARCHAR(100),
    "predicted_los_category": VARCHAR(30),

    # Integer
    "patient_age": Integer(),
    "previous_admissions": Integer(),
    "days_since_previous_admission": Integer(),
    "diagnosis_count": Integer(),
    "treatment_count": Integer(),
    "lab_test_count": Integer(),
    "abnormal_lab_count": Integer(),
    "length_of_stay": Integer(),

    # Decimal
    "readmission_probability": DECIMAL(8, 5),
    "readmission_probability_pct": DECIMAL(6, 2),
    "total_bill": DECIMAL(12, 2),
    "insurance_covered": DECIMAL(12, 2),
    "patient_paid": DECIMAL(12, 2),
    "predicted_length_of_stay": DECIMAL(8, 2),
    "prediction_error_days": DECIMAL(8, 2),
    "absolute_prediction_error_days": DECIMAL(8, 2),

    # Date
    "admission_date": Date()
}


# --------------------------------------------------
# Remove old table if it exists
# --------------------------------------------------

print("Removing old ml_patient_360 table if it exists...")

with engine.begin() as connection:
    connection.execute(
        text("DROP TABLE IF EXISTS ml_patient_360")
    )


# --------------------------------------------------
# Load data into MySQL
# --------------------------------------------------

print("Loading data into ml_patient_360 table...")

df.to_sql(
    "ml_patient_360",
    con=engine,
    if_exists="replace",
    index=False,
    dtype=dtype_map,
    chunksize=1000,
    method="multi"
)

print("Data successfully loaded into MySQL.")


# --------------------------------------------------
# Add primary key and indexes
# --------------------------------------------------

print("Creating indexes...")

with engine.begin() as connection:

    connection.execute(text("""
        ALTER TABLE ml_patient_360
        ADD PRIMARY KEY (patient_id)
    """))

    connection.execute(text("""
        CREATE INDEX idx_ml_admission
        ON ml_patient_360 (admission_id)
    """))

    connection.execute(text("""
        CREATE INDEX idx_ml_risk
        ON ml_patient_360 (risk_category)
    """))

    connection.execute(text("""
        CREATE INDEX idx_ml_department
        ON ml_patient_360 (department_name)
    """))

print("Indexes created successfully.")


# --------------------------------------------------
# Verify
# --------------------------------------------------

with engine.connect() as connection:

    count = connection.execute(
        text("SELECT COUNT(*) FROM ml_patient_360")
    ).scalar()

print()
print("=" * 50)
print("ML PATIENT 360 LOAD COMPLETE")
print("=" * 50)
print(f"Rows in MySQL: {count}")
print("=" * 50)