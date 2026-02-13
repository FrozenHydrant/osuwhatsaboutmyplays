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

@app.route("/")
def hello_page():
    # We prepare to concatenate all data from all storage slots
    # TODO: move image generation somewhere else..
    all_times = np.empty(0)
    all_pp = np.empty(0)
    for df in data_collect.DATA:
        t = df["date"].to_numpy()
        pp = df["pp"].to_numpy()

        all_times = np.concatenate([all_times, t])
        all_pp = np.concatenate([all_pp, pp])

    ans = Colorfinity.time_scattered(all_times, all_pp, "pp vs Date", "pp")
    return f"<img src='data:image/png;base64,{ans}'/>"

# App run for testing
if __name__ == "__main__":
    app.run()

    # Terminate it now
    print("Deactivating")
    data_collect.ACTIVE = False
