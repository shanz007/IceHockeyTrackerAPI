"""
This module list all Model classes for IceHockeyTracker API
 - Role
 - Student
 - User
 - Rankbase
 - UserRank
 - Team
 - TeamUser
 - Match
 - MatchFeedback
 - UserAuthenticationKey
"""
import datetime
import hashlib
import secrets

from flask import request
from sqlalchemy.orm import validates
from werkzeug.exceptions import Forbidden

from icehockeytracker import db, bcrypt
from icehockeytracker.utils import is_valid_email
from icehockeytracker.utils import is_valid_ssn

class Role(db.Model):
    """
    This class lists all the roles that each user belongs.
    """
    role_id = db.Column(db.Integer, primary_key=True)
    role_code = db.Column(db.String(128), unique=True, nullable=False)
    role_name = db.Column(db.String(128), unique=True, nullable=False)
    role_description = db.Column(db.String(256), unique=True, nullable=False) 

    role_user = db.relationship(
        "User", cascade="all, delete-orphan", back_populates="user_role"
    )
    role_rankbase = db.relationship(
        "Rankbase", cascade="all, delete-orphan", back_populates="rankbase_role"
    )
    
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["role_code", "role_name", "role_description"]
        }
        props = schema["properties"] = {}
        props["role_code"] = {
            "description": "Role's unique code",
            "type": "string"
        }
        props["role_name"] = {
            "description": "Role's unique name",
            "type": "string"
        }
        props["role_description"] = {
            "description": "Role's description",
            "type": "string"
        }
        return schema
    
    
    def serialize(self):
        """
        Serializes the object into a dictionary.

        Returns:
            dict: A dictionary containing the serialized object data.
        """
        role = {
            'role_id': self.role_id,
            'role_code': self.role_code,
            'role_name': self.role_name,
            'role_description': self.role_description,
            }
        return role
    
    
    def deserialize(self, doc):
        """
        Deserialize the given document and populate the object attributes.

        Args:
            doc (dict): The document containing the data to be deserialized.

        Returns:
            None
        """
        self.role_code =  doc["role_code"]
        self.role_name =  doc["role_name"]
        self.role_description = doc("role_description")


