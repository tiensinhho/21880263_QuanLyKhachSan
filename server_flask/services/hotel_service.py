from models.hotel_model import Hotel
from werkzeug.exceptions import NotFound

class HotelService:
    def __init__(self):
        self.hotel_repo=Hotel()
    
    def get_hotel_infomation(self):
        hotel=self.hotel_repo.get_hotel_by_id(1)
        if hotel:
            return hotel
        else:
            raise NotFound('Hotel not found')
            
