const report_service = require('../../shared/services/report_service');
const room_service = require("../../shared/services/room_service");
const booking_service = require("../../shared/services/booking_service");
controller = {
    get_monthly_report: async (req, res) => {
        report_service.get_monthly_report(req, res);
    },
    get_annual_report: async (req, res) => {
        report_service.get_annual_report(req, res);
    },
    get_category: async (req, res) => {
        room_service.get_category(req, res);
    },
    update_price: async (req, res) => {
        room_service.update_price(req, res);
    },
    get_bookings: async (req, res) => {
        booking_service.get_bookings(req, res);
    },
    get_booking_by_id: async (req, res) => {
        booking_service.get_booking_by_id(req, res);
    }
};

module.exports = controller;