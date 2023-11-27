
import datetime
import json
import os
import pandas as pd


class PlayerView():

    def display_player_menu():

        print("\nMenu de Gestion des Joueurs :")
        print("1. Ajouter un nouveau joueur")
        print("2. Afficher tous les joueurs")
        print("3. Revenir au menu principal")
        user_choice = input("Choisissez une option: ")
        return user_choice
    
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
    
    

    def choose_player(self):
        self.choose_player_ID=input("Choississez le numéro des joueurs à ajouter :")
        return self.choose_player_ID
    

