import os
import datetime
import json
import re


from controllers.match_controller import MatchController
from controllers.tournament_controller import TournamentController
from controllers.player_controller import PlayerController
from views.round_view import RoundView
from models.round_model import Round


class RoundController:
    def __init__(self):
        pass

    def start_round(self):

        start_date = datetime.datetime.today().strftime("%d-%m-%Y")
        round_number = 1
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        data_round = {
            "Nom du Round: ": f"Round {round_number}",
            "Date de début: ": start_date,
        }
        data_players = Round().create_pairs_round_one()
        data.extend([data_round, data_players])

        file_path2 = os.path.join("data", "tournament_pending.json")
        with open(file_path2, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(data_round)
        print(data_players)
        return data_round, data_players

    def new_round(self):
        data = Round.load_data("data", "tournament_pending.json")
        list_round_numbers = [round["Numéro de round: "] for round in data if isinstance(round, dict)]
        last_round_number = max(list_round_numbers)
        start_date = datetime.datetime.today().strftime("%d-%m-%Y")
        new_round_number = last_round_number + 1

        if new_round_number <= data[0]["Nombre de round: "]:
            data_new_round = {
                "Nom du Round: ": f"Round {new_round_number}",
                "Date de début: ": start_date,
            }
            file_path2 = os.path.join("data", "tournament_data.json")
            Round.save_data(file_path2, data_new_round)

            data_players = Round().create_pairs_new_round(data[-1]["Liste des paires: "])
            data.extend([data_new_round, data_players])

            file_path = os.path.join("data", "tournament_pending.json")
            Round.save_data(file_path, data)

            print(data_new_round)
            print(data_players)
        else:
            print("Tous les rounds du tournoi ont été joués")

        return new_round_number

    def end_round(self):
        end_date = datetime.datetime.today().strftime("%d-%m-%Y")
        end = {"Date de fin du round : ": end_date}
        data = Round.load_data("data", "tournament_pending.json")
        data.append(end)

        print(end)

        file_path = os.path.join("data", "tournament_pending.json")
        Round.save_data(file_path, data)
        file_path2 = os.path.join("data", "tournament_data.json")
        Round.save_data(file_path2, data)

        return end

    def round_menu(self):
        while True:
            choice = RoundView().display_round_menu()

            if choice == "1":
                RoundController().start_round()
            elif choice == "2":
                MatchController().process_match()
            elif choice == "3":
                RoundController().new_round()
            elif choice == "4":
                RoundController().end_round()
            elif choice == "5":
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")


class RoundTournamentController:
    '''Contrôleur pour la gestion des rounds dans un tournoi.'''

    def start_rounds(self, tournament, tournament_id, players_ids):
        '''Démarre les rounds d'un tournoi.'''

        selected_tournament = TournamentController.load_tournament_by_id(tournament_id)

        players = PlayerController.load_players_by_ids(players_ids)
        number_of_rounds = selected_tournament.number_of_tours
        print("\nce tournoi a ", number_of_rounds, " rounds")

        selected_tournament.Tournament.start_tournament(tournament)

        for round_number in range(1, number_of_rounds + 1):
            round_name = f"Round {round_number}"
            new_round = Round(round_name)
            new_round.start_round()
            print(f"debut du round : {round_number}")
            if round_number == 1:
                new_round.create_random_pairs(players)
            else:
                sorted_players = self.calculate_points_for_tournament(tournament_id)
                previous_results = self.get_previous_results(
                    tournament_id, round_number
                )
                pairs, _ = new_round.generate_pairs_for_next_round(
                    players, previous_results, sorted_players
                )
                print("\nprochain Match pour le round en cours :\n")
                for pair in pairs:
                    player1 = f"{pair['player1']['last_name']} {pair['player1']['first_name']}"
                    player2 = f"{pair['player2']['last_name']} {pair['player2']['first_name']}"
                    print(f"Match : {player1} vs {player2}")
            selected_tournament.add_tour_to_list(new_round)
            MatchController.play_match(new_round)
            new_round.end_round()
            TournamentController.update_tournament(
                tournament_id, {"list_of_tours": selected_tournament.list_of_tours}
            )
            if round_number < number_of_rounds:
                user_choice = input("Continuez a entrer les resultats O/N : ")
                if user_choice.lower() == "n":
                    break
            else:
                self.calculate_points_for_tournament_final(tournament_id)
                selected_tournament.end_tournament(tournament_id)

    def get_previous_results(self, tournament_id, round_number):
        '''Récupère les résultats des rounds précédents.'''
        previous_results = []
        selected_tournament = TournamentController.load_tournament_by_id(tournament_id)
        reversed_rounds = reversed(selected_tournament.list_of_tours)

        for round_data in reversed_rounds:
            current_round_number = round_data.get("round_number", 0)
            if current_round_number < round_number and round_data.get("matches"):
                previous_results.extend(round_data["matches"])
                break
        return previous_results

    def update_matches_in_round(self, round_number, tournament_id, updated_matches):
        selected_tournament = TournamentController.load_tournament_by_id(tournament_id)

        round_to_update = selected_tournament.get_round_by_number(round_number)
        if round_to_update:

            round_to_update.update_matches(updated_matches)

            TournamentController.update_tournament(
                tournament_id, {"list_of_tours": selected_tournament.list_of_tours}
            )

    def calculate_points_for_tournament(self, tournament_id):
        tournament = TournamentController.load_tournament_by_id(tournament_id)
        if not tournament:
            print(f"Tournament with ID {tournament_id} not found.")
            return
        player_points = {}
        for round_data in tournament.list_of_tours:
            for match_data in round_data.get("matches", []):
                for player_id, score in match_data:
                    self.update_player_points(player_points, player_id, score)
        sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
        return sorted_players

    def update_player_points(self, player_points, player_id, score):
        player_points.setdefault(player_id, 0)
        player_points[player_id] += score

    def resume_rounds(self, tournament_id, players_ids):
        '''Reprendre l'entrée des résultats pour les rounds d'un tournoi.'''

        selected_tournament = TournamentController.load_tournament_by_id(tournament_id)
        players = PlayerController.load_players_by_ids(players_ids)
        number_of_rounds = selected_tournament.number_of_tours

        round_number = [
            int(re.search(r"Round (\d+)", tour["round_name"]).group(1))
            for tour in selected_tournament.list_of_tours
        ]
        if round_number:
            dernier_numero_round = max(round_number)
            print("le dernier round est le : ", dernier_numero_round, "\n")
        for round_number in range(dernier_numero_round + 1, number_of_rounds + 1):
            round_name = f"Round {round_number}"
            new_round = Round(round_name)
            new_round.start_round()
            print(f"debut du round : {round_number}\n")
            if round_number == 1:
                new_round.create_random_pairs(players)
            else:
                sorted_players = self.calculate_points_for_tournament(tournament_id)
                previous_results = self.get_previous_results(
                    tournament_id, round_number
                )
                pairs, _ = new_round.generate_pairs_for_next_round(
                    players, previous_results, sorted_players
                )
                print("\nprochain Match pour le round en cours :\n")
                for pair in pairs:
                    player1 = f"{pair['player1']['last_name']} {pair['player1']['first_name']}"
                    player2 = f"{pair['player2']['last_name']} {pair['player2']['first_name']}"
                    print(f"Match : {player1} vs {player2}")
            selected_tournament.add_tour_to_list(new_round)
            MatchController.play_match(new_round)
            # Mets à jour le tournoi avec les nouvelles valeurs

            new_round.end_round()
            TournamentController.update_tournament(
                tournament_id, {"list_of_tours": selected_tournament.list_of_tours}
            )
            if round_number < number_of_rounds:
                user_choice = input("Continuez a entrer les resultats O/N : ")
                if user_choice.lower() == "n":
                    break
            else:
                break
        if not (user_choice.lower()) == "n":
            self.calculate_points_for_tournament_final(tournament_id)
            selected_tournament.end_tournament(tournament_id)

    def calculate_points_for_tournament_final(self, tournament_id):
        tournament = TournamentController.load_tournament_by_id(tournament_id)
        if not tournament:
            print(f"Tournament with ID {tournament_id} not found.")
            return
        player_points = {}
        new_tournament_score = 0
        score = 0
        for round_data in tournament.list_of_tours:
            for match_data in round_data.get("matches", []):
                for player_id, score in match_data:
                    player_points.setdefault(player_id, 0)
                    player_points[player_id] += score

                    player = PlayerController.get_player_by_id(player_id)
                    if player:
                        new_tournament_score = score
                        player.update_score_tournament(player_id, new_tournament_score)
                    else:
                        print(f"Joueur avec l'ID {player_id} non trouvé.")
        sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
        print("Classement Final du Tournoi :\n")
        for player_id, points in sorted_players:
            player = PlayerController.get_player_by_id(player_id)
            if player:
                print(f"{player.first_name} {player.last_name}: {points} points")
            else:
                print(f"Player with ID {player_id} not found.")
        print()
        return sorted_players
