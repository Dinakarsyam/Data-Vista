# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from flask_migrate import Migrate
from flask_minify import Minify
from sys import exit
from dotenv import load_dotenv

from apps import create_app, db
from apps.config import config_dict
import logging

# Load environment variables from .env file
load_dotenv()

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values
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
    logger.debug(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    logger.debug("Initializing database...")
    with app.app_context():
        db.create_all()
    logger.debug("Database initialized.")
    app.run(debug=True)
