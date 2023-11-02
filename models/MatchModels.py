"""Define the Match."""

from player import Player
from player import player1
from player import player2


class Match :
    def __init__(self, player1,player2) :
        self.player1=player1
        self.player2=player2

    
    def match(player1,player2) :
        ID_player1=getattr(player1, "ID")
        ID_player2=getattr(player2, "ID")
        result=input("Entrez l'ID du gagnant ou 0 en cas d'égalité :")
        if result == ID_player1 :
            getattr(player1, "winner") is True
            Player.MatchResult(player1)
            print(getattr(player1, "score"))
            getattr(player2, "looser")  is True
            Player.MatchResult(player2)
        if result == ID_player2 :
            getattr(player2, "winner")  is True
            Player.MatchResult(player2)
            getattr(player1, "looser")  is True
            Player.MatchResult(player1)
        if result == "0" :
            getattr(player1, "draw") is True
            Player.MatchResult(player1)
            getattr(player1, "draw") is True
            Player.MatchResult(player2)
        print("Le score de " + getattr(player1, "surname") + " " +getattr(player1, "name") + 
              " est de "+ str(getattr(player1, "score"))
               +" et le score de " + getattr(player2, "surname")+" " + getattr(player2, "name") 
               + " est de "+ str(getattr(player2, "score")))

    

match1=Match.match(player1, player2)

        