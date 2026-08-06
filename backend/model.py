import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
import joblib



def generate_training_data():

    data=[]


    for i in range(1000):

        temperature=np.random.normal(
            35,
            5
        )

        pressure=np.random.normal(
            1010,
            10
        )


        data.append(
            [
                temperature,
                pressure
            ]
        )


    return pd.DataFrame(
        data,
        columns=[
            "temperature",
            "pressure"
        ]
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