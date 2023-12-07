from flask import Flask
from flask_pymongo import PyMongo 
import os
from flask_jwt_extended import JWTManager

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY')
    )
    app.config["MONGO_URI"]=os.getenv("MONGO_URI")
    mongo = PyMongo(app)
    app.extensions['mongo'] = mongo
    jwt = JWTManager(app)
    from app.api import todo
    app.register_blueprint(todo.todo_bp)
    from app.api import auth
    app.register_blueprint(auth.user_bp)
    
    return app
