from models.match_model import Match


class MatchController:
    def __init__(self):
        '''Contrôleur pour gérer les matchs.'''
        pass

    @staticmethod
    def play_match(round, player1, player2):
        '''Permet à l'utilisateur de rentrer les scores d'un match'''
        # Créer un objet Match
        match = Match(player1, player2)

        print("\nProchain match: ")

        # Affiche les informations des joueurs du match
        print(
            f"{match.player1.get('Surname')} {match.player1.get('Name')} VS "
            f"{match.player2.get('Surname')} {match.player2.get('Name')}\n"
        )

        # Saisie des scores par les utilisateurs
        while True:

            try:
                score1 = float(input(
                    f"Score de {match.player1.get('Surname')} {match.player1.get('Name')}: "
                ))
                if score1 not in [0, 0.5, 1]:
                    print("\n Veuillez entrer un score valide: 0, 0.5 ou 1")
                    continue

                score2 = float(input(
                    f"Score de {match.player2.get('Surname')} {match.player2.get('Name')}: "
                ))
                if score2 not in [0, 0.5, 1]:
                    print("\n Veuillez entrer un score valide: 0, 0.5 ou 1")
                    continue
                # Condition qui vérifié que le score du joueur 1 est différent de celui
                # du joueur 2 quand score = 1 ou 0
                if (score1 == 1 and score2 == 1) or (score1 == 0 and score2 == 0):
                    print("\nLes scores ne peuvent pas être tous les deux 1 ou tous les deux 0. Veuillez réessayer.\n")
                    continue
                # Mettre à jour les scores des joueurs
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
