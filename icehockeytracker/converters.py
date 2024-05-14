
"""
This file contains the Converter methods
"""
from werkzeug.routing import BaseConverter
from icehockeytracker.models import Role, User, Team, UserRankings, Match, MatchFeedback, Department, Organization, LeavePlan, Employee
from icehockeytracker.utils import create_error_message


class RoleConverter(BaseConverter):
    """
    Converter for Role entity in URL parameter
    """

    def to_python(self, value):
        """
        convert to a role object
        """
        role = Role.query.filter_by(role_code=value).first()
        if role is None:
            return create_error_message(
                404, "Not found",
                "Role not found"
            )
        return role

    def to_url(self, value):
        """
        return role code
        """
        return str(value.role_code)


class RankbaseConverter(BaseConverter):
    """
    Converter for Rankbase entity in URL parameter
    """

    def to_python(self, value):
        """
        convert to a Rankbase object
        """
        department = Rankbase.query.filter_by(rank_base_id=value).first()
        if department is None:
            return create_error_message(
                404, "Not found",
                "Rankbase not found"
            )
        return department

    def to_url(self, value):
        """
        return rankbase id
        """
        return str(value.rank_base_id)


class UserRankConverter(BaseConverter):
    """
    Converter for UserRank entity in URL parameter
    """

    def to_python(self, value):
        """
        convert to a UserRank object
        """
        userRank = UserRank.query.filter_by(
            id=value).first()
        if userRank is None:
            return create_error_message(
                404, "Not found",
                "userRank not found"
            )
        return userRank

    def to_url(self, value):
        """
        return userRank id
        """
        return str(value.id)


class TeamConverter(BaseConverter):
    """
    Converter for team entity in URL parameter
    """

    def to_python(self, value):
        """
        convert to a Team  object
        """
        team = Team.query.filter_by(team_id=value).first()
        if team is None:
            return create_error_message(
                404, "Not found",
                "team not found"
            )
        return team

    def to_url(self, value):
        """
        return team id
        """
        return str(value.team_id)


class UserConverter(BaseConverter):
    """
    Converter for user entity in URL parameter
    """

    def to_python(self, value):
        """
        convert to a user object
        """
        user = User.query.filter_by(user_id=value).first()
        if user is None:
            return create_error_message(
                404, "Not found",
                "user not found"
            )
        return user

    def to_url(self, value):
        """
        return user id
        """
        return str(value.user_id)