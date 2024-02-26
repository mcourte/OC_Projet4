from colorama import Style

from views.main_view import MainView
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController


class MainController:
    '''Contrôleur principal de l'application.'''

    def __init__(self):
        '''Initialise le contrôleur principal.'''
        pass

    def run(self):
        ''' Permet de lancer les fonctions en fonction des choix de l'utilisateur'''
        while True:
            choice = MainView().main_menu()

            if choice == "1":
                PlayerController().player_menu()
            elif choice == "2":
                TournamentController().tournament_menu()
            elif choice == "3":
                ReportController().report_menu()
            elif choice == "4":
                phrase = "\n \n Au revoir & à Bientôt! \n \n \n \n"
                MainView().slow_print(phrase)
                break
            else:
                print(f"{Style.BRIGHT}Option invalide. Veuillez choisir une option valide{Style.RESET_ALL}")
