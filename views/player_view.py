from datetime import datetime

from views.main_view import MainView


class PlayerView:

    def display_player_menu(self):
        '''Affiche le menu de gestion des Joueurs'''
        MainView.clear_screen()
        title = "\nMenu de Gestion des Joueurs :\n"
        MainView().slow_print(title)
        menu = "\n 1. Ajouter un nouveau joueur \n 2. Revenir au menu principal \n"
        MainView().slow_print(menu)
        choice_prompt = "Choisissez une option:"
        MainView().slow_print(choice_prompt)
        self.choice = input().strip()
        return self.choice

    def player_name(self):
        '''Permet à l'utilisateur de rentrer le prénom du Joueur'''
        self.name = input("Quel est le prénom du joueur?")
        if self.name == "":
            print("Erreur, le prénom ne doit pas être vide")
            self.name = input("Quel est le prénom du joueur?")
        return self.name

    def player_surname(self):
        '''Permet à l'utilisateur de rentrer le nom du Joueur'''
        self.surname = input("Quel est le nom de famille du joueur?")
        if self.surname == "":
            print("Erreur, le nom ne doit pas être vide")
            self.surname = input("Quel est le nom de famille du joueur?")
        return self.surname

    def player_date_of_birth(self):
        '''Permet à l'utilisateur de rentrer la date de naissance du Joueur'''
        self.date_of_birth = input("Quelle est la date de naissance du joueur? (format JJ/MM/AAAA)")
        separator = self.date_of_birth.find("/")
        td = datetime.now()
        if separator == -1:
            print("Erreur, le format de la date n'est pas le bon JJ/MM/AAAA")
            self.date_of_birth = input("Quelle est la date de naissance du joueur? (format JJ/MM/AAAA)")
        dob = datetime.strptime(self.date_of_birth, "%d/%m/%Y")
        if dob.year >= td.year:
            print("Erreur, la date de naissance ne peut pas être postérieure à la date du jour")
            self.date_of_birth = input("Quelle est la date de naissance du joueur? (format JJ/MM/AAAA)")
        dob = datetime.strptime(self.date_of_birth, "%d/%m/%Y")
        date_of_birth = str(dob)
        self.date_of_birth = date_of_birth[0:10]
        return self.date_of_birth

    def player_ID(self):
        '''Permet à l'utilisateur de rentrer l'ID du Joueur'''
        self.player_ID = input("Quel est l'ID du joueur?")
        return self.player_ID
