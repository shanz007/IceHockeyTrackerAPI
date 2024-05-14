
"""
This class is used to initialize & poulate database with test data.
""" 
import secrets
import datetime
import click
from flask.cli import with_appcontext
from icehockeytracker import db
from icehockeytracker.models import Role, Rankbase, User, UserAuthenticationKey,UserRank, Team, TeamUser, Match, MatchFeedback


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
@click.command("populate_test_data")
@with_appcontext
def populate_db_command():
    """
    Populates the database with sample data including users, teams, and team users.
    """
    print("Populate database===========================================>")

    # Format the current date as 'YYYY-MM-DD'
    #current_formatted_date = datetime.now().strftime('%Y-%m-%d')

    role1 = Role(role_code="PLA", role_name="Player", role_description="Player Role")
    role2 = Role(role_code="COA", role_name="Coach", role_description="Coach Role")
    role3 = Role(role_code="MAN", role_name="Manager", role_description="Manager Role")
    role4 = Role(role_code="ADM", role_name="Administrator", role_description="Administrator Role")
    
    
    db.session.add(role1)
    db.session.add(role2)
    db.session.add(role3)
    db.session.add(role4)
    
    db.session.commit()
    
    rankbase = Rankbase(rankbase_role=role1, rank_base_description="PLA-PASSING-WEAK", rank_score=0)
    rankbase1= Rankbase(rankbase_role=role1, rank_base_description="PLA-PASSING-LOW", rank_score=2)
    rankbase2 = Rankbase(rankbase_role=role1, rank_base_description="PLA-PASSING-MEDIUM", rank_score=4)
    rankbase3 = Rankbase(rankbase_role=role1, rank_base_description="PLA-PASSING-GOOD", rank_score=6)
    rankbase4 = Rankbase(rankbase_role=role1, rank_base_description="PLA-PASSING-EXCELLENT", rank_score=8)

    rankbase5 = Rankbase(rankbase_role=role1, rank_base_description="PLA-POSITION-WEAK", rank_score=0)
    rankbase6 = Rankbase(rankbase_role=role1, rank_base_description="PLA-POSITION-LOW", rank_score=2)
    rankbase7 = Rankbase(rankbase_role=role1, rank_base_description="PLA-POSITION-MEDIUM", rank_score=4)
    rankbase8 = Rankbase(rankbase_role=role1, rank_base_description="PLA-POSITION-GOOD", rank_score=6)
    rankbase9 = Rankbase(rankbase_role=role1, rank_base_description="PLA-POSITION-EXCELLENT", rank_score=8)
        
    rankbase10 = Rankbase(rankbase_role=role2, rank_base_description="COA-PLAYER-SWAP-WEAK", rank_score=0)
    rankbase11 = Rankbase(rankbase_role=role2, rank_base_description="COA-PLAYER-SWAP-LOW", rank_score=2)
    rankbase12 = Rankbase(rankbase_role=role2, rank_base_description="COA-PLAYER-SWAP-MEDIUM", rank_score=4)
    rankbase13 = Rankbase(rankbase_role=role2, rank_base_description="COA-PLAYER-SWAP-GOOD", rank_score=6)
    rankbase14 = Rankbase(rankbase_role=role2, rank_base_description="COA-PLAYER-SWAP-EXCELLENT", rank_score=8)

    rankbase15  = Rankbase(rankbase_role=role3, rank_base_description="MAN-TARGET-YIELD-WEAK", rank_score=0)
    rankbase16  = Rankbase(rankbase_role=role3, rank_base_description="MAN-TARGET-YIELD-LOW", rank_score=2)
    rankbase17  = Rankbase(rankbase_role=role3, rank_base_description="MAN-TARGET-YIELD-MEDIUM", rank_score=4)
    rankbase18  = Rankbase(rankbase_role=role3, rank_base_description="MAN-TARGET-YIELD-GOOD", rank_score=6)
    rankbase19  = Rankbase(rankbase_role=role3, rank_base_description="MAN-TARGET-YIELD-EXCELLENT", rank_score=8)
    
    
    db.session.add(rankbase)
    db.session.add(rankbase1)
    db.session.add(rankbase2)
    db.session.add(rankbase3)
    db.session.add(rankbase4)
    db.session.add(rankbase5) 
    
    db.session.add(rankbase6)
    db.session.add(rankbase7)
    db.session.add(rankbase8) 
    db.session.add(rankbase9)
    db.session.add(rankbase10)
    db.session.add(rankbase11)
    db.session.add(rankbase12)
    db.session.add(rankbase13)
    db.session.add(rankbase14)
    
    db.session.add(rankbase15)
    db.session.add(rankbase16)
    db.session.add(rankbase17)
    db.session.add(rankbase18)
    db.session.add(rankbase19)
     
    
    
    db.session.commit()
    
    user1 = User(full_name="Player A Full Name ",nick_name="PLA", email="playera@gmail.com",date_of_birth=datetime.date.fromisoformat('1982-04-15'), ssn='150482-6176', 
    password="password1", role_id=role1.role_id, rank=0)
    
    user2 = User(full_name="Player B Full Name ",nick_name="PLB", email="playerb@gmail.com",date_of_birth=datetime.date.fromisoformat('1987-04-15'), ssn='150487-6176', 
    password="password2",role_id=role1.role_id, rank=0)
    
    user3 = User(full_name="Player C Full Name ",nick_name="PLC", email="playerc@gmail.com",date_of_birth=datetime.date.fromisoformat('1987-04-15'), ssn='150487-6178', 
    password="password3", role_id=role1.role_id, rank=0)

    user4 = User(full_name="Player D Full Name ",nick_name="PLD", email="playerd@gmail.com",date_of_birth=datetime.date.fromisoformat('1995-04-15'), ssn='150495-6976', 
    password="password4", role_id=role1.role_id, rank=0)
    
    user5 = User(full_name="Player E  Full Name ",nick_name="PLE", email="playereb@gmail.com",date_of_birth=datetime.date.fromisoformat('1989-07-15'), ssn='150789-6476', 
    password="password5", role_id=role1.role_id, rank=0)
    
    user6 = User(full_name="Player F Full Name ",nick_name="PLF", email="playerf@gmail.com",date_of_birth=datetime.date.fromisoformat('2000-08-24'), ssn='240800-8975', 
    password="password6", role_id=role1.role_id, rank=0)
    
    
    user7 = User(full_name="Player G Full Name ",nick_name="PLG", email="playerg@gmail.com",date_of_birth=datetime.date.fromisoformat('1995-04-15'), ssn='150495-6170', 
    password="password7", role_id=role1.role_id, rank=0)
        
    user8 = User(full_name="Player H Full Name ",nick_name="PLH", email="playerh@gmail.com",date_of_birth=datetime.date.fromisoformat('1987-04-15'), ssn='150487-4236', 
    password="password8", role_id=role1.role_id, rank=0)
    
    user9 = User(full_name="Player I Full Name ",nick_name="PLI", email="playeri@gmail.com",date_of_birth=datetime.date.fromisoformat('2004-08-24'), ssn='240804-6176', 
    password="password9", role_id=role1.role_id, rank=0)
    
    user10 = User(full_name="Coach A Full Name ",nick_name="COA", email="coacha@gmail.com",date_of_birth=datetime.date.fromisoformat('1995-04-15'), ssn='150495-1176', 
    password="password10", role_id=role2.role_id, rank=0)
    
    user11 = User(full_name="Coach B Full Name ",nick_name="COB", email="coachb@gmail.com",date_of_birth=datetime.date.fromisoformat('1987-04-30'), ssn='300487-6176', 
    password="password11", role_id=role2.role_id, rank=0)
    
    user12 = User(full_name="Coach C Full Name ",nick_name="COC", email="coachc@gmail.com",date_of_birth=datetime.date.fromisoformat('1981-06-24'), ssn='240681-6173', 
    password="password12", role_id=role2.role_id, rank=0)

    user13 = User(full_name="Manager Full Name ",nick_name="MANA", email="managera@gmail.com",date_of_birth=datetime.date.fromisoformat('2004-08-24'), ssn='240804-5421', 
    password="password13", role_id=role3.role_id, rank=0)

    user14 = User(full_name="Administrator Full Name ",nick_name="ADMIN", email="administrator@gmail.com",date_of_birth=datetime.date.fromisoformat('2004-08-24'), ssn='240804-5921', 
    password="password14", role_id=role4.role_id, rank=0)

     
    db.session.add(user1)
    db.session.add(user2)

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
    db.session.add(user14)
    
   

    db.session.commit()


    # populate userrank data
    userrank1 = UserRank(user_id=user1.user_id, rank_base_id=rankbase.rank_base_id, ranker_comment="passing is very weak and need more practice",
                         ranker_user_id=user10.user_id)
    
    userrank2 = UserRank(user_id=user1.user_id, rank_base_id=rankbase6.rank_base_id, ranker_comment="position need improvment",
                         ranker_user_id=user11.user_id, ranked_added_date=datetime.date.fromisoformat('2024-04-15'))
    
    userrank3 = UserRank(user_id=user2.user_id, rank_base_id=rankbase4.rank_base_id, ranker_comment="Keep conintuing the good work",
                         ranker_user_id=user11.user_id, ranked_added_date=datetime.date.fromisoformat('2024-04-15'))
    
    userrank4 = UserRank(user_id=user10.user_id, rank_base_id=rankbase18.rank_base_id, ranker_comment="Keep reporting the progress",
                         ranker_user_id=user13.user_id, ranked_added_date=datetime.date.fromisoformat('2024-04-15'))
   
    

    db.session.add(userrank1)
    db.session.add(userrank2)
    db.session.add(userrank3)
    db.session.add(userrank4)
  
  

    db.session.commit()
    
    # populate teams data
    team1 = Team(team_name="Ice Skaters",team_description="Ice Skaters description", team_user=user10)
    team2 = Team(team_name="Winter warriors",team_description="Winter warrior description", team_user=user11)
    team3 = Team(team_name="Huskies",team_description="Huskies  description", team_user=user12)
    
    db.session.add(team1)
    db.session.add(team2)
    db.session.add(team3)


    db.session.commit()

    # populate teamuser data
    teamuser1 = TeamUser (teamuser_team=team1, teamuser_user=user1, contract_start_date=datetime.date.fromisoformat('2024-03-17'), contract_end_date=datetime.date.fromisoformat('2025-02-17'))
    teamuser2 = TeamUser (teamuser_team=team1, teamuser_user=user2, contract_start_date=datetime.date.fromisoformat('2024-03-17'), contract_end_date=datetime.date.fromisoformat('2025-02-17'))
    teamuser3 = TeamUser (teamuser_team=team1, teamuser_user=user3, contract_start_date=datetime.date.fromisoformat('2024-03-17'), contract_end_date=datetime.date.fromisoformat('2025-02-17'))
 
    teamuser4 = TeamUser (teamuser_team=team2, teamuser_user=user4, contract_start_date=datetime.date.fromisoformat('2024-03-17'), contract_end_date=datetime.date.fromisoformat('2025-02-17'))
    teamuser5 = TeamUser (teamuser_team=team2, teamuser_user=user5, contract_start_date=datetime.date.fromisoformat('2024-03-17'), contract_end_date=datetime.date.fromisoformat('2025-02-17'))
    teamuser6 = TeamUser (teamuser_team=team2, teamuser_user=user6, contract_start_date=datetime.date.fromisoformat('2024-03-17'), contract_end_date=datetime.date.fromisoformat('2025-02-17'))
  
    teamuser7 = TeamUser (teamuser_team=team3, teamuser_user=user7, contract_start_date=datetime.date.fromisoformat('2024-03-17'), contract_end_date=datetime.date.fromisoformat('2025-02-17'))
    teamuser8 = TeamUser (teamuser_team=team3, teamuser_user=user8, contract_start_date=datetime.date.fromisoformat('2024-03-17'), contract_end_date=datetime.date.fromisoformat('2025-02-17'))
    teamuser9 = TeamUser (teamuser_team=team3, teamuser_user=user9, contract_start_date=datetime.date.fromisoformat('2024-03-17'), contract_end_date=datetime.date.fromisoformat('2025-02-17'))



    db.session.add(teamuser1)
    db.session.add(teamuser2)
    db.session.add(teamuser3)
    db.session.add(teamuser4)
    db.session.add(teamuser5)
    db.session.add(teamuser6)
    db.session.add(teamuser7)
    db.session.add(teamuser8)
    db.session.add(teamuser9)
    
    
    db.session.commit()
    
    # populate match data
    match1 = Match(1, 1, 2, 2, "decided", "semifinal", datetime.date.fromisoformat('2021-06-17'))
    match2 = Match(2, 1, 3, 1, "decided", "entry", datetime.date.fromisoformat('2021-04-12'))
    match3 = Match(3, 4, 1, 1, "decided", "entry", datetime.date.fromisoformat('2021-04-12'))
    match4 = Match(4, 5, 3, 3, "decided", "quarterfinal", datetime.date.fromisoformat('2021-04-12'))
    match5 = Match(5, 2, 3, 2, "decided", "semifinal", datetime.date.fromisoformat('2021-04-12'))
    match6 = Match(6, 5, 3, 5, "decided", "final", datetime.date.fromisoformat('2021-04-12'))
    
    # populate matchfeedback data
    matchfeedback   = MatchFeedback(matchfeedback_match=match1, ranker_user_id=user10.user_id, ranker_comment="Cocach A : Need extra defer",
                       ranked_added_date=datetime.date.fromisoformat('2024-02-17'))
     
    matchfeedback2  = MatchFeedback(matchfeedback_match=match1, ranker_user_id=user11.user_id, ranker_comment="Cocach B : too many penalties",
                       ranked_added_date=datetime.date.fromisoformat('2021-02-17'))
    
    matchfeedback3  = MatchFeedback(matchfeedback_match=match2, ranker_user_id=user12.user_id, ranker_comment="Cocach C : too many fowl incidents",
                       ranked_added_date=datetime.date.fromisoformat('2021-02-17'))

    matchfeedback4  = MatchFeedback(matchfeedback_match=match2, ranker_user_id=user13.user_id, ranker_comment="Man A : too many communication mishaps",
                       ranked_added_date=datetime.date.fromisoformat('2021-02-17'))
     
    matchfeedback5  = MatchFeedback(matchfeedback_match=match4, ranker_user_id=user11.user_id, ranker_comment="Cocach B : too many fowl incidents",
                       ranked_added_date=datetime.date.fromisoformat('2021-02-17'))
       
             

    db.session.add(match1)
    db.session.add(match2)


    db.session.add(match3)
    db.session.add(match4)

    db.session.add(match5)
    db.session.add(match6)


    db.session.add(matchfeedback)
    db.session.add(matchfeedback2)
    db.session.add(matchfeedback3)
    db.session.add(matchfeedback4)
    db.session.add(matchfeedback5)
    
    db.session.commit()


