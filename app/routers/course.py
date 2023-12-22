from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import secure
from db import course
from logger import get_logger

logger = get_logger(__name__)

course_router = APIRouter(
    prefix="/course",
    tags=["course"],
    responses={404: {"description": "no such course"}},
)

# Todo: may miss error handling
@course_router.get("/student")
async def get_course_by_student_id(tokenData: secure.TokenData = Depends(secure.decode_token)):
    store_course = course.get_course()
    res = store_course.get_course_by_student_id(tokenData.userid)
    return res

@course_router.get("/teacher")
async def get_course_by_teacher_id(tokenData: secure.TokenData = Depends(secure.decode_token)):
    store_course = course.get_course()
    res = store_course.get_course_by_teacher_id(tokenData.userid)
    return res

@course_router.post("/create")
async def create_course(
        new_course: course.courseModel,
        response_model=course.courseModel,
        tokenData: secure.TokenData = Depends(secure.decode_token)
    ):
    if tokenData.role not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Permission denied",
        )
    store_course = course.get_course()
    ok: bool = store_course.create_course(new_course)

    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Create course failed",
        )
    # Todo: may change response
    return new_course

# Todo: may change response
@course_router.delete("/delete/{courseid}")
async def delete_course(courseid: int,
    tokenData: secure.TokenData = Depends(secure.decode_token)
    ):
    if tokenData.role not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Permission denied",
        )

    store_course = course.get_course()
    ok: bool = store_course.delete_course(courseid)

    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Delete course failed",
        )
    return ok

@course_router.put("select/{courseid}")
async def select_course(
    courseid: int,
    tokenData: secure.TokenData = Depends(secure.decode_token)
    ):
    if tokenData.role != 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Permission denied",
        )

    store_course = course.get_course()
    ok: bool = store_course.select_course(courseid, tokenData.userid)

    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Select course failed",
        )
    return ok

class cancel_request(BaseModel):
    courseid: int
    userid: int

@course_router.delete("cancel")
async def cancel_course(
    cancel_req: cancel_request,
    notuse = Depends(secure.decode_token)
    ):
    store_course = course.get_course()
    ok: bool = store_course.cancel_course(cancel_req.courseid, cancel_req.userid)

    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cancel course failed",
        )
    return ok
