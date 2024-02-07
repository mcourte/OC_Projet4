import os
import json

from controllers.player_controller import PlayerController
from views.report_view import ReportView
from views.tournament_view import TournamentView


class ReportController:
    '''Contrôleur pour gérer les rapports et leurs opérations associées.'''
    def __init__(self):
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
                print("Option invalide. Veuillez choisir une option valide.")

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
            print(f"Rapport sauvegardé avec succès dans {file_path}")

    def display_players_alphabetically(self):
        '''Affiche les joueurs par ordre alphabétique et permet de sauvegarder
        le rapport.'''
        report_text = []
        players_report = PlayerController.display_players(self)
        for player in players_report:
            report_text.append(player)
        ReportController.save_report(self, report_text)

    def display_all_tournaments(self):
        '''Affiche tous les tournois.'''
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            tournaments = json.load(file)
        report_text = []
        tournament_report = TournamentView.display_list_tournament(self, tournaments)
        for tournament in tournament_report:
            report_text.append(tournament)
        print(report_text)
        ReportController.save_report(self, report_text)

    def display_tournament_players_alphabetically(self):
        '''Affiche les joueurs d'un tournoi par ordre alphabétique.'''
        report_text = []
        tournament_alpha_report = TournamentView.display_tournament_alphabetically(self)
        for tournament in tournament_alpha_report:
            report_text.append(tournament)
        ReportController.save_report(self, report_text)

    def display_tournaments_detail(self):
        '''Affiche les détails d'un tournoi.'''
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            tournaments = json.load(file)
        report_text = []
        report_text = TournamentView.display_tournament_details(self, tournaments)
        ReportController.save_report(self, report_text)

    def display_tournaments_data(self):
        '''Affiche tous les rounds et matchs d'un tournois.'''
        report_text = []
        tournament_report = TournamentView.display_tournament_data(self)
        for tournament in tournament_report:
            report_text.append(tournament)
        ReportController.save_report(self, report_text)
