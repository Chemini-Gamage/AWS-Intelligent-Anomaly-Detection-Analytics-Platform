from pathlib import Path
import joblib
import pandas as pd

MODEL_PATH = Path(__file__).parent / "anomaly_model.pkl"

model = joblib.load(MODEL_PATH)


def predict(
    temperature,
    pressure
):

    data = pd.DataFrame(
        [
            {
                "temperature": temperature,
                "pressure": pressure
            }
        ]
    )


    result = model.predict(data)[0]


    if result == -1:
        return "ANOMALY"

    return "NORMAL"