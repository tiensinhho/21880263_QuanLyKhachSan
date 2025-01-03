from models.database import Database


class Room:
    @staticmethod
    def get_all_rooms(limit=0, offset=0, conditions=""):        
        query = f"SELECT r.Id, concat(a.Name, f.Name, LPAD(r.Name, 2, '0')) as RoomNumber, c.Name as CategoryName, c.PricePerNight as PricePerNight, c.NumberOfGuests, r.Status, i.URL as ImageURL FROM Rooms r join Floors f on r.Floor_Id = f.Id join Areas a on f.Area_Id = a.Id join Hotels h on a.Hotel_Id = h.Id join Categories c on r.Category_Id = c.Id left join RoomImages i on r.Id = i.Room_Id"
        if conditions:
            query += f" WHERE {conditions}"
        if limit > 0 and offset > 0:
            query += f" LIMIT {limit} OFFSET {offset}"
        return Database.execute_query(query)

    @staticmethod
    def get_count_rooms(conditions=""):
        query = f"SELECT count(*) as count FROM Rooms r join Floors f on r.Floor_Id = f.Id join Areas a on f.Area_Id = a.Id join Hotels h on a.Hotel_Id = h.Id join Categories c on r.Category_Id = c.Id left join RoomImages i on r.Id = i.Room_Id"
        if conditions:
            query += f" WHERE {conditions}"
        return (
            Database.execute_query(query)[0]["count"]
            if Database.execute_query(query)
            else 0
        )

    @staticmethod
    def get_roomname_by_id(room_id):
        query = f"SELECT r.Id, concat(a.Name, f.Name, LPAD(r.Name, 2, '0')) as RoomNumber FROM Rooms r join Floors f on f.Id = r.Floor_Id left join Areas a on a.Id = f.Area_Id join Categories c on c.Id = r.Category_Id WHERE r.Id = {room_id}"
        return (
            Database.execute_query(query)[0]["RoomNumber"]
            if Database.execute_query(query)
            else None
        )

    @staticmethod
    def get_room_by_floor_id(floor_id):
        query = f"SELECT * FROM Rooms WHERE Floor_Id = {floor_id}"
        return Database.execute_query(query)

    @staticmethod
    def get_room_by_id(room_id):
        query = f"SELECT r.Id, r.Status, concat(a.Name, f.Name, LPAD(r.Name, 2, '0')) as RoomNumber, c.PricePerNight, c.NumberOfGuests FROM Rooms r join Floors f on f.Id = r.Floor_Id left join Areas a on a.Id = f.Area_Id join Categories c on r.Category_Id = c.Id WHERE r.Id = {room_id}"
        return Database.execute_query(query)

    @staticmethod
    def get_amenities_by_category_id(Category_Id):
        query = f"SELECT a.Name FROM Amenities a join Category_Amenity ca on a.Id = ca.Amenity_Id join Categories c on c.Id = ca.Category_Id WHERE c.Id = {Category_Id}"
        amenities = Database.execute_query(query)
        data = []
        for amenity in amenities:
            data.append(amenity["Name"])
        return data

    @staticmethod
    def get_floor_by_area_id(area_id):
        query = f"SELECT * FROM Floors WHERE Area_Id = {area_id}"
        return Database.execute_query(query)

    @staticmethod
    def get_category_by_id(Category_Id):
        query = f"SELECT * FROM Categories WHERE Id = {Category_Id}"
        return Database.execute_query(query)

    @staticmethod
    def get_all_categories(name=""):
        if name:
            query = f"SELECT * FROM Categories WHERE name like '%{name}%'"
        else:
            query = f"SELECT * FROM Categories"
        return Database.execute_query(query)

    @staticmethod
    def update_price_catogory(Category_Id, price):
        query = f"update Categories set PricePerNight = {price} where Id = {Category_Id}"
        return Database.execute_non_query(query)

    @staticmethod
    def get_areas_by_ids(areas=[]):
        if len(areas) == 0:
            return []
        list_area = ""
        list_area = ",".join(str(area["area_id"]) for area in areas)
        query = f"SELECT * FROM Areas WHERE Id in ({list_area})"
        return Database.execute_query(query)

    @staticmethod
    def get_price(room_id):
        query=f"Select c.PricePerNight from Rooms r join Categories c on r.Category_Id = c.Id where r.Id = {room_id} limit 1"
        result=Database.execute_query(query)
        return result[0]["PricePerNight"] if result else None
