'''Define the Tournament.'''
import json


class Tournament:

    def __init__(self, tournament_name="", tournament_location="", tournament_date_of_begin="",
                 number_of_round="", tournament_ID=None,
                 number_of_players="",
                 list_of_round=None, list_of_players=None,
                 tournament_description=""):

        self.tournament_name = tournament_name
        self.tournament_location = tournament_location
        self.tournament_date_of_begin = tournament_date_of_begin
        self.number_of_round = max(number_of_round, 4)  # Assure un minimum de 4 tours
        self.tournament_description = tournament_description
        self.number_of_players = number_of_players
        self.list_of_players = list_of_players if list_of_players is not None else []
        self.list_of_round = list_of_round if list_of_round is not None else []
        self.tournament_ID = tournament_ID

    def load_data(self, file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self, file_path, data):
        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_round_to_list(self, round):
        '''Ajoute un round à la liste des rounds du tournoi'''
        self.list_of_round.append(round)

    def load_tournament_by_id(cls, tournament_ID):
        '''Charger un tournoi grâce à son ID'''
        tournaments = cls.load_data()
        for tournament in tournaments:
            if tournament.tournament_ID == tournament_ID:
                return tournament
        return None

    def update_tournament(tournament_ID, updated_values):
        ''' Mise à jour des données d'un tournoi à partir de son ID'''
        tournaments = Tournament.load_data()
        for tournament in tournaments:
            if tournament.tournament_ID == tournament_ID:
                for key, value in updated_values.items():
                    setattr(tournament, key, value)

        Tournament.save_data(tournaments)

    def get_round_by_number(self, round_number):
        '''Trouve un Round grâce à son numéro'''
        for i, round_data in enumerate(self.list_of_round):
            if round_data.get("round_name") == f"Round {round_number}" and i > 0:
                return self.list_of_round[i - 1]
        return None
