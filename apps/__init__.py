from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import config_dict

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    # Registering blueprints
    from .blueprints.sales import sales_bp
    from .blueprints.financial import financial_bp

    app.register_blueprint(sales_bp)
    app.register_blueprint(financial_bp)

    from .database import close_db_connection
    app.teardown_appcontext(close_db_connection)

    return app
