import os
import random
import json
import datetime

from views.tournament_view import TournamentView
from controllers.round_controller import RoundController


class TournamentController:

    def __init__(self):
        '''Contrôleur pour gérer les tournois.'''
        self.tournament_data_view = None
        self.number_of_player = None
        self.score_tournoi = 0
        self.list_of_players = []

    def create_tournament(self):
        '''Permet de créer un tournoi'''
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

        list_player_ID = [player["Player_ID"] for player in self.list_of_players]

        return self.tournament_data, self.number_of_player, tournament_ID, list_player_ID

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

            choice = int(input("Veuillez sélectionner le numéro du tournoi à lancer : "))
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
        '''Permet de terminer un tournoi'''
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

                    break  # Permet de sortir de la boucle si un choix correct à été fait
                else:
                    print("Choix invalide: hors de la plage valide")

            except ValueError:
                print("Choix invalide")
        target_tournoi_name = selected_tournament.get("Nom_du_tournoi")
        target_tournoi_index = None

        # Cherche l'index du tournoi cible dans la liste des tournois
        for i, tournament in enumerate(tournament_inprogress):
            if tournament.get("Nom_du_tournoi") == target_tournoi_name:
                target_tournoi_index = i
                break

        # Si l'index existe, l'index du tournoi suivant est "None"
        if target_tournoi_index is not None:
            next_tournoi_index = None

            # Cherche la prochaine occurence de "Nom_du_tournoi" qui vient après le tournoi cible
            # Calcul son index
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
        '''Reprendre un tournoi sélectionné.'''
        data = TournamentController.load_tournament_pending()

        target_tournoi_name = selected_tournament.get("Nom_du_tournoi")
        target_tournoi_index = None

        # Cherche l'index du tournoi cible dans la liste des tournois
        for i, tournament in enumerate(data):
            if tournament.get("Nom_du_tournoi") == target_tournoi_name:
                target_tournoi_index = i
                break

        # Si l'index existe, l'index du tournoi suivant est "None"
        if target_tournoi_index is not None:
            next_tournoi_name = None
            next_tournoi_index = None

            # Cherche la prochaine occurence de "Nom_du_tournoi" qui vient après le tournoi cible
            # Récupère l'information du "Nom_du_tournoi" - Calcule son index
            for j, tournament in enumerate(data[target_tournoi_index + 1:], start=target_tournoi_index + 1):
                if tournament.get("Nom_du_tournoi"):
                    next_tournoi_name = tournament.get("Nom_du_tournoi")
                    next_tournoi_index = j
                    break

            if next_tournoi_name:
                tournament_data_list = data[target_tournoi_index - 1:next_tournoi_index]
            else:
                tournament_data_list = data
        tournaments = {}
        for list_data in tournament_data_list:
            tournaments.update(list_data)
        tournament_ID = tournaments.get("Tournoi_ID")
        number_of_rounds = tournaments.get("Nombre_de_round")
        list_players = tournaments.get("Liste_joueurs_inscrits")
        list_of_round = tournaments.get("Liste_des_rounds")
        list_player_ID = []
        for player in list_players:
            player.get("Player_ID")
            list_player_ID.append(player)
        if list_of_round == []:
            round_name = None
        else:
            round_name = list_of_round[0].get("Nom_du_round")
        if round_name is None:
            RoundController().start_round(list_player_ID, tournament_ID, number_of_rounds, list_of_round)
        else:
            round_number = int(round_name[-1])
            list_pairs = list_of_round[0].get("Matchs")
            RoundController().resume_rounds(list_player_ID, tournament_ID,
                                            round_number, number_of_rounds,
                                            list_of_round, list_pairs)
        return tournament_ID, list_player_ID, tournament, number_of_rounds

    def tournament_menu(self):
        '''Permet de lancer les fonctions suivant les choix de l'utilisateur'''
        while True:
            choice = TournamentView().display_tournament_menu()
            if choice == "1":
                TournamentController().create_tournament()
            elif choice == "2":
                TournamentController().begin_tournament_menu()
            elif choice == "3":
                TournamentController().resume_tournament_pending_menu()
            elif choice == "4":
                TournamentController().end_tournament()
            elif choice == "5":
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")

    def load_tournament_pending():
        ''' Permet de télécharger les tournois en cours'''
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

    def resume_tournament_pending_menu(self):
        '''Affiche les tournois en cours et permet à l'utilisateur de choisir
        le tournoi à reprendre.'''
        tournament_inprogress = TournamentController.load_tournament_pending()
        if not tournament_inprogress:
            print("Aucun tournoi en cours.")
            return

        for i, tournament_dict in enumerate(tournament_inprogress, start=1):
            if isinstance(tournament_dict, dict):
                tournament_name = tournament_dict.get("Nom_du_tournoi")
                if tournament_name is not None:
                    print(f"{i}. {tournament_name}")

        choice = int(input("Veuillez sélectionner le numéro du tournoi à reprendre : "))
        print(f"Choix saisi : {choice}")

        try:
            if 1 <= choice <= len(tournament_inprogress):
                tournament_index = choice - 1
                selected_tournament = tournament_inprogress[tournament_index]

                # Find the last round index
                last_round_index = len(selected_tournament.get("Liste_des_rounds", [])) - 1

                # If there are rounds in the tournament, resume from the last round
                if last_round_index >= 0:
                    last_round = selected_tournament["Liste_des_rounds"][last_round_index]
                    print(last_round)
                    self.resume_selected_tournament(selected_tournament)
                else:
                    print("Ce tournoi n'a pas de rounds.")
            else:
                print("Choix invalide: hors de la plage valide")

        except ValueError as e:
            print(f"Erreur lors de la conversion en entier : {e}")
        except Exception as e:
            print(f"Erreur inattendue : {e}")

        return selected_tournament

    def begin_tournament_menu(self):
        # Function to load JSON data from a file
        def load_json(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)

        # File paths
        json1_path = os.path.join("data", "tournament_data.json")
        json2_path = os.path.join("data", "tournament_pending.json")
        json3_path = os.path.join("data", "tournament_closed.json")

        # Load JSON data from files
        data1 = load_json(json1_path)
        data2 = load_json(json2_path)
        data3 = load_json(json3_path)

        # Combine dictionaries not in tournament_pending and tournament_closed
        not_in_pending = [item for item in data1 if item not in data2]
        not_in_closed = [item for item in data1 if item not in data3]

        # Function to create a new dictionary at each occurrence of "Nom_du_tournoi"
        def create_tournament_dict(data):
            result = []
            current_tournament = None

            for item in data:
                if "Nom_du_tournoi" in item:
                    # If a new tournament is found, append the previous one to the result list
                    if current_tournament is not None:
                        result.append(current_tournament)
                    # Start a new dictionary for the current tournament
                    current_tournament = {"Nom_du_tournoi": item["Nom_du_tournoi"]}
                elif current_tournament is not None:
                    # If a tournament is in progress, add the current item to it
                    current_tournament.update(item)

            # Append the last tournament after the loop
            if current_tournament is not None:
                result.append(current_tournament)
            return result

        # Create new dictionaries at each occurrence of "Nom_du_tournoi"
        tournament_to_begin = create_tournament_dict(not_in_pending + not_in_closed)

        while True:
            counter = 0

            for i, tournament_dict in enumerate(tournament_to_begin, start=1):
                if isinstance(tournament_dict, dict):
                    tournament_name = tournament_dict.get("Nom_du_tournoi")
                    if tournament_name is not None:
                        counter += 1
                        print(f"{counter}. {tournament_name}")

            choice = int(input("Veuillez sélectionner le numéro du tournoi à lancer : "))
            print(f"Choix saisi : {choice}")
            try:
                if 1 <= choice <= len(tournament_to_begin):
                    tournament_index = (choice - 1)
                    selected_tournament = tournament_to_begin[tournament_index]
                    self.resume_selected_tournament(selected_tournament)
                    break
                else:
                    print("Choix invalide: hors de la plage valide")

            except ValueError as e:
                print(f"Erreur lors de la conversion en entier : {e}")
            except Exception as e:
                print(f"Erreur inattendue : {e}")
        return selected_tournament
