from app.db import database_connection
from app.logger import get_logger
from pydantic import BaseModel
from typing import Union
from mysql.connector import Error
from datetime import datetime

logger = get_logger(__name__)

class commentModel(BaseModel):
    commentid: int | None = None
    content: str
    createAt: datetime
    solutionid: int
    contributorid: int

class comment_rep(BaseModel):
    commentid: int
    content: str
    createAt: datetime
    solutionid: int
    contributorid: int
    contributorname: str
    contributorrole: int

class comment:
    def __init__(self, database_conect):
        self.database_connect = database_conect

    def get_comment_by_solutionid(self, solutionid: int) -> list[commentModel]:
        logger.info("get_comment_by_solutionid: %d", solutionid)

        query: str = """
        SELECT comment.commentid, comment.content, comment.createAt, comment.solutionid, comment.contributorid
        FROM comment
        WHERE solutionid = %s
        """
        cursor = self.database_connect.cursor()
        cursor.execute(query, (solutionid,))
        res: list[commentModel] = [
            commentModel(
                commentid=int(commentid),
                content=str(content),
                createAt=createAt,
                solutionid=int(solutionid),
                contributorid=int(contributorid)
            ) for (commentid, content, createAt, solutionid, contributorid) in cursor
        ]
        return res

    def get_comment_by_id(self, commentid: int) -> Union[commentModel, None]:
        logger.info("get_comment_by_id: %d", commentid)

        query: str = """
        SELECT comment.commentid, comment.content, comment.createAt, comment.solutionid, comment.contributorid
        FROM comment
        WHERE commentid = %s
        """
        cursor = self.database_connect.cursor()
        cursor.execute(query, (commentid,))
        res: list[commentModel] = [
            commentModel(
                commentid=int(commentid),
                content=str(content),
                createAt=createAt,
                solutionid=int(solutionid),
                contributorid=int(contributorid)
            ) for (commentid, content, createAt, solutionid, contributorid) in cursor
        ]
        if len(res) == 0:
            return None
        return res[0]

    def create_comment(self, new_comment: commentModel) -> bool:
        logger.info("create_comment: %s", new_comment)

        query: str = """
        INSERT INTO comment(content, createAt, solutionid, contributorid)
        VALUES (%(content)s, %(createAt)s, %(solutionid)s, %(contributorid)s)
        """
        try:
            cursor = self.database_connect.cursor()
            cursor.execute(query, {
                "content": new_comment.content,
                "createAt": new_comment.createAt,
                "solutionid": new_comment.solutionid,
                "contributorid": new_comment.contributorid
            })
            self.database_connect.commit()
        except Error as e:
            logger.error("create_comment: %s", e)
            return False
        return True

    def delete_comment_by_commentid(self, commentid: int) -> bool:
        logger.info("delete_comment_by_commentid: %d", commentid)

        query: str = """
        DELETE FROM comment
        WHERE commentid = %s
        """
        try:
            cursor = self.database_connect.cursor()
            cursor.execute(query, (commentid,))
            self.database_connect.commit()
        except Error as e:
            logger.error("delete_comment_by_commentid: %s", e)
            return False
        return True

    def get_comment_by_solutionid_rep(self, solutionid: int) -> list[comment_rep]:
        logger.info("get_comment_by_solutionid_rep: %d", solutionid)

        query: str = """
        SELECT comment.commentid, comment.content, comment.createAt, comment.solutionid, comment.contributorid, user.username, user.role
        FROM comment
        INNER JOIN user
        ON comment.contributorid = user.userid
        WHERE solutionid = %s
        """
        cursor = self.database_connect.cursor()
        cursor.execute(query, (solutionid,))
        res: list[comment_rep] = [
            comment_rep(
                commentid=int(commentid),
                content=str(content),
                createAt=createAt,
                solutionid=int(solutionid),
                contributorid=int(contributorid),
                contributorname=str(contributorname),
                contributorrole=int(contributorrole)
            ) for (commentid, content, createAt, solutionid, contributorid, contributorname, contributorrole) in cursor
        ]
        return res

def get_comment():
    return comment(database_connection)
