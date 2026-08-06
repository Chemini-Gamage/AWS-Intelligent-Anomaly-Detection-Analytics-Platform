#prediction logic
import joblib
import pandas as pd

model = joblib.load("anomaly_model.pkl")


def predict(temperature, pressure):

    sample = pd.DataFrame([
        {
            "temperature": temperature,
            "pressure": pressure
        }
    ])

    prediction = model.predict(sample)[0]

    return "ANOMALY" if prediction == -1 else "NORMAL"