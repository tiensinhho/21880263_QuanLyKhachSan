require('dotenv').config();
const fetch_data = require('../utils/fetch_data');
const {data_domain} = require("../config");


service ={
    get_monthly_report: async (req, res, next) => {
        try {
            const today = new Date();
            let path = "";
            if (res.locals.user["Role"] == "Executive") {
                path = "executive";
            } else if (res.locals.user["Role"] == "Manager") {
                path = "manager";
            } else {
                error = new Error("Invalid role");
                next(error);
                return;
            }
            const year = req.query.year || today.getFullYear();
            const month = req.query.month || today.getMonth() + 1;
            const response = await fetch_data.get(`${data_domain}/${path}/reports/monthly?month=${month}&year=${year}`, req.cookies.auth_token, {});
            res.locals.report = response;
            let label= [];
            let data= [];
            let backgroundColor=  [];
            for (let i=0 ; i < response.Details.length; i++) {
                label[i] = (response.Details[i].CategoryName) , 
                data[i] = (response.Details[i].Percent), 
                backgroundColor[i] = (`"rgba(${(i+1)*10}, 156, 255, 0.${i+1})"`);
            }
            res.locals.label = "['" + label.join("', '") + "']";
            res.locals.backgroundColor = "[" + backgroundColor.join(", ") + "]"
            res.locals.data = "[" + data.join(", ") + "]"
            res.locals.year = year;
            res.locals.month = month;
            res.render('report_monthly');
        } catch (error) {
            console.error("Error fetching monthly report:", error);
            res.render('report_monthly');
        }
    },
    get_annual_report: async (req, res) => {
        const today = new Date();
        let path = "";
        if (res.locals.user["Role"] == "Executive") {
            path = "executive";
        } else if (res.locals.user["Role"] == "Manager") {
            path = "manager";
        } else {
            error = new Error("Invalid role");
            next(error);
            return;
        }
        const year = req.query.year || today.getFullYear();
        const response = await fetch_data.get(`${data_domain}/${path}/reports/annual?year=${year}`, req.cookies.auth_token, {});
        res.locals.report = response;
        let label= [];
        let data= [];
        let backgroundColor=  [];
        for (let i=0 ; i < response.Details.length; i++) {
            label[i] = (response.Details[i].Month) , 
            data[i] = (response.Details[i].Percent), 
            backgroundColor[i] = (`"rgba(0, 156, 255, 0.${i+1})"`);
        }
        res.locals.label = "['" + label.join("', '") + "']";
        res.locals.backgroundColor = "[" + backgroundColor.join(", ") + "]"
        res.locals.data = "[" + data.join(", ") + "]"
        res.locals.year = year;
        res.render('report_annual');
    }
}

module.exports = service