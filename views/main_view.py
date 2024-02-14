from os import name
from os import system


class MainView:

    def main_menu(self):
        print("\nBienvenue sur le gestionnaire de Tournois d'Echecs ! \n")
        print("\nMenu :")
        print("1. Gestion des joueurs")
        print("2. Gestion des tournois")
        print("3. Rapports")
        print("4. Quitter\n")

        self.choice = input("Choisissez une option: ")
        return self.choice

    def clear_screen():
        """Clear the terminal"""
        # for windows

        if name == "nt":
            _ = system("cls")
        # for mac and linux

        else:
            _ = system("clear")
