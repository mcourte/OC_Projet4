"""Define the Tournament."""


class RoundView:

    def __init__(self):
        pass

    def display_round_menu(self):
        print("\nMenu Compléter un tournoi: ")
        print("1. Ajouter un nouveau round")
        print("2. Rentrer les scores des matchs")
        print("2. Terminer un round")
        print("3. Revenir au menu principal\n")
        user_choice = input("Choisissez une option: ")
        return user_choice
