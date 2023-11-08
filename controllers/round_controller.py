"""Define the Round."""

import os
import json

import datetime

from models import round_model

class RoundController :
    def __init__(self):
        pass



    def start_round(self):
        self.star_date = datetime.datetime.today()
        self.round_number +=1

    def end_round(self):
        self.star_date = datetime.datetime()

round=round_model.Round()
round=RoundController()
round.duo_player()
round.start_round()
round.end_round()