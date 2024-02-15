
"""
This class is used to initialize & poulate database with test data.
"""

import datetime 
import click
from flask.cli import with_appcontext
from icehockeytracker import db
from icehockeytracker.models import User,Team,TeamUser,Match


# Create the database tables
@click.command("init-db")
@with_appcontext
def init_db_command():
    """
    Method to initialize database
    """
    print("create database===========================================>")
    db.create_all()


# Populate the database with some dummy data
@click.command("populate-db")
@with_appcontext
def populate_db_command():
    """
    Populates the database with sample data including users, teams, and team users.
    """
    print("Populate database===========================================>")
  
    user1 = User(full_name="Player A Full Name ",nick_name="PLA", email="playera@gmail.com",date_of_birth=datetime.date.fromisoformat('1982-04-15'), ssn='150482-6176', 
    password="password1", role="player", rank="8")
    
    user2 = User(full_name="Player B Full Name ",nick_name="PLB", email="playerb@gmail.com",date_of_birth=datetime.date.fromisoformat('1987-04-15'), ssn='150487-6176', 
    password="password2", role="player", rank="2")
    
    user3 = User(full_name="Player C Full Name ",nick_name="PLC", email="playerc@gmail.com",date_of_birth=datetime.date.fromisoformat('1987-04-15'), ssn='150487-6178', 
    password="password3", role="player", rank="1")
    
    
    
    user4 = User(full_name="Player D Full Name ",nick_name="PLD", email="playerd@gmail.com",date_of_birth=datetime.date.fromisoformat('1995-04-15'), ssn='150495-6976', 
    password="password2", role="player", rank="8")
    
    user5 = User(full_name="Player E Full Name ",nick_name="PLE", email="playereb@gmail.com",date_of_birth=datetime.date.fromisoformat('1989-07-15'), ssn='150789-6476', 
    password="password1", role="player", rank="3")
    
    user6 = User(full_name="Player F Full Name ",nick_name="PLF", email="playerf@gmail.com",date_of_birth=datetime.date.fromisoformat('2000-08-24'), ssn='240800-8975', 
    password="password3", role="player", rank="1")
    
    
    user7 = User(full_name="Player G Full Name ",nick_name="PLG", email="playerg@gmail.com",date_of_birth=datetime.date.fromisoformat('1995-04-15'), ssn='150495-6170', 
    password="password2", role="player", rank="8")
        
    user8 = User(full_name="Player H Full Name ",nick_name="PLH", email="playerh@gmail.com",date_of_birth=datetime.date.fromisoformat('1987-04-15'), ssn='150487-4236', 
    password="password4", role="player", rank="3")
    
    user9 = User(full_name="Player I Full Name ",nick_name="PLI", email="playeri@gmail.com",date_of_birth=datetime.date.fromisoformat('2004-08-24'), ssn='240804-6176', 
    password="password3", role="player", rank="1")
    
    

    user10 = User(full_name="Coach A Full Name ",nick_name="COA", email="coacha@gmail.com",date_of_birth=datetime.date.fromisoformat('1995-04-15'), ssn='150495-1176', 
    password="password2", role="coach", rank="8")
    
    user11 = User(full_name="Coach B Full Name ",nick_name="COB", email="coachb@gmail.com",date_of_birth=datetime.date.fromisoformat('1987-04-30'), ssn='300487-6176', 
    password="password4", role="coach", rank="3")
    
    user12 = User(full_name="Coach C Full Name ",nick_name="COC", email="coachc@gmail.com",date_of_birth=datetime.date.fromisoformat('1981-06-24'), ssn='240681-6173', 
    password="password3", role="coach", rank="1")


    user13 = User(full_name="Manager Full Name ",nick_name="MANA", email="managera@gmail.com",date_of_birth=datetime.date.fromisoformat('2004-08-24'), ssn='240804-5421', 
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
    teamuser6 = TeamUser (team=team2,user=user6, contract_start_date=datetime.date.fromisoformat('2021-04-17'), contract_end_date=datetime.date.fromisoformat('2022-02-17'))
  
    teamuser7 = TeamUser (team=team3,user=user7, contract_start_date=datetime.date.fromisoformat('2021-04-17'), contract_end_date=datetime.date.fromisoformat('2022-02-17'))
    teamuser8 = TeamUser (team=team3,user=user8, contract_start_date=datetime.date.fromisoformat('2021-04-17'), contract_end_date=datetime.date.fromisoformat('2022-02-17'))
    teamuser9 = TeamUser (team=team3,user=user9, contract_start_date=datetime.date.fromisoformat('2021-04-17'), contract_end_date=datetime.date.fromisoformat('2022-02-17'))

    # populate match data
    match1 = Match(1, 1, 2, 2, 10, "semifinal", datetime.date.fromisoformat('2021-06-17'), "Cocach A : Need extra defer")
    match2 = Match(2, 1, 3, 1, 11, "entry", datetime.date.fromisoformat('2021-04-12'), "Cocach B : too many penalties")
    match3 = Match(3, 4, 1, 1, 10, "entry", datetime.date.fromisoformat('2021-04-12'), "Cocach A : too many fowl incidents")
    match4 = Match(4, 5, 3, 3, 11, "quarterfinal", datetime.date.fromisoformat('2021-04-12'), "Cocach B : too many fowl incidents")
    match5 = Match(5, 2, 3, 2, 10, "semifinal", datetime.date.fromisoformat('2021-04-12'), "Cocach A : too many fowl incidents")
    match6 = Match(6, 5, 3, 5, 11, "final", datetime.date.fromisoformat('2021-04-12'), "Cocach B : too many fowl penalties")


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
    db.session.add(teamuser7)
    db.session.add(teamuser8)
    db.session.add(teamuser9)


    db.session.add(match1)
    db.session.add(match2)


    db.session.add(match3)
    db.session.add(match4)

    db.session.add(match5)
    db.session.add(match6)

    db.session.commit()
    

@click.command("delete-object")
@with_appcontext
def delete_object():
    """
    Method to delete object
    """
    print("delete session===========================================>")
    object = User.query.first()
    db.session.delete(object)
    db.session.commit()
