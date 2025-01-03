from models.database import Database


class Hotel:
    @staticmethod
    def get_hotel_by_id(self, hotel_id):
        query = f"SELECT * FROM Hotels WHERE Id = {hotel_id}"
        return Database.execute_query(query)
