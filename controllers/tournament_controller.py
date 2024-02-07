import os
import random
import json
import datetime

from views.tournament_view import TournamentView
from controllers.round_controller import RoundController


class TournamentController:

    def __init__(self):
        self.tournament_data_view = None
        self.number_of_player = None
        self.score_tournoi = 0
        self.list_of_players = []

    def start_tournament(self):
        self.tournament_data_view = TournamentView.start_tournament_view(self)
        file_path = os.path.join("data", "tournament_data.json")

        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            data = []

        data.extend(self.tournament_data_view)

        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        self.number_of_player = TournamentView.number_of_player(self)

        while int(self.number_of_player) % 2 != 0:
            print("Le nombre de joueurs doit être pair.")
            self.number_of_player = TournamentView.number_of_player(self)

        self.list_of_players = []

        file_path_players = os.path.join("data", "players_data.json")

        with open(file_path_players, "r") as file:
            data_players = json.load(file)

        self.choose_player = TournamentView.choose_players(self)

        if self.choose_player == "oui":
            index = int(self.number_of_player)
            self.list_of_players.extend(random.sample(data_players, index))
        elif self.choose_player == "non":
            for _ in range(int(self.number_of_player)):
                choose_player = TournamentView.choose_players_ID(self)
                chosen_player = next((player for player in data_players if player["player_ID"] == choose_player), None)
                if chosen_player:
                    self.list_of_players.append(chosen_player)

        self.tournament_data = [
            {
                "Nombre_joueurs_inscrits": self.number_of_player,
                "Liste_joueurs_inscrits": self.list_of_players,
            }
        ]

        data.extend(self.tournament_data)

        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        file_path_pending = os.path.join("data", "tournament_pending.json")

        with open(file_path_pending, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        tournament = self.tournament_data_view[0]
        tournament.update(self.tournament_data)
        tournament_ID = tournament.get("Tournoi_ID")
        player_ID = [player["Player_ID"] for player in self.list_of_players]

        RoundController().start_round(tournament, tournament_ID, player_ID)

        return self.tournament_data, self.number_of_player

    def resume_tournament_menu(self):
        """Affiche les tournois en cours et permet à l'utilisateur de choisir
        le tournoi à reprendre.
        """
        file_path = os.path.join("data", "tournament_pending.json")

        try:
            with open(file_path, "r") as file:
                tournament_inprogress = json.load(file)

            if not tournament_inprogress:
                print("Aucun tournoi en cours.")
                return
            print("Tournois en cours :")
            for i, tournament_dict in enumerate(tournament_inprogress, start=1):
                if isinstance(tournament_dict, dict):
                    tournament_name = tournament_dict.get("Nom_du_tournoi")
                    if tournament_name is not None:
                        print(f"{i}. {tournament_name}")

            try:
                choice = int(input("Veuillez sélectionner le numéro du tournoi à reprendre : "))
                if 1 <= choice <= len(tournament_inprogress):
                    selected_tournament_index = choice - 1
                    selected_tournament = tournament_inprogress[selected_tournament_index]
                    selected_tournament.update(tournament_inprogress[selected_tournament_index + 1])
                    self.resume_selected_tournament(selected_tournament)
                else:
                    print("Choix invalide")
            except ValueError:
                print("Choix invalide")

        except FileNotFoundError:
            print("Aucun fichier de tournoi en cours trouvé.")

    def end_tournament(self):
        file_path = os.path.join("data", "tournament_pending.json")

        try:
            with open(file_path, "r") as file:
                tournament_inprogress = json.load(file)

            if not tournament_inprogress:
                print("Aucun tournoi en cours.")
                return
            print("Tournois en cours :")
            for i, tournament_dict in enumerate(tournament_inprogress, start=1):
                if isinstance(tournament_dict, dict):
                    tournament_name = tournament_dict.get("Nom_du_tournoi")
                    if tournament_name is not None:
                        print(f"{i}. {tournament_name}")

            try:
                choice = int(input("Veuillez sélectionner le numéro du tournoi à reprendre : "))
                if 1 <= choice <= len(tournament_inprogress):
                    selected_tournament_index = choice - 1
                    selected_tournament = tournament_inprogress[selected_tournament_index]
                    selected_tournament.update(tournament_inprogress[selected_tournament_index + 1])
                else:
                    print("Choix invalide")
            except ValueError:
                print("Choix invalide")

        except FileNotFoundError:
            print("Aucun fichier de tournoi en cours trouvé.")
        date_of_end = datetime.date.today()
        tournament_end = {"Date_de_fin": str(date_of_end)}
        tournament_inprogress.append(tournament_end)

        with open(file_path, "w") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

        file_path2 = os.path.join("data", "tournament_closed.json")
        with open(file_path2, "a") as file:
            json.dump(tournament_inprogress, file, ensure_ascii=False, indent=4)
        print("Le tournoi est clos")

    def resume_selected_tournament(self, selected_tournament):
        """Reprendre un tournoi sélectionné."""
        # Obtenir la liste des joueurs inscrits au tournoi
        player_ID = []
        tournament_ID = selected_tournament.get("Tournoi_ID")
        list_players = selected_tournament.get("Liste_joueurs_inscrits")
        for player in list_players:
            player.get("Player_ID")
            player_ID.append(player)
        # Appel au contrôleur de round pour reprendre l'entrée des résultats
        RoundController().resume_rounds(tournament_ID, player_ID, selected_tournament)
        return tournament_ID, player_ID, selected_tournament

    def tournament_menu(self):
        '''Permet de lancer les fonctions suivant les choix de l'utilisateur'''
        while True:
            choice = TournamentView().display_tournament_menu()
            if choice == "1":
                TournamentController().start_tournament()
            elif choice == "2":
                TournamentController().resume_tournament_menu()
            elif choice == "3":
                TournamentController().end_tournament()
            elif choice == "4":
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")
