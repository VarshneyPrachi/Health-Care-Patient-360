import os
import random
from datetime import date, timedelta

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

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

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Reproducible synthetic data
random.seed(42)

# Final dataset size
NUM_DOCTORS = 40
NUM_PATIENTS = 5000
MIN_ADMISSIONS = 1
MAX_ADMISSIONS = 4

START_DATE = date(2021, 1, 1)
END_DATE = date(2026, 8, 31)


# ============================================================
# MASTER DATA
# ============================================================

DEPARTMENTS = [
    ("Cardiology", 1, 60),
    ("Neurology", 2, 45),
    ("Orthopedics", 3, 70),
    ("Pediatrics", 4, 55),
    ("Oncology", 5, 50),
    ("Gastroenterology", 6, 45),
    ("Pulmonology", 7, 50),
    ("General Medicine", 8, 80),
    ("General Surgery", 9, 65),
    ("Emergency", 10, 40),
    ("ICU", 11, 30),
    ("Nephrology", 12, 40),
]

SPECIALIZATIONS = {
    "Cardiology": [
        "Interventional Cardiology",
        "Cardiac Electrophysiology",
        "Clinical Cardiology",
    ],
    "Neurology": [
        "Clinical Neurology",
        "Neurocritical Care",
        "Stroke Medicine",
    ],
    "Orthopedics": [
        "Joint Replacement",
        "Sports Medicine",
        "Trauma Orthopedics",
    ],
    "Pediatrics": [
        "General Pediatrics",
        "Neonatology",
        "Pediatric Medicine",
    ],
    "Oncology": [
        "Medical Oncology",
        "Radiation Oncology",
        "Surgical Oncology",
    ],
    "Gastroenterology": [
        "Clinical Gastroenterology",
        "Hepatology",
        "Endoscopy",
    ],
    "Pulmonology": [
        "Respiratory Medicine",
        "Critical Care",
        "Sleep Medicine",
    ],
    "General Medicine": [
        "Internal Medicine",
        "Family Medicine",
        "Preventive Medicine",
    ],
    "General Surgery": [
        "General Surgery",
        "Laparoscopic Surgery",
        "Trauma Surgery",
    ],
    "Emergency": [
        "Emergency Medicine",
        "Trauma Medicine",
        "Acute Care",
    ],
    "ICU": [
        "Critical Care Medicine",
        "Intensive Care",
        "Emergency Critical Care",
    ],
    "Nephrology": [
        "Clinical Nephrology",
        "Renal Medicine",
        "Dialysis Medicine",
    ],
}

FIRST_NAMES_MALE = [
    "Aarav", "Aditya", "Arjun", "Aryan", "Dev", "Dhruv",
    "Karan", "Krishna", "Manav", "Mohit", "Nikhil", "Rahul",
    "Rohan", "Rohit", "Sahil", "Sameer", "Varun", "Vivek",
    "Yash", "Ankit", "Abhishek", "Aman", "Raj", "Harsh",
]

FIRST_NAMES_FEMALE = [
    "Aanya", "Ananya", "Anika", "Diya", "Isha", "Kavya",
    "Meera", "Neha", "Nisha", "Pooja", "Priya", "Riya",
    "Sakshi", "Shreya", "Simran", "Sneha", "Tanvi", "Tanya",
    "Vidhi", "Aditi", "Avni", "Ishita", "Kriti", "Muskan",
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Jain",
    "Mehta", "Kapoor", "Malhotra", "Agarwal", "Mishra",
    "Chopra", "Bansal", "Joshi", "Saxena", "Sinha",
    "Khanna", "Arora", "Srivastava", "Shah",
]

CITIES = [
    "Delhi",
    "Noida",
    "Greater Noida",
    "Ghaziabad",
    "Gurugram",
    "Faridabad",
    "Lucknow",
    "Jaipur",
    "Chandigarh",
    "Kanpur",
    "Agra",
    "Dehradun",
    "Meerut",
    "Varanasi",
    "Prayagraj",
]

