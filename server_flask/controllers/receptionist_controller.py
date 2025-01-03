from flask import Blueprint, jsonify, request
from services.user_service import role_required
from services.booking_service import BookingService
from services.room_service import RoomService

room_service = RoomService()
booking_service = BookingService()

receptionist_bp = Blueprint("receptionist", __name__)


@receptionist_bp.route("/receptionist/booking", methods=["GET"])
@role_required("Receptionist")
def get_bookings(areas):
    """
    Lấy thông tin phiếu đặt phòng
    ---
    tags:
      - receptionist
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


@receptionist_bp.route("/receptionist/booking/<int:booking_id>", methods=["GET"])
@role_required("Receptionist")
def get_booking_by_id(areas, booking_id):
    """
    Lấy thông tin phiếu đặt phòng theo ID
    ---
    tags:
      - receptionist
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
    booking = booking_service.get_booking_by_id(booking_id, areas)
    return jsonify(booking["data"]), booking["status"]


@receptionist_bp.route("/receptionist/booking/new", methods=["POST"])
@role_required("Receptionist")
def add_booking(areas):
    """
    Thêm mới phiếu đặt phòng
    ---
    tags:
      - receptionist
    parameters:
      - name: Authorization
        in: header
        type: string
        required: True
        description: "JWT token của người dùng, dạng 'Bearer <token>'"
      - name: body
        in: body
        required: True
        schema:
          type: object
          properties:
            room_id:
              type: integer
              example: 1
            check_in:
              type: string
              format: date-time
              example: "2024-03-10"
            check_out:
              type: string
              format: date-time
              example: "2024-03-17"
            total:
              type: number
              example: 1000000
            status:
              type: string
              example: "booked"
            customers:
              type: array
              items:
                type: object
                properties:
                  Fullname:
                    type: string
                    example: "John Doe"
                  CitizenId:
                    type: string
                    example: "1234567890"
          required:
            - room_id
            - check_in
            - check_out
            - total
            - status
            - customers
    responses:
      201:
        description: Đặt phòng thành công
      400:
        description: Thông tin đầu vào không hợp lệ
    """
    booking_service.add_booking(request.get_json())
    return jsonify({"message": "Booking added successfully"}), 201


@receptionist_bp.route("/receptionist/booking/new", methods=["GET"])
@role_required("Receptionist")
def get_new_booking(areas):
    """
    Lấy phiếu đặt phòng mới
    ---
    tags:
      - receptionist
    parameters:
      - name: Authorization
        in: header
        type: string
        required: True
        description: "JWT token của người dùng, dạng 'Bearer <token>'"
      - name: room_id
        type: integer
        in: query
        required: True
        example: 1
      - name: check_in
        type: string
        in: query
        format: date
        required: False
        example: "2024-03-10"
      - name: check_out
        type: string
        in: query
        format: date
        required: False
        example: "2024-03-17"
    responses:
      200:
        description: Thông tin phiếu đặt phòng mới
      400:
        description: Thông tin đầu vào không hợp lệ
      401:
        description: Không có quyền truy cập
    """
    result = booking_service.get_new_booking(areas, request.args)
    return jsonify(result), 200


@receptionist_bp.route("/receptionist/booking/<int:booking_id>", methods=["PUT"])
@role_required("Receptionist")
def update_booking(areas, booking_id):
    """
    Cập nhật trạng thái phiếu đặt phòng
    ---
    tags:
      - receptionist
    parameters:
      - name: Authorization
        in: header
        type: string
        required: True
        description: "JWT token của người dùng, dạng 'Bearer <token>'"
      - name: booking_id
        in: path
        type: number
        required: True
        description: "ID của phiếu đặt phòng"
        example: "1"
      - name: body
        in: body
        required: True
        schema:
          type: object
          properties:
            status:
              type: string
              example: "booked"
          required:
            - status
    responses:
      201:
        description: Đặt phòng thành công
      400:
        description: Thông tin đầu vào không hợp lệ
    """
    booking_service.update_booking(booking_id, request.get_json())
    return jsonify({"message": "Booking updated successfully"}), 201


@receptionist_bp.route("/receptionist/booking/<int:booking_id>", methods=["DELETE"])
@role_required("Receptionist")
def delete_booking(areas, booking_id):
    """
    Cập nhật trạng thái phiếu đặt phòng
    ---
    tags:
      - receptionist
    parameters:
      - name: Authorization
        in: header
        type: string
        required: True
        description: "JWT token của người dùng, dạng 'Bearer <token>'"
    responses:
      201:
        description: Đặt phòng thành công
      400:
        description: Thông tin đầu vào không hợp lệ
    """
    booking_service.delete_booking(booking_id)
    return jsonify({"message": "Booking deleted"}), 201


@receptionist_bp.route("/receptionist/rooms/", methods=["GET"])
@role_required("Receptionist")
def get_rooms(areas):
    """
    Lấy danh sách các phòng
    ---
    tags:
      - receptionist
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
        description: Tên phòng
      - name: category
        in: query
        type: string
        required: False
        description: Loại phòng
      - name: price_max
        in: query
        type: number
        required: False
        description: Giá phòng tối đa
      - name: price_min
        in: query
        type: number
        required: False
        description: Giá phòng tối thiểu
      - name: status
        in: query
        type: string
        required: False
        description: Trạng thái phòng
    responses:
      200:
        description: Danh sách các phòng
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
              Status:
                type: string
    """
    result = room_service.get_rooms(areas, request.args)
    return jsonify(result["data"]), result["status"]
