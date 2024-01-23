from dotenv import load_dotenv
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
    # Development-specific settings like database URIs

class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    # Testing-specific settings

class ProductionConfig(Config):
    """Production configuration."""

    # Production-specific settings

