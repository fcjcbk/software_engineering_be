from db import database_connection
from pydantic import BaseModel
from typing import Union
from mysql.connector import Error
from logger import get_logger

logger = get_logger(__name__)


class UserModel(BaseModel):
    userid: int
    username: str
    password: str
    email:  str
    role: int
    telephone: str
    major: str


class User:
    def __init__(self, database_conect):
        self.database_connect = database_conect


    def get_users(self) -> list[UserModel]:
        query: str = "SELECT userid, username, password, email, role, telephone, major FROM user"
        cursor = self.database_connect.cursor()
        cursor.execute(query)
        res: list[UserModel] = [
            UserModel(
                userid=int(userid),
                username=str(username),
                password=str(password),
                email=str(email),
                role=int(role),
                telephone=str(telephone),
                major=str(major)
            ) for (userid, username, password, email, role, telephone, major) in cursor
        ]
        return res

    def get_user_by_id(self, userid: int) -> Union[UserModel, None]:
        query: str = "SELECT userid, username, password, email, role, telephone, major FROM user WHERE userid = %s"
        cursor = self.database_connect.cursor()
        cursor.execute(query, (userid,))
        row = cursor.fetchone()
        if row is None:
            return None

        userid, username, password, email, role, telephone, major = row

        user = UserModel(
            userid=int(userid),
            username=str(username),
            password=str(password),
            email=str(email),
            role=int(role),
            telephone=str(telephone),
            major=str(major)
        )
        return user


    def insert_user(self, new_user: UserModel) -> bool:
        sql: str = """
        INSERT INTO user (userid, username, password, email, role, telephone, major) 
        VALUES (%(userid)s, %(username)s, %(password)s, %(email)s, %(role)s, %(telephone)s, %(major)s)
        """
        cursor = self.database_connect.cursor()
        try:
            cursor.execute(sql, dict(new_user))
            self.database_connect.commit()
        except Error as e:
            logger.error(e)
            return False
        return True


    def update_user(self, new_user: UserModel) -> bool:
        sql: str = """
            UPDATE user 
            SET username = %(username)s, 
                password = %(password)s, 
                email = %(email)s, 
                role = %(role)s, 
                telephone = %(telephone)s, 
                major = %(major)s
            WHERE userid = %(userid)s
        """
        cursor = self.database_connect.cursor()
        try:
            cursor.execute(sql, vars(new_user))
            self.database_connect.commit()
        except Error as e:
            logger.error(e)
            return False
        return True


    def get_by_email(self, email: str) -> Union[UserModel, None]:
        query: str = "SELECT userid, username, password, email, role, telephone, major FROM user WHERE email = %s"
        cursor = self.database_connect.cursor()
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        if row is None:
            return None

        userid, username, password, email, role, telephone, major = row

        user = UserModel(
            userid=int(userid),
            username=str(username),
            password=str(password),
            email=str(email),
            role=int(role),
            telephone=str(telephone),
            major=str(major)
        )
        return user


def get_User() -> User:
    return User(database_connection)
