import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")

    if DB_USER and DB_PASSWORD and DB_HOST and DB_NAME:
        DB_PASSWORD_ENCODED = quote_plus(DB_PASSWORD)
        SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD_ENCODED}@{DB_HOST}/{DB_NAME}'
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ASSETS_ROOT = '/static/assets'

class ProductionConfig(Config):
    DEBUG = False
    # Add any production-specific configurations here

class DebugConfig(Config):
    DEBUG = True

config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
