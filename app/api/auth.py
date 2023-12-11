from flask import request , jsonify , abort , Blueprint
from flask_bcrypt import  check_password_hash ,generate_password_hash
from flask_jwt_extended import create_access_token , get_current_user , jwt_required
import datetime , os
from controllers.auth import *
from flask import current_app as app

jwt =app.extensions['jwt']
user_bp = Blueprint('user',__name__)

#POST Route for user signup
@user_bp.route('/user/signup',methods=["POST"])
def signup():
    if not request.json:
        abort(500)
    email = request.json.get("email",None)
    password = request.json.get("password",None)
    role = request.json.get("role",Role.EMPLOYEE.value)
    is_role_validate = validate_role(role)
    if  not is_role_validate:
        return jsonify(message="Invalid Role"), 500
    validate_email_pass(email,password)
    user = get_user_by_email(email)
    if not user:
        add_user(email,password,role)
        return jsonify({
            "message":"User Signup Successfully",
            "status":True
        })
    return jsonify(message="User with this email already exists")


@jwt.user_identity_loader
def user_identity_lookup(user):
   return user

@user_bp.route('/user/login',methods=["POST"])
def login():
    if not request.json:
        abort(500)
    email = request.json.get("email",None)
    password = request.json.get("password",None)
    user = get_user_by_email(email)
    if user:
        c_password = check_password_hash(user["password"], password)
        if c_password:
            expires = datetime.timedelta(days=int(os.getenv('DAYS')))
            token = create_access_token(identity=email ,expires_delta=expires)
            return jsonify(access_token=token)
        
    return jsonify(message="The email or password is incorrect")


@user_bp.route('/user/forgot_pass' , methods=["POST"])
def forgot_password():
    if not request.json:
        abort(500)
    email = request.json.get("email",None)
    if email is None:
        return jsonify(message="Invalid Request") , 500
    user = get_user_by_email(email)
    if user:
        expires = datetime.timedelta(days=int(os.getenv('DAYS')))
        token = create_access_token(identity=email ,expires_delta=expires)
        return jsonify(access_token=token)
    
    return jsonify(message="The email is incorrect")

@user_bp.route('/user/reset_pass' , methods=["Patch"])
@jwt_required()
def reset_password():
    if not request.json:
       abort(500)
    password = request.json.get("password",None)
    if password is None:
        return jsonify(message="Invalid Request") , 500
    password = generate_password_hash(password).decode('utf8')
    user = get_current_user()
    email= user["email"]
    mongo.db.user.find_one_and_update({'email':email} , {"$set": {"password":password}})
    return jsonify(message="Password Reset Successfully")