"""Define the Round."""
import json
import random
import os
import re

from controllers.match_controller import MatchController
from controllers.tournament_controller import TournamentController
from controllers.round_controller import RoundController
from models.tournament_model import Tournament
from models.player_model import Player


class RoundModel:
    def __init__(self, name_of_tournoi, start_date, end_date,
                 round_number):

        self.name_of_tournoi = name_of_tournoi
        self.start_date = start_date
        self.end_date = end_date
        self.round_number = round_number

    def load_data(self, file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self, file_path, data):
        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def create_pairs_round_one(self):
        ''' Permet de créer les paires de joueurs lors du premier round d'un tournoi'''
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        players = data[-1]
        list_player = players.get("Liste_des_joueurs_inscrits")
        list_player = list_player[0]
        random.shuffle(list_player)
        pairings = [(list_player[i], list_player[i + 1]) for i in range(0, len(list_player), 2)]
        return pairings

    def create_pairs_new_round(self, pairing_data):
        ''' Permet de créer les paires de joueurs lors des rounds suivants'''
        dict_player = {}
        b = []
        list_players = []
        list_pairs = []

        for match in pairing_data:
            for player in match:
                dict_player.update(player)
                a = list(dict_player.items())
                b.append(a)

        sorted_b = sorted(b, key=lambda x: (x[-1]), reverse=True)
        list_players.append(sorted_b)
        list_players.pop()

        for i in range(0, len(list_players), 2):
            player1 = list_players[i]
            player2 = list_players[i + 1] if i + 1 < len(list_players) else None

            if (player1, player2) not in pairing_data and (player2, player1) not in pairing_data:
                dict_player1 = dict(player1)
                dict_player2 = dict(player2)
                pairings_player = [dict_player1, dict_player2]
                list_pairs.append(pairings_player)

        return {"Liste_des_paires": list_pairs}


