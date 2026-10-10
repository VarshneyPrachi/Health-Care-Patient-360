const pool = require("../config/db");

const getDashboardSummary = async (req, res) => {
    try {
        const [rows] = await pool.query(`
            SELECT
                COUNT(DISTINCT a.patient_id) AS total_patients,
                COUNT(DISTINCT a.admission_id) AS total_admissions,
                ROUND(AVG(a.length_of_stay), 2) AS average_los,
                ROUND(SUM(COALESCE(b.total_bill, 0)), 2) AS total_revenue
            FROM admissions a
            LEFT JOIN billing b
                ON a.admission_id = b.admission_id
        `);

        res.json({
            status: "success",
            data: {
                patients: Number(rows[0].total_patients),
                admissions: Number(rows[0].total_admissions),
                average_los: Number(rows[0].average_los),
                total_revenue: Number(rows[0].total_revenue)
            }
        });

    } catch (error) {
        console.error(
            "Dashboard API error:",
            error.message
        );

        res.status(500).json({
            status: "error",
            message: "Failed to fetch dashboard summary",
            error: error.message
        });
    }
};

module.exports = {
    getDashboardSummary
};