from flask import jsonify
from flask import current_app as app


mongo = app.extensions['mongo']

def validate_email_pass(email,password):
    if email is None or password is None:
        return jsonify(message="Invalid Request"), 500
    
def validate_role(role):
    if role in ["admin" , "manager" , "employee"]:
        return True
    else:
        False
        
def get_user_by_email(email):
    return mongo.db.user.find_one({"email":email})

def add_user(email,password,role):
    return mongo.db.user.insert_one({'email': email, 'password': password, "role":role})