"""Define the Tournament."""

import os

import datetime
import json


from models import tournament_model

class TournamentController:

    def __init__(self):
        pass

    def start_tournament(self):  
        # Opening JSON file
        f = open(os.path.join("data","players_data.json"))
        players = json.load(f)
        player1 = players[0]
        player2 = players[1]
        self.list_of_players = [player1,player2]
        date_of_begin = datetime.date.today()
        self.date_of_begin = date_of_begin.strftime("%d-%m-%Y") 
        self.tournament_data={
                        "Liste des joueurs inscrits: " : self.list_of_players,
                        "Date de début: " : self.date_of_begin,
                        }
        file_path=os.path.join("data","tournament_data.json")
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, create an empty list
            data = []
        except json.JSONDecodeError:
            # If the file is empty or contains invalid JSON, initialize data as an empty list
            data = []
        data.extend(self.tournament_data)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return self.tournament_data
    
    def end_tournament(self):
        with open(os.path.join("data","tournament_data.json"), "r") as f:
            data = json.load(f)
        date_of_end = datetime.date.today()
        self.date_of_end = date_of_end.strftime("%d-%m-%Y")
        tournament_end={"Date de fin: " : self.date_of_end}
        self.tournament_data.update(tournament_end)
        temp = json.dumps(self.tournament_data, indent=2,ensure_ascii=False )
        with open(os.path.join("data","tournament_data.json"),  "a", encoding="utf-8") as f:
            f.write(temp)


tournament1=tournament_model.Tournament()
tournament1=TournamentController()
tournament1.start_tournament()


# Step 1: Read the existing JSON data from the file
file_path = 'data.json'

# Check if the JSON file exists
try:
    with open(file_path, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    # If the file doesn't exist, create an empty list
    data = []
except json.JSONDecodeError:
    # If the file is empty or contains invalid JSON, initialize data as an empty list
    data = []

# Step 2: Modify the data (add new data without removing existing data)
new_entries = [
    {
        'name': 'Magali',
        'age': 25,
        'city': 'France'
    },
    {
        'name': 'Jane Smith',
        'age': 25,
        'city': 'Los Angeles'
    },
    {
        'name': 'Addi',
        'age': 32,
        'city': 'Sweden'
    }
]

data.extend(new_entries)

# Step 3: Write the updated data back to the JSON file
with open(file_path, 'w') as file:
    json.dump(data, file, indent=4)

print(f"New data added to {file_path} without removing existing data.")
