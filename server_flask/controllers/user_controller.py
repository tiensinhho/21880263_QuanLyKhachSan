from flask import Blueprint, jsonify, request
from services.user_service import UserService, token_required

user_bp = Blueprint('user', __name__)
user_service = UserService()

@user_bp.route('/users/login', methods=['POST'])
def login():
    """
    Đăng nhập người dùng
    ---
    tags:
      - users
    summary: Đăng nhập người dùng
    description: Endpoint cho phép người dùng đăng nhập.
    parameters:
      - name: body
        in: body
        required: True
        schema:
          type: object
          properties:
            email:
              type: string
              example: "user1@example.com"
            password:
              type: string
              example: "12345"
          required:
            - email
            - password
    responses:
      200:
        description: Đăng nhập thành công
        schema:
          type: object
          properties:
            token:
              type: string
              example: "jwt_token_string"
      401:
        description: Unauthorized
    """
    result = user_service.login(request.get_json())
    return jsonify({"token":result['token']}), result['status']

@user_bp.route('/users/register', methods=['POST'])
def register():
    """
    Đăng ký người dùng
    ---
    tags:
      - users
    summary: Đăng ký người dùng
    description: Endpoint cho phép người dùng đăng ký.
    parameters:
      - name: body
        in: body
        required: True
        schema:
          type: object
          properties:
            email:
              type: string
              example: "user2@example.com"
            password:
              type: string
              example: "12345"
            fullname:
              type: string
              example: "user2"
            role_id:
              type: integer
              example: 1
          required:
            - email
            - password
            - fullname
            - role_id
    responses:
      201:
        description: Đăng ký thành công
      402:
        description: Đăng ký thất bại
    """
    new_user = user_service.register(request.get_json())
    return jsonify(new_user), new_user['status']

@user_bp.route('/users/roles', methods=['GET'])
def get_roles():
    """
    Lấy thông tin các vai trò
    ---
    tags:
      - users
    summary: Lấy thông tin form đăng nhập
    description: Trả về thông tin form đăng nhập.
    responses:
      200:
        description: Thông tin form đăng nhập
    """
    roles = user_service.get_all_roles()
    return jsonify(roles['data']), roles['status']

@user_bp.route('/users/profile', methods=['POST'])
@token_required
def profile(current_user):
    """
    Lấy thông tin người dùng tóm tắt
    ---
    tags:
      - users
    summary: Lấy thông tin người dùng
    description: Trả về thông tin người dùng nếu xác thực thành công.
    parameters:
      - name: Authorization
        in: header
        type: string
        required: True
        description: "JWT token của người dùng, dạng 'Bearer <token>'"
    responses:
      200:
        description: Thông tin người dùng
        schema:
          type: object
          properties:
            fullname:
              type: string
              example: "user1"
            role:
              type: string
              example: "user"
      401:
        description: Unauthorized
    """
    return jsonify(current_user), 200

@user_bp.route('/users/account', methods=['POST'])
@token_required
def account(current_user):
    """
    Lấy thông tin tài khoản người dùng
    ---
    tags:
      - users
    summary: Lấy thông tin người dùng
    description: Trả về thông tin người dùng nếu xác thực thành công.
    parameters:
      - name: Authorization
        in: header
        type: string
        required: True
        description: "JWT token của người dùng, dạng 'Bearer <token>'"
    responses:
      200:
        description: Thông tin người dùng
        schema:
          type: object
          properties:
            Email:
              type: string
              example: "user@example.com"
            FullName:
              type: string
              example: "Full Name"
            Id:
              type: integer
              example: "1"
            Password:
              type: string
              example: "******"
            RoleName:
              type: string
              example: "Admin"
            Role_Id:
              type: interger
              example: "1"
      401:
        description: Unauthorized
    """
    user=user_service.get_user_infomation(current_user['Email'])
    return jsonify(user['data']), user['status']

