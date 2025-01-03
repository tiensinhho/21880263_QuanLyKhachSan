from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

error_bp = Blueprint("error", __name__)

@error_bp.app_errorhandler(Exception) 
def handle_exception(e):     
    if isinstance(e, HTTPException): 
        response = e.get_response() 
        response.data = jsonify({ "status": e.code, "name": e.name, "description": e.description }).get_data() 
        response.content_type = "application/json" 
        return response  
    return jsonify({ "status": 500, "name": "Internal Server Error", "description": str(e) }), 500
