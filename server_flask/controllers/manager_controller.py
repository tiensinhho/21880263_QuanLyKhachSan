from flask import Blueprint, jsonify, request
from services.report_service import ReportService
from services.user_service import role_required
from services.booking_service import BookingService

manager_bp = Blueprint("manager", __name__)
report_service = ReportService()
booking_service = BookingService()


@manager_bp.route("/manager/reports/monthly", methods=["GET"])
@role_required("Manager")
def get_monthly_report(areas):
    """
    Lấy báo cáo doanh thu theo tháng
    ---
    tags:
      - manager
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
    data = report_service.get_monthly_report(request.args, areas)
    return jsonify(data), 200


@manager_bp.route("/manager/reports/annual", methods=["GET"])
@role_required("Manager")
def get_annual_report(areas):
    """
    Lấy báo cáo doanh thu theo năm
    ---
    tags:
      - manager
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
    data = report_service.get_annual_report(request.args, areas)
    return jsonify(data), 200

@manager_bp.route("/manager/booking", methods=["GET"])
@role_required("Manager")
def get_bookings(areas):
    """
    Lấy thông tin phiếu đặt phòng
    ---
    tags:
      - manager
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
    bookings = booking_service.get_bookings(request.args, areas)
    return jsonify(bookings["data"]), bookings["status"]

@manager_bp.route("/manager/booking/<int:booking_id>", methods=["GET"])
@role_required("Manager")
def get_booking_by_id(areas,booking_id):
    """
    Lấy thông tin phiếu đặt phòng theo ID
    ---
    tags:
      - manager
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
