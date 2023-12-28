from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app import secure
from app.db import course
from app.logger import get_logger

logger = get_logger(__name__)

course_router = APIRouter(
    prefix="/course",
    tags=["course"],
    responses={404: {"description": "no such course"}},
)

class course_req(BaseModel):
    name: str
    info: str
    teacherid: int

# Todo: may miss error handling
@course_router.get("/student")
async def get_course_by_student_id(
    tokenData: secure.TokenData = Depends(secure.decode_token),
    response_model=list[course.courseModel],
    ) -> list[course.courseModel]:
    store_course = course.get_course()
    res = store_course.get_course_by_student_id(tokenData.userid)
    return res

@course_router.get("/teacher")
async def get_course_by_teacher_id(
    tokenData: secure.TokenData = Depends(secure.decode_token),
    response_model=list[course.courseModel],
    ) -> list[course.courseModel]:
    store_course = course.get_course()
    res = store_course.get_course_by_teacher_id(tokenData.userid)
    return res

@course_router.post("/create")
async def create_course(
        new_course: course_req,
        tokenData: secure.TokenData = Depends(secure.decode_token)
    ):
    if tokenData.role not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Permission denied",
        )
    store_course = course.get_course()
    insert_course: course.courseModel = course.courseModel(**dict(new_course))

    ok: bool = store_course.create_course(insert_course)

    if not ok:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Create course failed",
        )
    # Todo: may change response
    return True

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
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
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
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
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
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Cancel course failed",
        )
    return ok
