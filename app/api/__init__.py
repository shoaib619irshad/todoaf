from flask import Flask
from flask_pymongo import PyMongo 
import os
from flask_jwt_extended import JWTManager
from flask_mail import Mail

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY')
    )
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)
    app.extensions['jwt'] = jwt
    app.config["MONGO_URI"]=os.getenv("MONGO_URI")
    mongo = PyMongo(app)
    app.extensions['mongo'] = mongo
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] =os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] =os.getenv("MAIL_PASSWORD")
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    app.extensions['mail'] = mail
    app.app_context().push()
    from .todo import todo_bp
    from .auth import user_bp
    from .routes import role_bp 
    app.register_blueprint(todo_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(role_bp)
    
    return app
