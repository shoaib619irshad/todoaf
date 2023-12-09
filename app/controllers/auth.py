from flask import jsonify
from flask import current_app as app
from enum import Enum
from flask_bcrypt import generate_password_hash


mongo = app.extensions['mongo']

def validate_email_pass(email,password):
    if email is None or password is None:
        return jsonify(message="Invalid Request"), 500
    
def validate_role(role):
    role_list = [member.value for member in Role]
    if role in role_list:
        return True
    else:
        False
        
def get_user_by_email(email):
    return mongo.db.user.find_one({"email":email})

def add_user(email,password,role):
    password = generate_password_hash(password).decode('utf8')
    return mongo.db.user.insert_one({'email': email, 'password': password, "role":role})

class Role(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"
    def __str__(self):
        return self.value