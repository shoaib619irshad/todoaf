from flask import Flask
from flask_pymongo import PyMongo 
import os

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY')
    )
    app.config["MONGO_URI"]=os.getenv("MONGO_URI")
    mongo = PyMongo(app)
    app.extensions['mongo'] = mongo
    from app.api import todo
    app.register_blueprint(todo.todo_bp)
    
    return app
