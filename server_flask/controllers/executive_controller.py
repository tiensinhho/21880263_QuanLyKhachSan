from flask import Blueprint, jsonify, request
from services.user_service import role_required
from services.report_service import ReportService
from services.booking_service import BookingService
from services.room_service import RoomService

executive_bp = Blueprint("executive", __name__)
report_service = ReportService()
booking_service = BookingService()
room_service = RoomService()


@executive_bp.route("/executive/reports/monthly", methods=["GET"])
@role_required("Executive")
def get_monthly_report():
    """
    Lấy báo cáo doanh thu theo tháng
    ---
    tags:
      - executive
    parameters:
      - name: Authorization
        in: header
        type: string
        required: True
        description: "JWT token của người dùng, dạng 'Bearer <token>'"
      - name: month
        in: query
        type: integer
        required: True
        description: Tháng cần lấy báo cáo
      - name: year
        in: query
        type: integer
        required: True
        description: Năm cần lấy báo cáo
    responses:
      200:
        description: Thông tin báo cáo
    """
    data = report_service.get_monthly_report(request.args)
    return jsonify(data), 200


@executive_bp.route("/executive/reports/annual", methods=["GET"])
@role_required("Executive")
def get_annual_report():
    """
    Lấy báo cáo doanh thu theo năm
    ---
    tags:
      - executive
    parameters:
      - name: Authorization
        in: header
        type: string
        required: True
        description: "JWT token của người dùng, dạng 'Bearer <token>'"
      - name: year
        in: query
        type: integer
        required: True
        description: Năm cần lấy báo cáo
    responses:
      200:
        description: Thông tin báo cáo
    """
    data = report_service.get_annual_report(request.args)
    return jsonify(data), 200


@executive_bp.route("/executive/booking", methods=["GET"])
@role_required("Executive")
def get_bookings():
    """
    Lấy thông tin phiếu đặt phòng
    ---
    tags:
      - executive
    parameters:
      - name: Authorization
        in: header
        type: string
        required: True
        description: "JWT token của người dùng, dạng 'Bearer <token>'"
      - name: limit
        in: query
        type: integer
        required: False
        description: Số lượng phiếu đặt phòng muốn lấy
        example: 10
      - name: page
        in: query
        type: integer
        required: False
        description: trang cần lấy
        example: 1
      - name: date
        in: query
        type: string
        format: date
        required: False
        description: Ngày bắt đầu (YYYY-MM-DD)
        example: "2024-01-01"
      - name: customer_name
        in: query
        type: string
        required: False
        description: Tên khách hàng
        example: ""
      - name: category
        in: query
        type: string
        required: False
        description: Loại phòng
        example: "King"
    responses:
      200:
        description: thông tin đặt phòng
        schema:
          type: object
          properties:
            bookings:
              type: array
              items:
                type: object
                properties:
                  Check_In:
                    type: string
                    example: "2024-03-10T00:00:00"
                  Check_Out:
                    type: string
                    example: "2024-03-17T00:00:00"
                  Room_Id:
                    type: integer
                    example: 1
                  Status:
                    type: string
                    example: "booked"
                  RoomNumber:
                    type: string
                    example: "A101"
            count:
              type: integer
    """
    bookings = booking_service.get_bookings(request.args)
    return jsonify(bookings["data"]), bookings["status"]


@executive_bp.route("/executive/booking/<int:booking_id>", methods=["GET"])
@role_required("Executive")
def get_booking_by_id(booking_id):
    """
    Lấy thông tin phiếu đặt phòng theo ID
    ---
    tags:
      - executive
    parameters:
      - name: Authorization
        in: header
        type: string
        required: True
        description: "JWT token của người dùng, dạng 'Bearer <token>'"
      - name: booking_id
        in: path
        type: integer
        required: True
        description: ID của phiếu đặt phòng
    responses:
      200:
        description: thông tin đặt phòng
        schema:
          type: object
          properties:
            booking:
              type: object
              properties:
                Check_In:
                  type: string
                  example: "2024-03-10"
                Check_Out:
                  type: string
                  example: "2024-03-17"
                Room_Id:
                  type: integer
                  example: 1
                Status:
                  type: string
                  example: "booked"
                RoomNumber:
                  type: string
                  example: "A101"
      404:
        description: Phiếu đặt phòng không tồn tại
    """
    booking = booking_service.get_booking_by_id(booking_id)
    return jsonify(booking["data"]), booking["status"]


@executive_bp.route("/executive/category/<int:category_id>", methods=["PUT"])
@role_required("Executive")
def update_price_category(category_id):
    """
    Cập nhật giá phòng theo category_id
    ---
    tags:
      - executive
    parameters:
      - name: Authorization
        in: header
        type: string
        required: True
        description: "JWT token của người dùng, dạng 'Bearer <token>'"
      - name: category_id
        in: path
        type: number
        required: True
        description: ID của loại phòng
      - name: body
        in: body
        required: True
        schema:
          type: object
          properties:
            price:
              type: float
              example: 1000000
    responses:
      200:
        description: Cập nhật giá thành công
      400:
        description: Thông tin đầu vào không hợp lệ
    """
    room_service.update_price_category(category_id, request.get_json())
    return jsonify({"message": "Update price category successfully"}), 200


@executive_bp.route("/executive/category", methods=["GET"])
@role_required("Executive")
def get_all_categories():
    """
    Lấy danh sách các loại phòng
    ---
    tags:
      - executive
    parameters:
      - name: Authorization
        in: header
        type: string
        required: True
        description: "JWT token của người dùng, dạng 'Bearer <token>'"
      - name: name
        in: query
        type: string
        required: False
        description: Tên loại phòng
    responses:
      200:
        description: Danh sách các loại phòng
        schema:
          type: array
          items:
            type: object
            properties:
              Id:
                type: integer
              Name:
                type: string
              Price:
                type: number
                format: float
              NumberOfGuests:
                type: integer
    """
    result = room_service.get_all_categories(request.args)
    return jsonify(result["data"]), result["status"]
