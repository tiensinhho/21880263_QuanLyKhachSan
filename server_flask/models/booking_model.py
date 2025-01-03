from models.database import Database


class Booking:
    @staticmethod
    def get_all_bookings(conditions="", limitoffset=""):
        query = f"select distinct b.id  , b.Room_Id, concat(a.Name, f.Name, LPAD(r.Name, 2, '0')) as RoomNumber, DATE_FORMAT(b.CheckInDate, '%Y-%m-%d') as Check_In, DATE_FORMAT(DATE_ADD(b.CheckInDate, INTERVAL b.Nights DAY), '%Y-%m-%d') as Check_Out, ca.Name as Category, b.Status, b.Total, c.Fullname FROM Bookings b join Booking_Customer bc on b.id   = bc.Booking_Id join Customers c on bc.Customer_Id = c.id join Rooms r on b.Room_Id = r.Id join Floors f on r.Floor_Id = f.Id join Areas a on f.Area_Id = a.Id join Categories ca on r.Category_Id = ca.Id {conditions} order by DATE_FORMAT(b.CheckInDate, '%Y-%m-%d') desc {limitoffset}"
        result = Database.execute_query(query)
        return result if result else None

    @staticmethod
    def get_count_bookings(conditions=""):
        query = f"select count(distinct b.id) as count FROM Bookings b join Booking_Customer bc on b.id = bc.Booking_Id join Customers c on bc.Customer_Id = c.id join Rooms r on b.Room_Id = r.Id join Floors f on r.Floor_Id = f.Id join Areas a on f.Area_Id = a.Id join Categories ca on r.Category_Id = ca.Id {conditions}"
        return Database.execute_query(query)[0]["count"]

    @staticmethod
    def get_booking_by_id(booking_id):
        query = f"select distinct b.id, b.Room_Id, concat(a.Name, f.Name, LPAD(r.Name, 2, '0')) as RoomNumber, DATE_FORMAT(b.CheckInDate, '%Y-%m-%d') as CheckInDate, DATE_FORMAT(DATE_ADD(b.CheckInDate, INTERVAL b.Nights DAY), '%Y-%m-%d') as CheckOutDate, ca.Name as Category, b.Status, b.Total, c.Fullname FROM Bookings b join Booking_Customer bc on b.id = bc.Booking_Id join Customers c on bc.Customer_Id = c.id join Rooms r on b.Room_Id = r.Id join Floors f on r.Floor_Id = f.Id join Areas a on f.Area_Id = a.Id join Categories ca on r.Category_Id = ca.Id where b.id = {booking_id}"
        return Database.execute_query(query)

    @staticmethod
    def add_booking(Room_Id, check_in, nights, total_price, status):
        query = f"INSERT INTO Bookings (Room_Id, CheckInDate, Nights, Total, Status) VALUES ({Room_Id}, '{check_in}', {nights}, {total_price}, '{status}')"
        Database.execute_non_query(query)
        query = f"SELECT id FROM Bookings WHERE Room_Id = {Room_Id} AND CheckInDate = '{check_in}' AND Total = {total_price} AND Status = '{status}' ORDER BY Id DESC LIMIT 1"
        return Database.execute_query(query)[0]["id"]

    @staticmethod
    def update_booking(booking_id, status):
        query = f"UPDATE Bookings SET Status = '{status}' WHERE id = {booking_id}"
        return Database.execute_non_query(query)

    @staticmethod
    def add_customer(Fullname, CitizenId):
        customer = Booking.get_customer_by_citizen_id(CitizenId)
        if customer:
            if customer["Fullname"] != Fullname:
                return Booking.update_customer(Fullname, CitizenId)
            return None
        else:
            query = f"INSERT INTO Customers (Fullname, CitizenId) VALUES ('{Fullname}', '{CitizenId}')"
            return Database.execute_non_query(query)

    @staticmethod
    def update_customer(Fullname, CitizenId):
        query = f"UPDATE Customers SET Fullname = '{Fullname}' WHERE CitizenId = '{CitizenId}'"
        return Database.execute_non_query(query)

    @staticmethod
    def add_booking_customer(booking_id, customer_id):
        query = f"INSERT INTO Booking_Customer (Booking_Id, Customer_Id) VALUES ({booking_id}, {customer_id})"
        Database.execute_non_query(query)
        return

    @staticmethod
    def get_customer_by_booking_id(booking_id):
        query = f"SELECT c.Fullname, c.CitizenId FROM Booking_Customer bc join Customers c on bc.Customer_Id = c.id WHERE bc.Booking_Id = {booking_id}"
        result = Database.execute_query(query)
        return result if result else None

    @staticmethod
    def get_customer_by_customer_id(customer_id):
        query = f"SELECT * FROM Customers WHERE Id = {customer_id}"
        return Database.execute_query(query)

    @staticmethod
    def get_customer_by_citizen_id(CitizenId):
        query = f"SELECT * FROM Customers WHERE CitizenId = '{CitizenId}'"
        result = Database.execute_query(query)
        return result[0] if result else None
