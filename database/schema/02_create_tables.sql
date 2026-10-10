USE healthcare_analytics;

-- =========================================================
-- 1. PATIENTS
-- =========================================================

CREATE TABLE patients (
    patient_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    city VARCHAR(100),
    blood_group VARCHAR(5),
    insurance_type VARCHAR(50),
    registration_date DATE NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- 2. DEPARTMENTS
-- =========================================================

CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    floor_number INT,
    bed_capacity INT
);


-- =========================================================
-- 3. DOCTORS
-- =========================================================

CREATE TABLE doctors (
    doctor_id VARCHAR(20) PRIMARY KEY,
    doctor_name VARCHAR(100) NOT NULL,
    department_id INT NOT NULL,
    specialization VARCHAR(100),
    years_of_experience INT,

    CONSTRAINT fk_doctor_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);


-- =========================================================
-- 4. ADMISSIONS
-- =========================================================

CREATE TABLE admissions (
    admission_id VARCHAR(20) PRIMARY KEY,
    patient_id VARCHAR(20) NOT NULL,
    doctor_id VARCHAR(20) NOT NULL,
    department_id INT NOT NULL,

    admission_date DATE NOT NULL,
    discharge_date DATE,

    admission_type VARCHAR(50),
    admission_source VARCHAR(100),

    room_number VARCHAR(20),
    bed_number VARCHAR(20),

    diagnosis_summary VARCHAR(255),
    outcome VARCHAR(100),

    length_of_stay INT,

    CONSTRAINT fk_admission_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id),

    CONSTRAINT fk_admission_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctors(doctor_id),

    CONSTRAINT fk_admission_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);


-- =========================================================
-- 5. DIAGNOSES
-- =========================================================

CREATE TABLE diagnoses (
    diagnosis_id VARCHAR(20) PRIMARY KEY,
    admission_id VARCHAR(20) NOT NULL,

    diagnosis_code VARCHAR(20),
    diagnosis_name VARCHAR(150),
    diagnosis_category VARCHAR(100),
    severity VARCHAR(50),
    is_primary BOOLEAN DEFAULT FALSE,

    CONSTRAINT fk_diagnosis_admission
        FOREIGN KEY (admission_id)
        REFERENCES admissions(admission_id)
);


-- =========================================================
-- 6. TREATMENTS
-- =========================================================

CREATE TABLE treatments (
    treatment_id VARCHAR(20) PRIMARY KEY,
    admission_id VARCHAR(20) NOT NULL,

    treatment_name VARCHAR(150),
    treatment_type VARCHAR(100),
    treatment_date DATE,

    treatment_cost DECIMAL(12,2),

    CONSTRAINT fk_treatment_admission
        FOREIGN KEY (admission_id)
        REFERENCES admissions(admission_id)
);


-- =========================================================
-- 7. LAB RESULTS
-- =========================================================

CREATE TABLE lab_results (
    lab_result_id VARCHAR(20) PRIMARY KEY,
    patient_id VARCHAR(20) NOT NULL,
    admission_id VARCHAR(20),

    test_name VARCHAR(150),
    test_category VARCHAR(100),

    test_date DATE,

    result_value DECIMAL(12,3),
    unit VARCHAR(50),

    reference_range VARCHAR(100),
    result_status VARCHAR(50),

    CONSTRAINT fk_lab_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id),

    CONSTRAINT fk_lab_admission
        FOREIGN KEY (admission_id)
        REFERENCES admissions(admission_id)
);


-- =========================================================
-- 8. BILLING
-- =========================================================

CREATE TABLE billing (
    bill_id VARCHAR(20) PRIMARY KEY,
    admission_id VARCHAR(20) NOT NULL,

    room_charges DECIMAL(12,2) DEFAULT 0,
    doctor_charges DECIMAL(12,2) DEFAULT 0,
    treatment_charges DECIMAL(12,2) DEFAULT 0,
    medication_charges DECIMAL(12,2) DEFAULT 0,
    laboratory_charges DECIMAL(12,2) DEFAULT 0,

    total_bill DECIMAL(12,2),

    insurance_provider VARCHAR(100),
    insurance_covered DECIMAL(12,2) DEFAULT 0,
    patient_paid DECIMAL(12,2) DEFAULT 0,

    payment_status VARCHAR(50),

    billing_date DATE,

    CONSTRAINT fk_billing_admission
        FOREIGN KEY (admission_id)
        REFERENCES admissions(admission_id)
);