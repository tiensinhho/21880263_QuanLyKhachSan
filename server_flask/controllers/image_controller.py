from flask import Blueprint, send_from_directory

image_bp = Blueprint("image", __name__)


@image_bp.route("/public/images/<path:filename>")
def serve_images_file(filename):
    """
    Lấy hình ảnh
    ---
    tags:
      - images
    parameters:
      - name: filename
        in: path
        type: string
        required: True
        description: Tên file hình
    responses:
      200:
        description: Hình ảnh
    """
    return send_from_directory("public/images", filename)
