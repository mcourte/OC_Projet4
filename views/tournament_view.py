"""Define the Tournament."""
import random
import string
from datetime import datetime
import os
import json

from views.main_view import MainView


class TournamentView:

    def __init__(self):
        pass

    def display_tournament_menu(self):
        # MainView.clear_screen()
        '''Permet d'afficher le menu de gestion des tournois'''
        print("\nMenu de Gestion des Tournois :\n")
        print("1. Commencer un nouveau tournoi")
        print("2. Reprendre un tournoi en cours")
        print("3. Clôturer un tournoi")
        print("4. Revenir au menu principal\n")
        user_choice = input("Choisissez une option: ")
        return user_choice

    def start_tournament_view(self):
        '''Permet d'initier un nouveau tournoi'''
        # MainView.clear_screen()
        while True:
            tournament_name = input("Quel est le nom du tournoi?")
            if tournament_name != "":
                break
            else:
                print("Le nom du tournoi ne peut pas être vide.")
        while True:
            tournament_location = input("Quelle est la localisation du tournoi?")
            if tournament_location != "":
                break
            else:
                print("La localisation du tournoi ne peut pas être vide.")

        while True:
            tournament_date_of_begin = input("Quelle est la date de début du tournoi? (Format : JJ/MM/AAAA)")
            try:
                # Essayer de convertir la chaîne en objet datetime

                datetime.strptime(tournament_date_of_begin, "%d/%m/%Y")
                # La conversion a réussi, la date est valide
                break  # Sortir de la boucle si la date est conforme
            except ValueError:
                # La conversion a échoué, la date n'est pas valide
                print(
                    "Format de date invalide. Assurez-vous d'utiliser "
                    + "le format JJ/MM/AAAA. Réessayez."
                )
        nb_round = int(input("Combien il y aura-t-il de round?(par défaut 4)"))
        if nb_round == "" or "4":
            number_of_round = 4
        else:
            number_of_round = nb_round
        nb_numbers = 6
        numbers = ''.join((random.choice(string.digits))
                          for x in range(nb_numbers))

        ID_list = list(numbers)
        tournament_ID = ''.join(ID_list)
        self.list_of_round = []
        tournament_description = input("Entrez les remarques générales du tournoi : ")
        tournament_data = [{
                        "Nom_du_tournoi": tournament_name,
                        "Lieu": tournament_location,
                        "Description": tournament_description,
                        "Date_de_debut": tournament_date_of_begin,
                        "Tournoi_ID": tournament_ID,
                        "Nombre_de_round": number_of_round,
                        "Liste_des_rounds": self.list_of_round
                        }
        ]
        return tournament_data

    def number_of_player(self):
        '''Permet à l'utilisateur de choisir le nombre de joueur qu'il veut dans le tournoi'''
        self.number_of_players = input("Combien y aura-t-il de joueurs dans le tournoi ?" +
                                       "Le nombre de joueur doit être un nombre pair " +
                                       "au moins 1 joueur de plus que le nombre de round): ")
        while int(self.number_of_players) % 2 != 0:
            print("Le nombre de joueurs doit être pair.")

        return self.number_of_players

    def choose_players(self):
        '''Permet de choisir si on veut créer une liste aléatoire de joueur'''
        self.choose_player = input("Voulez-vous créer une liste aléatoire de joueurs ? Oui/Non ").lower()
        return self.choose_player

    def choose_players_ID(self):
        ''' Permet de rentrer l'ID du joueur que l'on veut sélectionner'''
        self.choose_ID = input("Veuillez rentrer l'ID du joueur que vous souhaitez rajouter : ").upper()
        return self.choose_ID

    def choose_tournament_2(self):
        '''Permet à l'utilisateur de choisir le tournoi dont il veut les détails'''
        self.choice_tournament = input("Choisissez le nom du tournoi dont vous voulez les détails : ")
        return self.choice_tournament

    def display_list_tournament(self, tournaments):
        # MainView.clear_screen()
        '''Affiche la liste des tournois.'''
        list_tournament = []
        print("\nListe des tournois:")
        for tournament in tournaments:
            tournament_name = tournament.get("Nom_du_tournoi")
            if tournament_name is not None:
                list_tournament.append(tournament_name)
        return list_tournament

    def display_tournament(tournament):
        """Affiche les détails du tournoi."""
        # MainView.clear_screen()
        details = (
            f"{tournament.tournament_ID}. {tournament.tournament_name})"
            f" - {tournament.tournament_location} - {tournament.tournament_date_of_begin}\n"
        )
        print(details)

    def display_tournament_launched(tournament_name):
        '''Affiche le message indiquant que le tournoi a été lancé avec succès.'''
        print(f"Le tournoi '{tournament_name}' a été lancé avec succès.\n")

    def display_tournament_details(self, tournaments):
        """Affiche les détails d'un tournoi."""
        list_tournaments = []
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            tournaments = json.load(file)
        for tournament in tournaments:
            list_tournaments.append(tournament)
        for i, tournament in enumerate(list_tournaments, start=1):
            tournament_name = tournament.get("Nom_du_tournoi")
            if tournament_name is not None:
                print(f"{i}. {tournament_name}")
        try:
            choice = int(input("Veuillez sélectionner le numéro du tournoi : "))
            if 1 <= choice <= len(list_tournaments):
                selected_tournament_index = choice - 1
                selected_tournament = list_tournaments[selected_tournament_index]
                date_of_begin = selected_tournament.get("Date_de_debut")[0:10]
                tournament_name = selected_tournament.get("Nom_du_tournoi")
                print("Nom du tournoi: " + tournament_name + "\nDate de début :" + date_of_begin)
            else:
                print("Votre numéro de choix est invalide")
        except ValueError:
            print("Votre numéro de choix est invalide")

    def display_tournament_alphabetically(self):
        '''Permet de ranger la liste des joueurs du tournoi par ordre alphabétique'''
        file_path = os.path.join("data", "tournament_data.json")
        user_choice = TournamentView().choose_tournament(file_path)
        print(user_choice)
        dict_player = {}
        sorted_player = []
        with open(file_path, "r") as file:
            data = json.load(file)
        for index, item in enumerate(data):
            if item.get("Nom_du_tournoi") == user_choice:
                players_data = data[index + 1]
                list_player = players_data.get("Liste_joueurs_inscrits")[0]
                for player in list_player:
                    dict_player.update(player)
                    a = list(dict_player.items())
                    sorted_player.append(a)
                sorted_name = sorted(sorted_player, key=lambda x: (x[0], x[1]))
                sorted_name.append(sorted_name)
                sorted_name.pop()
        return sorted_name

    def display_tournament_data(self, tournaments):
        '''Permet d'afficher les détails d'un tournoi'''
        file_path = os.path.join("data", "tournament_closed.json")
        user_choice = TournamentView.choose_tournament(file_path)
        tournament_number = user_choice[-1]
        next_tournament_number = int(tournament_number) + 1
        list_tournament = []
        with open(file_path, "r") as file:
            data = json.load(file)
        for i in range(0, len(data), 3):
            one_tournament = data[i:(i+3)]
            del one_tournament[1]
            list_tournament.append(one_tournament)
        key_to_search = "Nom_du_tournoi"
        value_to_search = user_choice
        value_to_search2 = "Tournoi n°" + str(next_tournament_number)
        for index, item in enumerate(data):
            if item.get(key_to_search) == value_to_search:
                result_start = index
            if item.get(key_to_search) == value_to_search2:
                result_end = index
            else:
                result_end = -1
        tournament_data = data[result_start:result_end]
        return tournament_data
