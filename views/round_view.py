"""Define the Tournament."""

import datetime
import json
import os



class RoundView:

    def __init__(self):
        pass

    def start_round_view(self):  
        file_path=os.path.join("data","tournament_data.json")
        with open(file_path, "r") as file:
            data=json.load(file)
        test2=list(data)[1]
        print(test2)
            
        
       

        

       
    