@click.command("authkey")
@with_appcontext
def generate_master_key():
    """
    Used for generating  Administrator and other role related keys 
    """
      
    # Player auth realted data
    token1 = secrets.token_urlsafe()
    token2 = secrets.token_urlsafe()
    token3 = secrets.token_urlsafe()
    
    print("Player 1: key: " + token1)
    print("Player 2: key: " + token2)
    print("Player 3: key: " + token3)

    userAuthkey1 = UserAuthenticationKey(key=UserAuthenticationKey.key_hash(token1), admin=False, userauthkey_user=user1)
    userAuthkey2 = UserAuthenticationKey(key=UserAuthenticationKey.key_hash(token2), admin=False, userauthkey_user=user2)
    userAuthkey3 = UserAuthenticationKey(key=UserAuthenticationKey.key_hash(token3), admin=False, userauthkey_user=user3)


    # Coach,Manager auth realted data
    token4 = secrets.token_urlsafe()
    token5 = secrets.token_urlsafe()
    
    print("Coach 10 : key: " + token4)
    print("Manager 13: key: " + token5)
    
    userAuthkey4 = UserAuthenticationKey(key=UserAuthenticationKey.key_hash(token4), admin=False, userauthkey_user=user10)
    userAuthkey5= UserAuthenticationKey(key=UserAuthenticationKey.key_hash(token5), admin=False, userauthkey_user=user13)


    # Administrator auth realted data
    token6 = secrets.token_urlsafe()
    print("Administrator 14 : key: " + token6)
    
    # Administrator key
    userAuthkey6 = UserAuthenticationKey(
             key = UserAuthenticationKey.key_hash(token6), 
             admin=True, 
             userauthkey_user=user14
            )

    db.session.add(userAuthkey1)
    db.session.add(userAuthkey2)
    db.session.add(userAuthkey3)
    db.session.add(userAuthkey4)
    db.session.add(userAuthkey5)
    db.session.add(userAuthkey6)

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
