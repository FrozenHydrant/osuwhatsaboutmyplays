import json
import os
from dotenv import load_dotenv
from flask import Flask
import threading
import sys

# Load own packages
sys.path.insert(1, os.getcwd())
from data_collect import DataCollect

# Load env variables
load_dotenv()

data_collect = DataCollect()
app = Flask(__name__)

@app.route("/")
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

    if best_pp_data is None:
        return "No data to show right now"
    
    return best_pp_data.to_json()

# App run for testing
if __name__ == "__main__":
    app.run()

    # Terminate it now
    print("Deactivating")
    data_collect.ACTIVE = False
