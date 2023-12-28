from app.db import database_connection
from app.logger import get_logger
from pydantic import BaseModel
from typing import Union
from mysql.connector import Error

logger = get_logger(__name__)

class courseModel(BaseModel):
    courseid: int | None = None
    name: str
    info: str
    teacherid: int

class StuCourseModel(BaseModel):
    courseid: int
    userid: int

class select_course_rep(BaseModel):
    courseid: int
    name: str
    info: str
    teacherid: int
    teachername: str


class Course:
    def __init__(self, database_conect):
        self.database_connect = database_conect

    def get_course_by_student_id(self, userid: int) -> list[courseModel]:

        logger.info("get_course_by_student_id: %d", userid)
        # Todo: 是否要返回老师姓名？
        query: str = """
            SELECT course.courseid, course.name, course.info, course.teacherid
              FROM course
              JOIN stu_course
                ON course.courseid = stu_course.courseid
             WHERE stu_course.userid = %s
        """
        cursor = self.database_connect.cursor()
        cursor.execute(query, (userid,))
        res: list[courseModel] = [
            courseModel(
                courseid=int(courseid),
                name=str(name),
                info=str(info),
                teacherid=int(teacherid)
            ) for (courseid, name, info, teacherid) in cursor
        ]

        logger.info("get_course_by_student_id %d res: %s", userid, res)
        return res

    def get_course_by_teacher_id(self, teacherid: int) -> list[courseModel]:
        logger.info("get_course_by_teacher_id: %d", teacherid)

        query: str = "SELECT courseid, name, info, teacherid FROM course WHERE teacherid = %s"
        cursor = self.database_connect.cursor()
        cursor.execute(query, (teacherid,))
        res: list[courseModel] = [
            courseModel(
                courseid=int(courseid),
                name=str(name),
                info=str(info),
                teacherid=int(teacherid)
            ) for (courseid, name, info, teacherid) in cursor
        ]

        logger.info("get_course_by_teacher_id %d res: %s", teacherid, res)
        return res

    def create_course(self, course: courseModel) -> bool:
        logger.info("create_course: %s", course)

        query: str = """
        INSERT INTO course (name, info, teacherid) 
        VALUES (%(name)s, %(info)s, %(teacherid)s)
        """
        cursor = self.database_connect.cursor()
        try:
            cursor.execute(query, {
                "name": course.name,
                "info": course.info,
                "teacherid": course.teacherid
            })
            self.database_connect.commit()
        except Error as e:
            logger.error(e)
            return False
        return True


    def delete_course(self, courseid: int) -> bool:
        logger.info("delete_course: %d", courseid)

        query: str = "DELETE FROM course WHERE courseid = %s"
        cursor = self.database_connect.cursor()
        try:
            cursor.execute(query, (courseid,))
            self.database_connect.commit()
        except Error as e:
            logger.error(e)
            return False
        return True


    def select_course(self, courseid: int, userid: int) -> bool:
        logger.info("select_course: %d %d", courseid, userid)

        query: str = """
        INSERT INTO stu_course (courseid, userid)
        VALUES (%s, %s)
        """
        cursor = self.database_connect.cursor()
        try:
            cursor.execute(query, (courseid, userid))
            self.database_connect.commit()
        except Error as e:
            logger.error(e)
            return False
        return True

    def cancel_course(self, courseid: int, userid: int) -> bool:
        logger.info("cancel_course: %d %d", courseid, userid)

        query: str = "DELETE FROM stu_course WHERE courseid = %s AND userid = %s"
        cursor = self.database_connect.cursor()
        try:
            cursor.execute(query, (courseid, userid))
            self.database_connect.commit()
        except Error as e:
            logger.error(e)
            return False
        return True

    def get_unselected_course(self, userid: int) -> list[select_course_rep] | None:
        logger.info("get_unselected_course: %d", userid)
        sql = """
        SELECT course.courseid, course.name, course.info, course.teacherid, user.username
          FROM course
          JOIN user
            ON course.teacherid = user.userid
         WHERE course.courseid NOT IN (
            SELECT courseid
              FROM stu_course
             WHERE userid = %s
         )
        """
        try:
            cursor = self.database_connect.cursor()
            cursor.execute(sql, (userid,))
            res: list[select_course_rep] = [
                select_course_rep(
                    courseid=int(courseid),
                    name=str(name),
                    info=str(info),
                    teacherid=int(teacherid),
                    teachername=str(teachername)
                ) for (courseid, name, info, teacherid, teachername) in cursor
            ]
            logger.info("get_unselected_course userid = %d: %s", userid, res)
        except Error as e:
            logger.error(e)
            return None
        return res

def get_course() -> Course:
    return Course(database_connection)
