from app import db, bcrypt
import click
from flask.cli import with_appcontext
from sqlalchemy import event, CheckConstraint
from sqlalchemy.future import Engine
from sqlalchemy.orm import validates

from app.utilitys import is_valid_email

import datetime

class User(db.Model):
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
        return  {
			   'user_id': self.user_id,
               'full_name': self.full_name,
               'nick_name': self.nick_name,
			   'email': self.email,
               'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d'),
			   'ssn': self.ssn,
			   'role': self.role,
			   'rank': self.rank}
    
    def deserialize(self, doc):
        self.full_name = doc["full_name"]
        self.nick_name = doc["nick_name"]
        self.email = doc["email"]
        self.date_of_birth = datetime.date.fromisoformat(doc["date_of_birth"])
        self.ssn = doc["ssn"]
        self.password = self.hash_password(doc["password"])
        self.role = doc["role"]
        self.rank = doc["rank"]
	

class Team(db.Model):
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
        return  {
			   'team_id': self.team_id,
               'team_name': self.team_name,
               'team_description': self.team_description,
			   'team_coach_user_id': self.team_coach_user_id}
               
    def deserialize(self, doc):
        self.team_id = doc["team_id"]
        self.team_name = doc["team_name"]
        self.team_description = doc["team_description"]
        self.team_coach_user_id = doc["team_coach_user_id"]
     

class TeamUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey(
        "team.team_id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"), unique=True, nullable=False)
  
    contract_start_date = db.Column(db.Date, nullable=False)
    contract_end_date = db.Column(db.Date, nullable=False)

    user = db.relationship(
        "User", back_populates="teamusers", uselist=False)
    team = db.relationship(
        "Team", back_populates="teamusers", uselist=False)
    
    def serialize(self):
        return {
			   'team_id': self.team_id,
               'user_id': self.user_id,
               'contract_start_date': self.contract_start_date,
			   'contract_end_date': self.contract_end_date}
               
    def deserialize(self, doc):
        self.team_id = doc["team_id"]
        self.user_id = doc["user_id"]
        self.contract_start_date = doc["contract_start_date"]
        self.contract_end_date = doc["contract_end_date"]
     


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    rival_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    winner_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    
    match_level = db.Column(db.String(128), nullable=False)
    match_date = db.Column(db.Date, nullable=False)
    coach_comment = db.Column(db.String(256), nullable=False)
    team_coach_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    # Define relationships with Team
    host_team = db.relationship('Team', foreign_keys=[host_team_id], back_populates='matches_hosted', lazy=True)
    rival_team = db.relationship('Team', foreign_keys=[rival_team_id], back_populates='matches_rivaled', lazy=True)
    winner_team = db.relationship('Team', foreign_keys=[winner_team_id], back_populates='matches_won', lazy=True)


    user = db.relationship("User", back_populates="matches")
    

    def __init__(self, host_team_id, rival_team_id, winner_team_id, match_level, match_date, coach_comment, team_coach_user_id):
        self.host_team_id = host_team_id
        self.rival_team_id = rival_team_id
        self.winner_team_id = winner_team_id
        self.match_level = match_level
        self.match_date = match_date
        self.coach_comment = coach_comment
        self.team_coach_user_id = team_coach_user_id

    @staticmethod
    @validates('host_team_id', 'rival_team_id')
    def validate_host_rival_team_id(key, team_id):
        # Check that host and rival teams are not the same
        if key == 'rival_team_id' and team_id == getattr(g, 'host_team_id', None):
            raise ValueError('Rival team cannot be the same as the host team')
        return team_id
 
 
# Create the database tables
@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()


