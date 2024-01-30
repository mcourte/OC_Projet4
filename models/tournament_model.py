'''Define the Tournament.'''
import json


class Tournament:

    def __init__(self, name="", location="", date_of_begin="",
                 date_of_end="", number_of_round=4,
                 number_of_players="", round_number="",
                 list_of_round=None, list_of_players=None,
                 description=""):
        self.name = name
        self.location = location
        self.date_of_begin = date_of_begin
        self.date_of_end = date_of_end
        self.number_of_round = number_of_round
        self.round_number = round_number
        self.list_of_round = list_of_round
        self.list_of_players = list_of_players
        self.description = description
        self.number_of_players = number_of_players

    def load_data(self, file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self, file_path, data):
        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_tour_to_list(self, round):
        '''Ajoute un round à la liste des rounds du tournoi'''
        self.list_of_tours.append(round)

    def load_tournament_by_id(cls, tournament_id):
        '''Charger un tournoi grâce à son ID'''
        tournaments = cls.load_tournaments()
        for tournament in tournaments:
            if tournament.tournament_id == tournament_id:
                return tournament
        return None

    def update_tournament(tournament_id, updated_values):
        ''' Mise à jour des données d'un tournoi à partir de son ID'''
        tournaments = Tournament.load_tournaments()
        for tournament in tournaments:
            if tournament.tournament_id == tournament_id:
                for key, value in updated_values.items():
                    setattr(tournament, key, value)

        Tournament.save_data(tournaments)

    def get_round_by_number(self, round_number):
        '''Trouve un Round grâce à son numéro'''
        for i, round_data in enumerate(self.list_of_tours):
            if round_data.get("round_name") == f"Round {round_number}" and i > 0:
                return self.list_of_tours[i - 1]
        return None
