"""Flask middleware setup."""
from functools import wraps
from flask import request, jsonify, g
import jwt
from app.extensions import supabase_client


def verify_supabase_jwt(token: str) -> dict | None:
    """Verify Supabase JWT token."""
    try:
        jwt_secret = supabase_client.jwt_secret
        if not jwt_secret:
            return None
        
        # Supabase uses HS256 algorithm
        payload = jwt.decode(
            token,
            jwt_secret,
            algorithms=["HS256"],
            options={"verify_exp": True}
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def require_auth(f):
    """Decorator to require Supabase JWT authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return jsonify({"error": "Missing authorization header"}), 401
        
        try:
            scheme, token = auth_header.split(" ", 1)
            if scheme.lower() != "bearer":
                return jsonify({"error": "Invalid authorization scheme"}), 401
        except ValueError:
            return jsonify({"error": "Invalid authorization header format"}), 401
        
        payload = verify_supabase_jwt(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Store user info in Flask g
        g.current_user_id = payload.get("sub")
        g.current_user_email = payload.get("email")
        g.current_user_metadata = payload.get("user_metadata", {})
        
        return f(*args, **kwargs)
    
    return decorated_function


def setup_middleware(app):
    """Setup application middleware."""
    @app.before_request
    def before_request():
        """Execute before each request."""
        # Add request ID for tracing
        import uuid
        g.request_id = str(uuid.uuid4())
        
        # Log request
        app.logger.info(
            "Request started",
            extra={
                "request_id": g.request_id,
                "method": request.method,
                "path": request.path,
                "remote_addr": request.remote_addr,
            }
        )

    @app.after_request
    def after_request(response):
        """Execute after each request."""
        # Add request ID to response headers
        if hasattr(g, "request_id"):
            response.headers["X-Request-ID"] = g.request_id
        
        # Log response
        app.logger.info(
            "Request completed",
            extra={
                "request_id": getattr(g, "request_id", None),
                "status_code": response.status_code,
                "method": request.method,
                "path": request.path,
            }
        )
        
        return response

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        if request.path.startswith("/api/"):
            return jsonify({"error": "Not found"}), 404
        return error

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        app.logger.error(
            "Internal server error",
            extra={
                "request_id": getattr(g, "request_id", None),
                "error": str(error),
            },
            exc_info=True
        )
        if request.path.startswith("/api/"):
            return jsonify({"error": "Internal server error"}), 500
        return error

