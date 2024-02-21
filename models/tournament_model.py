'''Define the Tournament.'''
from typing import List

import json
import os

from models.round_model import RoundModel


class Tournament:

    def __init__(
        self, name="", location="", date_of_begin="",
        number_of_round="", description="", number_of_player="",
        list_of_round=None, players=None, tournament_ID=None,
    ):
        """Initialize a Tournament instance."""
        self.name = name
        self.location = location
        self.date_of_begin = date_of_begin
        self.number_of_round = number_of_round
        self.description = description
        self.number_of_player = number_of_player
        self.players = players if players is not None else []
        self.list_of_round = list_of_round if list_of_round is not None else []
        self.tournament_ID = tournament_ID

    def load_data(file_path) -> List["Tournament"]:
        """Load tournament data from a file."""
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                return [
                    Tournament.from_dict(tournament_data) for tournament_data in data
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @classmethod
    def from_dict(cls, tournament_data):
        """Create an instance of Tournament from a dictionary."""
        if isinstance(tournament_data, dict):  # Check if it's a dictionary
            renamed_tournament_data = {
                "name": tournament_data.get("Nom_du_tournoi"),
                "location": tournament_data.get("Lieu"),
                "date_of_begin": tournament_data.get("Date_de_debut"),
                "number_of_round": tournament_data.get("Nombre_de_round"),
                "description": tournament_data.get("Description"),
                "number_of_player": tournament_data.get("Nombre_joueurs_inscrits"),
                "list_of_round": tournament_data.get("Liste_des_rounds"),
                "players": [],
                "tournament_ID": tournament_data.get("Tournoi_ID"),
            }

            # Additional handling for nested structures
            if "Liste_joueurs_inscrits" in tournament_data:
                players_data = tournament_data["Liste_joueurs_inscrits"]
                renamed_tournament_data["players"] = [
                    {
                        "Surname": player.get("Surname"),
                        "Name": player.get("Name"),
                        "Date_of_birth": player.get("Date_of_birth"),
                        "Player_ID": player.get("Player_ID"),
                        "Score_tournament": player.get("Score_tournament", 0),
                    }
                    for player in players_data
                ]

            return cls(**renamed_tournament_data)
        elif isinstance(tournament_data, list):  # Check if it's a list
            return [cls.from_dict(item) for item in tournament_data]
        elif isinstance(tournament_data, Tournament):
            for item in tournament_data:
                return [cls.from_dict(item) for item in tournament_data]

    def to_dict(self):
        """Convert the Tournament object to a dictionary."""
        list_of_rounds_data = []
        for tour in self.list_of_round:
            if isinstance(tour, RoundModel):
                # Si le tour est une instance de la classe Round
                tour_data = {
                    "round_name": tour.round_name,
                    "start_time": (
                        tour.start_time.isoformat() if tour.start_time else None
                    ),
                    "end_time": tour.end_time,
                    "matches": [
                        (
                            [match.player1.get('Player_ID'), match.score1],
                            [match.player2.get('Player_ID'), match.score2],
                        )
                        for match in tour.matches
                    ],
                }
                print(tour_data)
                list_of_rounds_data.append(tour_data)
            else:
                # Sinon, ajoutez simplement le tour à la liste

                list_of_rounds_data.append(tour)
            tournament_dict = {
                "Nom_du_tournoi": self.name,
                "Lieu": self.location,
                "Date_de_debut": self.date_of_begin,
                "Nombre_de_round": self.number_of_round,
                "Description": self.description,
                "Nombre_joueurs_inscrits": self.number_of_player,
                "Joueurs": self.players,
                "Liste_des_rounds": list_of_rounds_data
            }
        return tournament_dict

    def add_round(self, round):
        '''Ajoute un round à la liste des rounds du tournoi'''
        self.list_of_round.append(round)

    def update_tournament(tournament_ID, updated_values):
        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path, "r") as file:
            tournaments = json.load(file)

        for index, tournament in enumerate(tournaments):
            if tournament.get("Tournoi_ID") == tournament_ID:
                # Create a new dictionary for the updated tournament
                updated_tournament = dict(tournament)

                # Update tournament values
                updated_tournament.update(updated_values)

                # Convert RoundModel instances to dictionaries
                updated_tournament["Liste_des_rounds"] = [
                    round_model.to_dict() if isinstance(round_model, RoundModel) else round_model
                    for round_model in updated_tournament["Liste_des_rounds"]
                ]

                # Replace the original tournament in the list with the updated dictionary
                tournaments[index] = updated_tournament
                with open(file_path, "w") as file:
                    json.dump(tournaments, file, ensure_ascii=False, indent=4)

    @staticmethod
    def load_tournament_by_id(tournament_ID, file_path):
        """Load tournament data by ID from a file."""
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                for tournament_data in data:
                    if isinstance(tournament_data, dict):
                        if tournament_data.get("Tournoi_ID") == tournament_ID:
                            return Tournament.from_dict(tournament_data)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        return None

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

    def get_round_by_number(self, round_number):
        """Retrieve a specific round by its number."""
        for i, round_data in enumerate(self.list_of_round):
            if round_data.get("round_name") == f"Round {round_number}" and i > 0:
                return self.list_of_round[
                    i - 1
                ]  # Utilisez get() pour éviter le KeyError
        print(
            f"Debug: Round {round_number} not found in the list of tournament rounds."
        )
        return None
