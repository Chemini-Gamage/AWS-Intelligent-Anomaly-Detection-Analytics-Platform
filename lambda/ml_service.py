import joblib
import pandas as pd


model = joblib.load(
    "anomaly_model.pkl"
)


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