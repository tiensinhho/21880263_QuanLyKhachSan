var express = require('express');
var router = express.Router();
var config = require('../../shared/config');
var controller = require("../controllers/executive_controller");

// Report
router.get('/', function (req, res, next) {
  res.locals.is_monthly_report = true; 
  next();
}, controller.get_monthly_report);

router.get('/annualreport', function (req, res, next) {
  res.locals.is_annual_report = true; next();
}, controller.get_annual_report);

// Category
router.get('/updateprice', function (req, res, next) {
  res.locals.is_category = true; next();
}, controller.get_category);

router.post("/updateprice", function (req, res, next) {
  if (!req.body.category_id || !req.body.price) {
    res.locals.error = "<div class='alert alert-danger' role='alert'>Category ID and price are required</div>";
  }
  if (parseFloat(req.body.price) <= 0) {
    res.locals.error = "<div class='alert alert-danger' role='alert'>Price must be greater than 0</div>";
  }
  res.locals.is_category = true;
  if (res.locals.error){
    res.render("room_category");
    return;
  }
   next();
}, controller.update_price);

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
