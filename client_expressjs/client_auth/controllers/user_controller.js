const fetch_data = require('../../shared/utils/fetch_data');
const config = require("../../shared/config");
const user_service = require("../../shared/services/user_service");
controller = {
    middle_signin : function (req, res, next) {
        res.locals.error = [];
        if (!('email' in req.body) || !('password' in req.body)) {
            res.locals.error.push("Missing email or password!");
        }
        if (req.body["email"].trim() == "" || req.body["password"].trim() == ""  ) {
            res.locals.email = req.body["email"];
            res.locals.error.push("Empty email or password!");
            res.render('signin');
            return;
        } else {
            next();
        }
    },
    post_signin : async function (req, res) {
        user_service.post_signin(req, res);
    },
    get_signin : function (req, res) {
        res.render('signin');
    },
    get_signup : function (req, res) {
        res.render('signup');
    },
    get_signout : function (req, res) {
        user_service.get_signout(req, res);
    }
}

module.exports = controller;