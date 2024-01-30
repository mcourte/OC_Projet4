class MainView:

    def main_menu(self):
        print("\nMenu :")
        print("1. Gestion des joueurs")
        print("2. Gestion des tournois")
        print("3. Rapports")
        print("4. Quitter\n")

        self.choice = input("Choisissez une option: ")
        return self.choice
