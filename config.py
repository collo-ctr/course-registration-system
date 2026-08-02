import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Secret key for sessions and security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production-12345')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///course_registration.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database pool settings (for production)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
    
    # Session configuration
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Application settings
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
