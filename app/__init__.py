from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

db = SQLAlchemy()

def create_app(config_class=None):
    app = Flask(__name__)
    
    # Load config from app.config module
    if config_class is None:
        app.config.from_object('app.config.Config')
    else:
        app.config.from_object(config_class)
    
    # Initialize SQLAlchemy
    db.init_app(app)
    
    # Initialize Swagger/OpenAPI documentation
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Pricing Service API",
            "description": "API for cryptocurrency pricing data and market information",
            "version": "1.0.0"
        },
        "host": "",  # Will be set dynamically based on request
        "basePath": "/",
        "schemes": ["http", "https"],
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "JWT Bearer token authentication. Format: 'Bearer <token>'"
            }
        },
        "tags": [
            {
                "name": "Health",
                "description": "Health and readiness endpoints"
            },
            {
                "name": "Coins",
                "description": "Cryptocurrency data operations"
            }
        ]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Set up request logging middleware
    from app.utils.logger import setup_request_logging
    setup_request_logging(app)
    
    # Register routes
    from app.api.health import health_bp
    from app.api.coin import coin_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(coin_bp)
    
    # Register CLI commands
    register_cli_commands(app)
    
    return app


def register_cli_commands(app):
    """Register Flask CLI commands."""
    
    @app.cli.command()
    def seed():
        """Seed the database with initial coins."""
        from app.services.coin_service import CoinService
        from app.repositories.coin_repository import CoinRepository
        from app.utils.logger import get_logger
        
        logger = get_logger(__name__)
        
        with app.app_context():
            service = CoinService(CoinRepository())
            service.seed_database()
            logger.info("Database seeded successfully!")

    @app.cli.command()
    def update_market_data():
        """Update the market data for all coins."""
        from app.services.coin_service import CoinService
        from app.repositories.coin_repository import CoinRepository
        from app.services.alert_trigger_service import trigger_alert_check
        from app.utils.logger import get_logger
        
        logger = get_logger(__name__)
        
        with app.app_context():
            service = CoinService(CoinRepository())
            service.updateCoinMarketData()
            logger.info("Market data updated successfully!")
            
            # Trigger alert checking in alert-service with resilience
            try:
                trigger_alert_check()
            except Exception as e:
                logger.warning(f"Failed to trigger alert check (will retry): {e}")

