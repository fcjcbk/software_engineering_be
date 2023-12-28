from app.db import database_connection
from app.logger import get_logger
from pydantic import BaseModel
from typing import Union
from mysql.connector import Error

logger = get_logger(__name__)

class attemptModel(BaseModel):
    problemid: int
    studentid: int
    point: float | None = None
    content: str | None = None

class attempt:
    def __init__(self, database_conect):
        self.database_connect = database_conect

    def get_attempt_by_problemid(self, problemid: int) -> list[attemptModel]:
        logger.info("get_attempt_by_problemid: %d", problemid)

        query: str = """
        SELECT problemid, studentid, point, content
        FROM attempt
        WHERE problemid = %s
        """
        cursor = self.database_connect.cursor()
        cursor.execute(query, (problemid,))
        res: list[attemptModel] = [
            attemptModel(
                problemid=int(problemid),
                studentid=int(studentid),
                point=float(point),
                content=str(content)
            ) for (problemid, studentid, point, content) in cursor
        ]
        return res

    def get_attempt(self, problemid: int, studentid: int) -> attemptModel | None:
        logger.info("get_attempt: problemid=%d, studentid=%d", problemid, studentid)

        query: str = """
        SELECT problemid, studentid, point, content
        FROM attempt
        WHERE problemid = %(problemid)s AND studentid = %(studentid)s
        """
        cursor = self.database_connect.cursor()
        cursor.execute(query, {
            "problemid": problemid,
            "studentid": studentid
        })

        row = cursor.fetchone()

        if row is None:
            return None

        problemid, studentid, point, content = row

        logger.info("get attempt res: problemid=%d, studentid=%d, point=%f, content=%s",
                    problemid, studentid, point, content)
        return attemptModel(
            problemid=int(problemid),
            studentid=int(studentid),
            point=float(point),
            content=str(content)
        )

    def create_attempt(self, new_attempt: attemptModel) -> bool:
        logger.info("create_attempt: %s", new_attempt)

        query: str = """
        INSERT INTO attempt(problemid, studentid, point, content)
        VALUES(%(problemid)s, %(studentid)s, %(point)s, %(content)s)
        """

        try:
            cursor = self.database_connect.cursor()
            cursor.execute(query, dict(new_attempt))
            self.database_connect.commit()
        except Error as e:
            logger.error(e)
            return False

        return True

    def update_attempt_content(self, new_attempt: attemptModel) -> bool:
        logger.info("update_attempt: %s", new_attempt)

        query: str = """
        UPDATE attempt
        SET content = %(content)s
        WHERE problemid = %(problemid)s AND studentid = %(studentid)s
        """

        try:
            cursor = self.database_connect.cursor()
            cursor.execute(query, {
                "problemid": new_attempt.problemid,
                "studentid": new_attempt.studentid,
                "content": new_attempt.content
            })
            self.database_connect.commit()

            affect_rows = cursor.rowcount
            logger.info("affect_rows: %d", affect_rows)

            if affect_rows == 0:
                return False

        except Error as e:
            logger.error(e)
            return False

        return True

    def update_attempt_point(self, new_attempt: attemptModel) -> bool:
        logger.info("update_attempt_point: %s", new_attempt)

        query: str = """
        UPDATE attempt
        SET point = %(point)s
        WHERE problemid = %(problemid)s AND studentid = %(studentid)s
        """

        try:
            cursor = self.database_connect.cursor()
            cursor.execute(query, {
                "problemid": new_attempt.problemid,
                "studentid": new_attempt.studentid,
                "point": new_attempt.point
            })
            self.database_connect.commit()

            affect_rows = cursor.rowcount
            logger.info("affect_rows: %d", affect_rows)

            if affect_rows == 0:
                return False

        except Error as e:
            logger.error(e)
            return False

        return True

    def delete_attempt(self, problemid: int, studentid: int) -> bool:
        logger.info("delete_attempt: problemid=%d sudentid=%d", problemid, studentid)

        query: str = "DELETE FROM attempt WHERE problemid = %(problemid)s AND studentid = %(studentid)s"
        cursor = self.database_connect.cursor()
        try:
            cursor.execute(query, {
                "problemid": problemid,
                "studentid": studentid
            })
            self.database_connect.commit()
        except Error as e:
            logger.error(e)
            return False
        return True

def get_attempt() -> attempt:
    return attempt(database_connection)