BLOOD_GROUPS = [
    "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"
]

INSURANCE_TYPES = [
    "Private",
    "Government",
    "Corporate",
    "Self-Pay",
]

ADMISSION_TYPES = [
    "Emergency",
    "Elective",
    "Urgent",
    "Routine",
]

ADMISSION_SOURCES = [
    "Emergency Department",
    "Outpatient Referral",
    "Primary Care Referral",
    "Specialist Referral",
    "Transfer from Other Hospital",
]

OUTCOMES = [
    "Recovered",
    "Improved",
    "Transferred",
    "Against Medical Advice",
]

DIAGNOSES = [
    ("D001", "Hypertension", "Cardiovascular", "Moderate"),
    ("D002", "Type 2 Diabetes", "Endocrine", "Moderate"),
    ("D003", "Coronary Artery Disease", "Cardiovascular", "Severe"),
    ("D004", "Pneumonia", "Respiratory", "Moderate"),
    ("D005", "Asthma", "Respiratory", "Mild"),
    ("D006", "Chronic Kidney Disease", "Renal", "Severe"),
    ("D007", "Migraine", "Neurological", "Mild"),
    ("D008", "Stroke", "Neurological", "Severe"),
    ("D009", "Fracture", "Orthopedic", "Moderate"),
    ("D010", "Arthritis", "Orthopedic", "Mild"),
    ("D011", "Gastritis", "Gastrointestinal", "Mild"),
    ("D012", "Liver Disease", "Gastrointestinal", "Severe"),
    ("D013", "COPD", "Respiratory", "Severe"),
    ("D014", "Anemia", "Hematological", "Moderate"),
    ("D015", "Cancer", "Oncology", "Severe"),
    ("D016", "Appendicitis", "Surgical", "Moderate"),
    ("D017", "Thyroid Disorder", "Endocrine", "Mild"),
    ("D018", "Urinary Tract Infection", "Renal", "Mild"),
    ("D019", "Sepsis", "Critical Care", "Critical"),
    ("D020", "Viral Infection", "General", "Mild"),
]

TREATMENTS = [
    ("Medication", 500, 5000),
    ("Surgery", 15000, 150000),
    ("Physiotherapy", 500, 5000),
    ("Dialysis", 3000, 8000),
    ("Chemotherapy", 10000, 50000),
    ("Radiation Therapy", 15000, 80000),
    ("Cardiac Procedure", 20000, 200000),
    ("Diagnostic Procedure", 1000, 15000),
    ("Emergency Treatment", 2000, 25000),
]

LAB_TESTS = [
    ("Hemoglobin", "Hematology", "g/dL", 12.0, 17.0),
    ("White Blood Cell Count", "Hematology", "10^3/uL", 4.0, 11.0),
    ("Platelet Count", "Hematology", "10^3/uL", 150, 450),
    ("Blood Glucose", "Biochemistry", "mg/dL", 70, 140),
    ("HbA1c", "Diabetes", "%", 4.0, 6.5),
    ("Creatinine", "Kidney", "mg/dL", 0.6, 1.3),
    ("Urea", "Kidney", "mg/dL", 15, 45),
    ("Total Cholesterol", "Lipid Profile", "mg/dL", 125, 200),
    ("LDL Cholesterol", "Lipid Profile", "mg/dL", 50, 130),
    ("HDL Cholesterol", "Lipid Profile", "mg/dL", 40, 80),
    ("Sodium", "Electrolytes", "mmol/L", 135, 145),
    ("Potassium", "Electrolytes", "mmol/L", 3.5, 5.1),
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_date(start_date, end_date):
    days = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, days))


def random_date_of_birth():
    """
    Generate a realistic DOB that is always before
    the earliest admission date in our dataset.
    """
    start_dob = date(1935, 1, 1)
    end_dob = date(2020, 12, 31)

    return random_date(
        start_dob,
        end_dob
    )


