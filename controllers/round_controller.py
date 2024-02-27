import os
from colorama import Style

from models.round_model import RoundModel
from models.player_model import Player
from models.tournament_model import Tournament
from controllers.match_controller import MatchController


class RoundController:
    def __init__(self):
        '''Contrôleur pour gérer les rounds.'''
        self.player_points = {}

    def calculate_points_for_tournament_final(self, tournament_ID):
        '''Permet de calculer le score de chaque joueur lorsque le tournoi est terminé.'''
        # Charger le tournoi spécifique
        file_path = os.path.join("data", "tournament_pending.json")
        tournament = Tournament.load_tournament_by_id(tournament_ID, file_path)
        if not tournament:
            print(f"Tournament with ID {tournament_ID} not found.")
            return
        # Remise à zéro des points des joueurs avant calcul
        self.player_points = {}

        list_of_round = tournament.list_of_round
        for round_data in list_of_round:
            for match_data in round_data.get("Matchs"):
                player1_ID = match_data[0][0]
                player1_score = int(match_data[0][1])

                player2_ID = match_data[1][0]
                player2_score = int(match_data[1][1])

                self.update_player_points(player1_ID, player1_score)
                self.update_player_points(player2_ID, player2_score)

        sorted_players = sorted(self.player_points.items(), key=lambda x: x[1], reverse=True)
        print(f"{Style.BRIGHT}\nClassement Final du Tournoi :\n{Style.RESET_ALL}", end='', flush=True)
        for player_ID, points in sorted_players:
            player = Player.get_player_ID(player_ID)
            if player:
                print(f"{player.get('Name')} {player.get('Surname')}: {points} points")
            else:
                print(f"Player with ID {player_ID} not found.")

        return sorted_players

    def start_round(self, list_player_ID, tournament_ID, number_of_rounds, list_of_round):
        '''Permet de lancer le premier round d'un tournoi'''
        file_path = os.path.join("data", "tournament_data.json")
        selected_tournament = Tournament.load_tournament_by_id(tournament_ID, file_path)
        tournament_ID = selected_tournament.tournament_ID
        number_of_rounds = selected_tournament.number_of_round
        tournament_name = selected_tournament.name
        print(f"{Style.BRIGHT}\nBienvenue sur le tournoi: {tournament_name}\n", end='', flush=True)
        print("\nLe tournoi a", number_of_rounds, "rounds\n")

        for round_number in range(1, number_of_rounds + 1):
            round_name = f"Round {round_number}"
            new_round = RoundModel(round_name)
            new_round.start_round_model()
            print(f"{Style.BRIGHT}nDébut du round : {round_number}\n", end='', flush=True)

            if round_number == 1:
                list_pairs_one = new_round.create_pairs_round_one(list_player_ID)
                selected_tournament.add_round(new_round)
                print("\n Les matchs à venir pour le Round en cours sont les suivants :\n")
                for pair in list_pairs_one:
                    player1_ID = pair[0]
                    player2_ID = pair[1]
                    player1 = Player.get_player_ID(player1_ID)
                    player2 = Player.get_player_ID(player2_ID)
                    print(f"{player1.get('Surname')} {player1.get('Name')} contre {player2.get('Surname')}"
                          f" {player2.get('Name')}")
                    print(f"{Style.BRIGHT}\nAttention, il est impératif de remplir les scores de l'ensemble des "
                          f"matchs du round :\n", end='', flush=True)
                print("\nLe score d'un joueur peut être 0, 1 ou 0.5")
                # Joue les matchs pour le Round en cours

                for pair in list_pairs_one:
                    player1 = pair[0]
                    player2 = pair[1]
                    MatchController.play_match(new_round, player1, player2)

                # Termine le Round après que les matchs soient joués
                new_round.end_round()
                # Converti le Round en dictionnaire
                new_round.to_dict()

                # Mat à jour le tournoi avec toutes les informations du Round et des Matchs
                selected_tournament.to_dict()
                Tournament.create_tournament_pending(selected_tournament)
                if round_number < number_of_rounds:
                    user_choice = input("\n\nContinuez à entrer les resultats Oui/Non : ")
                    if user_choice.lower() == "oui":
                        round_controller = RoundController()
                        round_controller.resume_rounds(list_player_ID, tournament_ID,
                                                       round_number, number_of_rounds,
                                                       list_of_round, list_pairs_one)
                    else:
                        break
        return selected_tournament

    def resume_rounds(self, list_player_ID, tournament_ID, round_number,
                      number_of_rounds, list_of_round, list_pairs_one):
        '''Reprendre l'entrée des résultats pour les rounds d'un tournoi.'''
        file_path = os.path.join("data", "tournament_pending.json")
        selected_tournament = Tournament.load_tournament_by_id(tournament_ID, file_path)
        # Trouve le plus grand nombre de Round joué
        max_round_number = max(int(round_data.get("Nom_du_round").split(" ")[-1]) for round_data
                               in selected_tournament.list_of_round)
        # Le round suivant sera égal au max_round_number + 1
        next_round_number = max_round_number + 1

        tournament_name = selected_tournament.name
        print(f"{Style.BRIGHT}\nBienvenue sur le tournoi: {tournament_name}\n", end='', flush=True)
        round_number = next_round_number
        if (round_number <= number_of_rounds and
            f"Round {round_number}" not in [round_data.get('Nom')
                                            for round_data in selected_tournament.list_of_round]):
            round_name = f"Round {round_number}"
            new_round = RoundModel(round_name)
            new_round.start_round_model()

            print(f"\nDébut du round : {round_number}\n")

            print(f"{Style.BRIGHT}\nAttention, il est impératif de remplir les scores de l'ensemble des "
                  f"matchs du round :\n", end='', flush=True)
            previous_result = self.get_previous_results(tournament_ID, round_number)
            # Remise à 0 des points des joueurs au début de chaque round
            self.player_points = {}
            sorted_players = self.calculate_points_for_tournament(tournament_ID)
            list_pairs = new_round.create_pairs_new_round(list_pairs_one, previous_result, sorted_players)
            for pair in list_pairs:
                player1_ID = pair.get("player1")
                player2_ID = pair.get("player2")
                MatchController.play_match(new_round, player1_ID, player2_ID)

            # Termine le round après que les matchs soient joués
            new_round.end_round()

            # Converti le Round en dictionnaire
            new_round_dict = new_round.to_dict()

            # Mise à jour du tournoi
            selected_tournament.list_of_round.append(new_round_dict)
            Tournament.update_tournament(tournament_ID, {'Liste_des_rounds': selected_tournament.list_of_round})
            list_pairs_one = list_pairs

            if round_number < number_of_rounds:
                user_choice = input("\nContinuez a entrer les resultats Oui/Non : ")
                if user_choice.lower() == "oui":
                    self.resume_rounds(list_player_ID, tournament_ID,
                                       round_number, number_of_rounds,
                                       list_of_round, list_pairs)
            else:
                self.calculate_points_for_tournament_final(tournament_ID)
        else:
            self.calculate_points_for_tournament_final(tournament_ID)
            return
        return selected_tournament, list_pairs

    def calculate_points_for_tournament(self, tournament_ID):
        '''Permet de calculer les points des joueurs en cours de tournoi'''
        file_path = os.path.join("data", "tournament_pending.json")
        tournament = Tournament.load_tournament_by_id(tournament_ID, file_path)
        if not tournament:
            print(f"Tournament with ID {tournament_ID} not found.")
            return

        list_of_round = tournament.list_of_round
        for round_data in list_of_round:
            for match_data in round_data.get("Matchs"):
                player1_ID = match_data[0][0]
                player1_score = match_data[0][1]
                player2_ID = match_data[1][0]
                player2_score = match_data[1][1]
                self.update_player_points(player1_ID, player1_score)
                self.update_player_points(player2_ID, player2_score)

            # Save the results of the current round

        sorted_players = sorted(self.player_points.items(), key=lambda x: x[1], reverse=True)
        return sorted_players

    def get_previous_results(self, tournament_ID, round_number):
        '''Récupère les résultats des rounds précédents.'''

        previous_results = []
        # Charge les données du tournoi depuis le fichier JSON
        file_path = os.path.join("data", "tournament_pending.json")
        selected_tournament = Tournament.load_tournament_by_id(tournament_ID, file_path)
        # Renverse la liste des tours pour parcourir du dernier au premier
        list_of_round = selected_tournament.list_of_round
        reversed_rounds = reversed(list_of_round)
        # Parcourt les rounds précédents et récupère les résultats des matchs
        for round_data in reversed_rounds:
            round_name = round_data.get("Nom_du_round")
            current_round_number = int(round_name[-1])
            if current_round_number < round_number and round_data.get("Matchs"):
                previous_results.extend(round_data["Matchs"])
                break
        return previous_results

    def update_player_points(self, player_ID, score):
        '''Permet de mettre à jour les point des Joueurs'''
        self.player_points[player_ID] = self.player_points.get(player_ID, 0) + int(score)
