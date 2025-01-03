from datetime import datetime, timedelta
from models.booking_model import Booking
from models.room_model import Room
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized


class BookingService:
    def __init__(self):
        self.booking_repo = Booking
        self.room_repo = Room

    def get_bookings(self, request, areas=[]):
        date = request.get("date") or request.get("check_in")
        room_id = request.get("room_id")
        customer_name = request.get("customer_name")
        category = request.get("category")
        limit = int(request.get("limit", 0))
        page = int(request.get("page", 1))
        conditions = ""
        if date:
            conditions += f"'{date}' between b.CheckInDate and DATE_ADD(b.CheckInDate, INTERVAL b.Nights DAY)"
        if room_id:
            if conditions:
                conditions += " and "
            conditions += f"b.Room_Id = {room_id}"
        if category:
            if conditions:
                conditions += " and "
            conditions += f"ca.Name = '{category}'"
        if customer_name:
            if conditions:
                conditions += " and "
            conditions += f"c.Fullname like '%{customer_name}%'"
        if len(areas) > 0:
            if conditions:
                conditions += " and "
            list_area = ",".join([str(area.get("Area_Id")) for area in areas if "Area_Id" in area])
            conditions += f"a.Id in ({list_area})"
        if conditions:
            conditions = "where " + conditions
        data = {}
        data["count"] = Booking.get_count_bookings(conditions)
        if limit < 0 or page <= 0:
            raise BadRequest("limit and page must be positive integers")
        offset = (page - 1) * limit
        limitoffset = ""
        if limit > 0:
            limitoffset += f" LIMIT {limit} OFFSET {offset}"
        data["bookings"] = Booking.get_all_bookings(conditions, limitoffset)
        data["categories"] = Room.get_all_categories()
        return {"status": 200, "data": data}

    def get_booking_by_id(self, booking_id, areas=[]):
        data = Booking.get_booking_by_id(booking_id)
        if len(data) > 0:
            booking = data[0]
            booking["Customers"] = Booking.get_customer_by_booking_id(booking_id)
            return {"data": booking, "status": 200}
        else:
            raise NotFound("Booking not found")

    def add_booking(self, request):
        try:
            if (self.get_bookings(request)["data"]["count"] > 0):
                raise BadRequest("Room is not available")
            room_id = int(request.get("room_id"))
            total = float(request.get("total"))
            status = request.get("status")
            customers = request.get("customers")
            check_in = request.get("check_in")
            if check_in < datetime.now().strftime("%Y-%m-%d"):
                raise BadRequest("Check-in date must be in the future")
            check_out = request.get("check_out")
            nights = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
            if nights <= 0:
                raise BadRequest("Check-out date must be after check-in date")
            if not (room_id and total and status and customers and check_in and check_out):
                raise BadRequest("Missing data")
            if not self.check_status(status):
                raise BadRequest("Invalid status")
            if len(customers) == 0:
                raise BadRequest("Customers don't have value")
            room = self.room_repo.get_room_by_id(room_id)
            if not room:
                raise NotFound("Room not found")
            if room[0]["Status"] != "available":
                raise BadRequest("Room is not available")
            newbooking = self.booking_repo.add_booking(room_id, check_in, nights, total, status)
            for customer in customers:
                if customer["CitizenId"] != "":
                    self.booking_repo.add_customer(customer["Fullname"], customer["CitizenId"])
                    newCustomer = self.booking_repo.get_customer_by_citizen_id(customer["CitizenId"])
                    self.booking_repo.add_booking_customer(newbooking, newCustomer["Id"])
            return {"status": 201}
        except ValueError:
            raise BadRequest("Incorrect data")


    def update_booking(self, booking_id, request):
        status = request.get("status")
        if not self.check_status(status):
            raise BadRequest("Invalid status")
        self.booking_repo.update_booking(booking_id, status)
        return {"status": 200}

    def delete_booking(self, booking_id):
        self.booking_repo.update_booking(booking_id, "cancelled")
        return {"status": 200}

    def check_status(self, status):
        if status not in ["booked", "paid", "prepaid", "cancelled"]:
            return False
        return True

    def get_new_booking(self, areas, request):
        if len(areas) == 0 and 'room_id' not in request:
            raise Unauthorized("Unauthorized")
        new_booking = {}
        room = Room.get_room_by_id(request['room_id'])
        if room is None or len(room) == 0:
            raise Unauthorized("Unauthorized")
        if room[0]["Status"] != "available":
            raise Unauthorized("Unauthorized")
        new_booking["CheckInDate"] = request.get("check_in") or datetime.now().strftime("%Y-%m-%d")
        new_booking["CheckOutDate"] = request.get("check_out") or (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        new_booking["room_id"] = request.get("room_id")
        new_booking["RoomNumber"] = room[0]["RoomNumber"]
        new_booking["PricePerNight"]=room[0]["PricePerNight"]
        numberNight = (datetime.strptime(new_booking["CheckOutDate"], "%Y-%m-%d") - datetime.strptime(new_booking["CheckInDate"], "%Y-%m-%d")).days
        new_booking["Total"]=new_booking["PricePerNight"]*numberNight
        new_booking["Customers"]=[]
        for i in range(room[0]["NumberOfGuests"]):
            new_booking["Customers"].append({"FullName":"", "CitizenId":""})
        new_booking["status_list"] = ["booked", "paid", "prepaid", "cancelled"]
        new_booking["Status"] = new_booking["status_list"][0]
        return new_booking
