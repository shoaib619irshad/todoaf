from flask import Flask
from flask_pymongo import PyMongo 

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    app.config["MONGO_URI"]="mongodb://localhost:27017/todo_af"
    mongo = PyMongo(app)
    app.extensions['mongo'] = mongo
    from app.api import todo
    app.register_blueprint(todo.todo_bp)
    
    return app
