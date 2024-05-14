"""
This module contains all the classes related to the Role resource:
 - the collection of all roles
 - a singular role
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

from icicehockeytracker import cache
from icehockeytracker import db
from icehockeytracker.builder import IceHockeyTrackerBuilder, create_error_response
from icehockeytracker.constants \
import ROLE_PROFILE, MASON, LINK_RELATIONS_URL, NAMESPACE, DOC_FOLDER
from icehockeytracker.models import Role, require_admin_key
from icehockeytracker.utils import request_path_cache_key
from icehockeytracker.constants import *


from icehockeytracker.utils import create_error_message, IceHockeyTrackerBuilder
from icehockeytracker.utils import require_admin


class RoleCollection(Resource):
    """ This class contains the GET and POST method implementations for role data
        Arguments:
        Returns:
        Endpoint: /api/roles/
    """
    @require_admin
    @swag_from(os.getcwd() + f"{DOC_FOLDER}role_collection/get.yml")
    @cache.cached(timeout=None, make_cache_key=request_path_cache_key)
    def get(self):
        """ GET list of roles as json response
            Arguments:
            Returns:
                List of roles
            responses:
                '200':
                description: The Roles retrieve successfully
        """

        body = IceHockeyTrackerBuilder(items=[])
        body.add_namespace(NAMESPACE, LINK_RELATIONS_URL)
        body.add_control('self', url_for("api.rolecollection"))
        body.add_control_add_role()
        body.add_control_get_employee_all()
        body["items"] = []

    
        for role in Role.query.all():
            item = IceHockeyTrackerBuilder(roles.serialize())
            item.add_control("self", url_for('api.roleitem', role=role))
            item.add_control("profile", ROLE_COLLECTION_PROFILE)
            body["items"].append(item)

        return Response(json.dumps(body), 200, mimetype=MASON)
    
    
    @require_admin
    def post(self):
        """ Create a new Role
        Arguments:
            request:
                name: Manager
                code: MAN
                description: Manager role
        Returns:
            responses:
                '201':
                description: The Role was created successfully
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
            validate(request.json, Role.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        try:
            db_role = Role.query.filter_by(code=request.json["role_code"]).first()
            if db_role is not None:
                return create_error_message(
                    409, "Already Exist",
                    "Role id is already exist"
                )
            role = Role()
            role.deserialize(request)
            db.session.add(role)
            db.session.commit()

            location = url_for("api.roleitem", role=role)
        except Exception as error:
            if isinstance(error, HTTPException):
                return create_error_message(
                    413, "Already Exist",
                    "role code is already exist"
                )
            return create_error_message(
                500, "Internal Server Error",
                "Internal Server Error occurred!"
            )
        self._clear_cache()
        return Response(response={}, status=201, headers={
            "Location": location
        }, mimetype=MASON)


class RoleItem(Resource):
    """ This class contains the GET, PUT and DELETE method implementations for a single role
        Arguments:
        Returns:
        Endpoint - /api/roles/<role>
    """
    @require_admin
    @swag_from(os.getcwd() + f"{DOC_FOLDER}role_item/get.yml")
    @cache.cached(timeout=None, make_cache_key=request_path_cache_key)
    def get(self, role):
        """ get details of one role
        Arguments:
            role object containing the information about the role
        Returns:
            Response
                '200':
                description: Data of list of role
                '404':
                description: The role was not found
        """
        body = IceHockeyTrackerBuilder(student.serialize())

        body.add_namespace(NAMESPACE, LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.roleitem", role=role))
        body.add_control("profile", ROLE_PROFILE)
        body.add_control("collection", url_for("api.rolecollection"))
       #body.add_control_delete_role(role)
       #body.add_control_modify_role(role)
        body.add_control_put("Modify a role", self_url, Role.json_schema())
        body.add_control_delete("Delete a role", self_url)
        
        return Response(json.dumps(body), 200, mimetype=MASON)

    
    @swag_from(f"{DOC_FOLDER}role_item/delete.yml")
    @require_admin_key
    def delete(self, role):
        """ Delete the selected role
        Arguments:
            role
        Returns:
            responses:
                '204':
                    description: The role was successfully deleted
                '404':
                    description: The role was not found
        """
        db.session.delete(role)
        db.session.commit()
        self._clear_cache()

        return Response(status=204, mimetype=MASON)
        
    def _clear_cache(self):
        collection_path = url_for('api.roletcollection')
        cache.delete_many(
            collection_path,
            request.path,
        )

    @swag_from(f"{DOC_FOLDER}role_item/put.yml")
    @require_admin_key    
    def put(self, role):
        """ Replace role's basic data with new values
        Arguments:
            role
        Returns:
            responses:
                '204':
                description: The role's attributes were updated successfully
                '400':
                description: The request body was not valid
                '404':
                description: The role was not found
                '409':
                description: A role with the same name already exists
                '415':
                description: Wrong media type was used
        """
        db_role = Role.query.filter_by(code=role.code).first()

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Role.get_schema())
            
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        db_role.role_name = request.json["role_name"]
        db_role.role_code = request.json["role_code"]
        db_role.role_description = request.json["role_description"]

        try:
            db.session.commit()
        except (Exception, ):
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the role"
            )
        self._clear_cache()
        return Response(status=204, mimetype=MASON)
    
    
    
    def _clear_cache(self):
        cache.delete(
            request.path
        )