import { useEffect, useState } from "react";
import {
    Search,
    UserRound,
    ArrowUpRight,
    ChevronLeft,
    ChevronRight,
    Users,
    Filter,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

import api from "../services/api";

function Patients() {
    const navigate = useNavigate();

    const [patients, setPatients] = useState([]);
    const [search, setSearch] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [page, setPage] = useState(1);

    const rowsPerPage = 10;

    useEffect(() => {
        const loadPatients = async () => {
            try {
                setLoading(true);
                setError("");

                const response = await api.get("/patients", {
                    params: {
                        search: search || undefined,
                    },
                });

                setPatients(response.data.patients || []);

            } catch (err) {
                console.error("Patients loading error:", err);
                setError("Unable to load patient data.");
            } finally {
                setLoading(false);
            }
        };

        const timer = setTimeout(() => {
            loadPatients();
        }, 300);

        return () => clearTimeout(timer);

    }, [search]);

    useEffect(() => {
        setPage(1);
    }, [search]);

    const totalPages = Math.ceil(
        patients.length / rowsPerPage
    );

    const startIndex = (page - 1) * rowsPerPage;

    const visiblePatients = patients.slice(
        startIndex,
        startIndex + rowsPerPage
    );

    const getRiskClass = (risk) => {
        if (risk === "High") return "risk-high";
        if (risk === "Medium") return "risk-medium";
        return "risk-low";
    };

    return (
        <div>

            {/* Header */}

            <div className="patients-header">

                <div>
                    <div className="page-label">
                        PATIENT MANAGEMENT
                    </div>

                    <h1 className="page-title">
                        Patients
                    </h1>

                    <p className="page-description">
                        Search, explore and review patient intelligence.
                    </p>
                </div>

                <div className="patient-count-card">

                    <div className="patient-count-icon">
                        <Users size={17} />
                    </div>

                    <div>
                        <div className="patient-count-value">
                            {patients.length}
                        </div>

                        <div className="patient-count-label">
                            Records found
                        </div>
                    </div>

                </div>

            </div>


            {/* Search / Filter bar */}

            <div className="patient-toolbar">

                <div className="patient-search">

                    <Search size={17} />

                    <input
                        type="text"
                        placeholder="Search by Patient ID, city or department..."
                        value={search}
                        onChange={(e) =>
                            setSearch(e.target.value)
                        }
                    />

                    {search && (
                        <button
                            className="clear-search"
                            onClick={() => setSearch("")}
                        >
                            ×
                        </button>
                    )}

                </div>

                <button className="filter-button">
                    <Filter size={15} />
                    Filters
                </button>

            </div>


            {/* Table card */}

            <div className="patients-table-card">

                <div className="table-heading">

                    <div>

                        <div className="table-title">
                            Patient Directory
                        </div>

                        <div className="table-subtitle">
                            Showing patient records from the healthcare database
                        </div>

                    </div>

                    <div className="table-record-count">
                        {patients.length} records
                    </div>

                </div>


                {loading ? (

                    <div className="table-state">
                        <div className="loading-spinner"></div>
                        <span>Loading patient records...</span>
                    </div>

                ) : error ? (

                    <div className="table-state error-state">
                        <span>{error}</span>
                    </div>

                ) : patients.length === 0 ? (

                    <div className="table-state">
                        <UserRound size={30} />
                        <span>No patients found.</span>
                    </div>

                ) : (

                    <>

                        <div className="table-wrapper">

                            <table className="patients-table">

                                <thead>

                                    <tr>
                                        <th>Patient</th>
                                        <th>Age</th>
                                        <th>City</th>
                                        <th>Department</th>
                                        <th>Insurance</th>
                                        <th>AI Risk</th>
                                        <th>Predicted LOS</th>
                                        <th></th>
                                    </tr>

                                </thead>

                                <tbody>

                                    {visiblePatients.map(
                                        (patient) => (

                                            <tr
                                                key={
                                                    patient.patient_id
                                                }
                                            >

                                                <td>

                                                    <div className="patient-cell">

                                                        <div className="patient-avatar">
                                                            {patient.patient_id
                                                                ?.slice(-2)}
                                                        </div>

                                                        <div>

                                                            <div className="patient-id">
                                                                {
                                                                    patient.patient_id
                                                                }
                                                            </div>

                                                            <div className="patient-gender">
                                                                {
                                                                    patient.gender
                                                                }
                                                            </div>

                                                        </div>

                                                    </div>

                                                </td>


                                                <td>
                                                    {patient.patient_age}
                                                </td>


                                                <td>
                                                    {patient.city}
                                                </td>


                                                <td>
                                                    <span className="department-badge">
                                                        {
                                                            patient.department_name
                                                        }
                                                    </span>
                                                </td>


                                                <td>
                                                    {
                                                        patient.insurance_type
                                                    }
                                                </td>


                                                <td>

                                                    <span
                                                        className={`risk-badge ${getRiskClass(
                                                            patient.risk_category
                                                        )}`}
                                                    >

                                                        <span className="risk-badge-dot"></span>

                                                        {
                                                            patient.risk_category
                                                        }

                                                    </span>

                                                </td>


                                                <td>

                                                    <span className="los-value">
                                                        {
                                                            patient.predicted_length_of_stay
                                                        }

                                                        <small>
                                                            {" "}days
                                                        </small>
                                                    </span>

                                                </td>


                                                <td>

                                                    <button
                                                        className="view-patient-button"
                                                        onClick={() =>
                                                            navigate(
                                                                `/patient-360?patient=${patient.patient_id}`
                                                            )
                                                        }
                                                    >
                                                        View
                                                        <ArrowUpRight
                                                            size={14}
                                                        />
                                                    </button>

                                                </td>

                                            </tr>

                                        )
                                    )}

                                </tbody>

                            </table>

                        </div>


                        {/* Pagination */}

                        <div className="table-pagination">

                            <div className="pagination-info">

                                Showing{" "}
                                <strong>
                                    {startIndex + 1}
                                </strong>{" "}
                                to{" "}
                                <strong>
                                    {Math.min(
                                        startIndex +
                                            rowsPerPage,
                                        patients.length
                                    )}
                                </strong>{" "}
                                of{" "}
                                <strong>
                                    {patients.length}
                                </strong>

                            </div>


                            <div className="pagination-buttons">

                                <button
                                    disabled={page === 1}
                                    onClick={() =>
                                        setPage(
                                            (previous) =>
                                                previous - 1
                                        )
                                    }
                                >
                                    <ChevronLeft size={15} />
                                </button>

                                <span>
                                    {page} / {totalPages || 1}
                                </span>

                                <button
                                    disabled={
                                        page === totalPages ||
                                        totalPages === 0
                                    }
                                    onClick={() =>
                                        setPage(
                                            (previous) =>
                                                previous + 1
                                        )
                                    }
                                >
                                    <ChevronRight size={15} />
                                </button>

                            </div>

                        </div>

                    </>

                )}

            </div>

        </div>
    );
}

export default Patients;