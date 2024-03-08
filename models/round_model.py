
import random
import datetime

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
        self.start_date = datetime.datetime.today().strftime("%d/%m/%Y")[0:10]

    def end_round(self):
        '''Permet d'ajouter la date de fin de round'''
        self.end_date = datetime.datetime.today().strftime("%d/%m/%Y")[0:10]

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

        pairings = []
        sorted_players_info = []
        paired_data = [(sorted_players[i], sorted_players[i + 1]) for i in range(0, len(sorted_players), 2)]
        result = [(player_ID, score) for pair in paired_data for player_ID, score in pair]

        def custom_sort(player_info):
            '''Permet de trier les joueurs par score'''
            _, score, player = player_info
            return (-score, player["Surname"], player["Name"])

        # Chargez les informations complètes des joueurs pour trier par nom et prénom
        sorted_players_info = [
            (player_ID, score, Player.get_player_ID(player_ID))
            for player_ID, score in result
        ]

        sorted_players_info = sorted(sorted_players_info, key=custom_sort)

        # On crée une copie de la liste de sorted_players_info avant de la trié
        shuffled_players = sorted_players_info.copy()
        random.shuffle(shuffled_players)
        list_test = shuffled_players

        for i in range(0, len(list_test), 2):
            player1_ID = list_test[i][0]
            player2_ID = list_test[i + 1][0]

            player1_info = Player.get_player_ID(player1_ID)
            player2_info = Player.get_player_ID(player2_ID)

            while self.has_played_before(player1_ID, player2_ID, pairing_data):
                # On retrie la liste et on réessaye
                random.shuffle(shuffled_players)
                player1_ID = shuffled_players[i][0]
                player2_ID = shuffled_players[i + 1][0]

                if player1_ID is None or player2_ID is None:
                    break

                player1_info = Player.get_player_ID(player1_ID)
                player2_info = Player.get_player_ID(player2_ID)

                if player1_info is None or player2_info is None:
                    break

            pairings.append({"player1": player1_ID, "player2": player2_ID})

        return pairings

    def to_dict(self):
        '''Permet de transformer un objet Round en dictionnaire'''
        match_data = []
        for match in self.matches:
            player1_info = Player.get_player_info(match.player1)
            player2_info = Player.get_player_info(match.player2)

            player1_ID = player1_info.get("Player_ID")
            player2_ID = player2_info.get("Player_ID")
            match_tuple = [
                            [player1_ID, match.score1 if match.score1 is not None else 0.0],
                            [player2_ID, match.score2 if match.score2 is not None else 0.0]
            ]

            match_data.append(match_tuple)

        return {
            "Nom_du_round": self.round_name,
            "Date_de_debut": self.start_time.isoformat() if self.start_time else None,
            "Date_de_fin": self.end_time.isoformat() if self.end_time else None,
            "Matchs": match_data
        }

    def has_played_before(self, player1_ID, player2_ID, previous_results):
        '''Permet de vérifier si les joueurs ont déjà joué l'un contre l'autre avant'''
        for result in previous_results:
            try:
                if (result['player1'] == player1_ID and result['player2'] == player2_ID) or \
                   (result['player1'] == player2_ID and result['player2'] == player1_ID):
                    return True
            except Exception:
                pass

        return False
