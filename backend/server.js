const express = require("express");
const cors = require("cors");
require("dotenv").config();

const pool = require("./config/db");
const patientRoutes = require("./routes/patientRoutes");
const dashboardRoutes = require("./routes/dashboardRoutes");
const operationsRoutes = require("./routes/operationsRoutes");
const financialRoutes = require("./routes/financialRoutes");
const aiRoutes = require("./routes/aiRoutes");

const app = express();

app.use(cors());
app.use(express.json());

// API routes
app.use("/api/patients", patientRoutes);
app.use("/api/dashboard", dashboardRoutes);
app.use("/api/operations", operationsRoutes);
app.use("/api/financial", financialRoutes);
app.use("/api/ai", aiRoutes);

// Home route
app.get("/", (req, res) => {
    res.json({
        message: "Healthcare Patient 360 API is running",
        status: "success"
    });
});

// Database health check
app.get("/api/health", async (req, res) => {
    try {
        const [rows] = await pool.query(
            "SELECT 1 AS database_connected"
        );

        res.json({
            status: "success",
            message: "Backend and MySQL are connected",
            database: rows[0].database_connected === 1
        });

    } catch (error) {
        console.error("Database error:", error.message);

        res.status(500).json({
            status: "error",
            message: "Database connection failed",
            error: error.message
        });
    }
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
    console.log(
        `Healthcare Patient 360 API running on port ${PORT}`
    );
});