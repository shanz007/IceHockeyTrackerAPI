import datetime
from icehockeytracker import db, bcrypt

from flask.cli import with_appcontext
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

from icehockeytracker.utils import is_valid_email
from icehockeytracker.utils import is_valid_ssn

class User(db.Model):
    """
    User model class
    """
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(256), nullable=False)
    nick_name = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    ssn = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(64), default='player', nullable=False)
    rank = db.Column(db.Integer, CheckConstraint('rank >= 0 AND rank <= 10'), default=10, nullable=False)
    
    @validates("role")
    def validate_role(self, key, role):
        """
        Validates the role parameter.

        Args:
            key (str): The key associated with the role.
            role (str): The role to be validated.

        Returns:
            str: The validated role.

        Raises:
            AssertionError: If the role is not one of 'player', 'coach', or 'manager'.
        """
        assert role in (['player', 'coach', 'manager'])
        return role
    
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
    
    teams = db.relationship(
        "Team", cascade="all, delete-orphan", back_populates="user"
    )
    
    teamusers = db.relationship(
        "TeamUser", cascade="all, delete-orphan", back_populates="user")
    
    matches = db.relationship(
        "Match", cascade="all, delete-orphan", back_populates="user")
    
    def __init__(self, full_name, nick_name, email, date_of_birth, ssn, password, role, rank):
        self.full_name = full_name
        self.nick_name = nick_name
        self.email = email
        self.date_of_birth = date_of_birth
        self.ssn = ssn
        self.password =  bcrypt.generate_password_hash(password).decode("utf-8")
        self.role = role
        self.rank = rank
        
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
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d'),
            'ssn': self.ssn,
            'role': self.role,
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
        self.role = doc["role"]
        self.rank = doc["rank"]
    

class Team(db.Model):
    """
    Team model class
    """
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(128), unique=True, nullable=False)
    team_description = db.Column(db.String(256), nullable=False)
    team_coach_user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), unique=True, nullable=False)
    
    user = db.relationship("User", back_populates="teams")
    
    teamusers = db.relationship(
        "TeamUser", cascade="all, delete-orphan", back_populates="team")
    
    matches_hosted = db.relationship("Match", cascade="all, delete-orphan", back_populates="host_team", foreign_keys="[Match.host_team_id]")
    
    matches_rivaled = db.relationship("Match", cascade="all, delete-orphan", back_populates="rival_team", foreign_keys="[Match.rival_team_id]")
    
    matches_won = db.relationship("Match", cascade="all, delete-orphan", back_populates="winner_team", foreign_keys="[Match.winner_team_id]")
        
    
    
    def serialize(self):
        team = {
            'team_id': self.team_id,
            'team_name': self.team_name,
            'team_description': self.team_description,
            'team_coach_user_id': self.team_coach_user_id
            }
        return team
    
                
    def deserialize(self, doc):
        self.team_id = doc["team_id"]
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

    user = db.relationship(
        "User", back_populates="teamusers", uselist=False)
    team = db.relationship(
        "Team", back_populates="teamusers", uselist=False)
    
    def serialize(self):
        teamuser = {
            'team_id': self.team_id,
            'user_id': self.user_id,
            'contract_start_date': self.contract_start_date,
            'contract_end_date': self.contract_end_date
            }
        return teamuser
                
    def deserialize(self, doc):
        self.team_id = doc["team_id"]
        self.user_id = doc["user_id"]
        self.contract_start_date = doc["contract_start_date"]
        self.contract_end_date = doc["contract_end_date"]
        


class Match(db.Model):
    """
    Match class
    """
    match_id = db.Column(db.Integer)
    host_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), primary_key=True, nullable=False)
    rival_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), primary_key=True, nullable=False)
    winner_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), primary_key=True, nullable=False)
    team_coach_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    match_level = db.Column(db.String(128), nullable=False)
    match_date = db.Column(db.Date, nullable=False)
    coach_comment = db.Column(db.String(256), nullable=False)
    
    # Define relationships with Team
    host_team = db.relationship('Team', foreign_keys=[host_team_id], back_populates='matches_hosted', lazy=True)
    rival_team = db.relationship('Team', foreign_keys=[rival_team_id], back_populates='matches_rivaled', lazy=True)
    winner_team = db.relationship('Team', foreign_keys=[winner_team_id], back_populates='matches_won', lazy=True)

    user = db.relationship("User", back_populates="matches")
    
    
    @validates("match_level")
    def validate_match_level(self, key, match_level):
        assert match_level in (['entry', 'quarterfinal', 'semifinal', 'final'])
        return match_level
    
    
    def __init__(self, match_id, host_team_id, rival_team_id, winner_team_id, team_coach_user_id, match_level, match_date, coach_comment):
        self.match_id = match_id
        self.host_team_id = host_team_id
        self.rival_team_id = rival_team_id
        self.winner_team_id = winner_team_id
        self.team_coach_user_id = team_coach_user_id
        self.match_level = match_level
        self.match_date = match_date
        self.coach_comment = coach_comment

    def serialize(self):        
        match = {
            'match_id': self.match_id,
            'host_team_id': self.host_team_id,
            'rival_team_id': self.rival_team_id,
            'winner_team_id': self.winner_team_id,
            'team_coach_user_id': self.team_coach_user_id,
            'match_level': self.match_level,
            'match_date': self.match_date,
            'coach_comment': self.coach_comment
            }
        return match
    
    def deserialize(self, doc):
        self.match_id = doc["match_id"]
        self.host_team_id = doc["host_team_id"]
        self.rival_team_id = doc["rival_team_id"]
        self.winner_team_id = doc["winner_team_id"] 
        self.team_coach_user_id = doc["team_coach_user_id"]
        self.match_level = doc["match_level"]
        self.match_date = doc["match_date"]
        self.coach_comment = doc["coach_comment"]

        
    @staticmethod
    @validates('host_team_id', 'rival_team_id')
    def validate_host_rival_team_id(key, team_id):
        # Check that host and rival teams are not the same
        if key == 'rival_team_id' and team_id == getattr(g, 'host_team_id', None):
            raise ValueError('Rival team cannot be the same as the host team')
        return team_id