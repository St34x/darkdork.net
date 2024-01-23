# app/__init__.py

from .routes.change_token_price import change_token_price_blueprint
from .routes.get_token_price import get_token_price_blueprint
from .routes.restore_session import restore_session_blueprint
from .routes.change_username import change_username_blueprint
from .routes.change_password import change_passwd_blueprint
from config import DevelopmentConfig, ProductionConfig
from flask import Flask, session, send_from_directory
from .routes.logout import logout_blueprint
from .routes.login import auth_blueprint
from flask_login import LoginManager
from flask_talisman import Talisman
from flask_session import Session
from datetime import timedelta
from .models import load_user
from flask_cors import CORS
from .database import db

def create_app():
    app = Flask(__name__, static_folder='../static')
    CORS(app)
    Talisman(app)
    
    app.config["ENV"] = 'development'
    
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # or 'Strict'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=3) 
    Session(app)

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(load_user)

    # Register the Blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    app.register_blueprint(logout_blueprint, url_prefix='/api/session')
    app.register_blueprint(restore_session_blueprint, url_prefix='/api/restore-session')
    app.register_blueprint(change_passwd_blueprint, url_prefix='/api/change-password')
    app.register_blueprint(change_username_blueprint, url_prefix='/api/change-username')
    app.register_blueprint(change_token_price_blueprint, url_prefix='/api/change-price')
    app.register_blueprint(get_token_price_blueprint, url_prefix='/api/tokens')

    if app.config["ENV"] == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    return app
