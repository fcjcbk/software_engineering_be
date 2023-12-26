from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app import secure
from app.db import attempt
from app.logger import get_logger

logger = get_logger(__name__)

# Todo: need to test
attempt_router = APIRouter(
    prefix="/attempt",
    tags=["attempt"],
    responses={404: {"description": "no such attempt"}},
)

@attempt_router.get("/problem/{problemid}")
async def get_attempt_by_problemid(
    problemid: int,
    tokenData: secure.TokenData = Depends(secure.decode_token)
    ):

    if tokenData.role not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Permission denied",
        )

    store_attempt = attempt.get_attempt()
    res = store_attempt.get_attempt_by_problemid(problemid)
    return res

@attempt_router.get("/")
async def get_attempt(
    problemid: int,
    studentid: int,
    tokenData: secure.TokenData = Depends(secure.decode_token)
    ):

    store_attempt = attempt.get_attempt()
    res = store_attempt.get_attempt(problemid, studentid)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such attempt",
        )
    return res

class attempt_create_req(BaseModel):
    problemid: int
    content: str

@attempt_router.put("/create")
async def create_attempt(
    new_attempt: attempt_create_req,
    tokenData: secure.TokenData = Depends(secure.decode_token)
    ):

    if tokenData.role != 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Permission denied",
        )

    store_attempt = attempt.get_attempt()

    insert_attempt: attempt.attemptModel = attempt.attemptModel(
        problemid=new_attempt.problemid,
        studentid=tokenData.userid,
        point=0,
        content=new_attempt.content
    )

    ok: bool = store_attempt.create_attempt(insert_attempt)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Create attempt failed",
        )
    return True

class attempt_update_req(BaseModel):
    problemid: int
    content: str

@attempt_router.post("/update")
async def stu_update_attempt(
    new_attempt: attempt_update_req,
    tokenData: secure.TokenData = Depends(secure.decode_token)
    ):

    if tokenData.role != 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Permission denied",
        )

    store_attempt = attempt.get_attempt()

    insert_attempt: attempt.attemptModel = attempt.attemptModel(
        problemid=new_attempt.problemid,
        studentid=tokenData.userid,
        point=None,
        content=new_attempt.content
    )

    ok: bool = store_attempt.update_attempt_content(insert_attempt)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Update attempt failed",
        )
    return True

class attempt_update_point_req(BaseModel):
    problemid: int
    studentid: int
    point: float

@attempt_router.post("/updatepoint")
async def teacher_update_attempt(
    new_attempt: attempt_update_point_req,
    tokenData: secure.TokenData = Depends(secure.decode_token)
    ):

    if tokenData.role not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Permission denied",
        )

    store_attempt = attempt.get_attempt()

    insert_attempt: attempt.attemptModel = attempt.attemptModel(
        problemid=new_attempt.problemid,
        studentid=new_attempt.studentid,
        point=new_attempt.point,
        content=None
    )

    ok: bool = store_attempt.update_attempt_point(insert_attempt)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Update attempt failed",
        )
    return True

@attempt_router.delete("/delete")
async def delete_attempt(
    problemid: int,
    studentid: int,
    tokenData: secure.TokenData = Depends(secure.decode_token)
    ):

    if tokenData.role not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Permission denied",
        )

    store_attempt = attempt.get_attempt()

    ok: bool = store_attempt.delete_attempt(problemid, studentid)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Delete attempt failed",
        )
    return True