class User(db.Model):
    """
    This class lists all the users.
    """
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(256), nullable=False, unique=True)
    nick_name = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    ssn = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id", ondelete="CASCADE"), nullable=False)
    rank = db.Column(db.Integer, default=0, nullable=False)
    
    @validates("email")
    def validate_email(self, key, email):
        assert is_valid_email(email)
        return email
    
    @validates("date_of_birth")
    def validate_date_of_birth(self, key, date_of_birth):
        # Check if date_of_birth is in the past
        assert date_of_birth < datetime.date.today(), "Date of birth must be in the past"
        return date_of_birth
    
    @validates("ssn")
    def validate_ssn(self, key, ssn):
        assert is_valid_ssn(ssn, self.date_of_birth)
        return ssn
    
    user_userauthkey = db.relationship("UserAuthenticationKey", cascade="all, delete-orphan", back_populates="userauthkey_user")
    user_role = db.relationship("Role", back_populates="role_user")
    user_team = db.relationship("Team", cascade="all, delete-orphan", back_populates="team_user")
    user_teamuser = db.relationship("TeamUser", cascade="all, delete-orphan", back_populates="teamuser_user")
    user_matchfeedback = db.relationship("MatchFeedback", cascade="all, delete-orphan", back_populates="matchfeedback_user")
    
    user_userrank = db.relationship("icehockeytracker.models.UserRank", cascade="all, delete-orphan", back_populates="userrank_user", foreign_keys="[UserRank.user_id]")
    user_userrank_ranker = db.relationship("icehockeytracker.models.UserRank", cascade="all, delete-orphan", back_populates="userrank_ranker_user", foreign_keys="[UserRank.ranker_user_id]")

    def __init__(self, full_name, nick_name, email, date_of_birth, ssn, password, role_id, rank):
        self.full_name = full_name
        self.nick_name = nick_name
        self.email = email
        self.date_of_birth = date_of_birth
        self.ssn = ssn
        self.password =  bcrypt.generate_password_hash(password).decode("utf-8")
        self.role_id = role_id
        self.rank = rank
    
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": [
                "full_name",
                "nick_name",
                "email",
                "date_of_birth",
                "ssn",
                "password",
                "role_id",
                "rank"]
            }
        props = schema["properties"] = {}
        props["full_name"] = {
            "description": "User's full_name",
            "type": "string"
        }
        props["nick_name"] = {
            "description": "User's nick name",
            "type": "string"
        }
        props["email"] = {
            "description": "User's email",
            "type": ["string"]
        }   
        props["date_of_birth"] = {
            "description": "User's date of birth  in format yyyy-mm-dd",
            "type": "string",
            "format": "date"
        }
        props["ssn"] = {
            "description": "User's social security number",
            "type": "string"
        }
        props["password"] = {
            "description": "User's password",
            "type": ["string"]
        }  
        props["role_id"] = {
            "description": "User's role id",
            "type": "integer"
        }
        props["rank"] = {
            "description": "User's rank",
            "type": "integer"
        }
        return schema
        
    def serialize(self):
        """
        Serializes the object into a dictionary.

        Returns:
            dict: A dictionary containing the serialized object data.
        """
        user = {
            'user_id': self.user_id,
            'full_name': self.full_name,
            'nick_name': self.nick_name,
            'email': self.email,
            'date_of_birth': self.date_of_birth,
            'ssn': self.ssn,
            'role_id': self.role_id,
            'rank': self.rank
            }
        return user
                
    def deserialize(self, doc):
        """
        Deserialize the given document and populate the object attributes.

        Args:
            doc (dict): The document containing the data to be deserialized.

        Returns:
            None
        """
        self.full_name = doc["full_name"]
        self.nick_name = doc["nick_name"]
        self.email = doc["email"]
        self.date_of_birth = datetime.date.fromisoformat(doc["date_of_birth"])
        self.ssn = doc["ssn"]
        self.password = self.hash_password(doc["password"])
        self.role_id = doc["role_id"]
        self.rank = doc["rank"]   


class Rankbase(db.Model):
    """
    Rankbase model class
    """
    rank_base_id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id", ondelete="CASCADE"))
    rank_base_code = db.Column(db.String(256), unique=True, nullable=False) 
    rank_score = db.Column(db.Integer, nullable=False)
    
    rankbase_role = db.relationship("Role", back_populates="role_rankbase")
    rankbase_userrank= db.relationship("UserRank", cascade="all, delete-orphan", back_populates="userrank_rankbase") 
 
    @staticmethod   
    def json_schema():
        schema = {
            "type": "object",
            "required": ["role_id", "rank_base_code", "rank_score"]
        }
        props = schema["properties"] = {}
        props["role_id"] = {
            "description": "Role's ID",
            "type": "integer"
        }
        props["rank_base_code"] = {
            "description": "Rankbase's unique code",
            "type": "string"
        }
        props["rank_score"] = {
            "description": "Rank's Score",
            "type": "integer"
        }
        return schema

    def serialize(self):
        """
        Serializes the object into a dictionary.

        Returns:
            dict: A dictionary containing the serialized object data.
        """
        rankbase = {
            'rank_base_id': self.rank_base_id,
            'role_id': self.role_id,
            'rank_base_code': self.rank_base_code,
            'rank_score': self.rank_score,
            }
        return rankbase
    
    def deserialize(self, doc):
        """
        Deserialize the given document and populate the object attributes.

        Args:
            doc (dict): The document containing the data to be deserialized.

        Returns:
            None
        """
        self.role_id =  doc["role_id"]
        self.rank_base_code =  doc["rank_base_code"]
        self.rank_score = doc("rank_score")

