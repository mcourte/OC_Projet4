"""Define the Round."""
import random
import datetime

from models.match_model import Match
from models.player_model import Player


class RoundModel:
    def __init__(self, round_name, start_time=None, end_time=None):
        """Initialise une instance de Round avec un nom, une heure de début et une heure de fin optionnelles."""
        self.round_name = round_name
        self.start_time = start_time or datetime.datetime.now()
        self.end_time = end_time
        self.matches = []
        self.players = []

    def get_players(self):
        return self.players

    def start_round_model(self):
        self.start_date = datetime.datetime.today().strftime("%d/%m/%Y")

    def end_round(self):
        self.end_date = datetime.datetime.today().strftime("%d/%m/%Y")

    def create_pairs_round_one(self, list_player_ID):
        random.shuffle(list_player_ID)

        pairings = [(list_player_ID[i], list_player_ID[i + 1]) for i in range(0, len(list_player_ID), 2)]

        for pair in pairings:
            player1 = pair[0]
            player2 = pair[1]

            player1_info = {
                "Name": player1.get("Name"),
                "Surname": player1.get("Surname"),
                "Date_of_birth": player1.get("Date_of_birth"),
                "Player_ID": player1.get("Player_ID"),
                "Score_tournament": player1.get("Score_tournament")
            }

            player2_info = {
                "Name": player2.get("Name"),
                "Surname": player2.get("Surname"),
                "Date_of_birth": player2.get("Date_of_birth"),
                "Player_ID": player2.get("Player_ID"),
                "Score_tournament": player2.get("Score_tournament")
            }

            match = Match(player1_info, player2_info)
            self.matches.append(match)

        return pairings

    def create_pairs_new_round_2(self, pairing_data, list_player_ID):
        random.shuffle(list_player_ID)
        print(list_player_ID)
        # Create pairs while avoiding players who have already played against each other
        pairings = []
        for i in range(0, len(list_player_ID), 2):
            player1 = list_player_ID[i]
            player2 = list_player_ID[i + 1]

            # Check if players have already played against each other
            while (player1, player2) in pairing_data or (player2, player1) in pairing_data:
                # Reshuffle and try again
                random.shuffle(list_player_ID)
                player1 = list_player_ID[i]
                player2 = list_player_ID[i + 1]

            pairings.append((player1, player2))

        return pairings

    def update_matches(self, updated_matches):
        '''Met à jour les matchs du round avec de nouvelles valeurs.'''
        for match_index, match in enumerate(self.matches):
            # Mets à jour les valeurs du match
            if match_index < len(updated_matches):
                match_data = updated_matches[match_index]
                for key, value in match_data.items():
                    setattr(match, key, value)

    def to_dict(self):
        return {
            "round_name": self.round_name,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "matches": [
                {
                    "player1": Player.get_player_info(match.player1),
                    "player2": Player.get_player_info(match.player2),
                    "score1": match.score1 if match.score1 is not None else 0,
                    "score2": match.score2 if match.score2 is not None else 0,
                }
                for match in self.matches
            ],
        }

    @classmethod
    def from_dict(cls, round_data, players):
        """Crée une instance de Round à partir d'un dictionnaire."""
        round_name = round_data["round_name"]
        start_time = (
            datetime.datetime.fromisoformat(round_data["start_time"])
            if round_data["start_time"]
            else None
        )
        end_time = (
            datetime.datetime.fromisoformat(round_data["end_time"])
            if round_data["end_time"]
            else None
        )
        new_round = cls(round_name, start_time, end_time)

        matches_data = round_data.get("matches", [])
        for match_data in matches_data:
            if len(match_data) == 2:
                player1_data, player2_data = match_data
                player1_ID, score1 = player1_data
                player2_ID, score2 = player2_data
                # Recherchez les joueurs

                player1 = next(
                    (player for player in players if player.player_ID == player1_ID),
                    None,
                )
                player2 = next(
                    (player for player in players if player.player_ID == player2_ID),
                    None,
                )
                if player1 and player2:
                    new_round.matches.append(Match(player1, player2, score1, score2))
                else:
                    print(
                        f"Erreur : Impossible de trouver les joueurs pour le match {match_data}"
                    )
            else:
                print("Format invalide pour un match :", match_data)
        return new_round

    @staticmethod
    def get_player_info_match(player1, player2):
        from models.player_model import Player
        # Your implementation to retrieve and return player information
        player1_info = Player.get_player_info(player1)
        player2_info = Player.get_player_info(player2)
        return player1_info, player2_info

    def create_pairs_new_round(self, players, previous_results, sorted_players):
        """Génère des paires pour le prochain tour en fonction des résultats précédents et du classement
        des joueurs."""
        print("Classement des joueurs :\n")
        pairs = []

        def custom_sort(player_info):
            # Fonction de comparaison personnalisée pour le tri des joueurs

            _, score, player = player_info
            return (-score, player.surname, player.name)

        # Chargez les informations complètes des joueurs pour trier par nom et prénom

        sorted_players_info = [
            (player_ID, score, Player.get_player_ID(player_ID))
            for player_ID, score in sorted_players
        ]
        print(sorted_players_info)
        sorted_players_info = sorted(sorted_players_info, key=custom_sort)
        for player_ID, points, player in sorted_players_info:
            print(
                f"{player.surname} {player.name} {player.player_ID}: {points} points"
            )
        # Utilisé pour suivre les joueurs déjà appariés dans ce round

        print()
        paired_players = set()
        players_set = set()
        # Iteration sur chaque paire dans previous_results

        for pair in previous_results:
            # Extraction des identifiants des joueurs de la paire actuelle

            current_pair_ids = frozenset([player[0] for player in pair])
            # Ajout des identifiants à l'ensemble

            players_set.add(current_pair_ids)
        # Utilisé pour suivre les paires déjà utilisées

        used_pairs = set()

        # Les deux premiers joueurs du classement

        i = 0
        while i < len(sorted_players_info) - 1:
            player_id, points, player = sorted_players_info[i]
            # Vérifiez si le joueur a déjà été apparié

            if player_id not in paired_players:
                # Cherchez le joueur suivant disponible

                j = i + 1
                while j < len(sorted_players_info):
                    next_player_id, next_points, next_player = sorted_players_info[j]
                    next_pair = frozenset([player_id, next_player_id])
                    # Vérifie si la paire a déjà été utilisée ou si elle a été jouée au tour précédent

                    if not any(
                        next_pair == prev_pair
                        or next_pair in used_pairs
                        or prev_pair in used_pairs
                        for prev_pair in players_set
                    ):
                        # Ajoute les joueurs à la paire et les suivre dans l'ensemble

                        pairs.append(
                            {
                                "player1": player.to_dict(),
                                "player2": next_player.to_dict(),
                            }
                        )
                        paired_players.add(player_id)
                        paired_players.add(next_player_id)
                        # Ajoute la paire à l'ensemble des paires utilisées

                        used_pairs.add(next_pair)
                        # Ajoute la paire à la liste des matchs

                        match = Match(player, next_player)
                        self.matches.append(match)
                        # Supprime les joueurs appariés de la liste sorted_players_info

                        sorted_players_info = [
                            p
                            for p in sorted_players_info
                            if p[0] not in (player_id, next_player_id)
                        ]
                        i = (
                            -1
                        )  # reprends a zero dans la list sorted_players_info vue que les index on changer
                        # Sort de la boucle interne une fois la paire validée

                        break
                    # Incrémente l'indice pour passer au joueur suivant

                    j += 1
                # Assure que la boucle ne continue pas indéfiniment

                i += 1
        # Ajoute la dernière paire manquante avec les joueurs restants

        if len(sorted_players_info) == 2:
            player1_id, points1, player1 = sorted_players_info[0]
            player2_id, points2, player2 = sorted_players_info[1]
            remaining_pair = frozenset([player1_id, player2_id])
            # Ajoute les joueurs à la paire et les suit dans l'ensemble

            pairs.append({"player1": player1.to_dict(), "player2": player2.to_dict()})
            # Ajoute la paire à l'ensemble des paires utilisées

            used_pairs.add(remaining_pair)
            # Ajoute la paire à la liste des matchs

            match = Match(player1, player2)
            self.matches.append(match)
        return pairs, self.matches
