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
    icehockeytracker = Flask(__name__, instance_relative_config=True)

    # Configure the Flask application
    configure_app(icehockeytracker, test_config)

    # Initialize extensions and configure within the application context
    with icehockeytracker.app_context():
        initialize_extensions(icehockeytracker)

    # Add CLI commands
    add_cli_commands(icehockeytracker)

    return icehockeytracker

def configure_app(icehockeytracker, test_config):
    # Default configuration
    icehockeytracker.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(icehockeytracker.instance_path, "development.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CACHE_TYPE="FileSystemCache",
        CACHE_DIR=os.path.join(icehockeytracker.instance_path, "cache"),
    )

    # Load additional configuration from test_config if provided
    if test_config:
        icehockeytracker.config.from_mapping(test_config)

    # Ensure the instance directory exists
    try:
        os.makedirs(icehockeytracker.instance_path)
    except OSError:
        pass

def initialize_extensions(icehockeytracker):
    # Initialize and configure Flask extensions
    db.init_app(icehockeytracker)
    db.create_all()
    cache.init_app(icehockeytracker)
    bcrypt.init_app(icehockeytracker)

def add_cli_commands(icehockeytracker):
    # Add CLI commands from models.py
    from . import dbutills
    icehockeytracker.cli.add_command(dbutills.init_db_command)
    icehockeytracker.cli.add_command(dbutills.populate_db_command)
    icehockeytracker.cli.add_command(dbutills.delete_object)