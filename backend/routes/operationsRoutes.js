const express = require("express");

const {
    getDepartmentPerformance,
    getDoctorPerformance,
    getLabAnalytics
} = require("../controllers/operationsController");

const router = express.Router();

router.get("/departments", getDepartmentPerformance);

router.get("/doctors", getDoctorPerformance);

router.get("/labs", getLabAnalytics);

module.exports = router;