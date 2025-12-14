"""Celery worker entry point."""
import os
from dotenv import load_dotenv
from app import create_app
from app.config import config

# Load environment variables
load_dotenv()

# Get config class from environment
env = os.environ.get("FLASK_ENV", "development")
config_class = config.get(env, config["default"])

app = create_app(config_class)
celery = app.celery

# Import tasks to register them
from app.tasks import example_tasks

if __name__ == "__main__":
    celery.start()