# Populate the database with some dummy data
@click.command("populate-db")
@with_appcontext
def populate_db_command():
    # populate users : players, coaches and a manager

    user1 = User(full_name="Player A Full Name ",nick_name="PLA", email="playera@gmail.com",date_of_birth=datetime.date.fromisoformat('1982-04-15'), ssn='4516784578', 
    password="password1", role="player", rank="8")
    
    user2 = User(full_name="Player B Full Name ",nick_name="PLB", email="playerb@gmail.com",date_of_birth=datetime.date.fromisoformat('1987-04-15'), ssn='4784591245', 
    password="password2", role="player", rank="2")
    
    user3 = User(full_name="Player C Full Name ",nick_name="PLC", email="playerc@gmail.com",date_of_birth=datetime.date.fromisoformat('1987-04-15'), ssn='7894564578', 
    password="password3", role="player", rank="1")
    
    
    
    user4 = User(full_name="Player D Full Name ",nick_name="PLD", email="playerd@gmail.com",date_of_birth=datetime.date.fromisoformat('1995-04-15'), ssn='4514084578', 
    password="password2", role="player", rank="8")
    
    user5 = User(full_name="Player E Full Name ",nick_name="PLE", email="playereb@gmail.com",date_of_birth=datetime.date.fromisoformat('1989-07-15'), ssn='4568981457', 
    password="password1", role="player", rank="3")
    
    user6 = User(full_name="Player F Full Name ",nick_name="PLF", email="playerf@gmail.com",date_of_birth=datetime.date.fromisoformat('2000-08-24'), ssn='7804567895', 
    password="password3", role="player", rank="1")
    
    
    user7 = User(full_name="Player G Full Name ",nick_name="PLG", email="playerg@gmail.com",date_of_birth=datetime.date.fromisoformat('1995-04-15'), ssn='4514784578', 
    password="password2", role="player", rank="8")
        
    user8 = User(full_name="Player H Full Name ",nick_name="PLH", email="playerh@gmail.com",date_of_birth=datetime.date.fromisoformat('1987-04-15'), ssn='1457831457', 
    password="password4", role="player", rank="3")
    
    user9 = User(full_name="Player I Full Name ",nick_name="PLI", email="playeri@gmail.com",date_of_birth=datetime.date.fromisoformat('2004-08-24'), ssn='7404567695', 
    password="password3", role="player", rank="1")
    
   

    user10 = User(full_name="Coach A Full Name ",nick_name="COA", email="coacha@gmail.com",date_of_birth=datetime.date.fromisoformat('1995-04-15'), ssn='4511784578', 
    password="password2", role="coach", rank="8")
    
    user11 = User(full_name="Coach B Full Name ",nick_name="COB", email="coachb@gmail.com",date_of_birth=datetime.date.fromisoformat('1987-04-30'), ssn='1957891457', 
    password="password4", role="coach", rank="3")
    
    user12 = User(full_name="Coach C Full Name ",nick_name="COC", email="coachc@gmail.com",date_of_birth=datetime.date.fromisoformat('1981-06-24'), ssn='7474567695', 
    password="password3", role="coach", rank="1")
    
    
    user13 = User(full_name="Manager Full Name ",nick_name="MANA", email="managera@gmail.com",date_of_birth=datetime.date.fromisoformat('2004-08-24'), ssn='7434567695', 
    password="password3", role="manager", rank="1")
    
    
    # populate teams data
    team1 = Team(team_name="Ice Skaters",team_description="Ice Skaters description", user=user10)
    team2 = Team(team_name="Winter warriors",team_description="Winter warrior description", user=user11)
    team3 = Team(team_name="Huskies",team_description="Huskies  description", user=user12)
 

    # populate teamuser data
    teamuser1 = TeamUser (team=team1,user=user1, contract_start_date=datetime.date.fromisoformat('2021-02-17'), contract_end_date=datetime.date.fromisoformat('2022-02-17'))
    teamuser2 = TeamUser (team=team1,user=user2, contract_start_date=datetime.date.fromisoformat('2021-02-17'), contract_end_date=datetime.date.fromisoformat('2022-02-17'))
    teamuser3 = TeamUser (team=team1,user=user3, contract_start_date=datetime.date.fromisoformat('2021-02-17'), contract_end_date=datetime.date.fromisoformat('2022-02-17'))
 
    teamuser4 = TeamUser (team=team2,user=user4, contract_start_date=datetime.date.fromisoformat('2021-04-17'), contract_end_date=datetime.date.fromisoformat('2022-02-17'))
    teamuser5 = TeamUser (team=team2,user=user5, contract_start_date=datetime.date.fromisoformat('2021-04-17'), contract_end_date=datetime.date.fromisoformat('2022-02-17'))
    
    teamuser6 = TeamUser (team=team3,user=user6, contract_start_date=datetime.date.fromisoformat('2021-04-17'), contract_end_date=datetime.date.fromisoformat('2022-02-17'))
 
    
    # populate match data
    
   # match1 = Match(host_team_id=team1,rival_team_id=team2,winner_team_id=team2, match_level="semifinal",match_date=datetime.date.fromisoformat('2021-06-17'), 
   #                coach_comment="Cocach A : Need extra defender", user=user10)
 
   # match2 = Match(host_team_id=team1,rival_team_id=team3,winner_team_id=team1, match_level="entry", match_date=datetime.date.fromisoformat('2021-04-12'),
   #               coach_comment="Cocach A : too many fowl incidents", user=user11)
 
 
    
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    
    db.session.add(user4)
    db.session.add(user5)
    db.session.add(user6)
    
    db.session.add(user7)
    db.session.add(user8)
    db.session.add(user9)
    
    
    db.session.add(user10)
    db.session.add(user11)
    db.session.add(user12)
    db.session.add(user13)
    
    
    
    db.session.add(team1)
    db.session.add(team2)
    db.session.add(team3)
    
    db.session.add(teamuser1)
    db.session.add(teamuser2)
    db.session.add(teamuser3)
    db.session.add(teamuser4)
    db.session.add(teamuser5)
    db.session.add(teamuser6)
   

    #db.session.add(match1)
    #db.session.add(match2)
    
  
    db.session.commit()
    
    
@click.command("delete-object")
@with_appcontext
def delete_object():
    object = User.query.first()
    db.session.delete(object)
    db.session.commit()
	
	