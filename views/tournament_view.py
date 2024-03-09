
import random
import string
from datetime import datetime
import os
import json

from views.main_view import MainView


class TournamentView:

    def display_tournament_menu(self):
        '''Affiche le menu de création des Tournois'''
        title = "\nMenu de Gestion des Tournois :\n"
        MainView().slow_print(title)
        menu = ("\n 1. Créer un nouveau tournoi \n 2. Lancer un tournoi \n 3. Reprendre un tournoi en cours \n"
                " 0. Revenir au menu principal\n")
        MainView().slow_print(menu)
        choice = "Choisissez une option: "
        MainView().slow_print(choice)
        self.choice = input()
        return self.choice

    def start_tournament_view(self):
        '''Permet de créer un nouveau tournoi'''
        MainView.clear_screen()
        while True:
            tournament_name = input("Quel est le nom du tournoi? ")
            if tournament_name != "":
                break
            else:
                print("Le nom du tournoi ne peut pas être vide.")
        while True:
            tournament_location = input("Quelle est la localisation du tournoi? ")
            if tournament_location != "":
                break
            else:
                print("La localisation du tournoi ne peut pas être vide.")

        while True:
            tournament_date_of_begin = input("Quelle est la date de début du tournoi? (Format : JJ/MM/AAAA) ")
            try:
                # Essayer de convertir la chaîne en objet datetime

                datetime.strptime(tournament_date_of_begin, "%d/%m/%Y")
                # La conversion a réussi, la date est valide
                break
            except ValueError:
                # La conversion a échoué, la date n'est pas valide
                print(
                    "Format de date invalide. Assurez-vous d'utiliser "
                    + "le format JJ/MM/AAAA. Réessayez."
                )
        nb_round_input = input("Combien il y aura-t-il de round? (par défaut 4) : ")

        if nb_round_input.strip() == "" or nb_round_input.strip() == "4":
            number_of_round = 4
        else:
            try:
                number_of_round = int(nb_round_input)
            except ValueError:
                print("Erreur : Veuillez entrer un nombre entier pour le nombre de rounds.")
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
        self.number_of_players = input("Combien y aura-t-il de joueurs dans le tournoi ?\n" +
                                       "Le nombre de joueur doit être un nombre pair " +
                                       "au moins 1 joueur de plus que le nombre de round):\n ")
        while int(self.number_of_players) % 2 != 0:
            print("Le nombre de joueurs doit être pair.")

        return self.number_of_players

    def choose_players(self):
        '''Permet de choisir si on veut créer une liste aléatoire de joueur'''
        self.choose_player = input("Voulez-vous créer une liste aléatoire de joueurs ? Oui/Non ").lower()
        return self.choose_player

    def choose_players_ID(self):
        ''' Permet de rentrer l'ID du joueur que l'on veut sélectionner'''
        self.choose_ID = input("Veuillez rentrer l'ID du joueur que vous souhaitez rajouter: ").upper()
        return self.choose_ID

    def display_list_tournament(self, tournaments):
        '''Affiche la liste des tournois.'''
        list_tournament = []
        print("\nListe des tournois:")
        for tournament in tournaments:
            tournament_name = tournament.get("Nom_du_tournoi")
            if tournament_name is not None:
                list_tournament.append(tournament_name)
        return list_tournament

    def display_tournament_details(self, tournaments):
        '''Affiche les détails (nom + date) d'un tournoi.'''
        counter = 0
        list_tournaments = []
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            tournaments = json.load(file)
        for tournament in tournaments:
            list_tournaments.append(tournament)
        for i, tournament in enumerate(list_tournaments, start=1):
            tournament_name = tournament.get("Nom_du_tournoi")
            if tournament_name is not None:
                counter += 1
                print(f"{counter}. {tournament_name}")
        try:
            choice = int(input("Veuillez sélectionner le numéro du tournoi: "))

            if 1 <= choice <= len(list_tournaments):
                # Déterminez le décalage en fonction de la valeur de choice
                offset = (choice - 1) // 2 * 2

                selected_tournament_index = choice - 1 + offset
                if selected_tournament_index < len(list_tournaments):
                    if "Nombre_joueurs_inscrits" in list_tournaments[selected_tournament_index]:
                        selected_tournament_index += 1

                    selected_tournament = list_tournaments[selected_tournament_index]
                    date_of_begin = selected_tournament.get("Date_de_debut")
                    tournament_name = selected_tournament.get("Nom_du_tournoi")
                else:
                    print("Erreur : Indice de tournoi sélectionné hors des limites.")
            else:
                print("Erreur : Choix de tournoi invalide.")
        except ValueError:
            print("Votre numéro de choix est invalide")

        return tournament_name, date_of_begin

    def display_tournament_alphabetically(self):
        '''Permet de ranger la liste des joueurs du tournoi par ordre alphabétique'''
        counter = 0
        list_players_data = []
        list_tournaments = []
        tournament_data_list = []
        file_path = os.path.join("data", "tournament_data.json")

        with open(file_path, "r") as file:
            tournaments = json.load(file)

        for tournament in tournaments:
            list_tournaments.append(tournament)

        for i, tournament in enumerate(list_tournaments, start=1):
            tournament_name = tournament.get("Nom_du_tournoi")
            if tournament_name is not None:
                counter += 1
                print(f"{counter}. {tournament_name}")

        try:
            choice = int(input("Veuillez sélectionner le numéro du tournoi : "))

            if 1 <= choice <= len(list_tournaments):
                # Déterminez le décalage en fonction de la valeur de choice
                offset = (choice - 1) // 2 * 2

                selected_tournament_index = choice - 1 + offset
                if selected_tournament_index < len(list_tournaments):
                    if "Nombre_joueurs_inscrits" in list_tournaments[selected_tournament_index]:
                        selected_tournament_index += 1

                    tournament_i = list_tournaments[selected_tournament_index]
                    tournament_i_1 = list_tournaments[selected_tournament_index + 1]

                    # Utilisez ces variables comme nécessaire
                else:
                    print("Erreur : Indice de tournoi sélectionné hors des limites.")
                    return
            else:
                print("Erreur : Choix de tournoi invalide.")
                return

            tournament_data_list.append(tournament_i)
            tournament_data_list.append(tournament_i_1)
            target_tournoi_name = tournament_data_list[0].get("Nom_du_tournoi")
            list_player = tournament_data_list[1].get("Liste_joueurs_inscrits")

            for player in list_player:
                player_data = []
                for key, value in player.items():
                    if key not in ['Score_tournament']:
                        player_data.append(value)

                list_players_data.append(player_data)

            # Tri alphabétique par le nom du joueur
            sorted_players_data = sorted(list_players_data, key=lambda x: x[0])

            data = {"Nom du tournoi": target_tournoi_name, "Liste_joueurs_triées": sorted_players_data}
            return data

        except ValueError:
            print("Votre numéro de choix est invalide")
            return

    def display_tournament_data(self):
        '''Permet d'afficher les détails d'un tournoi'''
        counter = 0
        file_path = os.path.join("data", "tournament_closed.json")
        list_tournaments = []
        with open(file_path, "r") as file:
            tournaments = json.load(file)
        for tournament in tournaments:
            tournament.pop("Date_de_fin", None)
        cleaned_tournaments = [tournament for tournament in tournaments if tournament]
        for tournament in cleaned_tournaments:
            list_tournaments.append(tournament)
        for i, tournament in enumerate(list_tournaments, start=1):
            tournament_name = tournament.get("Nom_du_tournoi")
            if tournament_name is not None:
                counter += 1
                print(f"{counter}. {tournament_name}")
        choice = int(input("Veuillez sélectionner le numéro du tournoi : "))
        if 1 <= choice <= len(list_tournaments):
            selected_tournament_index = choice - 1
            selected_tournament = list_tournaments[selected_tournament_index:selected_tournament_index + 2]
        target_tournoi_name = selected_tournament[0].get("Nom_du_tournoi")
        target_tournoi_index = None

        # Cherche l'index du tournoi cible dans la liste des tournois
        for i, tournament in enumerate(tournaments):
            if tournament.get("Nom_du_tournoi") == target_tournoi_name:
                target_tournoi_index = i
                break

        # Si l'index existe, l'index du tournoi suivant est "None"
        if target_tournoi_index is not None:
            next_tournoi_name = None
            next_tournoi_index = None

            # Cherche la prochaine occurence de "Nom_du_tournoi" qui vient après le tournoi cible
            # Récupère l'information du "Nom_du_tournoi" - Calcule son index
            for j, tournament in enumerate(tournaments[target_tournoi_index + 1:], start=target_tournoi_index + 1):
                if tournament.get("Nom_du_tournoi"):
                    next_tournoi_name = tournament.get("Nom_du_tournoi")
                    next_tournoi_index = j
                    break
            if next_tournoi_name is not None:
                next_tournoi_index = next((index for index, tournament in enumerate(tournaments)
                                          if tournament.get('Nom_du_tournoi') == next_tournoi_name), None)
                tournament_data_list = tournaments[target_tournoi_index:next_tournoi_index]
                if tournament_data_list and tournament_data_list[0].get("Date_de_fin"):
                    del tournament_data_list[0]
                else:
                    tournament_data_list = tournaments[target_tournoi_index:next_tournoi_index]
            else:
                next_tournoi_index = len(tournaments)
                tournament_data_list = tournaments[target_tournoi_index:next_tournoi_index]

        return tournament_data_list
