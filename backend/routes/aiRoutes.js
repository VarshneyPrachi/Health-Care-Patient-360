const express = require("express");

const {
    getAISummary,
    getRiskDistribution,
    getRiskByDepartment,
    getPatientAIRisk,
    getLOSDistribution
} = require("../controllers/aiController");

const router = express.Router();

router.get("/summary", getAISummary);
router.get("/risk-distribution", getRiskDistribution);
router.get("/risk-by-department", getRiskByDepartment);
router.get("/patient/:id", getPatientAIRisk);
router.get("/los-distribution", getLOSDistribution);

module.exports = router;