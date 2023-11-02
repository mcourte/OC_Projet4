"""Define the Round."""

import datetime

class Round :
    def __init__(self,start_date="",end_date="",number_of_round=0,couple_of_player="") :
        self.start_date=start_date
        self.end_date=end_date
        self.number_of_round=number_of_round
        self.couple_of_player=couple_of_player
  
#round_number ?? dans Tournament ou Round ? Classe abstraite?

    def start_round(self):  
        self.star_date=datetime.datetime.today()
        self.number_of_round +=1
        print(self.star_date)
        print(self.number_of_round)

    def end_round(self):
        self.star_date=datetime.datetime()

round=Round()
round.start_round()
round.start_round()
round.start_round()