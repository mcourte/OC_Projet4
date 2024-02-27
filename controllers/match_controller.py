from models.match_model import Match
from models.player_model import Player


class MatchController:
    def __init__(self):
        '''Contrôleur pour gérer les matchs.'''
        pass

    @staticmethod
    def play_match(round, player1, player2):
        '''Permet à l'utilisateur de rentrer les scores d'un match'''
        player1_info = Player.get_player_ID(player1)
        player2_info = Player.get_player_ID(player2)
        # Check if player1 or player2 is None
        if player1 is None or player2 is None:
            print("Error: Player object is None.")
            return

        # Créer un objet Match
        match = Match(player1_info, player2_info)

        print("\nProchain match: ")

        # Check if player1 and player2 have the expected attributes
        if 'Surname' not in match.player1 or 'Name' not in match.player1 or \
           'Surname' not in match.player2 or 'Name' not in match.player2:
            print("Error: Player object does not have expected attributes.")
            return

        # Affiche les informations des joueurs du match
        print(
            f"{match.player1['Surname']} {match.player1['Name']} VS "
            f"{match.player2['Surname']} {match.player2['Name']}\n"
        )

        # Saisie des scores par les utilisateurs
        while True:
            try:
                score1 = float(input(
                    f"Score de {match.player1['Surname']} {match.player1['Name']}: "
                ))
                if score1 not in [0, 0.5, 1]:
                    print("\n Veuillez entrer un score valide: 0, 0.5 ou 1")
                    continue

                score2 = float(input(
                    f"Score de {match.player2['Surname']} {match.player2['Name']}: "
                ))
                if score2 not in [0, 0.5, 1]:
                    print("\n Veuillez entrer un score valide: 0, 0.5 ou 1")
                    continue

                if (score1 == 1 and score2 == 1) or (score1 == 0 and score2 == 0):
                    print("\nLes scores ne peuvent pas être tous les deux 1 ou tous les deux 0. Veuillez réessayer.\n")
                    continue

                player1 = Player.get_player_ID(player1)
                player2 = Player.get_player_ID(player2)
                match.score1 = score1
                match.score2 = score2
                player1["Score_tournament"] += match.score1
                player2["Score_tournament"] += match.score2

                break
            except ValueError:
                print("\nVeuillez entrer des chiffres valides pour les scores.")

        # Ajout du Match au Round en cours
        round.matches.append(match)

        return player1["Score_tournament"], player2["Score_tournament"]
