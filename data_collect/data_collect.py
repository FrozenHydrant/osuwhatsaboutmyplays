import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
import pandas as pd
import numpy as np
import threading

class DataCollect:
    #CONSTANTS
    SLOTS = 24 # One slot per hour = 1 day of data
    INSTANCE = None
    
    def __init__(self, osu_client):
        if DataCollect.INSTANCE is None:
            self.CLIENT = osu_client
            # 24 Boxes for hourly data
            self.DATA = []
            for i in range(DataCollect.SLOTS):
                self.DATA.append(pd.DataFrame(columns=["date", "id", "pp"]))

            # Start on a new thread
            self.ACTIVE = True
            self.DATA_THREAD = threading.Thread(target=self._start)
            self.DATA_THREAD.start()

            DataCollect.INSTANCE = self
        else:
            raise Exception("can't initialize another data collecting object")

    def _start(self):
        my_curse = None
        current_h = None
        data_pos = 0
        
        while True:
            osu_get_all_scores_result = self.CLIENT.get_all_scores("osu", cursor=my_curse)
            all_my_scores = osu_get_all_scores_result.scores
            my_curse = osu_get_all_scores_result.cursor            

            all_my_scores.sort(key=lambda score: score.ended_at) # Make sure scores in perfect order by time
            for score in all_my_scores:
                score_info = {}
                score_info["date"] = [score.ended_at]
                score_info["id"] = [score.id]
                score_info["pp"] = [score.pp]

                if current_h is None:
                    pass
                elif current_h != score.ended_at.hour:
                    # New hour = go to the next slot
                    # But wrap around if no space
                    data_pos += 1
                    data_pos %= self.SLOTS
                    #print(data_pos, "New data pos")
                    # Destroy the previous data we had
                    self.DATA[data_pos] = pd.DataFrame(columns=["date", "id", "pp"])
                    
                current_h = score.ended_at.hour

                # Add score info to the Data list
                # https://www.geeksforgeeks.org/pandas/how-to-add-one-row-in-an-existing-pandas-dataframe/
                new_row = pd.DataFrame(score_info)
                self.DATA[data_pos] = pd.concat([self.DATA[data_pos], new_row], ignore_index=True)
                            
            print("Documented new scores, now sleeping...")

            # "Busy wait for 60 seconds, but we need to exit if terminated"
            for i in range(60):
                time.sleep(1)
                if not self.ACTIVE:
                    return        

