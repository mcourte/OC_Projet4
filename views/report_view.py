class ReportView:

    def display_report_menu(self):
        print("\nMenu de Rapports :")
        print("1. Liste de tous les joueurs par ordre alphabétique")
        print("2. Liste de tous les tournois")
        print("3. Nom et date d'un tournoi donné")
        print("4. Liste des joueurs d'un tournoi par ordre alphabétique")
        print("5. Liste de tous les tours d'un tournoi et de tous les matchs " +
              " et des round")
        print("6. Revenir au menu principal\n")
        user_choice = input("Choisissez une option: ")
        return user_choice

    def save_report(self):
        self.save = input("Voulez-vous sauvegarder ce rapport ? (Oui/Non): ").lower()
        return self.save

    def name_report(self):
        self.name = input("Choississez le nom sous lequel vous souhaitez enregistrer le rapport: ")
        return self.name
