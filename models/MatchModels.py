"""Define the Match."""

import PlayerModels



class Match :
    def __init__(self, player1,player2) :
        player1=PlayerModels.Player().CreatePlayer()
        player2=PlayerModels.Player().CreatePlayer()
        self.player1=player1
        self.player2=player2
    

    @classmethod
    def match(player1,player2) :
        ID_player1=getattr(player1, "ID")
        ID_player2=getattr(player2, "ID")
        result=input("Entrez l'ID du gagnant ou 0 en cas d'égalité :")
        #if result == ID_player1 :
        #if result == ID_player2 :
        #if result == "0" : 

        #return 

        print("Le score de " + getattr(player1, "surname") + " " +getattr(player1, "name") + 
                " est de "+ str(getattr(player1, "score"))
                +" et le score de " + getattr(player2, "surname")+" " + getattr(player2, "name") 
                + " est de "+ str(getattr(player2, "score")))

    

match1=Match()