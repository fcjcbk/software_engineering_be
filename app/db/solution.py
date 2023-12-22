from db import database_connection
from pydantic import BaseModel
from typing import Union
from mysql.connector import Error
from logger import get_logger

logger = get_logger(__name__)

class solutionModel(BaseModel):
    solutionid: int
    name: str
    content: str
    problemid: int
    contributorid: int

# Todo: 需要重写一个solution 返回
class solution_rep(BaseModel):
    solutionid: int
    name: str
    content: str
    author: str

class solution_brief(BaseModel):
    solutionid: int
    name: str
    author: str

class Solution:
    def __init__(self, database_conect):
        self.database_connect = database_conect

    def get_solution_by_problemid(self, problemid: int) -> list[solution_brief]:
        logger.info("get_solution_by_problemid: %d", problemid)
        query: str = """
        SELECT solution.solutionid, solution.name, user.username
        FROM solution
        JOIN user ON solution.contributorid = user.userid
        WHERE problemid = %s
        """
        cursor = self.database_connect.cursor()
        cursor.execute(query, (problemid,))
        res: list[solution_brief] = [
            solution_brief(
                solutionid=int(solutionid),
                name=str(name),
                author=str(author)
            ) for (solutionid, name, author) in cursor
        ]
        return res


    def create_solution(self, solution: solutionModel) -> bool:
        logger.info("create_solution: %s", solution.content)

        query: str = """
        INSERT INTO solution (solutionid, name, content, problemid, contributorid)
        VALUES (%(solutionid)s, %(name)s, %(content)s, %(problemid)s, %(contributorid)s)
        """
        try:
            cursor = self.database_connect.cursor()
            cursor.execute(query, dict(solution))
            self.database_connect.commit()
        except Error as e:
            logger.error("create_solution: %s", e)
            return False
        return True


    def delete_solution(self, solutionid: int) -> bool:
        logger.info("delete_solution: %d", solutionid)

        query: str = "DELETE FROM solution WHERE solutionid = %s"
        cursor = self.database_connect.cursor()
        try:
            cursor.execute(query, (solutionid,))
            self.database_connect.commit()
        except Error as e:
            logger.error(e)
            return False
        return True

    def get_solution_by_id(self, solutionid: int) -> Union[solution_rep, None]:
        logger.info("get_solution_by_solutionid: %d", solutionid)

        query: str = """
        SELECT solution.solutionid, solution.name, solution.content, user.username
        FROM solution
        JOIN user ON solution.contributorid = user.userid
        WHERE solutionid = %s
        """

        cursor = self.database_connect.cursor()
        cursor.execute(query, (solutionid,))
        res: list[solution_rep] = [
            solution_rep(
                solutionid=int(solutionid),
                name=str(name),
                content=str(content),
                author=str(author),
            ) for (solutionid, name, content, author) in cursor
        ]
        if len(res) == 0:
            return None
        return res[0]

def get_solution():
    return Solution(database_connection)
