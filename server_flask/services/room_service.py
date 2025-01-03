from models.room_model import Room
from werkzeug.exceptions import NotFound, BadRequest


class RoomService:
    def __init__(self):
        self.room_repo = Room()

    def get_rooms(self, areas, request):
        limit = int(request.get("limit", 0))
        page = int(request.get("page", 1))
        name = request.get("name")
        price_max = request.get("price_max") 
        price_min = request.get("price_min")
        category = request.get("category")
        status = request.get("status")
        if limit < 0 or page <= 0:
            raise BadRequest("limit and page must be positive integers")
        valid_statuses = ["available", "unavailable"]
        if status and status not in valid_statuses:
            raise BadRequest("Invalid room status")
        offset = (page - 1) * limit
        data = {}
        conditions = ""
        if category:
            conditions += f"c.Name like '%{category}%'"
        if len(areas) > 0:
            if conditions:
                conditions += " and "
            list_area = ",".join([str(area.get("Area_Id")) for area in areas if "Area_Id" in area])
            conditions += f"a.Id in ({list_area})"
        if price_max and price_min:
            if conditions:
                conditions += " and "
            conditions += f"c.PricePerNight between {price_min} and {price_max}"
        elif price_max:
            if conditions:
                conditions += " and "
            conditions += f"c.PricePerNight <= {price_max}".format(price_max)
        elif price_min:
            if conditions:
                conditions += " and "
            conditions += f"c.PricePerNight >= {price_min}".format(price_min)
        if status:
            if conditions:
                conditions += " and "
            conditions += f"r.Status = '{status}'"
        if name:
            if conditions:
                conditions += " and "
            conditions += (
                f"concat(a.Name, f.Name, LPAD(r.Name, 2, '0')) like '%{name}%'"
            )
        if conditions:
            data["rooms"] = self.room_repo.get_all_rooms(limit, offset, conditions)
        else:
            data["rooms"] = self.room_repo.get_all_rooms(limit, offset)
        data["count"] = self.room_repo.get_count_rooms(conditions)
        data["possible_statuses"] = ["available", "unavailable"]
        categories = self.room_repo.get_all_categories()
        data["categories"] = []
        for category in categories:
            data["categories"].append({"Id": category["id"], "Name": category["Name"]})
        return {"data": data, "status": 200}

    def update_price_category(self, category_id, request):
        price = request.get("price")
        if not category_id:
            raise BadRequest("Missing category_id")
        if not isinstance(category_id, int):
            raise BadRequest("Category ID must be an integer")
        if category_id <= 0:
            raise BadRequest("Category ID must be a positive integer")
        if not price:
            raise BadRequest("Missing price")
        if not isinstance(price, int):
            raise BadRequest("Price must be an integer")
        if price <= 0:
            raise BadRequest("Price must be a positive integer")
        self.room_repo.update_price_catogory(category_id, price)
        return {"status": 200}

    def get_room_by_id(self, room_id):
        if not isinstance(room_id, int):
            raise BadRequest("Room ID must be an integer")
        if room_id <= 0:
            raise BadRequest("Room ID must be a positive integer")
        room = self.room_repo.get_room_by_id(room_id)
        data = room[0] if room else None
        if data:
            data["Amenities"] = self.room_repo.get_amenities_by_category_id(
                data["Category_Id"]
            )
            return {"data": data, "status": 200}
        else:
            raise NotFound("Room not found")

    def get_all_categories(self, request):
        name = request.get("name")
        categoties = self.room_repo.get_all_categories(name)
        if len(categoties) > 0:
            for category in categoties:
                category["Amenities"] = self.room_repo.get_amenities_by_category_id(category["id"])
        return {"data": categoties, "status": 200}