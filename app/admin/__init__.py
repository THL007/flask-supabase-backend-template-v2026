"""Flask-Admin setup."""
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


def setup_admin(app):
    """Setup Flask-Admin."""
    from app.extensions import db
    
    admin = Admin(app, name="Admin Panel", template_mode="bootstrap3")
    
    # Add model views here
    # from app.models.user import User
    # admin.add_view(ModelView(User, db.session))
    
    return admin

