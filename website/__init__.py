import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

db = SQLAlchemy()
load_dotenv()
DB_NAME = os.environ.get("DB_URL")

def create_app(config_name=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SEC_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME

    if config_name:
        app.config.from_object(config_name)

    db.init_app(app)

    from .controllers.general import general
    from .controllers.admin.admin import admin

    app.register_blueprint(general, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin/')

    from .models import User
    from .data_loaders.load_data import run_data_loaders

    if not config_name:
        create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'general.home'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    if not config_name:
        run_data_loaders(app, db)

    return app

def create_database(app):
    if not os.path.exists('website/' + DB_NAME):
        with app.app_context():
            reset_database()
            db.create_all()
            print('Created Database')

def reset_database():
    db.drop_all() #RESET DATABASE
    print('DATABASE RESET')