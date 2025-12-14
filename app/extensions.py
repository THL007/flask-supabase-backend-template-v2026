"""Flask extensions initialization."""
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from supabase import create_client, Client
import redis
from celery import Celery


# SQLAlchemy
db = SQLAlchemy()

# Supabase Client
class SupabaseClient:
    """Supabase client wrapper."""
    def __init__(self):
        self.client: Client | None = None
        self.url: str | None = None
        self.key: str | None = None
        self.service_role_key: str | None = None
        self.jwt_secret: str | None = None

    def init_app(self, app):
        """Initialize Supabase client with app configuration."""
        self.url = app.config.get("SUPABASE_URL")
        self.key = app.config.get("SUPABASE_KEY")
        self.service_role_key = app.config.get("SUPABASE_SERVICE_ROLE_KEY")
        self.jwt_secret = app.config.get("SUPABASE_JWT_SECRET")
        
        if self.url and self.key:
            self.client = create_client(self.url, self.key)
        else:
            app.logger.warning("Supabase credentials not configured")

    def get_client(self) -> Client:
        """Get Supabase client instance."""
        if not self.client:
            raise RuntimeError("Supabase client not initialized")
        return self.client

    def get_service_client(self) -> Client:
        """Get Supabase client with service role key."""
        if not self.url or not self.service_role_key:
            raise RuntimeError("Supabase service role key not configured")
        return create_client(self.url, self.service_role_key)


supabase_client = SupabaseClient()

# Redis Client
class RedisClient:
    """Redis client wrapper."""
    def __init__(self):
        self.cache_client: redis.Redis | None = None
        self.celery_client: redis.Redis | None = None

    def init_app(self, app):
        """Initialize Redis clients with app configuration."""
        cache_url = app.config.get("REDIS_CACHE_URL")
        celery_url = app.config.get("REDIS_URL")
        
        if cache_url:
            self.cache_client = redis.from_url(cache_url, decode_responses=True)
        if celery_url:
            self.celery_client = redis.from_url(celery_url, decode_responses=True)

    def get_cache(self) -> redis.Redis:
        """Get Redis cache client."""
        if not self.cache_client:
            raise RuntimeError("Redis cache client not initialized")
        return self.cache_client

    def get_celery(self) -> redis.Redis:
        """Get Redis Celery client."""
        if not self.celery_client:
            raise RuntimeError("Redis Celery client not initialized")
        return self.celery_client


redis_client = RedisClient()

# Rate Limiter (will be initialized in app factory)
limiter = None

# Celery
celery = Celery(__name__)

def make_celery(app):
    """Create Celery app with Flask context."""
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
    )

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context."""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

