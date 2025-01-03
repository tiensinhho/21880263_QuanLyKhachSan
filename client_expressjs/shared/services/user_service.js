const fetch_data = require('../utils/fetch_data');
const {data_domain} = require("../config");

user_service = {
    get_profile: async (req, res) => {
        try {
            auth_token = req.cookies.auth_token;
            const response = await fetch_data.post(data_domain + '/users/profile', auth_token, {});
            const port = `${req.protocol}://${req.hostname}` === process.env.SERVER_URL ? process.env.DATA_PORT : process.env.IMAGE_PORT;
            response["ImageURL"] = `${req.protocol}://${req.hostname}:${port}` + response["ImageURL"];
            return response;
        } catch (error) {
            return error.data;
        }
    },
    post_signin: async (req, res) => {
        try {
            const response = await fetch_data.post(data_domain + '/users/login', null, req.body);
            res.cookie('auth_token', response.token);
            res.redirect('/');
        } catch (error) {
            console.error("Error during login:", error);
            res.locals.error = res.locals.error || []; 
            if (error.response && error.response.data && error.response.data.description) {
                res.locals.error.push(error.response.data.description);
            } else {
                res.locals.error.push('An error occurred during login. Please try again later.');
            }
            res.render("signin");        
        }
    },
    get_signout: async (req, res) => {
        res.clearCookie('auth_token');
        res.redirect('/signin');
    }
}

module.exports = user_service;