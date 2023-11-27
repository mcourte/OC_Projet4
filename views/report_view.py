class ReportView:

    @staticmethod
    def display_report_menu():

        print("\nMenu de Rapports :")
        print("1. Liste de tous les joueurs par ordre alphabétique")
        print("2. Liste de tous les tournois")
        print("3. Détails d'un tournoi donné")
        print("4. Liste des joueurs d'un tournoi par ordre alphabétique")
        print("5. Liste de tous les tours d'un tournoi et de tous les matchs" +
              "du tournoi")
        print("6. Revenir au menu principal")
        user_choice = input("Choisissez une option: ")
        return user_choice


    def display_invalid_option_message():

        print("Option invalide. Veuillez choisir une option valide pour" +
              "les rapports.")

    # Ajoutez d'autres fonctions pour l'affichage des différents rapports ici

    def save_report(self):
 
        self.save = input("Voulez-vous sauvegarder ce rapport ? (Oui/Non): ").lower()
        return self.save
    
    def name_report(self):

        self.name = input("Choississez le nom sous lequel vous souhaitez enregistrer le rapport: ")
        return self.name

