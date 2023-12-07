from flask import request , jsonify , abort , Blueprint
from flask import current_app as app
from flask_bcrypt import generate_password_hash , check_password_hash
from flask_jwt_extended import create_access_token
import datetime

user_bp = Blueprint('user',__name__)

#POST Route for user signup
@user_bp.route('/user/signup',methods=["POST"])
def signup():
    mongo = app.extensions['mongo']
    if not request.json:
        abort(500)
    email = request.json.get("email",None)
    password = request.json.get("password",None)
    if email is None or password is None:
        return jsonify(message="Invalid Request"), 500
    user = mongo.db.user.find_one({"email":email})
    if not user:
        password = generate_password_hash(password).decode('utf8')
        mongo.db.user.insert_one({'email': email, 'password': password})
        return jsonify({
            "message":"User Signup Successfully",
            "status":True
        })
    return jsonify(message="User already existed")

#POST Route for user login
@user_bp.route('/user/login',methods=["POST"])
def login():
    mongo = app.extensions['mongo']
    if not request.json:
        abort(500)
    email = request.json.get("email",None)
    password = request.json.get("password",None)
    user = mongo.db.user.find_one({"email":email})
    if user:
        c_password = check_password_hash(user["password"], password)
        if c_password:
            expires = datetime.timedelta(days=1)
            token = create_access_token(identity=email ,expires_delta=expires)
            return jsonify(access_token=token)
        
    return jsonify(message="The email or password is incorrect")