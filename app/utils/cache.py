"""Redis caching utilities."""
from functools import wraps
from flask import current_app
from app.extensions import redis_client
import json
import hashlib


def cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate a cache key from prefix and arguments."""
    key_parts = [prefix]
    if args:
        key_parts.extend(str(arg) for arg in args)
    if kwargs:
        sorted_kwargs = sorted(kwargs.items())
        key_parts.extend(f"{k}:{v}" for k, v in sorted_kwargs)
    
    key_string = ":".join(key_parts)
    return f"cache:{hashlib.md5(key_string.encode()).hexdigest()}"


def get_cache(key: str, default=None):
    """Get value from cache."""
    try:
        cache = redis_client.get_cache()
        value = cache.get(key)
        if value is not None:
            return json.loads(value)
        return default
    except Exception as e:
        current_app.logger.warning(f"Cache get error: {e}")
        return default


def set_cache(key: str, value, ttl: int = 3600):
    """Set value in cache with TTL (seconds)."""
    try:
        cache = redis_client.get_cache()
        cache.setex(key, ttl, json.dumps(value))
    except Exception as e:
        current_app.logger.warning(f"Cache set error: {e}")


def delete_cache(key: str):
    """Delete value from cache."""
    try:
        cache = redis_client.get_cache()
        cache.delete(key)
    except Exception as e:
        current_app.logger.warning(f"Cache delete error: {e}")


def cached(ttl: int = 3600, key_prefix: str = None):
    """Decorator to cache function results."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key
            prefix = key_prefix or f"{f.__module__}.{f.__name__}"
            cache_key_str = cache_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            cached_value = get_cache(cache_key_str)
            if cached_value is not None:
                return cached_value
            
            # Execute function and cache result
            result = f(*args, **kwargs)
            set_cache(cache_key_str, result, ttl)
            return result
        
        return decorated_function
    return decorator

