"""Define the Round."""


class Round:
    def __init__(self, name_of_tournoi="", start_date="", end_date="",
                 round_number=0, couple_of_player=""):
        self.name_of_tournoi = name_of_tournoi
        self.start_date = start_date
        self.end_date = end_date
        self.round_number = round_number
        self.couple_of_player = couple_of_player
