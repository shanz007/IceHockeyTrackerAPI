from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_bcrypt import Bcrypt
import os

# Initialize extensions
cache = Cache()
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(test_config=None):
    # Create the Flask application
    app = Flask(__name__, instance_relative_config=True)

    # Configure the Flask application
    configure_app(app, test_config)

    # Initialize extensions and configure within the application context
    with app.app_context():
        initialize_extensions(app)

    # Add CLI commands
    add_cli_commands(app)

    return app

def configure_app(app, test_config):
    # Default configuration
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "development.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CACHE_TYPE="FileSystemCache",
        CACHE_DIR=os.path.join(app.instance_path, "cache"),
    )

    # Load additional configuration from test_config if provided
    if test_config:
        app.config.from_mapping(test_config)

    # Ensure the instance directory exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

def initialize_extensions(app):
    # Initialize and configure Flask extensions
    db.init_app(app)
    db.create_all()
    cache.init_app(app)
    bcrypt.init_app(app)

def add_cli_commands(app):
    # Add CLI commands from models.py
    from . import models
    app.cli.add_command(models.init_db_command)
    app.cli.add_command(models.populate_db_command)
    app.cli.add_command(models.delete_object)