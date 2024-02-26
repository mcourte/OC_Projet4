from views.main_view import MainView


class ReportView:

    def display_report_menu(self):
        '''Affiche le menu de création des Rapports'''
        MainView.clear_screen()
        title = "\nMenu de Rapports :\n"
        MainView().slow_print(title)
        menu = ("\n 1. Liste de tous les joueurs par ordre alphabétique \n 2. Liste de tous les tournois \n" +
                " 3. Nom et dates d'un tournoi donné \n 4. Liste des joueurs d'un tournoi par ordre alphabétique " +
                "\n 5. Liste de tous les rounds d'un tournoi et de tous les matchs \n 6. Revenir au menu principal\n")
        MainView().slow_print(menu)
        choice = "Choisissez une option: "
        MainView().slow_print(choice)
        self.choice = input()
        return self.choice

    def save_report(self):
        '''Permet à l'utilisateur de choisir si il veut enregistrer son rapport'''
        self.save = input("Voulez-vous sauvegarder ce rapport ? (Oui/Non): ").lower()
        return self.save

    def name_report(self):
        '''Permet à l'utilisateur de choisir le nom du fichier'''
        self.name = input("Choississez le nom sous lequel vous souhaitez enregistrer le rapport: ")
        return self.name
