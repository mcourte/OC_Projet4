"""Define the Tournament."""
import random
import string
from datetime import datetime


class TournamentView:

    def __init__(self):
        pass

    def display_tournament_menu(self):
        '''Permet d'afficher le menu de gestion des tournois'''
        print("\nMenu de Gestion des Tournois :")
        print("1. Ajouter un nouveau tournoi")
        print("2. Compléter un tournoi")
        print("3. Terminer un tournoi")
        print("4. Revenir au menu principal\n")
        user_choice = input("Choisissez une option: ")
        return user_choice

    def start_tournament_view(self):
        '''Permet d'initier un nouveau tournoi'''
        tournament_name = input("Quel est le nom du tournoi?")
        self.tournament_name = "Tournoi n°" + str(tournament_name)
        self.tournament_location = input("Quelle est la localisation du tournoi?")
        nb_round = input("Combien il y aura-t-il de round?(par défaut 4)")
        if nb_round == "" or "4":
            self.number_of_round = 4
        else:
            self.number_of_round = nb_round

        tournament_date_of_begin = input("Quelle est la date de début du tournoi?")
        self.tournament_date_of_begin = datetime.strftime(tournament_date_of_begin, "%d-%m-%Y")
        nb_numbers = 6
        numbers = ''.join((random.choice(string.digits))
                          for x in range(nb_numbers))
        ID_list = list(numbers)
        self.tournament_ID = ''.join(ID_list)
        self.tournament_description = input("Entrez les remarques générales du tournoi : ")
        self.tournament_data_view = [{
                        "Nom_du_tournoi": self.tournament_name,
                        "Lieu": self.tournament_location,
                        "Nombre_de_round": self.number_of_round,
                        "Description": self.tournament_description,
                        "Date_de_debut": self.tournament_date_of_begin,
                        "Tournoi_ID": self.tournament_ID
                        }
        ]
        return self.tournament_data_view

    def number_of_player(self):
        '''Permet à l'utilisateur de choisir le nombre de joueur qu'il veut dans le tournoi'''
        self.number_of_players = input("Combien y aura-t-il de joueurs dans le tournoi ?" +
                                       "Le nombre de joueur doit être un nombre pair " +
                                       "au moins 1 joueur de plus que le nombre de round): ")
        return self.number_of_players

    def choose_players(self):
        '''Permet de choisir si on veut créer une liste aléatoire de joueur'''
        self.choose_player = input("Voulez-vous créer une liste aléatoire de joueurs ? Oui/Non ").lower()
        return self.choose_player

    def choose_players_ID(self):
        ''' Permet de rentrer l'ID du joueur que l'on veut sélectionner'''
        self.choose_ID = input("Veuillez rentrer l'ID du joueur que vous souhaitez rajouter : ").upper()
        return self.choose_ID

    def choose_tournament(self):
        '''Permet à l'utilisateur de choisir le tournoi dont il veut les détails'''
        self.choice_tournament = input("Choisissez le nom du tournoi dont vous voulez les détails : ")
        return self.choice_tournament

    def display_list_tournament(self, tournaments):
        '''Affiche la liste des tournois.'''
        print("\nListe des tournois:")
        for tournament in tournaments:
            print(f"- {tournament.tournament_name}")
        print()

    def display_ongoing_tournaments(tournaments):
        '''Affiche les tournois en cours.'''
        print("Tournois en cours :\n")
        for i, tournament in enumerate(tournaments):
            TournamentView.display_list_tournament(tournament, i)
        print()

    def display_tournament(tournament, index=None):
        """Affiche les détails du tournoi."""
        if index is not None:
            details = (
                f"{index + 1}. {tournament.tournament_name}"
                f" - {tournament.tournament_location} - {tournament.tournament_date_of_begin}\n"
            )
        else:
            details = (
                f"{tournament.tournament_ID}. {tournament.tournament_name})"
                f" - {tournament.tournament_location} - {tournament.tournament_date_of_begin}\n"
            )
        print(details)

    def display_tournament_launched(tournament_name):
        '''Affiche le message indiquant que le tournoi a été lancé avec succès.'''
        print(f"Le tournoi '{tournament_name}' a été lancé avec succès.\n")
