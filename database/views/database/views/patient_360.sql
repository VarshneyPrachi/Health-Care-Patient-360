USE healthcare_analytics;

CREATE OR REPLACE VIEW vw_patient_360 AS

SELECT
    p.patient_id,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.gender,
    p.date_of_birth,
    TIMESTAMPDIFF(
        YEAR,
        p.date_of_birth,
        CURDATE()
    ) AS age,
    p.city,
    p.blood_group,
    p.insurance_type,
    p.registration_date,

    a.admission_id,
    a.admission_date,
    a.discharge_date,
    a.admission_type,
    a.admission_source,
    a.room_number,
    a.bed_number,
    a.outcome,
    a.length_of_stay,

    d.department_name,

    doc.doctor_id,
    doc.doctor_name,
    doc.specialization,
    doc.years_of_experience,

    dg.diagnosis_name,
    dg.diagnosis_category,
    dg.severity,
    dg.is_primary,

    t.treatment_name,
    t.treatment_type,
    t.treatment_date,
    t.treatment_cost,

    l.test_name,
    l.test_category,
    l.test_date,
    l.result_value,
    l.unit,
    l.reference_range,
    l.result_status,

    b.room_charges,
    b.doctor_charges,
    b.treatment_charges,
    b.medication_charges,
    b.laboratory_charges,
    b.total_bill,
    b.insurance_provider,
    b.insurance_covered,
    b.patient_paid,
    b.payment_status,
    b.billing_date

FROM patients p

LEFT JOIN admissions a
    ON p.patient_id = a.patient_id

LEFT JOIN departments d
    ON a.department_id = d.department_id

LEFT JOIN doctors doc
    ON a.doctor_id = doc.doctor_id

LEFT JOIN diagnoses dg
    ON a.admission_id = dg.admission_id

LEFT JOIN treatments t
    ON a.admission_id = t.admission_id

LEFT JOIN lab_results l
    ON a.admission_id = l.admission_id

LEFT JOIN billing b
    ON a.admission_id = b.admission_id;