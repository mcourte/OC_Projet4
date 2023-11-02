"""Define the Tournament."""
import datetime
import PlayerModels

class Tournament :
    def __init__(self,name="",location="",dateofbegin="",dateofend="",numberofround=4,round_number="",list_of_round=None,list_of_players=None, description="") :
        self.name=name
        self.location=location
        self.dateofbegin=dateofbegin
        self.dateofend=dateofend
        self.numberofround=numberofround
        self.round_number=round_number
        self.list_of_round=list_of_round
        self.list_of_players=list_of_players
        self.description=description
        

    def start_tournament(self):  
        self.name=input("Quel est le nom du tournoi?")
        self.location=input("Quelle est la location du tournoi?")
        
        nb_round=input("Combien il y aura-t-il de round?(par défaut :4)")
        if nb_round == "" or "4":
           self.numberofround=4
        else :
            self.numberofround=nb_round

        self.list_of_round=[]
        round=0
        for i in range(self.numberofround):
            round="round"+str(i+1)
            self.list_of_round.append(round)
        #number_player=input("Quel est le nombre de joueur ?")
        player1=PlayerModels.Player().CreatePlayer()
        player2=PlayerModels.Player().CreatePlayer()
        self.list_of_players=[player1,player2]
        print(self.list_of_players)
        self.dateofbegin=datetime.date.today()
        self.description=input("Entrez les remarques générales du tournoi : ")
        print(self.dateofbegin)
            

    def end_tournament(self):
        self.dateofend=datetime.date.today()


test=Tournament()
test.start_tournament()