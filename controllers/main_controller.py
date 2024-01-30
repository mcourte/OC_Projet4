from views import main_view
from controllers import player_controller
from controllers import tournament_controller
from controllers import report_controller


class MainController:
    '''Contrôleur principal de l'application.'''

    def __init__(self):
        '''Initialise le contrôleur principal.'''
        pass

    def run(self):
        ''' Permet de lancer les fonctions en fonction des choix de l'utilisateur'''
        while True:
            choice = main_view.MainView().main_menu()

            if choice == "1":
                player_controller.PlayerController().player_menu()
            elif choice == "2":
                tournament_controller.TournamentController().tournament_menu()
            elif choice == "3":
                report_controller.ReportController().report_menu()
            elif choice == "4":
                print("Au revoir !")
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")
