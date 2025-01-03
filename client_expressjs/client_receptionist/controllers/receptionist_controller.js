const room_service = require("../../shared/services/room_service");
const booking_service = require("../../shared/services/booking_service");
const { put } = require("../../shared/utils/fetch_data");

controller = {
    get_rooms: async (req, res) => {
        room_service.get_rooms(req, res);
    },
    get_bookings: async (req, res) => {
        booking_service.get_bookings(req, res);
    },
    get_booking_by_id: async (req, res) => {
        booking_service.get_booking_by_id(req, res);
    },
    get_new_booking: async (req, res) => {
        booking_service.get_new_booking(req, res);
    },
    post_new_booking: async (req, res) => {
        booking_service.post_new_booking(req, res);
    },
    put_booking_by_id: async (req, res) => {
        booking_service.put_booking_by_id(req, res);
    }
}

module.exports = controller;