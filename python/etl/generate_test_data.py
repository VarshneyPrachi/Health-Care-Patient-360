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

engine = create_engine(DATABASE_URL)


# ============================================================
# RANDOM DATA CONFIGURATION
# ============================================================

random.seed(42)

NUMBER_OF_PATIENTS = 100
NUMBER_OF_DOCTORS = 20


# ============================================================
# REFERENCE DATA
# ============================================================

DEPARTMENTS = [
    ("Cardiology", 1, 40),
    ("Neurology", 2, 30),
    ("Orthopedics", 3, 35),
    ("Pediatrics", 4, 40),
    ("General Medicine", 5, 50),
    ("General Surgery", 6, 35),
    ("Oncology", 7, 30),
    ("Dermatology", 8, 20),
    ("Gastroenterology", 9, 25),
    ("Pulmonology", 10, 30),
    ("Emergency", 11, 45),
    ("ICU", 12, 25),
]

SPECIALIZATIONS = {
    "Cardiology": "Cardiologist",
    "Neurology": "Neurologist",
    "Orthopedics": "Orthopedic Specialist",
    "Pediatrics": "Pediatrician",
    "General Medicine": "General Physician",
    "General Surgery": "General Surgeon",
    "Oncology": "Oncologist",
    "Dermatology": "Dermatologist",
    "Gastroenterology": "Gastroenterologist",
    "Pulmonology": "Pulmonologist",
    "Emergency": "Emergency Medicine",
    "ICU": "Critical Care Specialist",
}

FIRST_NAMES = [
    "Aarav", "Aditi", "Aditya", "Ananya", "Arjun",
    "Diya", "Ishaan", "Kavya", "Krishna", "Meera",
    "Neha", "Rahul", "Riya", "Rohan", "Sahil",
    "Simran", "Tanvi", "Varun", "Vikram", "Yash",
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar",
    "Mehta", "Jain", "Agarwal", "Patel", "Shah",
    "Mishra", "Joshi", "Chauhan", "Malhotra", "Kapoor",
]

CITIES = [
    "Delhi",
    "Noida",
    "Gurgaon",
    "Ghaziabad",
    "Faridabad",
    "Lucknow",
    "Jaipur",
    "Chandigarh",
    "Agra",
    "Meerut",
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


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


# ============================================================
# INSERT DEPARTMENTS
# ============================================================

def generate_departments():

    print("Generating departments...")

    with engine.begin() as connection:

        connection.execute(
            text("DELETE FROM departments")
        )

        for department_name, floor, beds in DEPARTMENTS:

            connection.execute(
                text("""
                    INSERT INTO departments
                    (
                        department_name,
                        floor_number,
                        bed_capacity
                    )
                    VALUES
                    (
                        :department_name,
                        :floor_number,
                        :bed_capacity
                    )
                """),
                {
                    "department_name": department_name,
                    "floor_number": floor,
                    "bed_capacity": beds,
                },
            )

    print(f"Inserted {len(DEPARTMENTS)} departments.")


# ============================================================
# INSERT DOCTORS
# ============================================================

def generate_doctors():

    print("Generating doctors...")

    with engine.begin() as connection:

        connection.execute(
            text("DELETE FROM doctors")
        )

        result = connection.execute(
            text("""
                SELECT
                    department_id,
                    department_name
                FROM departments
            """)
        )

        departments = result.fetchall()

        doctors = []

        for i in range(1, NUMBER_OF_DOCTORS + 1):

            department_id, department_name = random.choice(
                departments
            )

            doctor_name = (
                f"Dr. "
                f"{random.choice(FIRST_NAMES)} "
                f"{random.choice(LAST_NAMES)}"
            )

            specialization = SPECIALIZATIONS[
                department_name
            ]

            experience = random.randint(2, 30)

            doctors.append(
                {
                    "doctor_id": f"D{i:04d}",
                    "doctor_name": doctor_name,
                    "department_id": department_id,
                    "specialization": specialization,
                    "years_of_experience": experience,
                }
            )

        connection.execute(
            text("""
                INSERT INTO doctors
                (
                    doctor_id,
                    doctor_name,
                    department_id,
                    specialization,
                    years_of_experience
                )
                VALUES
                (
                    :doctor_id,
                    :doctor_name,
                    :department_id,
                    :specialization,
                    :years_of_experience
                )
            """),
            doctors,
        )

    print(f"Inserted {len(doctors)} doctors.")


# ============================================================
# INSERT PATIENTS
# ============================================================

def generate_patients():

    print("Generating patients...")

    patients = []

    today = date.today()

    for i in range(1, NUMBER_OF_PATIENTS + 1):

        gender = random.choice([
            "Male",
            "Female"
        ])

        birth_start = date(1940, 1, 1)
        birth_end = date(
            today.year - 1,
            today.month,
            today.day
        )

        dob = random_date(
            birth_start,
            birth_end
        )

        registration_date = random_date(
            date(2021, 1, 1),
            today
        )

        patients.append(
            {
                "patient_id": f"P{i:05d}",
                "first_name": random.choice(FIRST_NAMES),
                "last_name": random.choice(LAST_NAMES),
                "gender": gender,
                "date_of_birth": dob,
                "city": random.choice(CITIES),
                "blood_group": random.choice(BLOOD_GROUPS),
                "insurance_type": random.choice(
                    INSURANCE_TYPES
                ),
                "registration_date": registration_date,
            }
        )

    with engine.begin() as connection:

        connection.execute(
            text("DELETE FROM patients")
        )

        connection.execute(
            text("""
                INSERT INTO patients
                (
                    patient_id,
                    first_name,
                    last_name,
                    gender,
                    date_of_birth,
                    city,
                    blood_group,
                    insurance_type,
                    registration_date
                )
                VALUES
                (
                    :patient_id,
                    :first_name,
                    :last_name,
                    :gender,
                    :date_of_birth,
                    :city,
                    :blood_group,
                    :insurance_type,
                    :registration_date
                )
            """),
            patients,
        )

    print(f"Inserted {len(patients)} patients.")


# ============================================================
# VERIFY DATA
# ============================================================

def verify_database():

    print("\nChecking database...")

    tables = [
        "departments",
        "doctors",
        "patients",
    ]

    with engine.connect() as connection:

        for table in tables:

            result = connection.execute(
                text(
                    f"SELECT COUNT(*) FROM {table}"
                )
            )

            count = result.scalar()

            print(
                f"{table:<15} : {count} records"
            )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("HEALTHCARE PATIENT 360")
    print("TEST DATA GENERATOR")
    print("=" * 60)

    generate_departments()
    generate_doctors()
    generate_patients()

    verify_database()

    print("=" * 60)
    print("TEST DATA GENERATION COMPLETED")
    print("=" * 60)