var express = require('express');
var router = express.Router();
var config = require('../../shared/config');
var controller = require("../controllers/receptionist_controller");

/* home page. */
router.get('/', function (req, res, next) {
  res.locals.is_rooms = true;
  next();
}, controller.get_rooms);

// Bookings
router.get('/booking/', function (req, res, next) {
  res.locals.is_bookings = true;
  next();
}, controller.get_bookings);

router.get('/booking/new', controller.get_new_booking);

router.post('/booking/new', controller.post_new_booking);

router.get('/booking/:id', controller.get_booking_by_id);

router.post('/booking/:id', controller.put_booking_by_id);

// Account
router.get('/account/', function (req, res) {
  res.render('account');
});

router.get('/logout/', function (req, res) {
  res.redirect(`${req.protocol}://${req.hostname}:${process.env.AUTH_PORT}` + '/logout');
});


module.exports = router;
