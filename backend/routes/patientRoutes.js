const express = require("express");

const {
    getPatients,
    getPatientById
} = require("../controllers/patientController");

const router = express.Router();

// Get all patients / search patients
router.get("/", getPatients);

// Get specific patient
router.get("/:id", getPatientById);

module.exports = router;