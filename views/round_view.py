"""Define the Tournament."""


class RoundView:

    def __init__(self):
        pass

    def display_round_menu(self):
        print("\nMenu Compléter un tournoi: ")
        print("1. Ajouter le premier round")
        print("2. Rentrer les scores des matchs")
        print("3. Ajouter un nouveau round")
        print("4. Terminer un round")
        print("5. Revenir au menu principal\n")
        user_choice = input("Choisissez une option: ")
        return user_choice
