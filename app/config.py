from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
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

    COINGEKO_API_KEY = environ.get("COINGECKO_API_KEY")