def weighted_choice(items, weights):
    return random.choices(items, weights=weights, k=1)[0]


# ============================================================
# CLEAR EXISTING DATA
# ============================================================

def clear_database():
    print("Clearing existing synthetic data...")

    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

        for table in [
            "billing",
            "lab_results",
            "treatments",
            "diagnoses",
            "admissions",
            "doctors",
            "patients",
            "departments",
        ]:
            conn.execute(text(f"TRUNCATE TABLE {table}"))

        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

    print("Database cleared.\n")


# ============================================================
# DEPARTMENTS
# ============================================================

def generate_departments():
    print("Generating departments...")

    rows = []

    for name, floor, capacity in DEPARTMENTS:
        rows.append({
            "department_name": name,
            "floor_number": floor,
            "bed_capacity": capacity,
        })

    df = pd.DataFrame(rows)

    df.to_sql(
        "departments",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    print(f"Inserted {len(df)} departments.")

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT department_id, department_name
                FROM departments
                ORDER BY department_id
            """)
        )

        return [dict(row._mapping) for row in result]


# ============================================================
# DOCTORS
# ============================================================

def generate_doctors(departments):
    print("Generating doctors...")

    rows = []

    for i in range(1, NUM_DOCTORS + 1):
        department = random.choice(departments)

        if random.random() < 0.5:
            first_name = random.choice(FIRST_NAMES_MALE)
        else:
            first_name = random.choice(FIRST_NAMES_FEMALE)

        last_name = random.choice(LAST_NAMES)

        rows.append({
            "doctor_id": f"DOC{i:04d}",
            "doctor_name": f"Dr. {first_name} {last_name}",
            "department_id": department["department_id"],
            "specialization": random.choice(
                SPECIALIZATIONS[department["department_name"]]
            ),
            "years_of_experience": random.randint(2, 30),
        })

    df = pd.DataFrame(rows)

    df.to_sql(
        "doctors",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    print(f"Inserted {len(df)} doctors.")

    return rows


# ============================================================
# PATIENTS
# ============================================================

def generate_patients():
    print("Generating patients...")

    rows = []

    for i in range(1, NUM_PATIENTS + 1):

        gender = random.choice(["Male", "Female"])

        if gender == "Male":
            first_name = random.choice(FIRST_NAMES_MALE)
        else:
            first_name = random.choice(FIRST_NAMES_FEMALE)

        last_name = random.choice(LAST_NAMES)

        rows.append({
            "patient_id": f"P{i:05d}",
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "date_of_birth": random_date_of_birth(),
            "city": random.choice(CITIES),
            "blood_group": random.choice(BLOOD_GROUPS),
            "insurance_type": weighted_choice(
                INSURANCE_TYPES,
                [40, 20, 20, 20]
            ),
            "registration_date": random_date(
                date(2020, 1, 1),
                END_DATE
            ),
        })

    df = pd.DataFrame(rows)

    df.to_sql(
        "patients",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000,
    )

    print(f"Inserted {len(df)} patients.")

    return rows


# ============================================================
# ADMISSIONS
# ============================================================

def generate_admissions(patients, doctors, departments):
    print("Generating admissions...")

    rows = []

    department_map = {
        d["department_id"]: d["department_name"]
        for d in departments
    }

    doctors_by_department = {}

    for doctor in doctors:
        doctors_by_department.setdefault(
            doctor["department_id"], []
        ).append(doctor)

    admission_counter = 1

    for patient in patients:

        number_of_admissions = random.randint(
            MIN_ADMISSIONS,
            MAX_ADMISSIONS
        )

        for _ in range(number_of_admissions):

            department = random.choice(departments)

            available_doctors = doctors_by_department.get(
                department["department_id"],
                doctors
            )

            doctor = random.choice(available_doctors)

            admission_date = random_date(
                START_DATE,
                END_DATE - timedelta(days=10)
            )

            admission_type = weighted_choice(
                ADMISSION_TYPES,
                [30, 25, 25, 20]
            )

            admission_source = random.choice(
                ADMISSION_SOURCES
            )

            # Emergency admissions tend to have longer stays
            if admission_type == "Emergency":
                length_of_stay = random.randint(2, 14)
            elif admission_type == "Urgent":
                length_of_stay = random.randint(2, 10)
            elif admission_type == "Elective":
                length_of_stay = random.randint(1, 8)
            else:
                length_of_stay = random.randint(1, 5)

            discharge_date = admission_date + timedelta(
                days=length_of_stay
            )

            # Don't allow discharge beyond dataset end date
            if discharge_date > END_DATE:
                discharge_date = END_DATE
                length_of_stay = max(
                    1,
                    (discharge_date - admission_date).days
                )

            diagnosis = random.choice(DIAGNOSES)

            if length_of_stay >= 10:
                outcome = weighted_choice(
                    OUTCOMES,
                    [55, 30, 5, 10]
                )
            else:
                outcome = weighted_choice(
                    OUTCOMES,
                    [65, 25, 3, 7]
                )

            rows.append({
                "admission_id": f"ADM{admission_counter:06d}",
                "patient_id": patient["patient_id"],
                "doctor_id": doctor["doctor_id"],
                "department_id": department["department_id"],
                "admission_date": admission_date,
                "discharge_date": discharge_date,
                "admission_type": admission_type,
                "admission_source": admission_source,
                "room_number": f"R{random.randint(101, 999)}",
                "bed_number": f"B{random.randint(1, 6)}",
                "diagnosis_summary": diagnosis[1],
                "outcome": outcome,
                "length_of_stay": length_of_stay,
            })

            admission_counter += 1

    df = pd.DataFrame(rows)

    df.to_sql(
        "admissions",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000,
    )

    print(f"Inserted {len(df)} admissions.")

    return rows


# ============================================================
# DIAGNOSES
# ============================================================

def generate_diagnoses(admissions):
    print("Generating diagnoses...")

    rows = []

    counter = 1

    for admission in admissions:

        # Every admission gets 1–3 diagnoses
        number_of_diagnoses = random.choices(
            [1, 2, 3],
            weights=[60, 30, 10],
            k=1
        )[0]

        selected = random.sample(
            DIAGNOSES,
            number_of_diagnoses
        )

        for index, diagnosis in enumerate(selected):

            severity = diagnosis[3]

            # Some variation
            if random.random() < 0.12:
                severity = random.choice(
                    ["Mild", "Moderate", "Severe"]
                )

            rows.append({
                "diagnosis_id": f"DIAG{counter:07d}",
                "admission_id": admission["admission_id"],
                "diagnosis_code": diagnosis[0],
                "diagnosis_name": diagnosis[1],
                "diagnosis_category": diagnosis[2],
                "severity": severity,
                "is_primary": index == 0,
            })

            counter += 1

    df = pd.DataFrame(rows)

    df.to_sql(
        "diagnoses",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000,
    )

    print(f"Inserted {len(df)} diagnoses.")

    return rows


# ============================================================
# TREATMENTS
# ============================================================

def generate_treatments(admissions):
    print("Generating treatments...")

    rows = []

    counter = 1

    for admission in admissions:

        number_of_treatments = random.choices(
            [1, 2, 3, 4],
            weights=[40, 35, 20, 5],
            k=1
        )[0]

        for _ in range(number_of_treatments):

            treatment_type, min_cost, max_cost = random.choice(
                TREATMENTS
            )

            treatment_date = admission["admission_date"] + timedelta(
                days=random.randint(
                    0,
                    max(0, admission["length_of_stay"] - 1)
                )
            )

            treatment_name = {
                "Medication": random.choice([
                    "Antibiotic Therapy",
                    "Pain Management",
                    "Insulin Therapy",
                    "Antihypertensive Therapy",
                ]),
                "Surgery": random.choice([
                    "Laparoscopic Surgery",
                    "Orthopedic Surgery",
                    "General Surgery",
                ]),
                "Physiotherapy": "Physiotherapy Session",
                "Dialysis": "Hemodialysis",
                "Chemotherapy": "Chemotherapy Cycle",
                "Radiation Therapy": "Radiation Session",
                "Cardiac Procedure": random.choice([
                    "Angioplasty",
                    "Cardiac Catheterization",
                    "ECG Monitoring",
                ]),
                "Diagnostic Procedure": random.choice([
                    "CT Scan",
                    "MRI",
                    "Ultrasound",
                    "X-Ray",
                ]),
                "Emergency Treatment": "Emergency Stabilization",
            }[treatment_type]

            cost = round(
                random.uniform(min_cost, max_cost),
                2
            )

            rows.append({
                "treatment_id": f"TRT{counter:07d}",
                "admission_id": admission["admission_id"],
                "treatment_name": treatment_name,
                "treatment_type": treatment_type,
                "treatment_date": treatment_date,
                "treatment_cost": cost,
            })

            counter += 1

    df = pd.DataFrame(rows)

    df.to_sql(
        "treatments",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000,
    )

    print(f"Inserted {len(df)} treatments.")

    return rows


# ============================================================
# LAB RESULTS
# ============================================================

def generate_lab_results(patients, admissions):
    print("Generating lab results...")

    rows = []

    counter = 1

    for admission in admissions:

        patient = next(
            p for p in patients
            if p["patient_id"] == admission["patient_id"]
        )

        # 3–7 tests per admission
        number_of_tests = random.randint(3, 7)

        selected_tests = random.sample(
            LAB_TESTS,
            number_of_tests
        )

        for test in selected_tests:

            test_name, category, unit, normal_min, normal_max = test

            # Generate mostly normal results,
            # with a controlled amount of abnormal results.
            if random.random() < 0.82:
                result_value = random.uniform(
                    normal_min,
                    normal_max
                )
                status = "Normal"
            else:
                if random.random() < 0.5:
                    result_value = random.uniform(
                        normal_min * 0.5,
                        normal_min * 0.95
                    )
                else:
                    result_value = random.uniform(
                        normal_max * 1.05,
                        normal_max * 1.5
                    )

                status = "Abnormal"

            test_date = admission["admission_date"] + timedelta(
                days=random.randint(
                    0,
                    max(0, admission["length_of_stay"] - 1)
                )
            )

            rows.append({
                "lab_result_id": f"LAB{counter:08d}",
                "patient_id": patient["patient_id"],
                "admission_id": admission["admission_id"],
                "test_name": test_name,
                "test_category": category,
                "test_date": test_date,
                "result_value": round(result_value, 3),
                "unit": unit,
                "reference_range": (
                    f"{normal_min}-{normal_max}"
                ),
                "result_status": status,
            })

            counter += 1

    df = pd.DataFrame(rows)

    df.to_sql(
        "lab_results",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=2000,
    )

    print(f"Inserted {len(df)} lab results.")

    return rows


# ============================================================
# BILLING
# ============================================================
def generate_billing(admissions, treatments, patients):
    print("Generating billing records...")

    treatment_totals = {}

    for treatment in treatments:
        admission_id = treatment["admission_id"]

        treatment_totals[admission_id] = (
            treatment_totals.get(admission_id, 0)
            + float(treatment["treatment_cost"])
        )

    # Patient insurance lookup
    patient_insurance = {
        patient["patient_id"]: patient["insurance_type"]
        for patient in patients
    }

    rows = []

    for admission in admissions:

        admission_id = admission["admission_id"]
        patient_id = admission["patient_id"]

        treatment_charge = treatment_totals.get(
            admission_id,
            0
        )

        # Longer stays → higher room charges
        room_charges = (
            admission["length_of_stay"]
            * random.uniform(2500, 7000)
        )

        doctor_charges = random.uniform(
            2000,
            12000
        )

        medication_charges = random.uniform(
            1000,
            15000
        )

        laboratory_charges = random.uniform(
            1000,
            10000
        )

        total_bill = (
            room_charges
            + doctor_charges
            + treatment_charge
            + medication_charges
            + laboratory_charges
        )

        # IMPORTANT:
        # Use the patient's actual insurance type.
        insurance_type = patient_insurance[patient_id]

        if insurance_type == "Self-Pay":
            coverage_percentage = 0.0

        elif insurance_type == "Government":
            coverage_percentage = random.uniform(
                0.60,
                0.90
            )

        elif insurance_type == "Corporate":
            coverage_percentage = random.uniform(
                0.70,
                0.95
            )

        else:  # Private
            coverage_percentage = random.uniform(
                0.50,
                0.90
            )

        insurance_covered = (
            total_bill * coverage_percentage
        )

        patient_paid = (
            total_bill - insurance_covered
        )

        payment_status = weighted_choice(
            ["Paid", "Partially Paid", "Pending"],
            [75, 15, 10]
        )

        # Self-pay patients should not have
        # an insurance provider.
        if insurance_type == "Self-Pay":
            insurance_provider = "None"

        elif insurance_type == "Government":
            insurance_provider = "Government Health Scheme"

        else:
            insurance_provider = random.choice([
                "Star Health",
                "ICICI Lombard",
                "HDFC ERGO",
                "Niva Bupa",
                "Care Health",
            ])

        rows.append({
            "bill_id": f"BILL{admission_id[3:]}",
            "admission_id": admission_id,

            "room_charges": round(
                room_charges,
                2
            ),

            "doctor_charges": round(
                doctor_charges,
                2
            ),

            "treatment_charges": round(
                treatment_charge,
                2
            ),

            "medication_charges": round(
                medication_charges,
                2
            ),

            "laboratory_charges": round(
                laboratory_charges,
                2
            ),

            "total_bill": round(
                total_bill,
                2
            ),

            "insurance_provider": insurance_provider,

            "insurance_covered": round(
                insurance_covered,
                2
            ),

            "patient_paid": round(
                patient_paid,
                2
            ),

            "payment_status": payment_status,

            "billing_date": admission["discharge_date"],
        })

    df = pd.DataFrame(rows)

    df.to_sql(
        "billing",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000,
    )

    print(
        f"Inserted {len(df)} billing records."
    )

    return rows

# ============================================================
# DATABASE SUMMARY
# ============================================================

def verify_database():
    print("\n" + "=" * 60)
    print("FINAL DATABASE SUMMARY")
    print("=" * 60)

    tables = [
        "departments",
        "doctors",
        "patients",
        "admissions",
        "diagnoses",
        "treatments",
        "lab_results",
        "billing",
    ]

    with engine.connect() as conn:

        for table in tables:

            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {table}")
            )

            count = result.scalar()

            print(
                f"{table:<15}: {count:,} records"
            )

    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("HEALTHCARE PATIENT 360")
    print("PRODUCTION SYNTHETIC DATA GENERATOR")
    print("=" * 60)
    print()

    clear_database()

    departments = generate_departments()

    doctors = generate_doctors(
        departments
    )

    patients = generate_patients()

    admissions = generate_admissions(
        patients,
        doctors,
        departments
    )

    diagnoses = generate_diagnoses(
        admissions
    )

    treatments = generate_treatments(
        admissions
    )

    lab_results = generate_lab_results(
        patients,
        admissions
    )

    billing = generate_billing(
        admissions,
        treatments,
        patients
    )

    verify_database()

    print()
    print("=" * 60)
    print("HEALTHCARE DATA GENERATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()