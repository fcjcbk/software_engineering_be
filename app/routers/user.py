from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import secure
from db import user
from logger import get_logger

logger = get_logger(__name__)
verify_router = APIRouter()

@verify_router.post("/register")
async def register(register_user: user.UserModel, response_model=user.UserModel):
    store_user = user.get_User()

    usr = store_user.get_user_by_id(register_user.userid)
    if usr is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User already exist",
        )

    register_user.password = secure.get_password_hash(register_user.password)
    ok: bool = store_user.insert_user(register_user)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Insert fail",
        )
    return register_user


class login_request(BaseModel):
    account: str
    password: str


@verify_router.post("/login")
async def login(form_data: login_request, response_model=secure.Token):
    """
    登录接口 返回token

    - **account**: 用户的账号，可以是电子邮件或用户ID(ID为数字)
    - **password**: 用户的密码
    """
    store_user = user.get_User()

    usr = None
    if '@' in form_data.account:
        usr = store_user.get_by_email(form_data.account)
    elif form_data.account.isdigit():
        usr = store_user.get_user_by_id(int(form_data.account))
    if usr is None:
        logger.info("User not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    if not secure.verify_password(form_data.password, usr.password):
        logger.info("Password incorrect")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    token: secure.Token = secure.create_token(
        secure.TokenData(userid=usr.userid, role=usr.role)
    )
    return token

token_router = APIRouter()
@token_router.post("/token", response_model=secure.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    store_user = user.get_User()

    if '@' in form_data.username:
        usr = store_user.get_by_email(form_data.username)
    else:
        usr = store_user.get_user_by_id(int(form_data.username))
    if usr is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    if not secure.verify_password(form_data.password, usr.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token: secure.Token = secure.create_token(
        secure.TokenData(userid=usr.userid, role=usr.role)
    )
    return token


user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(secure.decode_token)],
    # Todo: response may be change
    responses={404: {"msg": "no such user"}}
)

# Todo: response_model may be change
@user_router.get("/{userid}")
async def get_user_info(userid: int, response_model=user.UserModel):
    store_user = user.get_User()
    usr = store_user.get_user_by_id(userid)
    if usr is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return usr
