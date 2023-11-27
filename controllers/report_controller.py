import os

from controllers import player_controller
from views import report_view


class ReportController:
    """Contrôleur pour gérer les rapports et leurs opérations associées."""
    def __init__(self):
        """Initialise le contrôleur des rapports avec les contrôleurs
        des joueurs et de tournois en option."""
        pass

    def run_report_menu(self):
        """Exécute le menu de rapport en fonction du choix de l'utilisateur."""
        while True:
            choice = report_view.ReportView().display_report_menu()

            if choice == "1":
                self.display_players_alphabetically()
            elif choice == "2":
                self.display_all_tournaments()
            elif choice == "3":
                self.display_tournament_details()
            elif choice == "4":
                self.display_tournament_players_alphabetically()
            elif choice == "5":
                self.display_all_tournament_rounds_and_matches()
            elif choice == "6":
                break
            else:
                report_view.ReportView().display_invalid_option_message()
    
    def save_report_to_file(self, report_text):
        report_text.pop()
        print(report_text)
        save_report = report_view.ReportView().save_report()
        data_report = "reports"
        if save_report == "oui" :
            name = report_view.ReportView().name_report()
            file_name = name + ".txt"
            file_path = os.path.join(data_report, file_name)
            with open(file_path, 'w') as file:
                    file.write(str(report_text))
            print(f"Rapport sauvegardé avec succès dans {file_path}")

    def display_players_alphabetically(self):
        """Affiche les joueurs par ordre alphabétique et permet de sauvegarder
        le rapport."""
        players_report = player_controller.PlayerController().display_players()
        report_text = players_report
        save = ReportController().save_report_to_file(report_text)

    
    def display_all_tournaments(self):
        """Affiche tous les tournois."""
        tournament_report = self.player_controller.display_players()
        report_text = tournament_report
        save = ReportController().save_report_to_file(report_text)

    def display_tournament_details(self):
        """Affiche les détails d'un tournoi."""
        tournament_data_report = self.player_controller.display_players()
        report_text = tournament_data_report
        save = ReportController().save_report_to_file(report_text)

    def display_tournament_players_alphabetically(self):
        """Affiche les joueurs d'un tournoi par ordre alphabétique."""
        tournament_alpha_report = ""
        report_text = tournament_alpha_report
        save = ReportController().save_report_to_file(report_text)




test = ReportController()
test.display_players_alphabetically()
