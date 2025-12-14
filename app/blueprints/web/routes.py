"""Web routes for SSR."""
from flask import render_template, current_app
from app.blueprints.web import web_bp


@web_bp.route("/")
def index():
    """Home page."""
    return render_template("index.html", title="Home")


@web_bp.route("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": current_app.config.get("API_TITLE")}

