from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()  # This loads variables from .env

class Config:
    """Base configuration."""
    APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')
    DATABASE_URI = os.environ.get('DATABASE_URI')

    SECRET_KEY = APP_SECRET_KEY
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True

class ProductionConfig(Config):
    """Production configuration."""
    ENV = 'production'
    DEBUG = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Strict'  # or 'Lax'
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=3)

