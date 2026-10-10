const pool = require("../config/db");

// Get all patients / search patients
const getPatients = async (req, res) => {
    try {
        const { search } = req.query;

        let query = `
            SELECT
                patient_id,
                patient_age,
                gender,
                city,
                insurance_type,
                department_name,
                risk_category,
                readmission_probability_pct,
                predicted_length_of_stay
            FROM ml_patient_360
        `;

        const params = [];

        if (search) {
            query += `
                WHERE patient_id LIKE ?
                OR city LIKE ?
                OR department_name LIKE ?
            `;

            const searchValue = `%${search}%`;

            params.push(
                searchValue,
                searchValue,
                searchValue
            );
        }

        query += `
            ORDER BY patient_id
            LIMIT 100
        `;

        const [rows] = await pool.query(query, params);

        res.json({
            status: "success",
            count: rows.length,
            patients: rows
        });

    } catch (error) {
        console.error("Patients API error:", error.message);

        res.status(500).json({
            status: "error",
            message: "Failed to fetch patients",
            error: error.message
        });
    }
};


// Get one patient's complete Patient 360 data
const getPatientById = async (req, res) => {
    try {
        const { id } = req.params;

        const [rows] = await pool.query(
            `
            SELECT *
            FROM ml_patient_360
            WHERE patient_id = ?
            `,
            [id]
        );

        if (rows.length === 0) {
            return res.status(404).json({
                status: "error",
                message: "Patient not found"
            });
        }

        res.json({
            status: "success",
            patient: rows
        });

    } catch (error) {
        console.error("Patient API error:", error.message);

        res.status(500).json({
            status: "error",
            message: "Failed to fetch patient data",
            error: error.message
        });
    }
};

module.exports = {
    getPatients,
    getPatientById
};