"""
This module encapsulated all the requirments of Flask application
"""
import json
import os
import logging
from flasgger import Swagger, swag_from
from flask import Flask, send_from_directory, Response
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_bcrypt import Bcrypt


from icehockeytracker.constants import LINK_RELATIONS_URL, MASON, NAMESPACE, DOC_FOLDER
from icehockeytracker.utils import request_path_cache_key

# Initialize extensions
cache = Cache()
db = SQLAlchemy()
bcrypt = Bcrypt()

def configure_logging():
    logging.basicConfig(level=logging.DEBUG,  # Set the default logging level
                        format='%(levelname)s:%(name)s: %(message)s')  # Custom format

def create_app(test_config=None):
    # Create the Flask application
    icehockeytracker = Flask(__name__, instance_relative_config=True, static_folder='static', static_url_path='')

    # Configure the Flask application
    configure_app(icehockeytracker, test_config)
    
    
    # Configure logging
    configure_logging()

    # Initialize extensions and configure within the application context
    with icehockeytracker.app_context():
        initialize_extensions(icehockeytracker)

     
    # Add CLI commands
    add_cli_commands(icehockeytracker)
    print("add_cli_commands accessed!!!")  # Print to console
    logging.info("add_cli_commands accessed!!!")

    
    @icehockeytracker.route(LINK_RELATIONS_URL)
    def send_link_relations():
        return icehockeytracker.send_static_file("html/linkrelation.html")
        
   
    @icehockeytracker.route("/profiles/<profile>/")
    def send_profile(profile):
        # return "you requests {} profile".format(profile)
        if profile == 'role_item':
            return app.send_static_file("html/roleitem.html")
        elif profile == 'role_collection':
            return app.send_static_file("html/rolecollection.html")
        elif profile == 'user_item':
            return app.send_static_file("html/useritem.html")
        elif profile == 'user_collection':
            return app.send_static_file("html/usercollection.html")
        elif profile == 'team_item':
            return app.send_static_file("html/teamitem.html")
        elif profile == 'team_collection':
            return app.send_static_file("html/teamcollection.html")
        elif profile == 'match_item':
            return app.send_static_file("html/matchitem.html")
        elif profile == 'match_collection':
            return app.send_static_file("html/matchcollection.html")
        elif profile == 'rankbase_item':
            return app.send_static_file("html/rankbaseitem.html")
        elif profile == 'rankbase_collection':
            return app.send_static_file("html/rankbasecollection.html")
        elif profile == 'error':
            return app.send_static_file("html/error.html")
        else:
            return "Not available"

    @icehockeytracker.route("/icehockeytracker/")
    def admin_site():
        return app.send_static_file("index.html")
        
    
    # avoids circular imports
    from icehockeytracker.utils import IceHockeyTrackerSystemBuilder 

    @cache.cached(timeout=None, make_cache_key=request_path_cache_key)
    @icehockeytracker.route('/api/')
    @swag_from(os.getcwd() + f"{DOC_FOLDER}entrypoint/get.yml")
    def api_entrypoint():
        """
        Entrypoint to the API
        """
        body = IceHockeyTrackerSystemBuilder()
        body.add_namespace(NAMESPACE, LINK_RELATIONS_URL)
        body.add_control_all_roles()
        body.add_control_all_users()
        body.add_control_all_teams()
        return Response(json.dumps(body), 200, mimetype=MASON)

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
    icehockeytracker.config['DEBUG'] = True

    icehockeytracker.config["SWAGGER"] = {
        "title": "PWP IceHockeyTracker  API",
        "openapi": "3.0.3",
        "uiversion": 3,
        "doc_dir": "./doc",
    }
  
    SWAGGER_SETTINGS = {
        'DEFAULT_INFO': 'urls.swagger_info',   #your swagger_info on your urls page
    }

    REDOC_SETTINGS = {
        'SPEC_URL': ('schema-json', {'format': '.json'}),
    }

    Swagger(icehockeytracker, template_file="doc/doc.yml")
   
    # Load additional configuration from test_config if provided
    if test_config is None:
        icehockeytracker.config.from_pyfile("config.py", silent=True)
    else:
        icehockeytracker.config.from_mapping(test_config)

    # Ensure the instance directory exists
    try:
        os.makedirs(icehockeytracker.instance_path)
    except OSError:
        pass

def initialize_extensions(icehockeytracker):
    # Initialize and configure Flask extensions
    db.init_app(icehockeytracker)
   # db.create_all()
    cache.init_app(icehockeytracker)
    bcrypt.init_app(icehockeytracker)


def add_url_converters(icehockeytracker):
    
    from icehockeytracker.converters import (RoleConverter,
                                      UserConverter,
                                      TeamConverter,
                                      RankbaseConverter
                                      )

    # Add converters
    icehockeytracker.url_map.converters["Role"] = RoleConverter
    icehockeytracker.url_map.converters["User"] = UserConverter
    icehockeytracker.url_map.converters["Team"] = TeamConverter
    icehockeytracker.url_map.converters["Rankbase"] = RankbaseConverter
  #  icehockeytracker.url_map.converters["Match"] = MatchConverter
        

def add_cli_commands(icehockeytracker):
    # Add CLI commands from models.py  
    from icehockeytracker.dbutills import populate_db_command, init_db_command, generate_master_key, delete_object
    from . import api
    
    icehockeytracker.cli.add_command(dbutills.init_db_command)
    icehockeytracker.cli.add_command(dbutills.populate_db_command)
    #icehockeytracker.cli.add_command(run_tests)
    icehockeytracker.cli.add_command(generate_master_key)
    logging.info("generate_master_key accessed!!!")

 
    # icehockeytracker.cli.add_command(dbutills.delete_object)
 
    #Add URL Converters 
    add_url_converters(icehockeytracker)
    
    icehockeytracker.register_blueprint(api.api_bp)
