const config = require('../config');
const user_service = require("./user_service");
middleware = {
    auth: async (req, res, next) => {
        const auth_domain = `${req.protocol}://${req.hostname}:${process.env.AUTH_PORT}`;
        const manager_domain = `${req.protocol}://${req.hostname}:${process.env.MANAGER_PORT}`;
        const receptionist_domain = `${req.protocol}://${req.hostname}:${process.env.RECEPTIONIST_PORT}`;
        const executive_domain = `${req.protocol}://${req.hostname}:${process.env.EXECUTIVE_PORT}`;
        const currentPort = req.headers.host.split(':')[1];
        if (currentPort === config.auth_port && req.path === '/logout') {
            next(); 
            return;
        }
        auth_token = req.cookies.auth_token;
        if (!auth_token) {
            if (currentPort === config.auth_port && (req.path === '/signin') || (req.path === '/signup')) {
                next(); 
                return;
            }
            res.redirect(auth_domain + '/signin');
            return
        }
        res.locals.user = await user_service.get_profile(req, res);
        if (!res.locals.user) {
            res.redirect(auth_domain + '/signin');
            return
        }
        if (res.locals.user.Role == "Executive") {
            res.locals.user.isExecutive = true;
        } else if (res.locals.user.Role == "Receptionist") {
            res.locals.user.isReceptionist = true;
        } else if (res.locals.user.Role == "Manager") {
            res.locals.user.isManager = true;
        }
        if (res.locals.user.token) {
            res.cookie('auth_token', res.locals.user.token);
        }
        if (res.locals.user.Role == "Executive" && currentPort !== config.executive_port) {
            res.redirect(executive_domain);
        } else if (res.locals.user.Role == "Receptionist" && currentPort !== config.receptionist_port) {
            res.redirect(receptionist_domain);
        } else if (res.locals.user.Role == "Manager" && currentPort !== config.manager_port) {
            res.redirect(manager_domain);
        } else {
            next();
        }
    },
}


module.exports = middleware;