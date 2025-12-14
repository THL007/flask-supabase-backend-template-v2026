"""Web blueprint for SSR pages."""
from flask import Blueprint

web_bp = Blueprint("web", __name__)

from app.blueprints.web import routes

