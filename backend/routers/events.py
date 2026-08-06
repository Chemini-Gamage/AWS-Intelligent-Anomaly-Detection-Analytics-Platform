from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import random

import crud
import models

from database import get_db
from ml_service import predict
#with the sensor simulator
from pydantic import BaseModel

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


class SensorEvent(BaseModel):

    device_id: str

    timestamp: str

    temperature: float

    pressure: float

    vibration: float

@router.post("")
def create_event(
    event_data: SensorEvent,
    db: Session = Depends(get_db)
):
    # Generate mostly normal events
    if random.random() < 0.90:

        temperature = event_data.temperature

        pressure = event_data.pressure

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

    return crud.create_event(
        db,
        event
    )


@router.get("")
def get_events(
    db: Session = Depends(get_db)
):

    return crud.get_events(db)
