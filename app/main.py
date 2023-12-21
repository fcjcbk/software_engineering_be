from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from logger import get_logger
from db.user import get_User
from routers.user import verify_router, user_router

logger = get_logger(__name__)

app = FastAPI(debug=True)

app.include_router(verify_router)
app.include_router(user_router)

@app.get("/home")
async def test():
    model= get_User()
    lt = model.get_users()
    return lt
