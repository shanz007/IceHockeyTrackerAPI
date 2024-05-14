"""
This file encapsulates all the API mappings of the system
"""

from flask import Blueprint
from flask_restful import Api

from icehockeytracker.resources.roles import RoleCollection, RoleItem
from icehockeytracker.resources.matchfeedbacks import MatchFeedbackCollection, MatchFeedbackItem


from icehockeytracker.resources.users import (
    UserByRelationCollection, UserCollection, UserItem
)
from icehockeytracker.resources.teams import (
    TeamUserCollection, TeamCollection, TeamItem, TeamUserItem
)

from icehockeytracker.resources.matches import (
    MatchCollection, MatchItem
)

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

# roles related resources
api.add_resource(RoleCollection, "/roles/")
api.add_resource(RoleItem, "/roles/<Role:role>/")

# users related resources
api.add_resource(UserByRelationCollection, "/roles/<Role:role>/users/") # POST
api.add_resource(UserCollection, "/users/") #GET
api.add_resource(UserItem, "/users/<User:user>/") #GET # DELETE # PUT

# team related resources
api.add_resource(TeamCollection, "/teams/")      #GET #POST
api.add_resource(TeamItem,"/teams/<Team:team>/")  #PUT #GET # DELETE
    
# teamuser related resources
api.add_resource(TeamUserCollection, "/teams/<Team:team>/users/")        #GET #POST
api.add_resource(TeamUserItem,"/teams/<Team:team>/users/<User:user>/")   #GET # DELETE # PUT
    
api.add_resource(TeamUsersCollection, "/teamusers/")
api.add_resource(TeamUsersCollection, "/teams/<team:team>/teamusers/")
                 
# match related resources
api.add_resource(MatchCollection, "/matches/")
api.add_resource(MatchItem,"/matches/<Match:match>/")

# matchfeedback related resources
api.add_resource(MatchFeedbackCollection,"/matchfeedbacks/") #GET
api.add_resource(MatchFeedbackItem,"/matches/<Match:match>/matchfeedbacks/<Matchfeedback:MatchFeedback>/") #PUT #DELETE

# Rankbase related resources
api.add_resource(RankbaseCollection, "/rankbases/")             #GET #POST
api.add_resource(RankbaseItem,"/rankbases/<Rankbase:ranbase>/") #PUT #DELETE

api.add_resource(UserRankingCollection, "/userranks/")   #GET 
        
# User ranking related resources
api.add_resource(UserRankingByUserCollection, "/users/<User:user>/userranks/")       #GET #POST
api.add_resource(UserRankingItem, "/userranks/<Userrank:userrank>/")      #PUT # DELETE
        