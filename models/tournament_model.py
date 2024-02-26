'''Define the Tournament.'''
import json
import os

from models.round_model import RoundModel


class Tournament:

    def __init__(
        self, name="", location="", date_of_begin="",
        number_of_round="", description="", number_of_player="",
        list_of_round=None, players=None, tournament_ID=None,
    ):
        '''Initialise une instance de tournoi'''
        self.name = name
        self.location = location
        self.date_of_begin = date_of_begin
        self.number_of_round = number_of_round
        self.description = description
        self.number_of_player = number_of_player
        self.players = players if players is not None else []
        self.list_of_round = list_of_round if list_of_round is not None else []
        self.tournament_ID = tournament_ID

    @staticmethod
    def load_tournament_by_id(tournament_ID, file_path):
        '''Permet de charger les informations d'un tournoi via son ID'''
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

    def add_round(self, round):
        '''Ajoute un round à la liste des rounds du tournoi'''
        self.list_of_round.append(round)

    def update_tournament(tournament_ID, updated_values):
        '''Permet de mettre à jour le Tournoi dans le json'''
        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path, "r") as file:
            tournaments = json.load(file)

        for index, tournament in enumerate(tournaments):
            if tournament.get("Tournoi_ID") == tournament_ID:
                # Crée un nouveau dictionnaire pour le tournoi mis à jour
                updated_tournament = dict(tournament)

                # Ajout des valeurs mises à jour
                updated_tournament.update(updated_values)

                # Converti les instances de Round en dictionnaires
                updated_tournament["Liste_des_rounds"] = [
                    round_model.to_dict() if isinstance(round_model, RoundModel) else round_model
                    for round_model in updated_tournament["Liste_des_rounds"]
                ]

                # On remplace le tournoi mis à jour dans le JSON correspondant
                tournaments[index] = updated_tournament
                with open(file_path, "w") as file:
                    json.dump(tournaments, file, ensure_ascii=False, indent=4)

    @classmethod
    def from_dict(cls, tournament_data):
        '''Permet de créer une instance de tournoi depuis un dictionnaire'''
        if isinstance(tournament_data, dict):  # Vérifie si c'est un dictionnaire
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

            # Crée un dictionnaire imbriqué pour les informations des joueurs
            if "Liste_joueurs_inscrits" in tournament_data:
                players_data = tournament_data["Liste_joueurs_inscrits"]
                renamed_tournament_data["players"] = [
                    {
                        "Player_ID": player.get("Player_ID"),
                        "Score_tournament": player.get("Score_tournament", 0),
                    }
                    for player in players_data
                ]

            return cls(**renamed_tournament_data)
        elif isinstance(tournament_data, list):  # Vérifie si c'est une liste
            return [cls.from_dict(item) for item in tournament_data]
        elif isinstance(tournament_data, Tournament):  # Vérifie si c'est une instance de la classe Tournament
            for item in tournament_data:
                return [cls.from_dict(item) for item in tournament_data]

    def to_dict(self):
        '''Converti l'objet Tournoi en dictionnaire'''
        list_of_rounds_data = []
        for round in self.list_of_round:
            if isinstance(round, RoundModel):  # Vérifie si c'est une instance de la classe Round
                round_data = {
                    "Nom_du_round": round.round_name,
                    "Date_de_debut": (
                        round.start_time.isoformat() if round.start_time else None
                    ),
                    "Date_de_fin": round.end_time.isoformat() if round.end_time else None,
                    "Matchs": [
                        (
                            [match.player1.get('Player_ID'), match.score1],
                            [match.player2.get('Player_ID'), match.score2],
                        )
                        for match in round.matches
                    ],
                }
                list_of_rounds_data.append(round_data)
            else:
                list_of_rounds_data.append(round)

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

    def get_selected_tournament_data(choice, tournaments, list_tournaments):
        if 1 <= choice <= len(list_tournaments):
            selected_tournament_index = choice - 1
            selected_tournament = list_tournaments[selected_tournament_index:selected_tournament_index + 2]
            selected_tournament = selected_tournament[0]
            target_tournoi_name = selected_tournament[0].get("Nom_du_tournoi")
            target_tournoi_index = None

            # Cherche l'index du tournoi cible dans la liste des tournois
            for i, tournament in enumerate(tournaments):
                for l_tournament in tournament:
                    if l_tournament.get("Nom_du_tournoi") == target_tournoi_name:
                        target_tournoi_index = i
                        break

            # Si l'index existe, l'index du tournoi suivant est "None"
            if target_tournoi_index is not None:
                next_tournoi_name = None
                next_tournoi_index = None

                # Cherche la prochaine occurence de "Nom_du_tournoi" qui vient après le tournoi cible
                # Récupère l'information du "Nom_du_tournoi" - Calcule son index
                for j, tournament in enumerate(tournaments[target_tournoi_index + 1:], start=target_tournoi_index + 1):
                    if tournament.get("Nom_du_tournoi"):
                        next_tournoi_name = tournament.get("Nom_du_tournoi")
                        next_tournoi_index = j
                        break

                if next_tournoi_name is not None:
                    tournament_data_list = tournaments[target_tournoi_index:next_tournoi_index]
                else:
                    tournament_data_list = tournaments

        return tournament_data_list
