import re

from flask import request

def is_valid_email(email):
    """validare email

    Args:
        email (_type_): _description_

    Returns:
        _type_: _description_
    """    
    # Regular expression pattern for matching email addresses
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # Match the email address against the pattern
    if re.match(pattern, email):
        return True
    else:
        return False
    
def is_valid_ssn(ssn, date_of_birth):
    """ Validate provided ssn against the provided date of birth.
    Args:
        ssn (_type_): _description_
        date_of_birth (_type_): _description_

    Returns:
        _type_: _description_
    """    
    # Extracting the components of the SSN
    ssn_components = re.match(r'(\d{2})(\d{2})(\d{2})-(\d{4})', ssn)
    if not ssn_components:
        return False
    
    day, month, year, random = ssn_components.groups()
    
    # Formatting the date of birth
    formatted_dob = date_of_birth.strftime('%d%m%y')
    
    # Checking if the SSN date of birth matches the provided date of birth
    if day+month+year == formatted_dob:
        return True
    else:
        return False
        
        
       
"""
This file contains the util functions

"""

import os
import json
import secrets

from flask import abort, request, url_for, Response
from icehockeytracker.models import *

from icehockeytracker.constants import ERROR_PROFILE, MASON, NAMESPACE


class MasonBuilder(dict):
    """
    This class is taken directly from the Exercise 3 material on Lovelace:
    https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/exercise-3-api-documentation-and-hypermedia/#subclass-solution

    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.

    Note that child classes should set the *DELETE_RELATION* to the application
    specific relation name from the application namespace. The IANA standard
    does not define a link relation for deleting something.
    """

    DELETE_RELATION = ""

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.
        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.
        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, name_space, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.
        : param str name_space: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][name_space] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.
        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md
        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href

    def add_control_post(self, ctrl_name, title, href, schema):
        """
        Utility method for adding POST type controls. The control is
        constructed from the method's parameters. Method and encoding are
        fixed to "POST" and "json" respectively.

        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        : param str title: human-readable title for the control
        : param dict schema: a dictionary representing a valid JSON schema
        """

        self.add_control(
            ctrl_name,
            href,
            method="POST",
            encoding="json",
            title=title,
            schema=schema
        )

    def add_control_put(self, title, href, schema):
        """
        Utility method for adding PUT type controls. The control is
        constructed from the method's parameters. Control name, method and
        encoding are fixed to "edit", "PUT" and "json" respectively.

        : param str href: target URI for the control
        : param str title: human-readable title for the control
        : param dict schema: a dictionary representing a valid JSON schema
        """

        self.add_control(
            "edit",
            href,
            method="PUT",
            encoding="json",
            title=title,
            schema=schema
        )

    def add_control_delete(self, title, href):
        """
        Utility method for adding DELETE type controls. The control is
        constructed from the method's parameters. Control method is fixed to
        "DELETE", and control's name is read from the class attribute
        *DELETE_RELATION* which needs to be overridden by the child class.

        : param str href: target URI for the control
        : param str title: human-readable title for the control
        """

        self.add_control(
            f"{NAMESPACE}:delete",
            href,
            method="DELETE",
            title=title,
        )


