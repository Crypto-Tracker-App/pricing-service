from os import environ 

class Config:
    DB_USER = environ.get("POSTGRES_USER")
    DB_PASS = environ.get("POSTGRES_PASSWORD")
    DB_NAME = environ.get("POSTGRES_DB")
    DB_PORT = environ.get("DB_PORT")
    DB_HOST = environ.get("DB_HOST")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 3600,
        "pool_timeout": 30,
        "echo": False
    }