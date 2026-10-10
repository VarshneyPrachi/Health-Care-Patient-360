import os

import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sqlalchemy import create_engine


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# ============================================================
# OUTPUT DIRECTORIES
# ============================================================

OUTPUT_DIR = "ml/outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("HEALTHCARE PATIENT 360")
print("PYTHON EXPLORATORY DATA ANALYSIS")
print("=" * 60)


print("\nLoading admission analytics...")

admissions = pd.read_sql(
    "SELECT * FROM vw_admission_analytics",
    engine
)

print(
    f"Loaded {len(admissions):,} admission records."
)


print("\nLoading department performance...")

departments = pd.read_sql(
    "SELECT * FROM vw_department_performance",
    engine
)

print(
    f"Loaded {len(departments):,} departments."
)


print("\nLoading financial analytics...")

financial = pd.read_sql(
    "SELECT * FROM vw_financial_analytics",
    engine
)

print(
    f"Loaded {len(financial):,} billing records."
)


print("\nLoading laboratory analytics...")

labs = pd.read_sql(
    "SELECT * FROM vw_lab_analytics",
    engine
)

print(
    f"Loaded {len(labs):,} laboratory test types."
)


# ============================================================
# BASIC DATA QUALITY
# ============================================================

print("\n" + "=" * 60)
print("DATA QUALITY")
print("=" * 60)

print("\nMissing values:")

missing = admissions.isnull().sum()

missing = missing[
    missing > 0
].sort_values(
    ascending=False
)

print(
    missing if len(missing) > 0
    else "No missing values found."
)


print("\nDuplicate admission IDs:")

duplicates = admissions[
    admissions["admission_id"].duplicated()
]

print(
    f"{len(duplicates):,} duplicate records."
)


# ============================================================
# BASIC STATISTICS
# ============================================================

print("\n" + "=" * 60)
print("KEY STATISTICS")
print("=" * 60)

print("\nPatient age:")

print(
    admissions["patient_age"].describe()
)


print("\nLength of stay:")

print(
    admissions["length_of_stay"].describe()
)


print("\nTotal bill:")

print(
    admissions["total_bill"].describe()
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_admissions = admissions[
    "admission_id"
].nunique()

unique_patients = admissions[
    "patient_id"
].nunique()

avg_los = admissions[
    "length_of_stay"
].mean()

total_revenue = admissions[
    "total_bill"
].sum()

avg_bill = admissions[
    "total_bill"
].mean()

abnormal_lab_rate = (
    admissions["abnormal_lab_count"].sum()
    /
    admissions["lab_test_count"].sum()
    * 100
)

emergency_rate = (
    (
        admissions["admission_type"]
        == "Emergency"
    ).sum()
    /
    total_admissions
    * 100
)


print("\n" + "=" * 60)
print("HOSPITAL KPIs")
print("=" * 60)

print(
    f"Total Admissions       : {total_admissions:,}"
)

print(
    f"Unique Patients        : {unique_patients:,}"
)

print(
    f"Average Length of Stay : {avg_los:.2f} days"
)

print(
    f"Total Hospital Revenue : ₹{total_revenue:,.2f}"
)

print(
    f"Average Bill           : ₹{avg_bill:,.2f}"
)

print(
    f"Abnormal Lab Rate      : {abnormal_lab_rate:.2f}%"
)

print(
    f"Emergency Admission %  : {emergency_rate:.2f}%"
)


# ============================================================
# DEPARTMENT ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("DEPARTMENT ANALYSIS")
print("=" * 60)

department_summary = (
    admissions
    .groupby("department_name")
    .agg(
        admissions=("admission_id", "nunique"),
        patients=("patient_id", "nunique"),
        avg_los=("length_of_stay", "mean"),
        revenue=("total_bill", "sum"),
    )
    .sort_values(
        "admissions",
        ascending=False
    )
)

print(
    department_summary
)


# ============================================================
# DIAGNOSIS / ADMISSION TYPE ANALYSIS
# ============================================================

print("\nAdmission type distribution:")

print(
    admissions[
        "admission_type"
    ].value_counts()
)


print("\nOutcome distribution:")

print(
    admissions[
        "outcome"
    ].value_counts()
)


# ============================================================
# INSURANCE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("INSURANCE ANALYSIS")
print("=" * 60)

insurance_summary = (
    financial
    .groupby("insurance_type")
    .agg(
        bills=("bill_id", "count"),
        revenue=("total_bill", "sum"),
        insurance_paid=(
            "insurance_covered",
            "sum"
        ),
        patient_paid=(
            "patient_paid",
            "sum"
        ),
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)

print(
    insurance_summary
)


# ============================================================
# SAVE ANALYTICAL DATA
# ============================================================

admissions.to_csv(
    f"{OUTPUT_DIR}/admission_analytics.csv",
    index=False
)

departments.to_csv(
    f"{OUTPUT_DIR}/department_performance.csv",
    index=False
)

financial.to_csv(
    f"{OUTPUT_DIR}/financial_analytics.csv",
    index=False
)

labs.to_csv(
    f"{OUTPUT_DIR}/lab_analytics.csv",
    index=False
)


# ============================================================
# CHART 1 — ADMISSIONS BY DEPARTMENT
# ============================================================

plt.figure(figsize=(12, 6))

department_summary[
    "admissions"
].sort_values().plot(
    kind="barh"
)

plt.title(
    "Hospital Admissions by Department"
)

plt.xlabel("Number of Admissions")
plt.ylabel("Department")

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/admissions_by_department.png",
    dpi=200
)

plt.close()


# ============================================================
# CHART 2 — REVENUE BY DEPARTMENT
# ============================================================

plt.figure(figsize=(12, 6))

department_summary[
    "revenue"
].sort_values().plot(
    kind="barh"
)

plt.title(
    "Hospital Revenue by Department"
)

plt.xlabel("Revenue (₹)")
plt.ylabel("Department")

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/revenue_by_department.png",
    dpi=200
)

plt.close()


# ============================================================
# CHART 3 — ADMISSION TYPES
# ============================================================

plt.figure(figsize=(8, 6))

admissions[
    "admission_type"
].value_counts().plot(
    kind="bar"
)

plt.title(
    "Hospital Admissions by Admission Type"
)

plt.xlabel("Admission Type")
plt.ylabel("Number of Admissions")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/admission_types.png",
    dpi=200
)

plt.close()


# ============================================================
# CHART 4 — LENGTH OF STAY
# ============================================================

plt.figure(figsize=(10, 6))

admissions[
    "length_of_stay"
].plot(
    kind="hist",
    bins=20
)

plt.title(
    "Distribution of Patient Length of Stay"
)

plt.xlabel("Length of Stay (Days)")
plt.ylabel("Number of Admissions")

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/length_of_stay_distribution.png",
    dpi=200
)

plt.close()


# ============================================================
# CHART 5 — BILL DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

admissions[
    "total_bill"
].plot(
    kind="hist",
    bins=30
)

plt.title(
    "Distribution of Hospital Bills"
)

plt.xlabel("Total Bill (₹)")
plt.ylabel("Number of Admissions")

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/billing_distribution.png",
    dpi=200
)

plt.close()


print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 60)

print(
    f"\nOutput files saved to: {OUTPUT_DIR}/"
)

print("\nGenerated files:")

for file in sorted(
    os.listdir(OUTPUT_DIR)
):
    print(f"  - {file}")