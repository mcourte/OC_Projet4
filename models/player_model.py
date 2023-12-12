"""Define the Player."""


import string
import random


class Player:
    def __init__(self, score=0, name="", surname="", date_of_birth="", ID=""):
        self.name = name
        self.score = score
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.ID = ID

    def random_ID(self):
        ''' Cette fonction permet de générer aléatoirement des ID
        Elle sera supprimer une fois les tests finis'''
        nb_letters = 2
        nb_numbers = 5
        letters = ''.join((random.choice(string.ascii_uppercase))
                          for x in range(nb_letters))
        numbers = ''.join((random.choice(string.digits))
                          for x in range(nb_numbers))
        ID_list = list(letters + numbers)
        ID = ''.join(ID_list)
        return ID
