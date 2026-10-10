const pool = require("../config/db");


// Financial summary
const getFinancialSummary = async (req, res) => {
    try {
        const [rows] = await pool.query(`
            SELECT
                ROUND(
                    SUM(total_bill),
                    2
                ) AS total_revenue,

                ROUND(
                    SUM(insurance_covered),
                    2
                ) AS insurance_covered,

                ROUND(
                    SUM(patient_paid),
                    2
                ) AS patient_paid,

                ROUND(
                    AVG(total_bill),
                    2
                ) AS average_bill

            FROM billing
        `);

        res.json({
            status: "success",
            data: {
                total_revenue:
                    Number(rows[0].total_revenue || 0),

                insurance_covered:
                    Number(rows[0].insurance_covered || 0),

                patient_paid:
                    Number(rows[0].patient_paid || 0),

                average_bill:
                    Number(rows[0].average_bill || 0)
            }
        });

    } catch (error) {
        console.error(
            "Financial summary error:",
            error.message
        );

        res.status(500).json({
            status: "error",
            message: "Failed to fetch financial summary",
            error: error.message
        });
    }
};


// Revenue by insurance
const getRevenueByInsurance = async (req, res) => {
    try {
        const [rows] = await pool.query(`
            SELECT
                p.insurance_type,

                ROUND(
                    SUM(b.total_bill),
                    2
                ) AS total_revenue,

                ROUND(
                    SUM(b.insurance_covered),
                    2
                ) AS insurance_covered,

                ROUND(
                    SUM(b.patient_paid),
                    2
                ) AS patient_paid

            FROM billing b

            INNER JOIN admissions a
                ON b.admission_id = a.admission_id

            INNER JOIN patients p
                ON a.patient_id = p.patient_id

            GROUP BY p.insurance_type

            ORDER BY total_revenue DESC
        `);

        res.json({
            status: "success",
            data: rows
        });

    } catch (error) {
        console.error(
            "Insurance revenue error:",
            error.message
        );

        res.status(500).json({
            status: "error",
            message: "Failed to fetch revenue by insurance",
            error: error.message
        });
    }
};


// Revenue by department
const getRevenueByDepartment = async (req, res) => {
    try {
        const [rows] = await pool.query(`
            SELECT
                d.department_name,

                ROUND(
                    SUM(b.total_bill),
                    2
                ) AS total_revenue,

                ROUND(
                    AVG(b.total_bill),
                    2
                ) AS average_bill

            FROM billing b

            INNER JOIN admissions a
                ON b.admission_id = a.admission_id

            INNER JOIN departments d
                ON a.department_id = d.department_id

            GROUP BY
                d.department_id,
                d.department_name

            ORDER BY total_revenue DESC
        `);

        res.json({
            status: "success",
            data: rows
        });

    } catch (error) {
        console.error(
            "Department revenue error:",
            error.message
        );

        res.status(500).json({
            status: "error",
            message: "Failed to fetch revenue by department",
            error: error.message
        });
    }
};


// Payment status
const getPaymentStatus = async (req, res) => {
    try {
        const [rows] = await pool.query(`
            SELECT
                payment_status,
                COUNT(*) AS count

            FROM billing

            GROUP BY payment_status

            ORDER BY count DESC
        `);

        res.json({
            status: "success",
            data: rows
        });

    } catch (error) {
        console.error(
            "Payment status error:",
            error.message
        );

        res.status(500).json({
            status: "error",
            message: "Failed to fetch payment status",
            error: error.message
        });
    }
};


module.exports = {
    getFinancialSummary,
    getRevenueByInsurance,
    getRevenueByDepartment,
    getPaymentStatus
};