from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime
import secure
from db import homework
from logger import get_logger

logger = get_logger(__name__)
homework_router = APIRouter(
    prefix="/homework",
    tags=["homework"],
    # Todo: response may be change
    responses={404: {"msg": "no route found"}}
)

class homework_req(BaseModel):
    homeworkname: str
    duedate: datetime
    courseid: int

@homework_router.get("/{courseid}")
async def get_homework(
    courseid: int,
    response_model=list[homework.homeworkModel],
    tokenDate: secure.TokenData = Depends(secure.decode_token)
    ):
    store_homework = homework.get_homework()
    return store_homework.get_homework(courseid)

@homework_router.put("/create")
async def create_homework(
    new_homework: homework_req,
    tokenDate: secure.TokenData = Depends(secure.decode_token)
    ):
    if tokenDate.role not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Permission denied",
        )
    store_homework = homework.get_homework()

    insert_homework: homework.homeworkModel = homework.homeworkModel(**dict(new_homework))

    ok: bool = store_homework.create_homework(insert_homework)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Create homework failed",
        )
    return True

@homework_router.delete("/delete/{homeworkid}")
async def delete_homework(
    homeworkid: int,
    tokenDate: secure.TokenData = Depends(secure.decode_token)
    ):
    if tokenDate.role not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Permission denied",
        )
    store_homework = homework.get_homework()
    ok: bool = store_homework.delete_homework(homeworkid)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Delete homework failed",
        )
    return True
