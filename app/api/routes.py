from flask import current_app as app , request , abort, Blueprint
from controllers.auth import *
from utils.decorators import admin_required , admin_manager_required

mongo = app.extensions['mongo']
role_bp = Blueprint('add_manager_employee',__name__)

#POST Route to add manager
@role_bp.route('/user/manager', methods=["POST"])
@admin_required
def add_manager():
    if not request.json:
        abort(500)
    email = request.json.get("email",None)
    password = request.json.get("password",None)
    validate_email_pass(email,password)
    manager = get_user_by_email(email)
    if not manager:
        add_user(email,password,role=Role.MANAGER.value)
        return jsonify({
            "message":"Manager Added Successfully",
            "status":True
        })
    return jsonify(message="Manager with this email already exists")

#POST Route to add employee
@role_bp.route('/user/employee', methods=["POST"])
@admin_manager_required
def add_employee():
    if not request.json:
        abort(500)
    email = request.json.get("email",None)
    password = request.json.get("password",None)
    validate_email_pass(email,password)
    employee = get_user_by_email(email)
    if not employee:
        add_user(email,password,role=Role.EMPLOYEE.value)
        return jsonify({
            "message":"Employee Added Successfully",
            "status":True
        })
    return jsonify(message="Employee with this email already exists")