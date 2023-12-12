from flask import request , jsonify , abort , Blueprint , url_for
from flask_bcrypt import  check_password_hash ,generate_password_hash
from flask_jwt_extended import create_access_token , get_current_user , jwt_required
import datetime , os
from controllers.auth import *
from flask import current_app as app
from flask_mail import Message

jwt =app.extensions['jwt']
mail=app.extensions['mail']
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


@user_bp.route('/user/reset_password' , methods=["POST"])
def reset_password():
    if not request.json:
        abort(500)
    email = request.json.get("email",None)
    if email is None:
        return jsonify(message="Invalid Request") , 400
    user = get_user_by_email(email)
    if user:
        message = user["email"] + ":" + user["role"]
        key = encoder(message)
        msg = Message("Reset Pasword" , sender = 'shoaibirshad619@gmail.com', recipients= ['fawadansari110@gmail.com'])
        link = url_for('user.password_reset' , reset_key = key , _external = True)
        msg.body = 'Your forgot password  link is {}'.format(link)
        mail.send(msg)
        return jsonify(message="Password reset link has been sent to your email")
    
    return jsonify(message="The email is incorrect")

@user_bp.route('/user/password_reset/<reset_key>',  methods=["PATCH"])
def password_reset(reset_key):
    if not request.json:
       abort(500)
    old_password = request.json.get("old_password",None)
    new_password = request.json.get("new_password",None)
    confirm_password = request.json.get("confirm_password",None)
    if old_password is None or new_password is None or confirm_password is None:
        return jsonify(message="Invalid Request") , 400
    if old_password == new_password:
        return jsonify(message="Old password cannot be new password")
    if new_password != confirm_password:
        return jsonify(message="Confirm your password")
    password = generate_password_hash(new_password).decode('utf8')
    base64_message = reset_key
    message = decoder(base64_message)
    email = message.split(":")[0]
    mongo.db.user.find_one_and_update({'email':email} , {"$set": {"password":password}})
    return jsonify(message="Password Reset Successfully")