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
                "players": tournament_data.get("Liste_joueurs_inscrits"),
                "tournament_ID": tournament_data.get("Tournoi_ID"),
            }
            return cls(**renamed_tournament_data)

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
                    "end_time": tour.end_time.isoformat() if tour.end_time else None,
                    "matches": [
                        (
                            [match.player1.player_ID, match.score1],
                            [match.player2.player_ID, match.score2],
                        )
                        for match in tour.matches
                    ],
                }
                list_of_rounds_data.append(tour_data)
            else:
                # Sinon, ajoutez simplement le tour à la liste

                list_of_rounds_data.append(tour)
        return {
            "Nom_du_tournoi": self.name,
            "Lieu": self.location,
            "Date_de_debut": self.date_of_begin,
            "Nombre_de_round": self.number_of_round,
            "Description": self.description,
            "Nombre_joueurs_inscrits": self.number_of_player,
            "Joueurs": self.players,
            "Liste_des_rounds": list_of_rounds_data
        }

    def add_round(self, round):
        '''Ajoute un round à la liste des rounds du tournoi'''
        self.list_of_round.append(round)

    def update_tournament(tournament_ID, updated_values):
        ''' Mise à jour des données d'un tournoi à partir de son ID'''
        file_path = os.path.join("data", "tournament_pending.json")

        with open(file_path, "r") as file:
            tournaments = json.load(file)

        for tournament in tournaments:
            if isinstance(tournament, dict):
                tournament_ID_data = tournament.get("Tournoi_ID")
                if tournament_ID_data == tournament_ID:
                    tournament.update(updated_values)
                    tournament = Tournament().to_dict()
                    tournaments.append([tournament])
                    print(type(tournaments))
                    with open(file_path, "a") as file:
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