class IceHockeyTrackerSystemBuilder(MasonBuilder):
    """
    IceHockeyTrackerSystem Builder, built maily on MasonBuilder as listed in above
    """
   
    def add_control_all_roles(self):
        """
        A method for  collection of all roles with GET method.
        """
        self.add_control(
            f"{NAMESPACE}:roles-all",
            url_for('api.rolecollection'),
            method="GET",
            title="The collection of all roles"
        )
    
    
    def add_control_all_users(self):
        """
        A method for collection of all users with GET method.
        """
        self.add_control(
            f"{NAMESPACE}:users-all",
            url_for('api.usercollection'),
            method="GET",
            title="The collection of all users"
        )
    
   
    
    def add_control_all_teams(self):
        """
        A method for collection of all teams with GET method.
        """
        self.add_control(
            f"{NAMESPACE}:teams-all",
            url_for('api.teamcollection'),
            method="GET",
            title="The collection of all teams"
        )
    
    
   
    # For Role related ones

    def add_control_delete_role(self, role):
        """
        A method to add control to delete roles
        """
        self.add_control(
            f"{NAMESPACE}:delete-role",
            url_for("api.roleitem", role=role),
            method="DELETE",
            title="For delete a role"
        )

    def add_control_modify_role(self, role):
        """
        A method to add control to modify roles
        """
        self.add_control(
            "edit",
            url_for("api.roleitem", role=role),
            method="PUT",
            encoding="json",
            title="Edit this role",
            schema=Role.get_schema()
        )
        
    
    def add_control_add_role(self):
        """
        A method to add control to add roles
        """
        self.add_control(
            f"{NAMESPACE}:add-role",
            url_for("api.rolecollection"),
            method="POST",
            encoding="json",
            title="For add a new role",
            schema=Role.get_schema()
        )

    
    
    

    # For Team related ones


    def add_control_delete_team(self, team):
        """
        A method to add control to delete team
        """
        self.add_control(
            f"{NAMESPACE}:delete-team",
            url_for("api.teamitem", team=team),
            method="DELETE",
            title="For delete a team"
        )

    def add_control_add_team(self):
        """
        A method to add control to add a team
        """
        self.add_control(
            f"{NAMESPACE}:add-team",
            url_for("api.teamcollection"),
            method="POST",
            encoding="json",
            title="For add a new team",
            schema=Team.get_schema()
        )

    def add_control_modify_team(self, team):
        """
        A method to add control to modify team
        """
        self.add_control(
            "edit",
            url_for("api.teamitem", team=team),
            method="PUT",
            encoding="json",
            title="For edit a team",
            schema=Team.get_schema()
        )

    def add_control_add_user(self, role):
        """
        A method to add control to add user
        """
        self.add_control(
            f"{NAMESPACE}:add-user",
            url_for("api.usercollection", role=role),
            method="POST",
            encoding="json",
            title=" For adding a new user given the role",
            schema=User.get_schema()
        )

    def add_control_modify_user(self, user):
        """
        A method to add control to modify user
        """
        self.add_control(
            "edit",
            url_for("api.useritem", user=user),
            method="PUT",
            encoding="json",
            title="For editing a user",
            schema=User.get_schema()
        )

    def add_control_get_user(self, user):
        """
        A  method to add control to get user
        """
        self.add_control(
            f"{NAMESPACE}: user",
            url_for("api.useritem", user=user),
            method="GET",
            title="For getting a  user",
        )

    def add_control_delete_user(self, user):
        """
        A method to add control to delete user
        """
        self.add_control(
            f"{NAMESPACE}:delete-user",
            url_for("api.useritem", user=user),
            method="DELETE",
            title="For delete a user"
        )

    def add_control_user(self, user):
        """
        A method to add control to get a user
        """
        self.add_control(
            f"{NAMESPACE}:user",
            url_for("api.useritem", user=user),
            method="GET",
            title="For getting a user"
        )

    def add_control_match(self, Match):
        """
        A method to add control to get one match
        """
        self.add_control(
            f"{NAMESPACE}:match",
            url_for("api.matchtitem", match=match),
            method="GET",
            title="For getting match",
        )

    def add_control_match_list(self):
        """
        A method to add control to get matchs
        """
        self.add_control(
            f"{NAMESPACE}:matches-all",
            url_for("api.matchescollection"),
            method="GET",
            title="For getting a  matches",
        )

    def add_control_role(self, role):
        """
        A method  to add control to get one role
        """
        self.add_control(
            f"{NAMESPACE:role",
            url_for("api.roleitem", role=role),
            method="GET",
            title="get role"
        )

    def add_control_role_list(self):
        """
        A Method to the collection of all roles with GET method.

        """
        self.add_control(
            f"{NAMESPACE:roles-all",
            url_for("api.rolecollection"),
            method="GET",
            title="For getting a collection of all roles"
        )






