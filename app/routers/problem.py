from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import secure
from db import problem
from logger import get_logger

logger = get_logger(__name__)

problem_router = APIRouter(
    prefix="/problem",
    tags=["problem"],
    responses={404: {"description": "Not found"}},
)

class problem_brief(BaseModel):
    problemid: int
    name: str
    problemType: str
    point: float
    difficult: str

@problem_router.get("/{problemid}")
async def  get_problem_by_id(
    problemid: int,
    notuse: secure.TokenData = Depends(secure.decode_token),
    response_model=problem.problemModel
    ):
    store_problem = problem.get_problem()
    res = store_problem.get_problem_by_id(problemid)

    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )
    return res

@problem_router.get("/homework/{homeworkid}")
async def get_problem_by_homeworkid(
    homeworkid: int,
    notuse: secure.TokenData = Depends(secure.decode_token),
    response_model=list[problem_brief]
    ):
    store_problem = problem.get_problem()
    res = store_problem.get_problem_by_homeworkid(homeworkid)
    return res

class choice_req(BaseModel):
    content: str
    # problemid: int
    label: str
    iscorrect: bool

class problem_req(BaseModel):
    name: str
    problemType: str
    content: str
    point: float
    difficult: str
    homeworkid: int
    choice: list[choice_req] | None = None

@problem_router.put("/create")
async def create_problem(
    new_problem: problem_req,
    tokenDate: secure.TokenData = Depends(secure.decode_token)
    ):

    if tokenDate.role not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )
    store_problem = problem.get_problem()

    insert_problem = problem.problemModel(
        name=new_problem.name,
        problemType=new_problem.problemType,
        content=new_problem.content,
        point=new_problem.point,
        difficult=new_problem.difficult,
        homeworkid=new_problem.homeworkid
    )

    if new_problem.choice is not None:
        insert_problem.choice = [
            problem.choiceModel(
                content=choice.content,
                # problemid=choice.problemid,
                label=choice.label,
                iscorrect=choice.iscorrect
            ) for choice in new_problem.choice
        ]

    ok: bool = store_problem.create_problem(insert_problem)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Create problem failed",
        )
    return True

@problem_router.delete("/delete/{problemid}")
async def delete_problem(
    problemid: int,
    tokenDate: secure.TokenData = Depends(secure.decode_token)
    ):
    if tokenDate.role not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )
    store_problem = problem.get_problem()
    ok: bool = store_problem.delete_problem(problemid)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Delete problem failed",
        )
    return True
