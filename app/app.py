import json
import os
from dotenv import load_dotenv
from flask import Flask
from data_collect import DataCollect
import threading

# Load env variables
load_dotenv()

my_app = Flask(__name__)
data_collect = DataCollect()

@my_app.route("/")
def hello_page():
    ans = ""
    best_pp = -1
    best_pp_data = None
    for df in data_collect.DATA:
        if len(df) > 0:
            t_best_pp = df.max().loc["pp"]
            if t_best_pp > best_pp:
        
                # Update the info
                best_pp_data = df.loc[df["pp"] == t_best_pp]
                best_pp = t_best_pp

    return best_pp_data.to_json()

#my_app.run()

# Terminate it now
print("Deactivating")
data_collect.ACTIVE = False
