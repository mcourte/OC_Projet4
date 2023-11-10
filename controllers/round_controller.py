"""Define the Round."""

import os
import json

import datetime

from models import round_model

class RoundController :
    def __init__(self):
        pass

    def first_round(self):
        self.start_date = datetime.datetime.today()
        self.round_number=1
        return self.round_number
        
    def start_round(self):
        self.start_date = datetime.datetime.today()
        self.round_number =self.round_number +1
        return self.round_number
        

    def end_round(self):
        self.end_date = datetime.datetime.today()


