import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
import joblib
#event model imports
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
import random
from database import Base

from datetime import datetime

device_id = Column(String)
vibration = Column(Float)
def generate_training_data():
    data = []

    for _ in range(1000):
        temperature = random.uniform(25, 40)
        pressure = random.uniform(990, 1025)
        vibration = random.uniform(0.5, 3.5)

        data.append([
            temperature,
            pressure,
            vibration
        ])

    return pd.DataFrame(
        data,
        columns=["temperature", "pressure", "vibration"]
    )

def train_model():

    df=generate_training_data()


    model=IsolationForest(
        contamination=0.03,
        random_state=42
    )


    model.fit(df)


    joblib.dump(
        model,
        "anomaly_model.pkl"
    )


    print(
        "Model trained successfully"
    )



if __name__=="__main__":

    train_model()
#event Model



class Event(Base):

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )

    temperature = Column(Float)

    pressure = Column(Float)

    status = Column(String)