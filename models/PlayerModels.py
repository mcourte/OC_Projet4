"""Define the Player."""

import datetime
import string
import random

class Player :
    def __init__(self,score=0,name ="",surname="",dateofbirth="",ID="", winner=bool, looser=bool, draw=bool) :
        self.name=name
        self.score=score
        self.surname=surname
        self.dateofbirth=dateofbirth
        self.ID=ID
        self.winner=winner
        self.looser=looser
        self.draw=draw        
        
    @classmethod
    def random_ID(self):  
        ''' Cette fonction permet de générer aléatoirement des ID
        Elle sera supprimer une fois les tests finis'''
        nb_letters=2
        nb_numbers=5
        letters= ''.join((random.choice(string.ascii_uppercase)) for x in range(nb_letters))
        numbers=''.join((random.choice(string.digits)) for x in range(nb_numbers))
    
        ID_list = list(letters + numbers)
        ID = ''.join(ID_list)  
        return ID  



    def PlayerLastName(self) :
        self.name = input("Quel est le nom de famille du joueur?")
        if self.name == "" :
            print("Erreur, le nom ne doit pas être vide")
            self.name=input("Quel est le nom de famille du joueur?")
        return self.name
    
    def PlayerSurname(self):
        self.surname = input ("Quel est le prénom du joueur?")
        if self.surname == "" :
            print("Erreur, le nom ne doit pas être vide")
            self.surname=input("Quel est le prénom du joueur?")
        return self.surname

    def PlayerDateOfBirth(self) :
        self.dateofbirth = input ("Quelle est la date de naissance du joueur? (format jj-mm-aaaa)")
        separator=self.dateofbirth.find("-")
        td = datetime.date.today()
        if separator == -1: 
            print("Erreur, le format de la date n'est pas le bon jj-mm-aaaa")
            self.dateofbirth=input("Quelle est la date de naissance du joueur? (format jj-mm-aaaa)")
        dob = datetime.datetime.strptime(self.dateofbirth, '%d-%m-%Y')
        if dob.year >= td.year :
            print("Erreur, la date de naissance ne peut pas être postérieure à la date du jour")
            self.dateofbirth=input("Quelle est la date de naissance du joueur? (format jj-mm-aaaa)")
            dob = datetime.datetime.strptime(self.dateofbirth, '%d-%m-%Y')

        self.age= td.year - dob.year - ((td.month, td.day) < (dob.month, dob.day))
        
        return self.age



    def CreatePlayer(self) :
        self.name= self.PlayerLastName()
        self.surname=self.PlayerSurname()
        self.age=self.PlayerDateOfBirth()
        self.ID=self.random_ID()
      
        print(f"Le joueur s'appelle " +self.surname +" "+ self.name + " à "+ str(self.age) +" ans et son ID est :"+ self.ID)

        return self.name, self.surname, self.dateofbirth, self.ID

    def MatchResult(self):
        if self.winner is True:
           self.score+=1
        if self.looser is True:
            self.score+=0
        if self.draw is True :
            self.score+=0.5
        print(self.score)
        return self.score


