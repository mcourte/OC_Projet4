
import datetime

class PlayerView():

    def PlayerLastName(self):
        self.name = input("Quel est le prénom du joueur?")
        if self.name == "":
            print("Erreur, le prénom ne doit pas être vide")
            self.name=input("Quel est le prénom du joueur?")
        return self.name
    
    def PlayerSurname(self):
        self.surname = input ("Quel est le nom de famille du joueur?")
        if self.surname == "":
            print("Erreur, le nom ne doit pas être vide")
            self.surname = input("Quel est le nom de famille du joueur?")
        return self.surname

    def PlayerDateOfBirth(self):
        self.date_of_birth = input ("Quelle est la date de naissance du joueur? (format jj-mm-aaaa)")
        separator = self.date_of_birth.find("-")
        td = datetime.date.today()
        if separator == -1: 
            print("Erreur, le format de la date n'est pas le bon jj-mm-aaaa")
            self.date_of_birth=input("Quelle est la date de naissance du joueur? (format jj-mm-aaaa)")
        dob = datetime.datetime.strptime(self.date_of_birth, '%d-%m-%Y')
        if dob.year >= td.year:
            print("Erreur, la date de naissance ne peut pas être postérieure à la date du jour")
            self.date_of_birth = input("Quelle est la date de naissance du joueur? (format jj-mm-aaaa)")
            dob = datetime.datetime.strptime(self.date_of_birth, '%d-%m-%Y')
        self.date_of_birth = str(dob)
        return self.date_of_birth
    

