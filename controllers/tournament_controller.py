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
            for player in data_players:
                print(f"{player.get('Surname')},{player.get('Name')},{player.get('Player_ID')}")
            for _ in range(int(self.number_of_player)):
                choose_player = TournamentView.choose_players_ID(self)
                chosen_player = next((player for player in data_players if player["Player_ID"] == choose_player), None)
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
        tournament.update(self.tournament_data[0])
        tournament_ID = tournament.get("Tournoi_ID")

        player_ID = [player["Player_ID"] for player in self.list_of_players]

        RoundController().start_round(tournament_ID, player_ID)

        return self.tournament_data, self.number_of_player

    def resume_tournament_menu(self):
        """Affiche les tournois en cours et permet à l'utilisateur de choisir
        le tournoi à reprendre.
        """
        tournament_inprogress = TournamentController.load_tournament_pending()
        if not tournament_inprogress:
            print("Aucun tournoi en cours.")
            return

        while True:
            counter = 0

            for i, tournament_dict in enumerate(tournament_inprogress, start=1):
                if isinstance(tournament_dict, dict):
                    tournament_name = tournament_dict.get("Nom_du_tournoi")
                    if tournament_name is not None:
                        counter += 1
                        print(f"{counter}. {tournament_name}")

            choice = int(input("Veuillez sélectionner le numéro du tournoi à reprendre : "))
            print(f"Choix saisi : {choice}")
            try:
                if 1 <= choice <= len(tournament_inprogress):
                    tournament_index = (choice - 1)
                    selected_tournament = tournament_inprogress[tournament_index]
                    self.resume_selected_tournament(selected_tournament)
                    break
                else:
                    print("Choix invalide: hors de la plage valide")

            except ValueError as e:
                print(f"Erreur lors de la conversion en entier : {e}")
            except Exception as e:
                print(f"Erreur inattendue : {e}")
        return selected_tournament

    def end_tournament(self):
        tournament_inprogress = TournamentController.load_tournament_pending()
        if not tournament_inprogress:
            print("Aucun tournoi en cours.")
            return

        while True:
            print("Tournois en cours :")
            counter = 0

            for i, tournament_dict in enumerate(tournament_inprogress, start=1):
                if isinstance(tournament_dict, dict):
                    tournament_name = tournament_dict.get("Nom_du_tournoi")
                    if tournament_name is not None:
                        counter += 1
                        print(f"{counter}. {tournament_name}")

            choice = int(input("Veuillez sélectionner le numéro du tournoi à clôre : "))
            print(f"Choix saisi : {choice}")
            try:
                if 1 <= choice <= len(tournament_inprogress):
                    tournament_index = (choice - 1)
                    selected_tournament = tournament_inprogress[tournament_index]

                    break  # exit the loop if a valid choice is made
                else:
                    print("Choix invalide: hors de la plage valide")

            except ValueError:
                print("Choix invalide")
        target_tournoi_name = selected_tournament.get("Nom_du_tournoi")
        target_tournoi_index = None

        # Find the index of the selected tournament in the data list
        for i, tournament in enumerate(tournament_inprogress):
            if tournament.get("Nom_du_tournoi") == target_tournoi_name:
                target_tournoi_index = i
                break

        # Check if the selected tournament was found
        if target_tournoi_index is not None:
            next_tournoi_index = None

            # Search for the next occurrence of "Nom_du_tournoi" after the selected tournament
            for j, tournament in enumerate(tournament_inprogress[target_tournoi_index + 1:],
                                           start=target_tournoi_index + 1):
                if tournament.get("Nom_du_tournoi"):
                    next_tournoi_index = j
                    break

        tournament = tournament_inprogress[target_tournoi_index:next_tournoi_index]
        date_of_end = datetime.date.today()
        tournament_end = {"Date_de_fin": str(date_of_end)}
        tournament.append(tournament_end)
        tournament_closed = [tournament]
        del tournament_inprogress[target_tournoi_index:next_tournoi_index]
        file_path = "data/tournament_pending.json"
        with open(file_path, "w") as file:
            json.dump(tournament_inprogress, file, ensure_ascii=False, indent=4)

        file_path2 = os.path.join("data", "tournament_closed.json")
        with open(file_path2, "w") as file:
            json.dump(tournament_closed, file, ensure_ascii=False, indent=4)

        print("Le tournoi est clos")

    def resume_selected_tournament(self, selected_tournament):
        """Reprendre un tournoi sélectionné."""
        data = TournamentController.load_tournament_pending()
        target_tournoi_name = selected_tournament.get("Nom_du_tournoi")
        target_tournoi_index = None

        # Find the index of the selected tournament in the data list
        for i, tournament in enumerate(data):
            if tournament.get("Nom_du_tournoi") == target_tournoi_name:
                target_tournoi_index = i
                break

        # Check if the selected tournament was found
        if target_tournoi_index is not None:
            next_tournoi_name = None
            next_tournoi_index = None

            # Search for the next occurrence of "Nom_du_tournoi" after the selected tournament
            for j, tournament in enumerate(data[target_tournoi_index + 1:], start=target_tournoi_index + 1):
                if tournament.get("Nom_du_tournoi"):
                    next_tournoi_name = tournament.get("Nom_du_tournoi")
                    next_tournoi_index = j
                    break

            if next_tournoi_name:
                print(f"The next tournament is: {next_tournoi_name}")
                print(f"The index of the next tournament is: {next_tournoi_index}")

                tournament = data[target_tournoi_index:next_tournoi_index]

        player_ID = []
        tournament_ID = tournament[0].get("Tournoi_ID")
        number_of_rounds = tournament[0].get("Nombre_du_round")
        round_number = tournament[0].get("Nom_du_round")
        list_players = tournament[1].get("Liste_joueurs_inscrits")
        for player in list_players:
            player.get("Player_ID")
            player_ID.append(player)
        RoundController().resume_rounds(player_ID, tournament_ID, round_number, number_of_rounds)
        return tournament_ID, player_ID, tournament, round_number, number_of_rounds

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

    def load_tournament_pending():
        file_path = "data/tournament_pending.json"

        try:
            with open(file_path, 'r') as file:
                data = file.read()
                if data:
                    return json.loads(data)
                else:
                    return []
        except Exception as e:
            print(f"Erreur lors du chargement des données du tournoi : {e}")
            return []
