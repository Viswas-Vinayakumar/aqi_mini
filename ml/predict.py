import pandas as pd
from datetime import timedelta
import requests


# Load historical AQI
df = pd.read_csv("ml/data.csv", parse_dates=["date"])

# Sort by time (never skip this)
df = df.sort_values("date")

# VERY SIMPLE MODEL:
# prediction = average of last 3 days
window = 3
last_values = df["aqi"].tail(window)
predicted_value = int(last_values.mean())

last_date = df["date"].max()

predictions = [
    {
        "target_date": (last_date + timedelta(days=1)).date().isoformat(),
        "predicted_aqi": predicted_value,
    },
    {
        "target_date": (last_date + timedelta(days=2)).date().isoformat(),
        "predicted_aqi": predicted_value,
    },
]

payload = {
    "model_version": "mini_v1",
    "predictions": predictions,
}

API_URL = "http://127.0.0.1:8000/aqi/predictions"

response = requests.post(API_URL, json=payload)

print("Status code:", response.status_code)
print("Response:", response.json())

