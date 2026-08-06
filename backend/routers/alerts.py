from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud

from database import get_db

router = APIRouter(

    prefix="/alerts",

    tags=["Alerts"]

)


@router.get("")
def alerts(

    db: Session = Depends(get_db)

):

    events = crud.get_events(db)

    return [

        event

        for event in events

        if event.status == "ANOMALY"

    ]