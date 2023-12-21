from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
from logger import get_logger
from db.user import get_User
from routers.user import verify_router, user_router, token_router

logger = get_logger(__name__)

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["HEAD", "GET", "POST", "PUT", "DELETE, PATCH, OPTIONS"],
    allow_headers=["authorization", "origin", "content-type", "accept"],
)


app.include_router(token_router)
app.include_router(verify_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")

# for test may delete later
@app.get("/home")
async def test():
    model= get_User()
    lt = model.get_users()
    return lt
