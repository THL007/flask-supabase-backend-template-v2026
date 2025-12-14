"""Application configuration."""
import os
from pathlib import Path


class Config:
    """Base configuration."""
    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    DEBUG = os.environ.get("FLASK_ENV") == "development"
    
    # API Configuration
    API_TITLE = os.environ.get("APP_NAME", "Flask Supabase Backend")
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/api"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    API_SPEC_OPTIONS = {
        "info": {
            "title": API_TITLE,
            "version": API_VERSION,
        },
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        }
    }

    # Supabase Configuration
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET")

    # Database Configuration (Direct Postgres for SQLAlchemy)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "postgresql://postgres:postgres@localhost:5432/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Redis Configuration
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    REDIS_CACHE_URL = os.environ.get("REDIS_CACHE_URL", "redis://localhost:6379/1")

    # Celery Configuration
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TIMEZONE = "UTC"

    # Rate Limiting
    RATELIMIT_ENABLED = os.environ.get("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATELIMIT_STORAGE_URL = REDIS_URL
    # Default limits as a list (more reliable than string)
    rate_limit_per_minute = os.environ.get("RATE_LIMIT_PER_MINUTE", "60")
    RATELIMIT_DEFAULT = [f"{rate_limit_per_minute} per minute", "200 per day", "50 per hour"]

    # Sentry Configuration
    SENTRY_DSN = os.environ.get("SENTRY_DSN")
    SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT", "development")
    SENTRY_TRACES_SAMPLE_RATE = 1.0 if DEBUG else 0.1

    # OpenTelemetry Configuration
    OTEL_EXPORTER_OTLP_ENDPOINT = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    OTEL_SERVICE_NAME = os.environ.get("OTEL_SERVICE_NAME", "flask-backend")

    # Blog Configuration
    BLOG_STORAGE_BUCKET = os.environ.get("BLOG_STORAGE_BUCKET", "blog-content")
    BLOG_MAX_FILE_SIZE = int(os.environ.get("BLOG_MAX_FILE_SIZE", "10485760"))  # 10MB
    BLOG_CONTENT_DIR = Path(__file__).parent.parent / "content" / "blog"

    # Flask-Admin
    FLASK_ADMIN_ENABLED = os.environ.get("FLASK_ADMIN_ENABLED", "False").lower() == "true"

    # API Prefix
    API_PREFIX = os.environ.get("API_PREFIX", "/api/v1")


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SENTRY_TRACES_SAMPLE_RATE = 0.1


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    REDIS_URL = "redis://localhost:6379/2"
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}

