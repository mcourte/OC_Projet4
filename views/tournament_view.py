"""Define the Tournament."""


class TournamentView:

    def __init__(self):
        pass

    def display_tournament_menu(self):
        '''Permet d'afficher le menu de gestion des tournois'''
        print("\nMenu de Gestion des Tournois :")
        print("1. Ajouter un nouveau tournoi")
        print("2. Compléter un tournoi")
        print("3. Terminer un tournoi")
        print("4. Revenir au menu principal\n")
        user_choice = input("Choisissez une option: ")
        return user_choice

    def start_tournament_view(self):
        '''Permet d'initier un nouveau tournoi'''
        name = input("Quel est le numéro du tournoi?")
        self.name = "Tournoi n°" + str(name)
        self.location = input("Quelle est la localisation du tournoi?")
        nb_round = input("Combien il y aura-t-il de round?(par défaut :4)")
        if nb_round == "" or "4":
            self.number_of_round = 4
        else:
            self.number_of_round = nb_round

        self.description = input("Entrez les remarques générales du tournoi : ")
        self.tournament_data_view = [
            {
                        "Nom du tournoi: ": self.name,
                        "Lieu: ": self.location,
                        "Nombre de round: ": self.number_of_round,
                        "Description: ": self.description
                        }
                        ]
        return self.tournament_data_view

    def number_of_player(self):
        '''Permet à l'utilisateur de choisir le nombre de joueur qu'il veut dans le tournoi'''
        self.number_of_players = input("Combien y aura-t-il de joueurs dans le tournoi ?" +
                                       "Le nombre de joueur doit être un nombre pair " +
                                       "au moins 1 joueur de plus que le nombre de round): ")
        return self.number_of_players

    def choose_players(self):
        '''Permet de choisir si on veut créer une liste aléatoire de joueur'''
        self.choose_player = input("Voulez-vous créer une liste aléatoire de joueurs ? Oui/Non ").lower()
        return self.choose_player

    def choose_players_ID(self):
        ''' Permet de rentrer l'ID du joueur que l'on veut sélectionner'''
        self.choose_ID = input("Veuillez rentrer l'ID du joueur que vous souhaitez rajouter : ").upper()
        return self.choose_ID

    def choose_tournament(self):
        '''Permet à l'utilisateur de choisir le tournoi dont il veut les détails'''
        self.choice_tournament = input("Choisissez le nom du tournoi dont vous voulez les détails : ")
        return self.choice_tournament
