from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load config from app.config module
    app.config.from_object('app.config.Config')
    
    # Initialize SQLAlchemy
    db.init_app(app)
    
    # Set up request logging middleware
    from app.utils.logger import setup_request_logging
    setup_request_logging(app)
    
    # Register routes
    from app.api.health import health_bp
    from app.api.coin import coin_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(coin_bp)
    
    return app

