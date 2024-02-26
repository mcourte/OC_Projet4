
import random
import datetime

from models.match_model import Match
from models.player_model import Player


class RoundModel:
    def __init__(self, round_name, start_time=None, end_time=None, matches=None, players=None):
        '''Initialise une instance de Round'''
        self.round_name = round_name
        self.start_time = start_time or datetime.datetime.now()
        self.end_time = end_time or datetime.datetime.now()
        self.matches = []
        self.players = []

    def start_round_model(self):
        '''Permet d'ajouter la date de début de round'''
        self.start_date = datetime.datetime.today().strftime("%d/%m/%Y")

    def end_round(self):
        '''Permet d'ajouter la date de fin de round'''
        self.end_date = datetime.datetime.today().strftime("%d/%m/%Y")

    @staticmethod
    def get_player_info_match(player1, player2):
        '''Permet d'obtenir les informations sur les joueurs d'un match'''
        from models.player_model import Player
        player1_info = Player.get_player_info(player1)
        player2_info = Player.get_player_info(player2)
        return player1_info, player2_info

    def create_pairs_round_one(self, list_player_ID):
        '''Permet de générer une première liste de paires de joueurs aléatoires'''
        random.shuffle(list_player_ID)

        pairings = [(list_player_ID[i], list_player_ID[i + 1]) for i in range(0, len(list_player_ID), 2)]

        return pairings

    def create_pairs_new_round(self, pairing_data, previous_results, sorted_players):
        '''Génère des paires pour le prochain tour en fonction des résultats précédents et du classement
        des joueurs.'''
        print("Classement des joueurs :\n")
        pairings = []
        sorted_players_info = []
        paired_data = [(sorted_players[i], sorted_players[i + 1]) for i in range(0, len(sorted_players), 2)]
        result = [(player_ID, score) for pair in paired_data for player_ID, score in pair]

        def custom_sort(player_info):
            # Fonction de comparaison personnalisée pour le tri des joueurs

            _, score, player = player_info
            return (-score, player["Surname"], player["Name"])

        # Chargez les informations complètes des joueurs pour trier par nom et prénom

        sorted_players_info = [
            (player_ID, score, Player.get_player_ID(player_ID))
            for player_ID, score in result
        ]
        sorted_players_info = sorted(sorted_players_info, key=custom_sort)
        for player_ID, points, player in sorted_players_info:
            print(
                f"{player['Surname']} {player['Name']} {player['Player_ID']}: {points} points"
            )

        for i in range(0, len(sorted_players), 2):
            player1 = sorted_players[i]
            player2 = sorted_players[i + 1]

            # Check if players have already played against each other
            while (player1, player2) in pairing_data or (player2, player1) in pairing_data:
                # Reshuffle and try again
                random.shuffle(sorted_players)
                player1 = sorted_players[i]
                player2 = sorted_players[i + 1]

            pairings.append({"player1": player1, "player2": player2})
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
        '''Permet de transformer un objet Round en dictionnaire'''
        match_data = []
        for match in self.matches:
            player1_info = Player.get_player_info(match.player1)
            player2_info = Player.get_player_info(match.player2)

            player1_ID = player1_info.get("Player_ID")
            player2_ID = player2_info.get("Player_ID")
            match_dict = {
                "player1": player1_ID,
                "score1": match.score1 if match.score1 is not None else 0,
                "player2": player2_ID,
                "score2": match.score2 if match.score2 is not None else 0
            }
            match_data.append(match_dict)

        return {
            "Nom_du_round": self.round_name,
            "Date_de_debut": self.start_time.isoformat() if self.start_time else None,
            "Date_de_fin": self.end_time.isoformat() if self.end_time else None,
            "Matchs": match_data
        }

    @classmethod
    def from_dict(cls, round_data, players):
        '''Crée une instance de Round à partir d'un dictionnaire.'''
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
