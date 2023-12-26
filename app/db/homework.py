from app.db import database_connection
from app.logger import get_logger
from pydantic import BaseModel
from typing import Union
from mysql.connector import Error

from datetime import datetime

logger = get_logger(__name__)

class homeworkModel(BaseModel):
    homeworkid: int | None = None
    homeworkname: str
    duedate: datetime
    courseid: int

class Homework:
    def __init__(self, database_conect):
        self.database_connect = database_conect

    def get_homework(self, courseid: int) -> list[homeworkModel]:
        logger.info("get_homework: %d", courseid)

        query: str = "SELECT homeworkid, homeworkname, duedate, courseid FROM homework WHERE courseid = %s"
        cursor = self.database_connect.cursor()
        cursor.execute(query, (courseid,))
        res: list[homeworkModel] = [
            homeworkModel(
                homeworkid=int(homeworkid),
                homeworkname=str(homeworkname),
                duedate=datetime.strptime(str(duedate), '%Y-%m-%d %H:%M:%S'),
                courseid=int(courseid)
            ) for (homeworkid, homeworkname, duedate, courseid) in cursor
        ]
        return res

    def create_homework(self, homework: homeworkModel) -> bool:
        logger.info("create_homework: %s", homework.homeworkname)

        query: str = """
        INSERT INTO homework (homeworkname, duedate, courseid)
        VALUES (%(homeworkname)s, %(duedate)s, %(courseid)s)
        """
        try:
            cursor = self.database_connect.cursor()
            cursor.execute(query, {
                'homeworkname': homework.homeworkname,
                'duedate': homework.duedate,
                'courseid': homework.courseid
            })
            self.database_connect.commit()
        except Error as e:
            logger.error("create_homework: %s", e)
            return False
        return True

    def delete_homework(self, homeworkid: int) -> bool:
        logger.info("delete_homework: %d", homeworkid)

        query: str = "DELETE FROM homework WHERE homeworkid = %s"
        cursor = self.database_connect.cursor()
        try:
            cursor.execute(query, (homeworkid,))
            self.database_connect.commit()
        except Error as e:
            logger.error(e)
            return False
        return True

    def delete_homework_by_course(self, courseid: int) -> bool:
        logger.info("delete_homework_by_course: %d", courseid)
        query: str = "DELETE FROM homework WHERE courseid = %s"
        cursor = self.database_connect.cursor()
        try:
            cursor.execute(query, (courseid,))
            self.database_connect.commit()
        except Error as e:
            logger.error(e)
            return False
        return True

def get_homework():
    return Homework(database_connection)
