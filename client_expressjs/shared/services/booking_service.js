require('dotenv').config();
const fetch_data = require('../utils/fetch_data');
const { data_domain } = require("../config");

service = {
    get_bookings: async (req, res) => {
        try {
            let path = "";
            if (res.locals.user["Role"] == "Executive") {
                path = "executive";
            } else if (res.locals.user["Role"] == "Manager") {
                path = "manager";
            } else if (res.locals.user["Role"] == "Receptionist") {
                path = "receptionist";
            } else {
                error = new Error("Invalid role");
                next(error);
                return;
            }
            const category = req.query.category || "";
            res.locals.category = category;
            const customer_name = req.query.customer_name || "";
            res.locals.customer_name = customer_name;
            const date = req.query.date || "";
            res.locals.date = date;
            const limit = req.query.limit || 7;
            const currentPage = parseInt(req.query.p) || 1;
            const response = await fetch_data.get(`${data_domain}/${path}/booking?category=${category}&customer_name=${customer_name}&date=${date}&limit=${limit}&page=${currentPage}`, req.cookies.auth_token);
            const totalItems = response['count'];
            const pageCount = Math.ceil(totalItems / limit);
            res.locals.bookings = response["bookings"];
            res.locals.pagination = {
                page: currentPage,
                pageCount: pageCount
            }
            res.locals.categories = response["categories"];
            res.render('bookings');
        } catch (error) {
            console.error("Error fetching monthly report:", error);
            res.render('bookings');
        }
    },
    get_booking_by_id: async (req, res) => {
        try {
            const booking_id = req.params.id || "";
            let path = "";
            if (res.locals.user["Role"] == "Executive") {
                path = "executive";
            } else if (res.locals.user["Role"] == "Manager") {
                path = "manager";
            } else if (res.locals.user["Role"] == "Receptionist") {
                path = "receptionist";
            } else {
                error = new Error("Invalid role");
                next(error);
                return;
            }
            const response = await fetch_data.get(`${data_domain}/${path}/booking/${booking_id}`, req.cookies.auth_token);
            res.locals.booking = response;
            res.locals.booking["disabled"] = "disabled";
            res.locals.status_list = ["booked", "paid", "prepaid", "cancelled"];
            res.render('booking_detail');
        } catch (error) {
            console.error("Error fetching monthly report:", error); res.render("booking_detail");
        }
    },
    get_new_booking: async (req, res) => {
        try {
            let path = "";
            if (res.locals.user["Role"] == "Executive") {
                path = "executive";
            } else if (res.locals.user["Role"] == "Manager") {
                path = "manager";
            } else if (res.locals.user["Role"] == "Receptionist") {
                path = "receptionist";
            } else {
                error = new Error("Invalid role");
                next(error);
                return;
            }
            const room_id = req.query.room_id || "";
            const response = await fetch_data.get(`${data_domain}/${path}/booking/new?room_id=${room_id}`, req.cookies.auth_token);
            res.locals.booking = response;
            res.locals.status_list = ["booked", "prepaid"];
            res.render('booking_new');
        } catch (error) {
            console.error("Error fetching monthly report:", error);
            res.render('booking_new');
        }
    },
    post_new_booking: async (req, res) => {
        try {
            let path = "";
            if (res.locals.user["Role"] == "Executive") {
                path = "executive";
            } else if (res.locals.user["Role"] == "Manager") {
                path = "manager";
            } else if (res.locals.user["Role"] == "Receptionist") {
                path = "receptionist";
            } else {
                error = new Error("Invalid role");
                next(error);
                return;
            }
            const citizenIds = req.body["citizenid[]"] || [];
            const fullnames = req.body["fullname[]"] || [];
            const customers = [];
            const numCustomers = Math.min(citizenIds.length, fullnames.length);
            for (let i = 0; i < numCustomers; i++) {
                customers.push({
                    CitizenId: citizenIds[i],
                    Fullname: fullnames[i],
                });
            }
            const data = {
                room_id: req.body.room_id || "",
                check_in: req.body.check_in || "",
                check_out: req.body.check_out || "",
                customers: customers, 
                status: req.body.status || "",
                total: req.body.total || "",
            };
            const response = await fetch_data.post(`${data_domain}/${path}/booking/new`, req.cookies.auth_token, data);
            res.locals.message = response.message;
            res.render('booking_new');
        } catch (error) {
            console.error("Error:", error);
            res.render('booking_new', {error: error.response?.data?.description || error});
        }
    },
    put_booking_by_id: async (req, res) => {
        try {
            let path = "";
            if (res.locals.user["Role"] == "Executive") {
                path = "executive";
            } else if (res.locals.user["Role"] == "Manager") {
                path = "manager";
            } else if (res.locals.user["Role"] == "Receptionist") {
                path = "receptionist";
            } else {
                error = new Error("Invalid role");
                next(error);
                return;
            }
            const booking_id = req.params.id || "";
            const status = {status: req.body.status};
            const response = await fetch_data.put(`${data_domain}/${path}/booking/${booking_id}`, req.cookies.auth_token, status);
            res.locals.message = response.message;
            res.render('booking_detail');
        } catch (error) {
            console.error("Error:", error);
            res.render('booking_detail', {error: error.response?.data?.description || error});
        }
    }
}

module.exports = service;