class UserRank(db.Model):
    """
    UserRank model class
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="CASCADE"))
    rank_base_id = db.Column(db.Integer, db.ForeignKey("rankbase.rank_base_id", ondelete="CASCADE"))
    ranker_comment = db.Column(db.String(512), nullable=False, unique=True) 
    ranker_user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="CASCADE"))
    ranked_added_date = db.Column(db.Date, nullable=False, default=datetime.date.today)
  
   
    userrank_rankbase = db.relationship("Rankbase", back_populates="rankbase_userrank")

    #userrank_user = db.relationship("User", back_populates="user_userrank")
    #userrank_ranker_user = db.relationship("User", back_populates="user_userrank_ranker")
    
    userrank_user = db.relationship('icehockeytracker.models.User', foreign_keys=[user_id], back_populates='user_userrank', lazy=True)
    userrank_ranker_user = db.relationship('icehockeytracker.models.User', foreign_keys=[ranker_user_id], back_populates='user_userrank_ranker', lazy=True)
    
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["user_id", "rank_base_id", "ranker_comment", "ranker_user_id", "ranked_added_date"]
        }
        props = schema["properties"] = {}
        props["user_id"] = {
            "description": "User ID",
            "type": "integer"
        }
        props["rank_base_id"] = {
            "description": "User Rank Base ID",
            "type": "integer"
        }
        props["ranker_comment"] = {
            "description": "Ranker's comment",
            "type": "string"
        }
        props["ranker_user_id"] = {
            "description": "Ranker's User ID",
            "type": "integer"
        }
        props["ranked_added_date"] = {
            "description": "Ranker's ranking added date in format yyyy-mm-dd",
            "type": "string",
            "format": "date"
        }
        return schema

    def serialize(self):
        """
        Serializes the object into a dictionary.

        Returns:
            dict: A dictionary containing the serialized object data.
        """
        rankbase = {
            'id': self.id,
            'user_id': self.user_id,
            'rank_base_id': self.rank_base_id,
            'ranker_comment': self.ranker_comment,
            'ranker_user_id': self.ranker_user_id,
            'ranked_added_date': self.ranked_added_date.strftime('%Y-%m-%d'),
            }
        return rankbase
    
    def deserialize(self, doc):
        """
        Deserialize the given document and populate the object attributes.

        Args:
            doc (dict): The document containing the data to be deserialized.

        Returns:
            None
        """
        self.user_id =  doc["user_id"]
        self.rank_base_id =  doc["rank_base_id"]
        self.ranker_comment =  doc["ranker_comment"]
        self.ranker_user_id =  doc["ranker_user_id"]
        self.ranked_added_date = datetime.date.fromisoformat(doc["ranked_added_date"])

class Team(db.Model):
    """
    Team model class
    """
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(128), unique=True, nullable=False)
    team_description = db.Column(db.String(256), nullable=False)
    team_coach_user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="CASCADE"), unique=True, nullable=False)
    
    team_user = db.relationship("User", back_populates="user_team")
    team_teamuser = db.relationship("TeamUser", cascade="all, delete-orphan", back_populates="teamuser_team")
    
    #team_match_hostteam = db.relationship("Match", cascade="all, delete-orphan", back_populates="match_hostteam")
    #team_match_rivalteam = db.relationship("Match", cascade="all, delete-orphan", back_populates="match_rivalteam")
    #team_match_winnerteam = db.relationship("Match", cascade="all, delete-orphan", back_populates="match_winnerteam")
    
    team_match_hostteam = db.relationship("Match", cascade="all, delete-orphan", back_populates="host_team", foreign_keys="[Match.host_team_id]")
    team_match_rivalteam = db.relationship("Match", cascade="all, delete-orphan", back_populates="rival_team", foreign_keys="[Match.rival_team_id]")
    team_match_winnerteam = db.relationship("Match", cascade="all, delete-orphan", back_populates="winner_team", foreign_keys="[Match.winner_team_id]")
    
    #team_matches_hosted = db.relationship("Match", cascade="all, delete-orphan", back_populates="host_team", foreign_keys="[Match.host_team_id]")
    #team_matches_rivaled = db.relationship("Match", cascade="all, delete-orphan", back_populates="rival_team", foreign_keys="[Match.rival_team_id]")
    #team_matches_won = db.relationship("Match", cascade="all, delete-orphan", back_populates="winner_team", foreign_keys="[Match.winner_team_id]")
    
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["team_id", "team_name", "team_description", "team_coach_user_id"]
        }
        props = schema["properties"] = {}
        props["team_id"] = {
            "description": "Team's ID",
            "type": "integer"
        }
        props["team_name"] = {
            "description": "Team's unique name",
            "type": "string"
        }
        props["team_description"] = {
            "description": "Team's description",
            "type": "string"
        }
        props["team_coach_user_id"] = {
            "description": "Team Coacher's user ID",
            "type": "integer"
        }
        return schema
    
    def serialize(self):
        team = {
            'team_id': self.team_id,
            'team_name': self.team_name,
            'team_description': self.team_description,
            'team_coach_user_id': self.team_coach_user_id
            }
        return team
    
    def deserialize(self, doc):
        self.team_name = doc["team_name"]
        self.team_description = doc["team_description"]
        self.team_coach_user_id = doc["team_coach_user_id"]
        

class TeamUser(db.Model):
    """
    TeamUser class
    """
    team_id = db.Column(db.Integer, db.ForeignKey(
        "team.team_id", ondelete="CASCADE"), nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), unique=True, nullable=False, primary_key=True)
    
    contract_start_date = db.Column(db.Date, nullable=False)
    contract_end_date = db.Column(db.Date, nullable=False)
     
    teamuser_user = db.relationship("User", back_populates="user_teamuser", uselist=False)
    teamuser_team = db.relationship("Team", back_populates="team_teamuser", uselist=False)
    
    @validates("contract_start_date")
    def validate_contract_start_date(self, key, contract_start_date):
        if contract_start_date <= datetime.date.today():
            raise ValueError("Contract start date cannot be past date")
        return contract_start_date

    @validates("contract_end_date")
    def validate_contract_end_date(self, key, contract_end_date):
        if contract_end_date <= self.contract_start_date:
            raise ValueError("Contract end date must be greater than start date")
        return contract_end_date 
    
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["team_id", "user_id", "contract_start_date", "contract_end_date"]
        }
        props = schema["properties"] = {}
        props["team_id"] = {
            "description": "Team's ID ",
            "type": "integer"
        }
        props["user_id"] = {
            "description": "User's ID",
            "type": "integer"
        }
        props["contract_start_date"] = {
            "description": "User's Contract start date in format yyyy-mm-dd",
            "type": "string",
            "format": "date"
        }
        props["contract_end_date"] = {
            "description": "User's Contract end date in format yyyy-mm-dd",
            "type": "string",
            "format": "date"
        }
        return schema
    
    def serialize(self):
        teamuser = {
            'team_id': self.team_id,
            'user_id': self.user_id,
            'contract_start_date': str(self.contract_start_date),
            'contract_end_date': str(self.contract_end_date)
            }
        return teamuser
                
    def deserialize(self, doc):
        self.team_id = doc["team_id"]
        self.user_id = doc["user_id"]
        self.contract_start_date = datetime.date.fromisoformat(doc["contract_end_date"])
        self.contract_end_date = datetime.date.fromisoformat(doc["contract_end_date"])


class Match(db.Model):
    """
    Match class
    """
    match_id = db.Column(db.Integer)
    host_team_id = db.Column(db.Integer, db.ForeignKey("team.team_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    rival_team_id = db.Column(db.Integer, db.ForeignKey("team.team_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    winner_team_id = db.Column(db.Integer, db.ForeignKey("team.team_id", ondelete="CASCADE"), primary_key=True, nullable=True)
    match_result = db.Column(db.String(128), nullable=False)

    match_level = db.Column(db.String(128), nullable=False)
    match_date = db.Column(db.Date, nullable=False)
    
    # Define relationships with Team
    #host_team = db.relationship('Team', foreign_keys=[host_team_id], back_populates='matches_hosted', lazy=True)
    #rival_team = db.relationship('Team', foreign_keys=[rival_team_id], back_populates='matches_rivaled', lazy=True)
    #winner_team = db.relationship('Team', foreign_keys=[winner_team_id], back_populates='matches_won', lazy=True)

    #match_hostteam = db.relationship("Team", back_populates="team_match_hostteam")
    #match_rivalteam = db.relationship("Team", back_populates="team_match_rivalteam")
    #match_winnerteam = db.relationship("Team", back_populates="team_match_winnerteam")
    
    host_team = db.relationship('Team', foreign_keys=[host_team_id], back_populates='team_match_hostteam', lazy=True)
    rival_team = db.relationship('Team', foreign_keys=[rival_team_id], back_populates='team_match_rivalteam', lazy=True)
    winner_team = db.relationship('Team', foreign_keys=[winner_team_id], back_populates='team_match_winnerteam', lazy=True)

    match_matchfeedback = db.relationship("MatchFeedback", cascade="all, delete-orphan", back_populates="matchfeedback_match")
   
    @validates("match_level")
    def validate_match_level(self, key, match_level):
        assert match_level in (['entry', 'quarterfinal', 'semifinal', 'final'])
        return match_level
    
    @validates("match_result")
    def validate_match_result(self, key, match_result):
        assert match_result in (['decided', 'undecided'])
        return match_result
    
             
    @staticmethod
    @validates('host_team_id', 'rival_team_id')
    def validate_host_rival_team_id(key, team_id):
        # Check that host and rival teams are not the same
        if key == 'rival_team_id' and team_id == getattr(g, 'host_team_id', None):
            raise ValueError('Rival team cannot be the same as the host team')
        return team_id  
    
    def __init__(self, match_id, host_team_id, rival_team_id, winner_team_id, match_result, match_level, match_date):
        self.match_id = match_id
        self.host_team_id = host_team_id
        self.rival_team_id = rival_team_id
        self.winner_team_id = winner_team_id
        self.match_result = match_result
        self.match_level = match_level
        self.match_date = match_date
          
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["match_id", "host_team_id", "rival_team_id", "winner_team_id", "match_result", "match_level", "match_date"]
        }
        props = schema["properties"] = {}
        props["match_id"] = {
            "description": "Match ID",
            "type": "integer"
        }
        props["host_team_id"] = {
            "description": "Host Team ID",
            "type": "integer"
        }
        props["rival_team_id"] = {
            "description": "Rival Team ID",
            "type": "integer"
        }
        props["winner_team_id"] = {
            "description": "Winner Team",
            "type": "integer",
        }
        props["match_result"] = {
            "description": " Match Result",
            "type": "string",
        }
        props["match_level"] = {
            "description": "Match Level",
            "type": "string",
        }
        props["match_date"] = {
            "description": "Match Date",
            "type": "string",
            "format": "date"
        }
        return schema

    def serialize(self):        
        match = {
            'match_id': self.match_id,
            'host_team_id': self.host_team_id,
            'rival_team_id': self.rival_team_id,
            'winner_team_id': self.winner_team_id,
            'match_result': self.match_result,
            'match_level': self.match_level,
            'match_date': self.match_date,
            }
        return match
    
    def deserialize(self, doc):
        self.host_team_id = doc["host_team_id"]
        self.rival_team_id = doc["rival_team_id"]
        self.winner_team_id = doc["winner_team_id"] 
        self.match_result = doc["match_result"] 
        self.match_level = doc["match_level"]
        self.match_date = doc["match_date"]


class MatchFeedback (db.Model):
    """
    MatchFeedback  model class
    """
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey("match.match_id", ondelete="CASCADE"))
    ranker_user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="CASCADE"))
    ranker_comment = db.Column(db.String(512), nullable=False, unique=True) 
    ranked_added_date = db.Column(db.Date, nullable=False, default=datetime.date.today)
    
    matchfeedback_match = db.relationship("Match", back_populates="match_matchfeedback")
    matchfeedback_user = db.relationship("User", back_populates="user_matchfeedback")
    
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["match_id", "ranker_user_id", "ranker_comment", "ranked_added_date"]
        }
        props = schema["properties"] = {}
        props["match_id"] = {
            "description": "Match ID",
            "type": "integer"
        }
        props["ranker_user_id"] = {
            "description": "Ranker's User ID",
            "type": "integer"
        }
        props["ranker_comment"] = {
            "description": "Ranker's comment",
            "type": "string"
        }
        props["ranked_added_date"] = {
            "description": "User comment addeded_date  in format yyyy-mm-dd",
            "type": "string",
            "format": "date"
        }
        return schema

    def serialize(self):
        """
        Serializes the object into a dictionary.

        Returns:
            dict: A dictionary containing the serialized object data.
        """
        rankbase = {
            'id': self.id,
            'match_id': self.match_id,
            'ranker_user_id': self.ranker_user_id,
            'ranker_comment': self.ranker_comment,
            'ranked_added_date': str(self.ranked_added_date),
            }
        return rankbase
    
    def deserialize(self, doc):
        """
        Deserialize the given document and populate the object attributes.

        Args:
            doc (dict): The document containing the data to be deserialized.

        Returns:
            None
        """
        self.match_id =  doc["match_id"]
        self.ranker_user_id =  doc["ranker_user_id"]
        self.ranker_comment =  doc["ranker_comment"]
        self.ranked_added_date = datetime.date.fromisoformat(doc["ranked_added_date"])
        
class UserAuthenticationKey(db.Model):
    """
    UserAuthenticationKey  model class for key generation
    """
    key = db.Column(db.String(32), primary_key=True, nullable=False, unique=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.user_id", ondelete="CASCADE"), nullable=True
    )
    admin = db.Column(db.Boolean, nullable=False, default=False)

    userauthkey_user = db.relationship("User", back_populates="user_userauthkey")
    
    @staticmethod
    def key_hash(key):  
        """
        This function computes the SHA-256 hash for the provided randomly generated token.
        :param key: A string representing the token utilized for the API.
        :return: The SHA-256 digest of the 'key' parameter.
        """
        return hashlib.sha256(key.encode()).digest()
    
    
#Taken from the course Sensorhub assignemnt project
def require_admin_key(func):
    """
    This decorator function executes the provided function only if the request includes an admin key.
    :param func: The function to execute if the request contains a key with admin privileges.
    :raise Forbidden: If the request does not contain an admin key.
    """

    def wrapper(*args, **kwargs):
        key_hash = UserAuthenticationKey.key_hash(request.headers.get(
            "IceHockeyTracker-Api-Key", "").strip())
        db_key = UserAuthenticationKey.query.filter_by(admin=True).first()
        if db_key is None or secrets.compare_digest(key_hash, db_key.key):
            return func(*args, **kwargs)
        raise Forbidden

    return wrapper


#Taken from the course Sensorhub assignemnt project
def require_assessments_key(func):
    """
    "This decorator function executes the specified function only if the request includes an API key.
    :param func: The function to execute if the request contains a valid key.
    :raise Forbidden: If the request does not contain an API key.
    """

    def wrapper(*args, **kwargs):
        key_hash = UserAuthenticationKey.key_hash(request.headers.get(
            "IceHockeyTracker-Api-Key", "").strip())
        db_keys = UserAuthenticationKey.query.all()
        for k in db_keys:
            if secrets.compare_digest(key_hash, k.key):
                return func(*args, **kwargs)
        raise Forbidden

    return wrapper