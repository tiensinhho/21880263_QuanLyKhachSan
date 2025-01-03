from flask import Flask
from flask_cors import CORS
from config import Config
from flasgger import Swagger
from controllers.user_controller import user_bp
from controllers.image_controller import image_bp
from controllers.manager_controller import manager_bp
from controllers.executive_controller import executive_bp
from controllers.receptionist_controller import receptionist_bp
from controllers.error_controller import error_bp


app = Flask(__name__)
cors = CORS(app)
swagger = Swagger(app)
app.config.from_object(Config)
# Đăng ký blueprint
app.register_blueprint(user_bp)
app.register_blueprint(image_bp)
app.register_blueprint(manager_bp)
app.register_blueprint(executive_bp)
app.register_blueprint(receptionist_bp)
app.register_blueprint(error_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
