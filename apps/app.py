from flask import Flask
from apps.config import config_dict
from apps import db, login_manager
from apps.blueprints.sales import sales_bp
from apps.blueprints.financial import financial_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(sales_bp)
    app.register_blueprint(financial_bp)

    return app
