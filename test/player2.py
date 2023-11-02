"""Define the Player."""

import datetime
import string
import random

class Player :
    def __init__(self,name ="",surname="",dateofbirth="",ID="") :
        self.name=name
        self.surname=surname
        self.dateofbirth=dateofbirth
        self.ID=ID

    def random_ID():  
        ''' Cette fonction permet de générer aléatoirement des ID
        Elle sera supprimer une fois les tests finis'''
        nb_letters=2
        nb_numbers=5
        letters= ''.join((random.choice(string.ascii_uppercase)) for x in range(nb_letters))
        numbers=''.join((random.choice(string.digits)) for x in range(nb_numbers))
    
        ID_list = list(letters + numbers)
        ID = ''.join(ID_list)  
        return ID  


    def DefinePlayer(self) :
        self.name = input("Quel est le nom de famille du joueur?")
        self.surname=input("Quel est le prénom du joueur?")
        self.dateofbirth=input("Quelle est la date de naissance du joueur? (jj-mm-aaaa)")
        self.ID=Player.random_ID()

        dob = datetime.datetime.strptime(self.dateofbirth, '%d-%m-%Y')
        td = datetime.date.today()
        age= td.year - dob.year - ((td.month, td.day) < (dob.month, dob.day))

        print(f"Le joueur s'appelle " +self.surname +" "+ self.name + " à "+ str(age)+"ans et son ID est :"+self.ID)
        return self.name, self.surname, self.dateofbirth, self.ID 
    
player1=Player()
player1.DefinePlayer()
