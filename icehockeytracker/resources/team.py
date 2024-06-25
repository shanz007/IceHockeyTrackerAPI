"""
This module contains all the classes related to the Team resource:
 - the collection of all teams
 - a singular team
 - the related URL converter
"""
import json
import os

from flasgger import swag_from
from flask import request, url_for, Response
from flask_restful import Resource
from jsonschema import validate, ValidationError
from jsonschema.validators import Draft7Validator
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter
from icehockeytracker.models import Role

from icehockeytracker import cache
from icehockeytracker import db
from icehockeytracker.constants \
import TEAM_PROFILE, MASON, LINK_RELATIONS_URL, NAMESPACE, DOC_FOLDER
from icehockeytracker.models import Team, require_admin_key
from icehockeytracker.utils import request_path_cache_key
from icehockeytracker.constants import *


from icehockeytracker.utils import create_error_message, IceHockeyTrackerSystemBuilder
from icehockeytracker.utils import require_admin


class TeamCollection(Resource):
    """ This class contains the GET and POST method implementations for team data
        Arguments:
        Returns:
        Endpoint: /api/teams/
    """
    #@require_admin
    @swag_from(os.getcwd() + f"{DOC_FOLDER}team_collection/get.yml")
    @cache.cached(timeout=None, make_cache_key=request_path_cache_key)
    def get(self):
        """ GET list of teams as json response
            Arguments:
            Returns:
                List of teams
            responses:
                '200':
                description: The Teams retrieve successfully
        """

        body = IceHockeyTrackerSystemBuilder(items=[])
        body.add_namespace(NAMESPACE, LINK_RELATIONS_URL)
        body.add_control('self', url_for("api.teamcollection"))
        body.add_control_add_team()
        body["items"] = []

    
        for team in Team.query.all():
            item = IceHockeyTrackerSystemBuilder(teams.serialize())
            item.add_control("self", url_for('api.teamitem', team=team))
            item.add_control("profile", TEAM_COLLECTION_PROFILE)
            body["items"].append(item)

        return Response(json.dumps(body), 200, mimetype=MASON)
    
    
    @require_admin
    def post(self):
        """ Create a new Team
        Arguments:
            request:
                team_name: Ice Skaters
                team_description: Ice Skaters description
                team_coach_user_id: 10
        Returns:
            responses:
                '201':
                description: The Team was created successfully
                '400':
                description: The request body was not valid
                '409':
                description: A role with the same code already exists
                '415':
                description: Wrong media type/invalid json was used
        """
        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Team.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        try:
            db_team = Team.query.filter_by(code=request.json["team_code"]).first()
            if db_team is not None:
                return create_error_message(
                    409, "Already Exist",
                    "Team id is already exist"
                )
            team = Team()
            team.deserialize(request)
            db.session.add(team)
            db.session.commit()

            location = url_for("api.teamitem", team=team)
        except Exception as error:
            if isinstance(error, HTTPException):
                return create_error_message(
                    413, "Already Exist",
                    "team code is already exist"
                )
            return create_error_message(
                500, "Internal Server Error",
                "Internal Server Error occurred!"
            )
        self._clear_cache()
        return Response(response={}, status=201, headers={
            "Location": location
        }, mimetype=MASON)


class TeamItem(Resource):
    """ This class contains the GET, PUT and DELETE method implementations for a single team
        Arguments:
        Returns:
        Endpoint - /api/teams/<team>
    """
    @require_admin
    @swag_from(os.getcwd() + f"{DOC_FOLDER}team_item/get.yml")
    @cache.cached(timeout=None, make_cache_key=request_path_cache_key)
    def get(self, team):
        """ get details of one team
        Arguments:
            team object containing the information about the team
        Returns:
            Response
                '200':
                description: Data of list of team
                '404':
                description: The team was not found
        """
        body = IceHockeyTrackerBuilder(student.serialize())

        body.add_namespace(NAMESPACE, LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.teamitem", team=team))
        body.add_control("profile", TEAM_PROFILE)
        body.add_control("collection", url_for("api.teamcollection"))
        body.add_control_delete_team(team)
        body.add_control_modify_team(team)
        body.add_control_put("Modify a team", self_url, Team.json_schema())
        body.add_control_delete("Delete a team", self_url)
        
        return Response(json.dumps(body), 200, mimetype=MASON)

    
    @swag_from(f"{DOC_FOLDER}team_item/delete.yml")
    @require_admin_key
    def delete(self, team):
        """ Delete the selected team
        Arguments:
            team
        Returns:
            responses:
                '204':
                    description: The team was successfully deleted
                '404':
                    description: The team was not found
        """
        db.session.delete(team)
        db.session.commit()
        self._clear_cache()

        return Response(status=204, mimetype=MASON)
        
    def _clear_cache(self):
        collection_path = url_for('api.teamcollection')
        cache.delete_many(
            collection_path,
            request.path,
        )

    @swag_from(f"{DOC_FOLDER}team_item/put.yml")
    @require_admin_key    
    def put(self, team):
        """ Replace team's basic data with new values
        Arguments:
            team
        Returns:
            responses:
                '204':
                description: The role's attributes were updated successfully
                '400':
                description: The request body was not valid
                '404':
                description: The team was not found
                '409':
                description: A team with the same name already exists
                '415':
                description: Wrong media type was used
        """
        db_team = Team.query.filter_by(code=team.code).first()

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Team.get_schema())
            
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        db_team.team_name = request.json["team_name"]
        db_team.team_description  = request.json["team_description"]
        db_team.team_coach_user_id = request.json["team_coach_user_id"]

        try:
            db.session.commit()
        except (Exception, ):
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the team"
            )
        self._clear_cache()
        return Response(status=204, mimetype=MASON)
    
    
    
    def _clear_cache(self):
        cache.delete(
            request.path
        )
        
    