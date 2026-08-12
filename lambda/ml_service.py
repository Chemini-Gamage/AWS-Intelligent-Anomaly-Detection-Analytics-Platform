import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent / "anomaly_model.pkl"

model = joblib.load(MODEL_PATH)


def predict_anomaly(
    temperature,
    pressure,
    vibration
):
    """
    Run anomaly detection using the trained ML model.
    """

    data = pd.DataFrame(
        [[
            temperature,
            pressure,
            vibration
        ]],
        columns=[
            "temperature",
            "pressure",
            "vibration"
        ]
    )

    prediction = model.predict(data)[0]

    # Isolation Forest:
    #  1  = normal
    # -1  = anomaly

    if prediction == -1:
        return "ANOMALY"

    return "NORMAL"