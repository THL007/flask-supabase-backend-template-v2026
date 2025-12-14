"""API blueprint for REST endpoints."""
from flask_smorest import Blueprint as Blp

api_bp = Blp("api", __name__, description="API endpoints")
api = None  # Will be set by app factory after Api is created

# Routes will be imported after api is set

