import json
import os

# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# File paths
json1_path = os.path.join("data", "tournament_data.json")
json2_path = os.path.join("data", "tournament_pending.json")
json3_path = os.path.join("data", "tournament_closed.json")

# Load JSON data from files
data1 = load_json(json1_path)
data2 = load_json(json2_path)
data3 = load_json(json3_path)

# Combine dictionaries not in tournament_pending and tournament_closed
not_in_pending = [item for item in data1 if item not in data2]
not_in_closed = [item for item in data1 if item not in data3]
data = [not_in_closed + not_in_pending]

# Function to create a new dictionary at each occurrence of "Nom_du_tournoi"
def create_tournament_dict(data):
    result = []
    current_tournament = None

    for item in data:
        if "Nom_du_tournoi" in item:
            # If a new tournament is found, append the previous one to the result list
            if current_tournament is not None:
                result.append(current_tournament)
            # Start a new dictionary for the current tournament
            current_tournament = {"Nom_du_tournoi": item["Nom_du_tournoi"]}
        elif current_tournament is not None:
            # If a tournament is in progress, add the current item to it
            current_tournament.update(item)

    # Append the last tournament after the loop
    if current_tournament is not None:
        result.append(current_tournament)

    return result

# Create new dictionaries at each occurrence of "Nom_du_tournoi"
result = create_tournament_dict(not_in_pending + not_in_closed)

# Print or process the results
for tournament_dict in result:
    print(f"{tournament_dict} + \n")