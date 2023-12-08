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
    app.app_context().push()
    app.extensions['mongo'] = mongo
    jwt = JWTManager(app)
    from .todo import todo_bp
    from .auth import user_bp
    app.register_blueprint(todo_bp)
    app.register_blueprint(user_bp)
    
    return app
