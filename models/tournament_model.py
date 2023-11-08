"""Define the Tournament."""
import datetime
import models.player_model as player_model

class Tournament :
    def __init__(self):
        pass
    def tournament_datas(self,name = "", location = "",date_of_begin = "",
                 date_of_end = "", number_of_round = 4, round_number = "", 
                 list_of_round = None,list_of_players = None , description = ""):
        self.name = name
        self.location = location
        self.date_of_begin = date_of_begin
        self.date_of_end = date_of_end
        self.number_of_round = number_of_round
        self.round_number = round_number
        self.list_of_round = list_of_round
        self.list_of_players = list_of_players
        self.description = description
        
        return self.name, self.location, self.date_of_begin, self.date_of_end,\
            self.number_of_round, self.round_number,self.list_of_round,\
            self.list_of_players,self.description