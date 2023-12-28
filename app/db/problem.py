from app.db import database_connection
from app.logger import get_logger
from pydantic import BaseModel
from typing import Union
from mysql.connector import Error

logger = get_logger(__name__)

class choiceModel(BaseModel):
    choiceid: int | None = None
    content: str
    problemid: int | None = None
    label: str
    iscorrect: bool


class problemModel(BaseModel):
    problemid: int | None = None
    name: str
    problemType: str
    content: str
    point: float
    difficult: str
    homeworkid: int
    choice: list[choiceModel] | None = None

class problem:
    def __init__(self, database_conect):
        self.database_connect = database_conect

    def get_choice_by_problemid(self, problemid: int) -> list[choiceModel]:
        logger.info("get_choice_by_problemid: %d", problemid)

        query: str = """
        SELECT choice.choiceid, choice.content, choice.problemid, choice.label, choice.iscorrect
        FROM choice
        WHERE problemid = %s
        """
        cursor = self.database_connect.cursor()
        cursor.execute(query, (problemid,))
        res: list[choiceModel] = [
            choiceModel(
                choiceid=int(choiceid),
                content=str(content),
                problemid=int(problemid),
                label=str(label),
                iscorrect=bool(iscorrect)
            ) for (choiceid, content, problemid, label, iscorrect) in cursor
        ]

        logger.info("get_choice_by_problemid %d res: %s", problemid, res)
        return res


    def get_problem_by_homeworkid(self, homeworkid: int) -> list[problemModel]:
        logger.info("get_problem_by_homeworkid: %d", homeworkid)

        sql: str = """
        SELECT problem.problemid, problem.name, problem.problemType, problem.content, problem.point, problem.difficult, problem.homeworkid
        FROM problem
        WHERE homeworkid = %s
        """
        cursor = self.database_connect.cursor()
        cursor.execute(sql, (homeworkid,))

        row = cursor.fetchall()
        res: list[problemModel] = [
            problemModel(
                problemid=int(problemid),
                name=str(name),
                problemType=str(problemType),
                content=str(content),
                point=float(point),
                difficult=str(difficult),
                homeworkid=int(homeworkid),
                choice=self.get_choice_by_problemid(problemid)
            ) for (problemid, name, problemType, content, point, difficult, homeworkid) in row
        ]

        logger.info("get_problem_by_homeworkid %d res: %s", homeworkid, res)
        return res

    def get_problem_by_id(self, problemid: int) -> Union[problemModel, None]:
        logger.info("get_problem_by_id: %d", problemid)

        sql: str = """
        SELECT problem.problemid, problem.name, problem.problemType, problem.content, problem.point, problem.difficult, problem.homeworkid
        FROM problem
        WHERE problemid = %s
        """
        cursor = self.database_connect.cursor()
        cursor.execute(sql, (problemid,))
        row = cursor.fetchall()

        res: list[problemModel] = [
            problemModel(
                problemid=int(problemid),
                name=str(name),
                problemType=str(problemType),
                content=str(content),
                point=float(point),
                difficult=str(difficult),
                homeworkid=int(homeworkid),
                choice=self.get_choice_by_problemid(problemid)
            ) for (problemid, name, problemType, content, point, difficult, homeworkid) in row
        ]

        logger.info("get_problem_by_id %d res: %s", problemid, res)
        if len(res) == 0:
            return None
        return res[0]

    def create_problem(self, new_problem: problemModel) -> bool:
        logger.info("create_problem: %s",new_problem.name)

        sql: str = """
        INSERT INTO problem (name, problemType, content, point, difficult, homeworkid)
        VALUES (%(name)s, %(problemType)s, %(content)s, %(point)s, %(difficult)s, %(homeworkid)s)
        """
        try:
            cursor = self.database_connect.cursor()
            cursor.execute(sql, {
                "name": new_problem.name,
                "problemType": new_problem.problemType,
                "content": new_problem.content,
                "point": new_problem.point,
                "difficult": new_problem.difficult,
                "homeworkid": new_problem.homeworkid
            })

            problem_id = cursor.lastrowid

            sql: str = """
            INSERT INTO choice (content, problemid, label, iscorrect)
            VALUES (%(content)s, %(problemid)s, %(label)s, %(iscorrect)s)
            """

            if  new_problem.choice is not None:
                for choice in new_problem.choice:
                    cursor = self.database_connect.cursor()
                    cursor.execute(sql, {
                        "content": choice.content,
                        "problemid": problem_id,
                        "label": choice.label,
                        "iscorrect": choice.iscorrect
                    })
            self.database_connect.commit()
        except Error as e:
            logger.error("create_problem: %s", e)
            return False

        return True

    def delete_problem(self, problemid: int) -> bool:
        logger.info("delete_problem: %d", problemid)

        sql: str = "DELETE FROM problem WHERE problemid = %s"
        cursor = self.database_connect.cursor()
        try:
            cursor.execute(sql, (problemid,))
            self.database_connect.commit()
        except Error as e:
            logger.error("delete_problem: %s", e)
            return False
        return True

def get_problem():
    return problem(database_connection)