class RoundTournamentModel:
    """Contrôleur pour la gestion des rounds dans un tournoi."""

    def start_rounds(self, tournament, tournament_ID, list_pairs):
        """Démarre les rounds d'un tournoi."""
        # Charge l'instance spécifique du tournoi à partir du fichier JSON

        selected_tournament = Tournament.load_tournament_by_id(tournament_ID)
        # Charge uniquement les joueurs inscrits

        players = list_pairs
        number_of_rounds = selected_tournament.number_of_round
        print("\nce tournoi a ", number_of_rounds, " rounds")
        # Démarre le tournoi spécifique

        selected_tournament.start_tournament(tournament)

        for round_number in range(1, number_of_rounds + 1):
            round_name = f"Round {round_number}"
            new_round = RoundModel(round_name)
            new_round.start_round()
            print(f"debut du round : {round_number}")
            if round_number == 1:
                new_round.create_pairs_round_one(players)
            else:
                sorted_players = self.calculate_points_for_tournament(tournament_ID)
                previous_results = self.get_previous_results(
                    tournament_ID, round_number
                )
                pairs, _ = new_round.create_pairs_new_round(
                    players, previous_results, sorted_players
                )
                print("\nprochain Match pour le round en cours :\n")
                for pair in pairs:
                    player1 = f"{pair['player1']['name']} {pair['player1']['surname']}"
                    player2 = f"{pair['player2']['name']} {pair['player2']['surname']}"
                    print(f"Match : {player1} vs {player2}")
            selected_tournament.add_round_to_list(new_round)
            MatchController.play_match(new_round)
            new_round.end_round()
            Tournament.update_tournament(
                tournament_ID, {"list_of_round": selected_tournament.list_of_round}
            )
            if round_number < number_of_rounds:
                user_choice = input("Continuez a entrer les resultats O/N : ")
                if user_choice.lower() == "n":
                    break
            else:
                break
        if not (user_choice.lower()) == "n":
            self.calculate_points_for_tournament_final(tournament_ID)
            selected_tournament.end_tournament(tournament_ID)

    def update_matches(self, updated_matches):
        '''Met à jour les matchs du round avec de nouvelles valeurs.'''
        for match_index, match in enumerate(self.matches):
            # Mets à jour les valeurs du match
            if match_index < len(updated_matches):
                match_data = updated_matches[match_index]
                for key, value in match_data.items():
                    setattr(match, key, value)

    def get_previous_results(self, tournament_ID, round_number):
        """Récupère les résultats des rounds précédents."""
        previous_results = []
        # Charge les données du tournoi depuis le fichier JSON

        selected_tournament = Tournament.load_tournament_by_id(tournament_ID)
        # Renverse la liste des tours pour parcourir du dernier au premier

        reversed_rounds = reversed(selected_tournament.list_of_round)
        # Parcourt les rounds précédents et récupère les résultats des matchs

        for round_data in reversed_rounds:
            current_round_number = round_data.get("round_number", 0)
            if current_round_number < round_number and round_data.get("matches"):
                previous_results.extend(round_data["matches"])
                break
        return previous_results

    def update_matches_in_round(self, round_number, tournament_ID, updated_matches):
        # Charge l'instance spécifique du tournoi à partir du fichier JSON

        selected_tournament = Tournament.load_tournament_by_id(tournament_ID)
        # Récupére le round spécifique

        round_to_update = selected_tournament.get_round_by_number(round_number)
        if round_to_update:
            # Mets à jour les matchs dans le round

            round_to_update = MatchController.update_matches(updated_matches)
            # Mets à jour le tournoi avec les nouvelles valeurs

            Tournament.update_tournament(
                tournament_ID, {"list_of_tours": selected_tournament.list_of_round}
            )

    def calculate_points_for_tournament(self, tournament_ID):
        # Charger le tournoi spécifique

        tournament = Tournament.load_tournament_by_id(tournament_ID)
        if not tournament:
            print(f"Tournament with ID {tournament_ID} not found.")
            return
        player_points = {}
        for round_data in tournament.list_of_round:
            for match_data in round_data.get("matches", []):
                for player_ID, score in match_data:
                    self.update_player_points(player_points, player_ID, score)
        sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
        return sorted_players

    def calculate_points_tournament(self, tournament_ID):
        # Charger le tournoi spécifique

        tournament = Tournament.load_tournament_by_id(tournament_ID)
        if not tournament:
            print(f"Tournament with ID {tournament_ID} not found.")
            return
        player_points = {}
        new_tournament_score = 0
        score = 0
        for round_data in tournament.list_of_round:
            for match_data in round_data.get("matches", []):
                for player_ID, score in match_data:
                    player_points.setdefault(player_ID, 0)
                    player_points[player_ID] += score
                    # Mets à jour le score du tournoi dans le modèle Player

                    player = Player.get_player_by_id(player_ID)
                    if player:
                        new_tournament_score = score
                        player = Player.update_score_tournament(player_ID, new_tournament_score)
                    else:
                        print(f"Joueur avec l'ID {player_ID} non trouvé.")
        sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
        print("Classement Final du Tournoi :\n")
        for player_id, points in sorted_players:
            player = Player.get_player_by_id(player_ID)
            if player:
                print(f"{player.name} {player.surname}: {points} points")
            else:
                print(f"Player with ID {player_ID} not found.")
        print()
        return sorted_players

    def update_player_points(self, player_points, player_ID, score):
        player_points.setdefault(player_ID, 0)
        player_points[player_ID] += score

    def resume_rounds(self, tournament_ID, player_ID):
        """Reprendre l'entrée des résultats pour les rounds d'un tournoi."""
        # Charge l'instance spécifique du tournoi à partir du fichier JSON

        selected_tournament = Tournament.load_tournament_by_id(tournament_ID)
        players = Player.load_players_by_ids(
            player_ID
        )  # Charge uniquement les joueurs inscrits
        number_of_rounds = selected_tournament.number_of_round
        # Reprendre l'entrée des résultats pour chaque round

        round_number = [
            int(re.search(r"Round (\d+)", tour["round_name"]).group(1))
            for tour in selected_tournament.list_of_round
        ]
        if round_number:
            dernier_numero_round = max(round_number)
            print("le dernier round est le : ", dernier_numero_round, "\n")
        for round_number in range(dernier_numero_round + 1, number_of_rounds + 1):
            round_name = f"Round {round_number}"
            new_round = RoundModel(round_name)
            new_round = RoundController.start_round()
            print(f"debut_du_round_numero {round_number}\n")
            if round_number == 1:
                new_round.create_pairs_round_one(players)
            else:
                sorted_players = self.calculate_points_for_tournament(tournament_ID)
                previous_results = self.get_previous_results(
                    tournament_ID, round_number
                )
                pairs, _ = new_round.create_pairs_new_round(
                    players, previous_results, sorted_players
                )
                print("\nprochain Match pour le round en cours :\n")
                for pair in pairs:
                    player1 = f"{pair['player1']['name']} {pair['player1']['surname']}"
                    player2 = f"{pair['player2']['name']} {pair['player2']['surname']}"
                    print(f"Match : {player1} vs {player2}")
            selected_tournament = Tournament.add_round_to_list(new_round)
            MatchController.play_match(new_round)
            # Mets à jour le tournoi avec les nouvelles valeurs

            new_round = RoundController.end_round()
            Tournament.update_tournament(
                tournament_ID, {"list_of_round": selected_tournament.list_of_round}
            )
            if round_number < number_of_rounds:
                user_choice = input("Continuez a entrer les résultats suivants Oui/Non : ")
                if user_choice.lower() == "non":
                    break
            else:
                break
        if user_choice.lower() == "oui":
            self.calculate_points_tournament(tournament_ID)
            selected_tournament = TournamentController.end_tournament(tournament_ID)
