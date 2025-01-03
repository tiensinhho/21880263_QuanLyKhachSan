from flask import Blueprint, jsonify, request
from services.hotel_service import HotelService

hotel_bp = Blueprint('hotel', __name__)
hotel_service=HotelService()

@hotel_bp.route('/hotels', methods=['GET'])
def get_hotels():
    """
    Lấy thông tin khách sạn
    ---
    tags:
      - hotels
    paramester:
    responses:
      200:
        description: thông tin khách sạn
    """
    hotels = hotel_service.get_hotel_infomation()
    return jsonify(hotels)
