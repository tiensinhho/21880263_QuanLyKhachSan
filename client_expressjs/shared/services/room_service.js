require('dotenv').config();
const fetch_data = require('../utils/fetch_data');
const {data_domain} = require("../config");
const booking_service = require("./booking_service");

service= {
    get_category: async (req, res) => {
        try {
            const category_name = req.query.category_name || "";
            let path = "";
            if (res.locals.user["Role"] == "Executive") {
                path = "executive";
            } else {
                error = new Error("Invalid role");
                next(error);
                return;
            }
            const data = await fetch_data.get(`${data_domain}/${path}/category?name=${category_name}`, req.cookies.auth_token, {});
            res.locals.category = data;
            res.locals.category_name = category_name;
            res.render('room_category');
        } catch (error) {
            console.error("Error fetching monthly report:", error);
            res.render('room_category');
        }
    },
    update_price: async (req, res) => {
        try {
            category_id = req.body.category_id || "";
            const price = parseFloat(req.body.price) || 0;
            if (price <= 0) {
                res.render("room_category", {error: "Price must be greater than 0"});
                return;
            }
            const newprice = {price: price}
            let path = "";
            if (res.locals.user["Role"] == "Executive") {
                path = "executive";
            } else {
                error = new Error("Invalid role");
                next(error);
                return;
            }
            const data = await fetch_data.put(`${data_domain}/${path}/category/${category_id}`, req.cookies.auth_token, newprice);
            res.redirect(req.originalUrl); 
        } catch (error) {
            console.error("Error fetching monthly report:", error);
            res.render('room_category');
        }
    },
    get_rooms: async (req, res) => {
        try {
            let path = "";
            if (res.locals.user["Role"] == "Receptionist") {
                path = "receptionist";
            } else if (res.locals.user["Role"] == "Manager") {
                path = "manager";
            } else if (res.locals.user["Role"] == "Executive") {
                path = "executive";
            } else {
                error = new Error("Invalid role");
                next(error);
                return;
            }
            const category = req.query.category || "";
            const room_name = req.query.room_name || "";
            const datefrom = req.query.datefrom || "";
            const dateto = req.query.dateto || "";
            const status = req.query.status || "";
            const itemsPerPage = req.query.limit || 7; 
            const currentPage = parseInt(req.query.p) || 1;
            const token = req.cookies.auth_token;
            const response = await fetch_data.get(`${data_domain}/${path}/rooms/?limit=${itemsPerPage}&page=${currentPage}&category=${category}&room_name=${room_name}&datefrom=${datefrom}&dateto=${dateto}&status=${status}`, token);
            const totalItems = response['count']; 
            const pageCount = Math.ceil(totalItems / itemsPerPage);
            res.locals.rooms = response["rooms"];
            for (let room of res.locals.rooms) {
                const port = `${req.protocol}://${req.hostname}` === process.env.SERVER_URL ? process.env.DATA_PORT : process.env.IMAGE_PORT;
                room["ImageURL"] = `${req.protocol}://${req.hostname}:${port}` + room["ImageURL"] || "";
            }
            res.locals.status = response["possible_statuses"];
            res.locals.categories = response["categories"];   
            res.locals.category = category;
            res.locals.room_name = room_name;
            res.locals.datefrom = datefrom;
            res.locals.dateto = dateto;
            res.locals.status = status;         
            res.locals.pagination = {
                page: currentPage,
                pageCount: pageCount
            }
            res.render('rooms');
        } catch (error) {
            return error.data;
        }
    }

}

module.exports = service;