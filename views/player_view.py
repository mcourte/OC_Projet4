
import datetime

class PlayerView():

    def PlayerLastName(self):
        self.name = input("Quel est le nom de famille du joueur?")
        if self.name == "":
            print("Erreur, le nom ne doit pas être vide")
            self.name=input("Quel est le nom de famille du joueur?")
        return self.name
    
    def PlayerSurname(self):
        self.surname = input ("Quel est le prénom du joueur?")
        if self.surname == "":
            print("Erreur, le nom ne doit pas être vide")
            self.surname = input("Quel est le prénom du joueur?")
        return self.surname

    def PlayerDateOfBirth(self):
        self.dateofbirth = input ("Quelle est la date de naissance du joueur? (format jj-mm-aaaa)")
        separator = self.dateofbirth.find("-")
        td = datetime.date.today()
        if separator == -1: 
            print("Erreur, le format de la date n'est pas le bon jj-mm-aaaa")
            self.dateofbirth=input("Quelle est la date de naissance du joueur? (format jj-mm-aaaa)")
        dob = datetime.datetime.strptime(self.dateofbirth, '%d-%m-%Y')
        if dob.year >= td.year:
            print("Erreur, la date de naissance ne peut pas être postérieure à la date du jour")
            self.dateofbirth = input("Quelle est la date de naissance du joueur? (format jj-mm-aaaa)")
            dob = datetime.datetime.strptime(self.dateofbirth, '%d-%m-%Y')

        self.age = td.year-dob.year-((td.month,td.day)<(dob.month,dob.day))
        self.dob = dob

        return self.age, dob
    

