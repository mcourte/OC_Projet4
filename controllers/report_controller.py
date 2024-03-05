import os
import json
from tabulate import tabulate

from controllers.player_controller import PlayerController
from views.report_view import ReportView
from views.tournament_view import TournamentView
from views.main_view import MainView


class ReportController:

    def __init__(self):
        '''Contrôleur pour gérer les rapports.'''
        pass

    def report_menu(self):
        '''Exécute le menu de rapport en fonction du choix de l'utilisateur.'''
        while True:
            choice = ReportView().display_report_menu()

            if choice == "1":
                ReportController().display_players_alphabetically()
            elif choice == "2":
                ReportController().display_all_tournaments()
            elif choice == "3":
                ReportController().display_tournaments_detail()
            elif choice == "4":
                ReportController().display_tournament_players_alphabetically()
            elif choice == "5":
                ReportController().display_tournaments_data()
            elif choice == "6":
                break
            else:
                error_message = "Option invalide. Veuillez choisir une option valide."
                MainView().slow_print(error_message)

    def save_report(self, report_text):
        '''Permet de sauvegarder le rapport'''
        save_report = ReportView.save_report(self)
        data_report = "reports"
        if save_report == "oui":
            name = ReportView.name_report(self)
            file_name = name + ".txt"
            file_path = os.path.join(data_report, file_name)
            with open(file_path, 'w') as file:
                file.write(str(report_text))
            result_message = f"Rapport sauvegardé avec succès dans {file_path}"
            MainView().slow_print(result_message)
            print("\n\n\n\n")

    def display_players_alphabetically(self):
        '''Affiche les joueurs par ordre alphabétique et permet de sauvegarder
        le rapport.'''
        # Récuper la liste des joueurs par ordre alphabétique
        players_report = PlayerController.display_players(self)
        # Créer un dictionnaire avec comme key Joueur1, Joueur2, .. puis les infos associées en value
        players_dict = {'Joueur{}'.format(index + 1): dict(player_info) for index, player_info
                        in enumerate(players_report)}

        # Crée et affiche un tableau pour mettre en forme les données
        table = tabulate(players_dict.items(), headers=["Joueur", "Data"], tablefmt="pretty")
        print(table)
        ReportController.save_report(self, table)

    def display_all_tournaments(self):
        '''Affiche tous les tournois.'''
        # Variables
        tournament_names = []
        file_path = os.path.join("data", "tournament_data.json")

        with open(file_path, "r") as file:
            tournaments = json.load(file)
        # Liste les tournois existants
        tournament_report = TournamentView.display_list_tournament(self, tournaments)
        for tournament in tournament_report:
            tournament_names.append(tournament)
        # Créer un dictionnaire avec comme key Tournoi1, Tournoi2, .. puis les infos associées en value
        tournament_dict = {f'Tournoi {index + 1}': name for index, name in enumerate(tournament_names)}

        # Crée et affiche un tableau pour mettre en forme les données
        table = tabulate(tournament_dict.items(), headers=["Numéro du tournoi", "Nom du tournoi"], tablefmt="pretty")
        print(table)
        ReportController.save_report(self, table)

    def display_tournament_players_alphabetically(self):
        '''Affiche les joueurs d'un tournoi par ordre alphabétique.'''
        # Récupère les infos depuis le tournoi sélectionné
        tournament_alpha_report = TournamentView.display_tournament_alphabetically(self)
        tournament_name = tournament_alpha_report.get("Nom du tournoi")
        tournament_players = tournament_alpha_report.get("Liste_joueurs_triées")

        if tournament_name and tournament_players:
            headers = ["Surname", "Name", "Date_of_birth", "Player_ID", "Score_tournament"]
            table_data = []

            for player_info in tournament_players:
                player_data = [val for _, val in player_info]
                table_data.append(player_data)

            title = f"{tournament_name} - List of Players"

            table = "\n\n" + title + "\n\n" + tabulate(table_data, headers=headers, tablefmt="pretty")

            print(table)
        else:
            print("No tournament data available.")
        ReportController.save_report(self, table)

    def display_tournaments_data(self):
        '''Affiche tous les rounds et matchs d'un tournois.'''
        # Variables
        tournament_report = TournamentView.display_tournament_data(self)
        tournament_data = tournament_report[0]
        tournament_data = tournament_data[0]
        tournament_name = tournament_data.get("Nom_du_tournoi")
        list_of_round = tournament_data.get("Liste_des_rounds")

        list_of_rounds = []
        list_of_matches = []

        for round_data in list_of_round:
            round_name = round_data.get("Nom_du_round")
            list_match = round_data.get("Matchs")

            list_of_rounds.append(round_name)
            list_of_matches.append(list_match)

        # Crée et affiche un tableau pour mettre en forme les données
        table = tabulate(list(zip(list_of_rounds, list_of_matches)),
                         headers=["Nom du round", "Matchs"], tablefmt="pretty")

        # Add a row for the tournament name at the beginning of the table
        table = f"Tournament: {tournament_name}\n\n{table}"

        print(table)
        ReportController.save_report(self, table)
