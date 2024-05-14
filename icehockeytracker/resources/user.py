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

class UserCollection(Resource):
    """
    Class that represents a collection of Users, reachable at '/api/users/' and \n requires 
    admin authentication.
    """

    # must explicitly specify current working directory because otherwise
    # it will look in in cache dir
    @require_admin
    @swag_from(os.getcwd() + f"{DOC_FOLDER}user_collection/get.yml")
    @cache.cached(timeout=None, make_cache_key=request_path_cache_key)
    def get(self):
        """
        Get the list of al the users as a json response
        """

        body = IceHockeyTrackerBuilder(items=[])

        for user in User.query.all():
            item = IceHockeyTrackerBuilder(user.serialize(short_form=True))
            item.add_control("self", url_for('api.useritem', user=user))
            item.add_control("profile", USER_PROFILE)
            body["items"].append(item)

        body.add_namespace(NAMESPACE, LINK_RELATIONS_URL)
        body.add_control("self", url_for('api.usercollection'))
        body.add_control_add_user()

        return Response(json.dumps(body), 200, mimetype=MASON)

 

  @swag_from(f"{DOC_FOLDER}user_collection/post.yml")
    @require_admin_key
    def post(self):
 
        print(f"Request: {request.json}")
        print(f"Request Headers: {request.headers}")
        
        user = User()

        try:
            validate(request.json, User.json_schema(),
                     format_checker=Draft7Validator.FORMAT_CHECKER)

            user.deserialize(request.json)
            
            if User.query.filter_by(name=user.full_name).first():
                return create_error_response(409, "User already exists")

            
            db.session.add(user)
            db.session.commit()
        except ValidationError:
            return create_error_response(400, 'Bad Request', "Invalid request format")

        except IntegrityError:
            db.session.rollback()
            return create_error_response(
                409,
                'Conflict',
                f"User with full_name, nick_name, email, ssn '{user.ssn}' already exists."
            )

        self._clear_cache()
        return Response(
            status=201,
            headers={
                'Location': url_for('api.useritem', user=user)
            }
        )

    def _clear_cache(self):
        cache.delete(
            request.path
        )


class UserItem(Resource):
    """
    Class that represents a User Resource, reachable at '/api/users/<user_id>/'
    Available methods are GET, PUT and DELETE
    """

    # must explicitly specify current working directory because otherwise
    # it will look in in cache dir
    @swag_from(os.getcwd() + f"{DOC_FOLDER}user_item/get.yml")
    @cache.cached(timeout=None, make_cache_key=request_path_cache_key)
    def get(self, user):
     
        body = IceHockeyTrackerBuilder(user.serialize())

        self_url = url_for('api.useritem', user=user)

        body.add_namespace(NAMESPACE, LINK_RELATIONS_URL)
        body.add_control("self", self_url)
        body.add_control("profile", USER_PROFILE)
        body.add_control_put("Modify a user", self_url, User.json_schema())
        body.add_control_delete("Delete a user", self_url)
        body.add_control("collection", url_for('api.usercollection'))

        
        
        
        body.add_control(f"{NAMESPACE}:propic", self_url + "profilePicture/")

        return Response(json.dumps(body), 200, mimetype=MASON)

    @swag_from(f"{DOC_FOLDER}user_item/put.yml")
    @require_admin_key
    def put(self, user):
        try:
            validate(request.json, User.json_schema(),
                     format_checker=Draft7Validator.FORMAT_CHECKER)

            user.deserialize(request.json)

            db.session.add(user)
            db.session.commit()
        except ValidationError:
            return create_error_response(400, 'Bad Request', "Invalid request format")

        except IntegrityError:
            db.session.rollback()
            return create_error_response(
                409,
                'Conflict',
                f"User with ssn '{user.ssn}' already exists."
            )

        self._clear_cache()
        return Response(status=204)

    @swag_from(f"{DOC_FOLDER}user_item/delete.yml")
    @require_admin_key
    def delete(self, user):
      
        db.session.delete(user)
        db.session.commit()
        self._clear_cache()
        return Response(status=204)

    def _clear_cache(self):
        collection_path = url_for('api.usercollection')
        cache.delete_many(
            collection_path,
            request.path,
        )