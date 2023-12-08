from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth import get_user_by_email

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        role = get_user_by_email(current_user)["role"]
        if role != "admin":
            return jsonify(message="You do not have permission to add manager"), 403
        return f(*args, **kwargs)
    return decorated_function

def admin_manager_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        role = get_user_by_email(current_user)["role"]
        if role == "employee":
            return jsonify(message="You do not have permission to add employee"), 403
        return f(*args, **kwargs)
    return decorated_function



       