import jwt
import datetime
import bcrypt
from config import Config
from functools import wraps
from flask import request
from models.user_model import User
from werkzeug.exceptions import Unauthorized, Forbidden, NotFound


class UserService:
    def __init__(self):
        self.user_repo = User()
        self.secret_key = Config.JWT_SECRET_KEY

    def generate_token(self, email, fullname, role, areas=[], image_url=None):
        payload = {
            "Email": email,
            "Fullname": fullname,
            "Role": role,
            "Areas": areas,
            "ImageURL": image_url,
            "Exp": (
                datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(minutes=30)
            ).isoformat(),
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token

    def decode_token(self, token):
        try:
            data = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            expiration_datetime = datetime.datetime.fromisoformat(data["Exp"])
            remaining_time = expiration_datetime - datetime.datetime.now(
                datetime.timezone.utc
            )
            del data["Exp"]
            if remaining_time < datetime.timedelta(minutes=5):
                user = User.get_user_by_email(data["Email"]) 
                user["Areas"] = User.get_area_by_user_id(user["Id"])
                new_token = self.generate_token(
                    user["Email"], user["Fullname"], user["Role"], user["Areas"], user["ImageURL"]
                )
                data["token"] = new_token
            return data
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Token has expired!")
        except jwt.InvalidTokenError:
            raise Unauthorized("Invalid token!")

    def login(self, request):
        email = request.get("email")
        password = request.get("password")
        user = User.get_user_by_email(email)
        if user:
            if self.check_password(password, user["Password"]):
                user["Areas"] = User.get_area_by_user_id(user["Id"])
                token = self.generate_token(email, user["Fullname"], user["Role"], user["Areas"], user["ImageURL"])
                return {"status": 200, "token": token}
            raise Unauthorized("Invalid password!")
        else:
            raise Unauthorized("Invalid email!")

    def get_profile(self, token):
        decoded = self.decode_token(token)
        return decoded

    def get_user_infomation(self, email):
        user = User.get_user_by_email(email)
        if user:
            user["Password"] = "********"
            return {"data": user, "status": 200}
        else:
            raise NotFound("User not found")

    def register(self, request):
        email = request.get("email")
        password = request.get("password")
        fullname = request.get("fullname")
        role = request.get("role")
        user = User.get_user_by_email(email)
        if user:
            raise Unauthorized("Email already exists!")
        hashed_password = self.hash_password(password)
        User.add_user(fullname, email, hashed_password, role)
        return {"message": "User registered successfully", "status": 201}

    def get_all_roles(self):
        roles = User.get_all_roles()
        return {"status": 200, "data": roles}

    def hash_password(self, plain_password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    def check_password(self, plain_password, hashed_password):
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode("utf-8")
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        current_user = UserService().get_profile(token)
        return f(current_user, *args, **kwargs)
    return decorated


def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")
            current_user = UserService().get_profile(token)
            if current_user["Role"] != required_role:
                raise Forbidden("Permission denied!")
            if current_user["Role"] in ["Manager", "Receptionist"]:
                areas = current_user["Areas"]
                return fn(areas, *args, **kwargs)
            return fn(*args, **kwargs)

        return decorated

    return wrapper
