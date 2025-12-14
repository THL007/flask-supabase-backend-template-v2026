"""Flask application factory."""
import logging
from flask import Flask
from flask_smorest import Api
from app.config import Config
from app.extensions import (
    db,
    supabase_client,
    redis_client,
)
from app.middleware import setup_middleware
from app.monitoring import setup_monitoring


def create_app(config_class=Config):
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    supabase_client.init_app(app)
    redis_client.init_app(app)
    
    # Initialize rate limiter with Redis storage
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    
    # Get rate limit config - use list format for reliability
    default_limits = app.config.get("RATELIMIT_DEFAULT", ["200 per day", "50 per hour"])
    if not isinstance(default_limits, list):
        # Convert string to list if needed
        default_limits = [limit.strip() for limit in str(default_limits).split(",")]
    
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=default_limits if app.config.get("RATELIMIT_ENABLED", True) else [],
        storage_uri=app.config.get("RATELIMIT_STORAGE_URL", "memory://"),
    )
    app.limiter = limiter  # Make limiter accessible via app
    
    # Initialize Celery
    from app.extensions import make_celery
    celery_app = make_celery(app)
    app.celery = celery_app  # Make celery accessible via app

    # Setup monitoring
    setup_monitoring(app)

    # Setup middleware
    setup_middleware(app)

    # Initialize Flask-Smorest API
    api = Api(app)
    app.api = api  # Store api on app for easy access
    
    # Import blueprint module and set api instance BEFORE importing routes
    import app.blueprints.api as api_module
    from app.blueprints.api import api_bp
    api_module.api = api
    
    # Now import routes (they need api to be set, so import after setting it)
    from app.blueprints.api import routes, schemas
    
    # Register blueprints
    from app.blueprints.web import web_bp
    from app.blueprints.blog import blog_bp
    from app.blueprints.auth import auth_bp

    app.register_blueprint(web_bp)
    api.register_blueprint(api_bp, url_prefix=app.config.get("API_PREFIX", "/api/v1"))
    app.register_blueprint(blog_bp, url_prefix="/blog")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Setup Flask-Admin if enabled
    if app.config.get("FLASK_ADMIN_ENABLED", False):
        from app.admin import setup_admin
        setup_admin(app)

    # Configure logging
    configure_logging(app)

    return app


def configure_logging(app):
    """Configure structured logging."""
    if not app.debug:
        try:
            from python_json_logger import jsonlogger
            handler = logging.StreamHandler()
            formatter = jsonlogger.JsonFormatter()
            handler.setFormatter(formatter)
            app.logger.addHandler(handler)
            app.logger.setLevel(logging.INFO)
        except ImportError:
            # Fallback to standard logging if python-json-logger is not installed
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            app.logger.addHandler(handler)
            app.logger.setLevel(logging.INFO)
            app.logger.warning("python-json-logger not installed, using standard logging")
    else:
        app.logger.setLevel(logging.DEBUG)

