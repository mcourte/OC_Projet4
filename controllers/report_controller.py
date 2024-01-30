import os

from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from views.report_view import ReportView


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
        report_text.pop()
        save_report = ReportView().save_report(self)
        data_report = "reports"
        if save_report == "oui":
            name = ReportView().name_report()
            file_name = name + ".txt"
            file_path = os.path.join(data_report, file_name)
            with open(file_path, 'w') as file:
                file.write(str(report_text))
            print(f"Rapport sauvegardé avec succès dans {file_path}")

    def display_players_alphabetically(self):
        '''Affiche les joueurs par ordre alphabétique et permet de sauvegarder
        le rapport.'''
        report_text = []
        players_report = PlayerController().display_players()
        for player in players_report:
            print(player)
            report_text.append(player)
        ReportController().save_report(report_text)

    def display_all_tournaments(self):
        '''Affiche tous les tournois.'''
        report_text = []
        tournament_report = TournamentController().display_tournament()
        for tournament in tournament_report:
            print(tournament)
            report_text.append(tournament)
        ReportController().save_report(report_text)

    def display_tournament_players_alphabetically(self):
        '''Affiche les joueurs d'un tournoi par ordre alphabétique.'''
        report_text = []
        tournament_alpha_report = TournamentController().display_tournament_alphabetically()
        for tournament in tournament_alpha_report:
            print(tournament)
            report_text.append(tournament)
        ReportController().save_report(report_text)

    def display_tournaments_detail(self):
        '''Affiche les détails d'un tournoi.'''
        report_text = []
        tournament_report = TournamentController().display_tournament_details()
        for tournament in tournament_report:
            print(tournament)
            report_text.append(tournament)
        ReportController().save_report(report_text)

    def display_tournaments_data(self):
        '''Affiche tous les rounds et matchs d'un tournois.'''
        report_text = []
        tournament_report = TournamentController().display_tournament_data()
        for tournament in tournament_report:
            print(tournament)
            report_text.append(tournament)
        ReportController().save_report(report_text)
