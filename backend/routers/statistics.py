from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud

from database import get_db

router = APIRouter(

    prefix="/statistics",

    tags=["Statistics"]

)


@router.get("")
def statistics(

    db: Session = Depends(get_db)

):

    return crud.get_statistics(db)