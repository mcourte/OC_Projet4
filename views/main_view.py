from os import name
# from os import system

from colorama import Fore, Style
import time


class MainView:

    def main_menu(self):
        '''Affiche le menu principal du programme'''
        MainView.clear_screen()
        title = "\n Bienvenue sur le gestionnaire de Tournois d'Echecs ! \n"
        self.slow_print(title)
        title_menu = "\n Menu :"
        self.slow_print(title_menu)
        menu = "\n 1. Gestion des joueurs \n 2. Gestion des tournois \n 3. Rapports \n 4. Quitter\n"
        self.slow_print(menu)

        self.slow_print("Choisissez une option: ")
        self.choice = input()
        return self.choice

    def clear_screen():
        '''Permet de repartir à 0 dans l'affichage du terminal'''
        # Pour utilisateur Windows :
        if name == "nt":
            print("clear screen")
            # _ = system("cls")

        # Pour utilisateur Mac ou Linux :
        else:
            print("clear screen")
            # _ = system("clear")

    def slow_print(self, phrase, color=Fore.WHITE):
        '''Permet de styliser l'affichage des menus'''
        for letter in phrase:
            print(f"{color}{Style.BRIGHT}{letter}{Style.RESET_ALL}", end='', flush=True)
            time.sleep(0.02)
