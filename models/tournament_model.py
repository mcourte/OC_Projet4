'''Define the Tournament.'''
import json
import os
import datetime


class Tournament:

    def __init__(self, tournament_name="", tournament_location="", tournament_date_of_begin="",
                 number_of_round="", tournament_ID=None,
                 number_of_players="",
                 list_of_round=None, list_of_players=None,
                 tournament_description=""):

        self.tournament_name = tournament_name
        self.tournament_location = tournament_location
        self.tournament_date_of_begin = tournament_date_of_begin
        self.number_of_round = number_of_round
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

    def add_round(self, round):
        '''Ajoute un round à la liste des rounds du tournoi'''
        self.list_of_round.append(round)

    def update_tournament(tournament_ID, updated_values):
        ''' Mise à jour des données d'un tournoi à partir de son ID'''
        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path, "r") as file:
            tournaments = json.load(file)
        for tournament in tournaments:
            tournament_ID_data = tournament.get("Tournoi_ID")
            if tournament_ID_data == tournament_ID:
                for key, value in updated_values.items():
                    update_tournament = setattr(tournament, key, value)
                    with open(file_path, "a") as file:
                        json.dump(update_tournament, file, ensure_ascii=False, indent=4)

    def round_by_number(self, round_number):
        '''Trouve un Round grâce à son numéro'''
        for i, round_data in enumerate(self.list_of_round):
            if round_data.get("round_name") == f"Round {round_number}" and i > 0:
                return self.list_of_round[i - 1]
        return None

    def end_tournament_model(self):
        '''Permet de terminer un tournoi et de l'enregistrer dans le fichier tournament_closed'''
        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path, "r") as file:
            data = json.load(file)

        date_of_end = datetime.date.today()
        tournament_end = {"Date_de_fin": str(date_of_end)}
        data.append(tournament_end)

        with open(file_path, "w") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

        file_path2 = os.path.join("data", "tournament_closed.json")
        with open(file_path2, "a") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Le tournoi est clos")

    def close_tournament(self):
        '''Permet de lister les tournois terminés'''
        file_path = os.path.join("data", "tournament_closed.json")
        with open(file_path, "r") as file:
            data = json.load(file)

        close = {}
        list_close = []

        for i in range(len(data)):
            close.update(data[i])
            list_close.append(close)

        return list_close
