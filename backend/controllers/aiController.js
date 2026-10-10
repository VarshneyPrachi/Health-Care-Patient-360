const pool = require("../config/db");

// AI summary
const getAISummary = async (req, res) => {
    try {
        const [rows] = await pool.query(`
            SELECT
                COUNT(DISTINCT patient_id) AS total_patients,
                ROUND(AVG(readmission_probability) * 100, 2) AS avg_readmission_risk,
                ROUND(AVG(predicted_length_of_stay), 2) AS avg_predicted_los
            FROM ml_patient_360
        `);

        res.json({
            status: "success",
            data: rows[0]
        });

    } catch (error) {
        console.error("AI summary error:", error.message);

        res.status(500).json({
            status: "error",
            message: "Failed to fetch AI summary",
            error: error.message
        });
    }
};


// Risk distribution
const getRiskDistribution = async (req, res) => {
    try {
        const [rows] = await pool.query(`
            SELECT
                risk_category,
                COUNT(DISTINCT patient_id) AS patient_count
            FROM ml_patient_360
            GROUP BY risk_category
            ORDER BY patient_count DESC
        `);

        res.json({
            status: "success",
            data: rows
        });

    } catch (error) {
        console.error("Risk distribution error:", error.message);

        res.status(500).json({
            status: "error",
            message: "Failed to fetch risk distribution",
            error: error.message
        });
    }
};


// Risk by department
const getRiskByDepartment = async (req, res) => {
    try {
        const [rows] = await pool.query(`
            SELECT
                department_name,
                COUNT(DISTINCT patient_id) AS patients,
                ROUND(AVG(readmission_probability) * 100, 2) AS avg_readmission_risk
            FROM ml_patient_360
            GROUP BY department_name
            ORDER BY avg_readmission_risk DESC
        `);

        res.json({
            status: "success",
            data: rows
        });

    } catch (error) {
        console.error("Risk by department error:", error.message);

        res.status(500).json({
            status: "error",
            message: "Failed to fetch department risk",
            error: error.message
        });
    }
};


// Patient-specific AI risk
const getPatientAIRisk = async (req, res) => {
    try {
        const { id } = req.params;

        const [rows] = await pool.query(
            `
            SELECT
                patient_id,
                admission_id,
                patient_age,
                department_name,
                doctor_name,
                previous_admissions,
                days_since_previous_admission,
                diagnosis_count,
                treatment_count,
                lab_test_count,
                abnormal_lab_count,
                readmission_probability,
                readmission_probability_pct,
                risk_category,
                predicted_length_of_stay,
                predicted_los_category,
                prediction_error_days,
                absolute_prediction_error_days
            FROM ml_patient_360
            WHERE patient_id = ?
            `,
            [id]
        );

        if (rows.length === 0) {
            return res.status(404).json({
                status: "error",
                message: "Patient AI data not found"
            });
        }

        res.json({
            status: "success",
            patient_id: id,
            data: rows
        });

    } catch (error) {
        console.error("Patient AI error:", error.message);

        res.status(500).json({
            status: "error",
            message: "Failed to fetch patient AI data",
            error: error.message
        });
    }
};


// Predicted LOS distribution
const getLOSDistribution = async (req, res) => {
    try {
        const [rows] = await pool.query(`
            SELECT
                predicted_los_category,
                COUNT(DISTINCT patient_id) AS patient_count,
                ROUND(AVG(predicted_length_of_stay), 2) AS average_predicted_los
            FROM ml_patient_360
            GROUP BY predicted_los_category
            ORDER BY patient_count DESC
        `);

        res.json({
            status: "success",
            data: rows
        });

    } catch (error) {
        console.error("LOS distribution error:", error.message);

        res.status(500).json({
            status: "error",
            message: "Failed to fetch LOS distribution",
            error: error.message
        });
    }
};


module.exports = {
    getAISummary,
    getRiskDistribution,
    getRiskByDepartment,
    getPatientAIRisk,
    getLOSDistribution
};