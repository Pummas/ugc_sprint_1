from fastapi import APIRouter

router = APIRouter(prefix="/etl", tags=["etl"], responses={404: {"description": "Not found"}})


@router.post('/load')
def load():
    return "hello"
