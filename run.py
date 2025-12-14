"""Application entry point."""
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

if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_HOST", "0.0.0.0"),
        port=int(os.environ.get("FLASK_PORT", 5050)),
        debug=os.environ.get("FLASK_ENV") == "development",
    )

