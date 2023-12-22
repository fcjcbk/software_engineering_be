from db import database_connection
from pydantic import BaseModel
from typing import Union
from mysql.connector import Error
from logger import get_logger

logger = get_logger(__name__)

class choiceModel(BaseModel):
    choiceid: int
    content: str
    problemid: int
    label: str


class problemModel(BaseModel):
    problemid: int
    name: str
    problemType: str
    content: str
    point: float
    difficult: str
    homeworkid: int
    choice: list[choiceModel]
