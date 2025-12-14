"""API routes - imported after api is initialized in app factory."""
from flask.views import MethodView
from flask_smorest import abort
from app.blueprints.api import api_bp
from app.blueprints.api.schemas import HealthResponseSchema
from app.middleware import require_auth


@api_bp.route("/health")
class HealthAPI(MethodView):
    """Health check endpoint."""
    
    @api_bp.response(200, HealthResponseSchema)
    def get(self):
        """Get API health status."""
        return {
            "status": "healthy",
            "version": "1.0.0",
            "service": "Flask Supabase Backend API"
        }


@api_bp.route("/protected")
class ProtectedAPI(MethodView):
    """Protected endpoint example."""
    
    @require_auth
    @api_bp.response(200)
    def get(self):
        """Get protected resource."""
        from flask import g
        return {
            "message": "This is a protected endpoint",
            "user_id": g.current_user_id,
            "user_email": g.current_user_email,
        }

