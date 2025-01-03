var express = require('express');
var router = express.Router();
var user_controller = require("../controllers/user_controller");

/* GET home page. */
router.get('/signin', user_controller.get_signin);

router.post('/signin', user_controller.middle_signin, user_controller.post_signin );

router.get('/signup', user_controller.get_signup);

router.get('/logout', user_controller.get_signout);

module.exports = router;
