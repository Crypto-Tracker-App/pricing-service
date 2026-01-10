from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Service metadata
    SERVICE_NAME = environ.get("SERVICE_NAME", "pricing-service")
    SERVICE_VERSION = environ.get("SERVICE_VERSION", "1.0.0")
    ENVIRONMENT = environ.get("ENVIRONMENT", "development")
    
    # Security
    SECRET_KEY = environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Database configuration
    DB_USER = environ.get("POSTGRES_USER", "postgres")
    DB_PASS = environ.get("POSTGRES_PASSWORD", "postgres")
    DB_NAME = environ.get("POSTGRES_DB", "pricing_db")
    DB_PORT = environ.get("DB_PORT", "5432")
    DB_HOST = environ.get("DB_HOST", "localhost")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 3600,
        "pool_timeout": 30,
        "echo": False
    }

    # External API configuration
    COINGECKO_API_KEY = environ.get("COINGECKO_API_KEY")

    # Logging configuration
    EXTERNAL_LOG_LEVEL = environ.get("EXTERNAL_LOG_LEVEL", "WARNING")
    LOG_REQUEST_COMPLETION = environ.get("LOG_REQUEST_COMPLETION", "errors")


class TestingConfig(Config):
    """Configuration for testing environment."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {'check_same_thread': False}
    }
    SECRET_KEY = 'test-secret-key-do-not-use-in-production'