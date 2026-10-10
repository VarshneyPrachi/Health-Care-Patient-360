const express = require("express");

const {
    getFinancialSummary,
    getRevenueByInsurance,
    getRevenueByDepartment,
    getPaymentStatus
} = require("../controllers/financialController");

const router = express.Router();

router.get("/summary", getFinancialSummary);

router.get("/by-insurance", getRevenueByInsurance);

router.get("/by-department", getRevenueByDepartment);

router.get("/payment-status", getPaymentStatus);

module.exports = router;