from fastapi import FastAPI

from datetime import datetime

import random

import joblib

import pandas as pd



app=FastAPI(
    title="AWS Anomaly Detection API"
)



model=joblib.load(
    "anomaly_model.pkl"
)



events=[]



@app.get("/")
def home():

    return {
        "status":"running"
    }



@app.post("/events")
def create_event():



    if random.random() < 0.90:

        temperature = random.gauss(35, 4)
        pressure = random.gauss(1010, 8)

    else:

        temperature = random.choice([
            random.uniform(70, 120),
            random.uniform(-20, 10)
        ])

        pressure = random.choice([
            random.uniform(750, 850),
            random.uniform(1150, 1300)
        ])


    data=pd.DataFrame(
        [
            {
                "temperature":temperature,
                "pressure":pressure
            }
        ]
    )


    prediction=model.predict(
        data
    )[0]



    if prediction==-1:

        status="ANOMALY"

    else:

        status="NORMAL"



    event={

        "id":
        len(events)+1,


        "timestamp":
        datetime.utcnow(),


        "temperature":
        temperature,


        "pressure":
        pressure,


        "status":
        status

    }


    events.append(event)


    return event





@app.get("/events")
def get_events():

    return events




@app.get("/alerts")
def alerts():

    return [
        e
        for e in events
        if e["status"]=="ANOMALY"
    ]




@app.get("/statistics")
def statistics():


    total=len(events)


    anomalies=len(
        [
            e for e in events
            if e["status"]=="ANOMALY"
        ]
    )


    return {

        "total_events":total,

        "normal_events":
        total-anomalies,

        "anomalies":
        anomalies

    }