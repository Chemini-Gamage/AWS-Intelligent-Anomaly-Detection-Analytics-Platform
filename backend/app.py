from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models
import crud
from ml_service import predict

import random
from datetime import datetime
from routers import events
from routers import statistics
from routers import alerts

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AWS Real-Time Analytics Platform",
    version="1.0.0",
    description="Real-Time Sensor Analytics with ML Anomaly Detection"
)


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AWS Analytics Backend Online"
    }


@app.post("/events")
def generate_event(db: Session = Depends(get_db)):
    """
    Generate a simulated sensor event,
    classify it with the ML model,
    and store it in SQLite.
    """

    # 90% normal events
    if random.random() < 0.90:

        temperature = random.gauss(35, 4)
        pressure = random.gauss(1010, 8)

    # 10% anomalies
    else:

        temperature = random.choice([
            random.uniform(70, 120),
            random.uniform(-20, 10)
        ])

        pressure = random.choice([
            random.uniform(750, 850),
            random.uniform(1150, 1300)
        ])

    status = predict(
        temperature,
        pressure
    )

    event = models.Event(
        timestamp=datetime.utcnow(),
        temperature=temperature,
        pressure=pressure,
        status=status
    )

    return crud.create_event(db, event)



@app.get("/")
def home():

    return {

        "message": "Backend Running"

    }


app.include_router(events.router)

app.include_router(statistics.router)

app.include_router(alerts.router)

