var express = require('express');
var router = express.Router();
var config = require('../../shared/config');
var controller = require("../controllers/manager_controller");

// Report
router.get('/', function (req, res, next) {
  res.locals.is_monthly_report = true; 
  next();
}, controller.get_monthly_report);

router.get('/annualreport', function (req, res, next) {
  res.locals.is_annual_report = true; next();
}, controller.get_annual_report);

// Bookings
router.get('/searchbooking', function (req, res, next) {
  res.locals.is_bookings = true; next();
}, controller.get_bookings);

router.get('/booking/:id', function (req, res, next) {
  next();
}, controller.get_booking_by_id);

// Account
router.get('/account/', function (req, res) {
  res.render('account');
});

router.get('/logout', (req, res) => {
  res.redirect(`${req.protocol}://${req.hostname}:${process.env.AUTH_PORT}` + '/logout');
})

module.exports = router;
