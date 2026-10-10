const pool = require("../config/db");

// Department performance
const getDepartmentPerformance = async (req, res) => {
    try {
        const [rows] = await pool.query(`
            SELECT
                d.department_name,

                COUNT(a.admission_id) AS admissions,

                ROUND(
                    AVG(a.length_of_stay),
                    2
                ) AS average_los,

                SUM(
                    CASE
                        WHEN a.admission_type = 'Emergency'
                        THEN 1
                        ELSE 0
                    END
                ) AS emergency_admissions

            FROM admissions a

            INNER JOIN departments d
                ON a.department_id = d.department_id

            GROUP BY
                d.department_id,
                d.department_name

            ORDER BY admissions DESC
        `);

        res.json({
            status: "success",
            data: rows
        });

    } catch (error) {
        console.error(
            "Department API error:",
            error.message
        );

        res.status(500).json({
            status: "error",
            message: "Failed to fetch department performance",
            error: error.message
        });
    }
};


// Doctor workload
const getDoctorPerformance = async (req, res) => {
    try {
        const [rows] = await pool.query(`
            SELECT
                doc.doctor_name,
                d.department_name,

                COUNT(a.admission_id) AS admissions,

                ROUND(
                    AVG(a.length_of_stay),
                    2
                ) AS average_los

            FROM admissions a

            INNER JOIN doctors doc
                ON a.doctor_id = doc.doctor_id

            INNER JOIN departments d
                ON a.department_id = d.department_id

            GROUP BY
                doc.doctor_id,
                doc.doctor_name,
                d.department_name

            ORDER BY admissions DESC
        `);

        res.json({
            status: "success",
            data: rows
        });

    } catch (error) {
        console.error(
            "Doctor API error:",
            error.message
        );

        res.status(500).json({
            status: "error",
            message: "Failed to fetch doctor performance",
            error: error.message
        });
    }
};


// Laboratory analytics
const getLabAnalytics = async (req, res) => {
    try {
        const [rows] = await pool.query(`
            SELECT
                test_name,

                COUNT(*) AS total_tests,

                SUM(
                    CASE
                        WHEN result_status = 'Abnormal'
                        THEN 1
                        ELSE 0
                    END
                ) AS abnormal_tests

            FROM lab_results

            GROUP BY test_name

            ORDER BY total_tests DESC
        `);

        res.json({
            status: "success",
            data: rows
        });

    } catch (error) {
        console.error(
            "Lab API error:",
            error.message
        );

        res.status(500).json({
            status: "error",
            message: "Failed to fetch laboratory analytics",
            error: error.message
        });
    }
};


module.exports = {
    getDepartmentPerformance,
    getDoctorPerformance,
    getLabAnalytics
};