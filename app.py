import json
import os
from osu import Client
from dotenv import load_dotenv
from flask import Flask
import threading
import sys
import pandas as pd
import numpy as np

# Load own packages
sys.path.insert(1, os.getcwd())
from data_collect import DataCollect
from colorfinity import Colorfinity

# Load env variables and create the Client
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_s = os.getenv("CLIENT_SECRET")
CLIENT = Client.from_credentials(client_id, client_s, "http://localhost:8080")
data_collect = DataCollect(CLIENT)
app = Flask(__name__)

def collect_data(name):
    all_times = np.empty(0).astype(np.datetime64)
    all_data = np.empty(0)

    for i in range(data_collect.SLOTS):
        my_csv_path = os.path.join(os.getcwd(), "data", str(i) + ".csv")
       
        # Then read it into our dataframe
        df = None
        try:
            with open(my_csv_path, "r") as data_file:
                df = pd.read_csv(data_file)
        except:
            continue

        # Only proceed if data is available
        if df is None or len(df) < 1:
            continue

        # Convert date column before we want to plot it
        df["date"] = pd.to_datetime(df["date"])
        
        t = df["date"].to_numpy()
        data = df[name].to_numpy()

        all_times = np.concatenate([all_times, t])
        all_data = np.concatenate([all_data, data])
    return (all_times, all_data)

@app.route("/")
def hello_page():
    # We prepare to concatenate all data from all storage slots
    all_times, all_pp = collect_data("pp")

    # Only proceed if data is available
    if len(all_times) < 1:
        return "No data available"
    
    ans = Colorfinity.time_scattered(all_times, all_pp, "pp vs Date", "pp")
    return f"<img src='data:image/png;base64,{ans}'/>"

# App run for testing
if __name__ == "__main__":
    app.run()

    # Terminate it now
    print("Deactivating")
    data_collect.ACTIVE = False
