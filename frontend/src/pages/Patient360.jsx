import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";

import {
    UserRound,
    CalendarDays,
    ShieldCheck,
    BrainCircuit,
    Activity,
    Stethoscope,
    CreditCard,
    FlaskConical,
    ArrowLeft,
    Search,
    AlertTriangle,
} from "lucide-react";

import api from "../services/api";

function Patient360() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();

    const patientFromUrl = searchParams.get("patient");

    const [patientId, setPatientId] = useState(
        patientFromUrl || "P00001"
    );

    const [searchInput, setSearchInput] = useState(
        patientFromUrl || ""
    );

    const [patient, setPatient] = useState(null);
    const [aiData, setAiData] = useState(null);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        if (patientFromUrl) {
            setPatientId(patientFromUrl);
            setSearchInput(patientFromUrl);
        }
    }, [patientFromUrl]);

    useEffect(() => {
        const loadPatient = async () => {
            if (!patientId) return;

            try {
                setLoading(true);
                setError("");

                const [patientResponse, aiResponse] =
                    await Promise.all([
                        api.get(`/patients/${patientId}`),
                        api.get(`/ai/patient/${patientId}`),
                    ]);

                const patientRows =
                    patientResponse.data.patient || [];

                const aiRows =
                    aiResponse.data.data || [];

                if (patientRows.length === 0) {
                    throw new Error("Patient not found");
                }

                setPatient(patientRows[0]);
                setAiData(aiRows[0] || null);

            } catch (err) {
                console.error(
                    "Patient 360 loading error:",
                    err
                );

                setPatient(null);
                setAiData(null);

                setError(
                    "Patient not found. Please check the Patient ID."
                );
            } finally {
                setLoading(false);
            }
        };

        loadPatient();

    }, [patientId]);


    const handleSearch = (event) => {
        event.preventDefault();

        const value = searchInput.trim().toUpperCase();

        if (!value) return;

        navigate(
            `/patient-360?patient=${value}`
        );
    };


    const getRiskClass = (risk) => {
        if (risk === "High") return "p360-risk-high";
        if (risk === "Medium") return "p360-risk-medium";

        return "p360-risk-low";
    };


    const formatCurrency = (value) => {
        if (value === null || value === undefined) {
            return "₹0";
        }

        return `₹${Number(value).toLocaleString(
            "en-IN",
            {
                maximumFractionDigits: 0,
            }
        )}`;
    };


    if (loading) {
        return (
            <div className="p360-loading">

                <div className="loading-spinner"></div>

                <span>
                    Loading patient intelligence...
                </span>

            </div>
        );
    }


    if (error || !patient) {
        return (
            <div>

                <div className="page-label">
                    PATIENT INTELLIGENCE
                </div>

                <h1 className="page-title">
                    Patient 360
                </h1>

                <div className="p360-search-card">

                    <form
                        className="p360-search"
                        onSubmit={handleSearch}
                    >

                        <Search size={17} />

                        <input
                            value={searchInput}
                            onChange={(e) =>
                                setSearchInput(
                                    e.target.value
                                )
                            }
                            placeholder="Enter Patient ID, e.g. P00016"
                        />

                        <button type="submit">
                            Search
                        </button>

                    </form>

                </div>

                <div className="p360-error">

                    <AlertTriangle size={22} />

                    <div>
                        <strong>
                            Patient not found
                        </strong>

                        <p>
                            Enter a valid Patient ID such as
                            P00001 or P00016.
                        </p>
                    </div>

                </div>

            </div>
        );
    }


    return (
        <div>

            {/* Header */}

            <div className="p360-header">

                <div>

                    <button
                        className="back-button"
                        onClick={() =>
                            navigate("/patients")
                        }
                    >
                        <ArrowLeft size={15} />
                        Back to Patients
                    </button>

                    <div className="page-label">
                        PATIENT INTELLIGENCE
                    </div>

                    <h1 className="page-title">
                        Patient 360
                    </h1>

                    <p className="page-description">
                        Complete clinical, financial and
                        AI-powered patient profile.
                    </p>

                </div>


                <form
                    className="p360-search"
                    onSubmit={handleSearch}
                >

                    <Search size={16} />

                    <input
                        value={searchInput}
                        onChange={(e) =>
                            setSearchInput(
                                e.target.value
                            )
                        }
                        placeholder="Patient ID"
                    />

                    <button type="submit">
                        Search
                    </button>

                </form>

            </div>


            {/* Patient identity */}

            <div className="patient-identity-card">

                <div className="patient-main-info">

                    <div className="large-patient-avatar">
                        <UserRound size={28} />
                    </div>

                    <div>

                        <div className="patient-main-id">
                            {patient.patient_id}
                        </div>

                        <div className="patient-main-details">
                            {patient.gender} ·{" "}
                            {patient.patient_age} years ·{" "}
                            {patient.city}
                        </div>

                    </div>

                </div>


                <div className="identity-status">

                    <span
                        className={`p360-risk-badge ${getRiskClass(
                            patient.risk_category
                        )}`}
                    >
                        <span></span>
                        {patient.risk_category} Risk
                    </span>

                </div>

            </div>


            {/* Profile cards */}

            <div className="p360-profile-grid">

                <div className="p360-info-card">

                    <div className="p360-card-icon blue">
                        <UserRound size={17} />
                    </div>

                    <div>

                        <div className="p360-info-label">
                            AGE
                        </div>

                        <div className="p360-info-value">
                            {patient.patient_age}
                        </div>

                        <div className="p360-info-sub">
                            Years
                        </div>

                    </div>

                </div>


                <div className="p360-info-card">

                    <div className="p360-card-icon green">
                        <ShieldCheck size={17} />
                    </div>

                    <div>

                        <div className="p360-info-label">
                            INSURANCE
                        </div>

                        <div className="p360-info-value">
                            {patient.insurance_type}
                        </div>

                        <div className="p360-info-sub">
                            Coverage type
                        </div>

                    </div>

                </div>


                <div className="p360-info-card">

                    <div className="p360-card-icon purple">
                        <Activity size={17} />
                    </div>

                    <div>

                        <div className="p360-info-label">
                            DEPARTMENT
                        </div>

                        <div className="p360-info-value">
                            {patient.department_name}
                        </div>

                        <div className="p360-info-sub">
                            Current department
                        </div>

                    </div>

                </div>


                <div className="p360-info-card">

                    <div className="p360-card-icon orange">
                        <Stethoscope size={17} />
                    </div>

                    <div>

                        <div className="p360-info-label">
                            DOCTOR
                        </div>

                        <div className="p360-info-value doctor">
                            {patient.doctor_name}
                        </div>

                        <div className="p360-info-sub">
                            Assigned physician
                        </div>

                    </div>

                </div>

            </div>


            {/* AI section */}

            <div className="section-heading">

                <div className="section-heading-icon">
                    <BrainCircuit size={17} />
                </div>

                <div>

                    <div className="section-title">
                        AI Patient Intelligence
                    </div>

                    <div className="section-subtitle">
                        Machine-learning insights for this patient
                    </div>

                </div>

            </div>


            <div className="p360-ai-grid">

                <div className="p360-ai-card risk-card">

                    <div className="ai-card-top">

                        <div className="ai-label">
                            AI RISK
                        </div>

                        <BrainCircuit size={17} />

                    </div>

                    <div
                        className={`ai-main-value ${getRiskClass(
                            patient.risk_category
                        )}`}
                    >
                        {patient.risk_category}
                    </div>

                    <div className="ai-description">
                        Current predicted readmission risk category
                    </div>

                </div>


                <div className="p360-ai-card">

                    <div className="ai-card-top">

                        <div className="ai-label">
                            READMISSION PROBABILITY
                        </div>

                        <Activity size={17} />

                    </div>

                    <div className="ai-main-value">
                        {patient.readmission_probability_pct}%
                    </div>

                    <div className="ai-progress">
                        <div
                            style={{
                                width: `${Math.min(
                                    Number(
                                        patient.readmission_probability_pct
                                    ),
                                    100
                                )}%`,
                            }}
                        />
                    </div>

                    <div className="ai-description">
                        Estimated probability from the ML model
                    </div>

                </div>


                <div className="p360-ai-card">

                    <div className="ai-card-top">

                        <div className="ai-label">
                            PREDICTED LOS
                        </div>

                        <CalendarDays size={17} />

                    </div>

                    <div className="ai-main-value">
                        {patient.predicted_length_of_stay}
                        <span className="ai-unit">
                            days
                        </span>
                    </div>

                    <div className="ai-los-badge">
                        {patient.predicted_los_category}
                    </div>

                    <div className="ai-description">
                        Predicted length of hospital stay
                    </div>

                </div>

            </div>


            {/* Clinical + Financial */}

            <div className="p360-two-column">


                {/* Clinical */}

                <div className="p360-large-card">

                    <div className="large-card-header">

                        <div>

                            <div className="large-card-title">
                                Clinical Summary
                            </div>

                            <div className="large-card-subtitle">
                                Patient clinical activity
                            </div>

                        </div>

                        <div className="large-card-icon">
                            <FlaskConical size={17} />
                        </div>

                    </div>


                    <div className="clinical-grid">

                        <div className="clinical-item">
                            <span>
                                Previous Admissions
                            </span>

                            <strong>
                                {patient.previous_admissions}
                            </strong>
                        </div>

                        <div className="clinical-item">
                            <span>
                                Days Since Previous
                            </span>

                            <strong>
                                {patient.days_since_previous_admission}
                            </strong>
                        </div>

                        <div className="clinical-item">
                            <span>
                                Diagnoses
                            </span>

                            <strong>
                                {patient.diagnosis_count}
                            </strong>
                        </div>

                        <div className="clinical-item">
                            <span>
                                Treatments
                            </span>

                            <strong>
                                {patient.treatment_count}
                            </strong>
                        </div>

                        <div className="clinical-item">
                            <span>
                                Lab Tests
                            </span>

                            <strong>
                                {patient.lab_test_count}
                            </strong>
                        </div>

                        <div className="clinical-item">
                            <span>
                                Abnormal Labs
                            </span>

                            <strong
                                className={
                                    Number(
                                        patient.abnormal_lab_count
                                    ) > 0
                                        ? "abnormal-value"
                                        : ""
                                }
                            >
                                {patient.abnormal_lab_count}
                            </strong>
                        </div>

                    </div>

                </div>


                {/* Financial */}

                <div className="p360-large-card">

                    <div className="large-card-header">

                        <div>

                            <div className="large-card-title">
                                Financial Summary
                            </div>

                            <div className="large-card-subtitle">
                                Current admission billing
                            </div>

                        </div>

                        <div className="large-card-icon finance">
                            <CreditCard size={17} />
                        </div>

                    </div>


                    <div className="financial-list">

                        <div className="financial-row">

                            <div>
                                <span>
                                    Total Bill
                                </span>

                                <small>
                                    Overall admission cost
                                </small>
                            </div>

                            <strong>
                                {formatCurrency(
                                    patient.total_bill
                                )}
                            </strong>

                        </div>


                        <div className="financial-row">

                            <div>
                                <span>
                                    Insurance Covered
                                </span>

                                <small>
                                    Insurance contribution
                                </small>
                            </div>

                            <strong className="green-money">
                                {formatCurrency(
                                    patient.insurance_covered
                                )}
                            </strong>

                        </div>


                        <div className="financial-row">

                            <div>
                                <span>
                                    Patient Paid
                                </span>

                                <small>
                                    Patient contribution
                                </small>
                            </div>

                            <strong>
                                {formatCurrency(
                                    patient.patient_paid
                                )}
                            </strong>

                        </div>

                    </div>

                </div>

            </div>


            {/* Admission */}

            <div className="admission-card">

                <div className="large-card-header">

                    <div>

                        <div className="large-card-title">
                            Current Admission
                        </div>

                        <div className="large-card-subtitle">
                            Admission and outcome details
                        </div>

                    </div>

                    <div className="large-card-icon">
                        <CalendarDays size={17} />
                    </div>

                </div>


                <div className="admission-grid">

                    <div>
                        <span>Admission ID</span>
                        <strong>{patient.admission_id}</strong>
                    </div>

                    <div>
                        <span>Admission Date</span>
                        <strong>
                            {new Date(
                                patient.admission_date
                            ).toLocaleDateString("en-IN")}
                        </strong>
                    </div>

                    <div>
                        <span>Admission Type</span>
                        <strong>
                            {patient.admission_type}
                        </strong>
                    </div>

                    <div>
                        <span>Source</span>
                        <strong>
                            {patient.admission_source}
                        </strong>
                    </div>

                    <div>
                        <span>Actual LOS</span>
                        <strong>
                            {patient.length_of_stay} days
                        </strong>
                    </div>

                    <div>
                        <span>Outcome</span>
                        <strong>
                            {patient.outcome}
                        </strong>
                    </div>

                </div>

            </div>


            <div className="demo-note">
                <strong>Analytics note:</strong>{" "}
                AI predictions are based on the project's synthetic
                healthcare dataset and are intended for analytical
                demonstration, not clinical diagnosis.
            </div>

        </div>
    );
}

export default Patient360;