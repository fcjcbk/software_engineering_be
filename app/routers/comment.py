from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime
from app import secure
from app.db import comment
from app.logger import get_logger

logger = get_logger(__name__)

comment_router = APIRouter(
    prefix="/comment",
    tags=["comment"],
    responses={404: {"description": "Not found"}},
)

@comment_router.get("/solution/{solutionid}")
async def get_comment_by_solutionid(
    solutionid: int,
    notuse: secure.TokenData = Depends(secure.decode_token),
    response_model=list[comment.comment_rep]
    ) -> list[comment.comment_rep]:
    store_comment = comment.get_comment()
    res = store_comment.get_comment_by_solutionid_rep(solutionid)
    return res

class comment_req(BaseModel):
    content: str
    createAt: datetime

class comment_create_req(BaseModel):
    content: str
    createAt: datetime

@comment_router.put("/solution/{solutionid}")
async def create_comment(
    solutionid: int,
    new_comment: comment_create_req,
    tokenDate: secure.TokenData = Depends(secure.decode_token),
    ):
    store_comment = comment.get_comment()

    insert_comment: comment.commentModel = comment.commentModel(
        commentid=None,
        content=new_comment.content,
        createAt=new_comment.createAt,
        solutionid=solutionid,
        contributorid=tokenDate.userid
    )

    res = store_comment.create_comment(insert_comment)

    if res is False:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="create comment fail",
        )
    return res

@comment_router.delete("/{commentid}")
async def delete_comment(
    commentid: int,
    tokenDate: secure.TokenData = Depends(secure.decode_token),
    ):

    store_comment = comment.get_comment()

    old_comment = store_comment.get_comment_by_id(commentid)
    if old_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="comment not found",
        )

    if tokenDate.role == 0 and tokenDate.userid != old_comment.contributorid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    res = store_comment.delete_comment_by_commentid(commentid)

    if res is False:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="delete comment fail",
        )
    return res
