from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app import secure
from app.db import solution
from app.logger import get_logger

logger = get_logger(__name__)

solution_router = APIRouter(
    prefix="/solution",
    tags=["solution"],
    responses={404: {"description": "Not found"}},
)

class solution_req(BaseModel):
    problemid: int
    content: str
    contributorid: int
    name: str

@solution_router.get("/problemid/{problemid}")
async def get_solution_by_problemid(
    problemid: int,
    notuse: secure.TokenData = Depends(secure.decode_token),
    response_model=list[solution.solution_brief]
    ) -> list[solution.solution_brief]:
    store_solution = solution.get_solution()
    res = store_solution.get_solution_by_problemid(problemid)
    return res

@solution_router.get("/{solutionid}")
async def get_solution_by_id(
    solutionid: int,
    notuse: secure.TokenData = Depends(secure.decode_token),
    response_model=solution.solution_rep
    ) -> solution.solution_rep:
    store_solution = solution.get_solution()
    res = store_solution.get_solution_by_id(solutionid)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solution not found",
        )
    return res

@solution_router.put("/create")
async def create_solution(
    new_solution: solution_req,
    tokenDate: secure.TokenData = Depends(secure.decode_token)
    ):
    store_solution = solution.get_solution()

    insert_solution: solution.solutionModel = solution.solutionModel(**dict(new_solution))
    ok: bool = store_solution.create_solution(insert_solution)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Create solution failed",
        )
    return True

@solution_router.delete("/delete/{solutionid}")
async def delete_solution(
    solutionid: int,
    tokenDate: secure.TokenData = Depends(secure.decode_token)
    ):
    store_solution = solution.get_solution()
    ok: bool = store_solution.delete_solution(solutionid)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Delete solution failed",
        )
    return True
