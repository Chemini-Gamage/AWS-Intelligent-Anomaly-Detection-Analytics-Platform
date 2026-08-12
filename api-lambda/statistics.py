from fastapi import APIRouter

import crud


router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)


@router.get("")
def statistics():
    return crud.get_statistics()