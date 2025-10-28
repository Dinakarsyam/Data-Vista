import os
from flask_migrate import Migrate
from flask_minify import Minify
from sys import exit
from dotenv import load_dotenv

from apps.app import create_app
from apps import db
from apps.config import config_dict
import logging

load_dotenv()

DEBUG = (os.getenv('DEBUG', 'False') == 'True')
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT = ' + app_config.ASSETS_ROOT)
    app.logger.info("Flask app is running and endpoints should be accessible.")

if __name__ == "__main__":
    with app.app_context():
        # db.create_all() # This is commented out to prevent accidental table creation.
        # It's better to use Flask-Migrate for database schema management.
        pass
    app.run(debug=True)
