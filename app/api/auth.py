from flask import request , jsonify , abort , Blueprint
from flask_bcrypt import generate_password_hash , check_password_hash
from flask_jwt_extended import create_access_token
import datetime , os
from controllers.auth import *

user_bp = Blueprint('user',__name__)

#POST Route for user signup
@user_bp.route('/user/signup',methods=["POST"])
def signup():
    if not request.json:
        abort(500)
    email = request.json.get("email",None)
    password = request.json.get("password",None)
    validate_email_pass(email,password)
    user = get_user_by_email(email)
    if not user:
        password = generate_password_hash(password).decode('utf8')
        add_user(email,password)
        return jsonify({
            "message":"User Signup Successfully",
            "status":True
        })
    return jsonify(message="User with this email already exists")

#POST Route for user login
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