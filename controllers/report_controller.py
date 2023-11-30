import os

from controllers import player_controller
from controllers import tournament_controller
from views import report_view


class ReportController:
    """Contrôleur pour gérer les rapports et leurs opérations associées."""
    def __init__(self):
        """Initialise le contrôleur des rapports avec les contrôleurs
        des joueurs et de tournois en option."""
        pass

    def report_menu(self):
        """Exécute le menu de rapport en fonction du choix de l'utilisateur."""
        while True:
            choice = report_view.ReportView().display_report_menu()

            if choice == "1":
                ReportController().display_players_alphabetically()
            elif choice == "2":
                ReportController().display_all_tournaments()
            elif choice == "3":
                pass
            elif choice == "4":
                ReportController().display_tournament_players_alphabetically()
            elif choice == "5":
                pass
            elif choice == "6":
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")
    
    def save_report_to_file(self, report_text):
        '''Permet de sauvegarder le rapport'''
        report_text.pop()
        save_report = report_view.ReportView().save_report()
        data_report = "reports"
        if save_report == "oui" :
            name = report_view.ReportView().name_report()
            file_name = name + ".txt"
            file_path = os.path.join(data_report, file_name)
            with open(file_path, 'w') as file:
                    file.write(report_text)
            print(f"Rapport sauvegardé avec succès dans {file_path}")

    def display_players_alphabetically(self):
        """Affiche les joueurs par ordre alphabétique et permet de sauvegarder
        le rapport."""
        report_text=[]
        players_report = player_controller.PlayerController().display_players()
        for l in players_report:
            print(l)
        save = ReportController().save_report_to_file(report_text)

    
    def display_all_tournaments(self):
        """Affiche tous les tournois."""
        report_text=[]
        tournament_report = tournament_controller.TournamentController().display_tournament()
        print(tournament_report)
        #for l in tournament_report :
        #    print(report_text + "\n")
        #save = ReportController().save_report_to_file(report_text)
        


    def display_tournament_players_alphabetically(self):
        """Affiche les joueurs d'un tournoi par ordre alphabétique."""
        report_text=[]
        tournament_player_alpha_report = tournament_controller.TournamentController().display_tournament_alphabetically()
        for l in tournament_player_alpha_report :
            report_text.append(l)
        save = ReportController().save_report_to_file(report_text)

