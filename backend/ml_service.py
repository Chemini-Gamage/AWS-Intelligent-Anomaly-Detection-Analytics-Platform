import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent / "anomaly_model.pkl"

model = joblib.load(MODEL_PATH)

FEATURES = [
    "temperature",
    "pressure",
    "vibration"
]


def predict_anomaly(temperature, pressure, vibration):

    data = pd.DataFrame([{
        "temperature": temperature,
        "pressure": pressure,
        "vibration": vibration
    }])

    prediction = model.predict(data)[0]

    if prediction == -1:
        return "ANOMALY"

    return "NORMAL"