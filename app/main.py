from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.logger import get_logger
from app.db import close
from app.db.user import get_User
from app.routers.user import verify_router, user_router
from app.routers.course import course_router
from app.routers.homework import homework_router
from app.routers.solution import solution_router
from app.routers.problem import problem_router
from app.routers.attempt import attempt_router
from app.routers.comment import comment_router

logger = get_logger(__name__)

@asynccontextmanager
async def lifesapn(server: FastAPI):
    yield
    logger.info("shutdown")
    close()

app = FastAPI(debug=True, lifespan=lifesapn)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["HEAD", "GET", "POST", "PUT", "DELETE, PATCH, OPTIONS"],
    allow_headers=["authorization", "origin", "content-type", "accept"],
)

# the path may be change
app.include_router(verify_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(course_router, prefix="/api/v1")
app.include_router(homework_router, prefix="/api/v1")
app.include_router(problem_router, prefix="/api/v1")
app.include_router(solution_router, prefix="/api/v1")
app.include_router(attempt_router, prefix="/api/v1")
app.include_router(comment_router, prefix="/api/v1")

# for test may delete later
@app.get("/home")
async def test():
    model= get_User()
    lt = model.get_users()
    return lt
