from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
from logger import get_logger
from db import close
from db.user import get_User
from routers.user import verify_router, user_router
from routers.course import course_router
from routers.homework import homework_router
from routers.solution import solution_router
from routers.problem import problem_router
from routers.attempt import attempt_router
from routers.comment import comment_router

logger = get_logger(__name__)

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["HEAD", "GET", "POST", "PUT", "DELETE, PATCH, OPTIONS"],
    allow_headers=["authorization", "origin", "content-type", "accept"],
)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("shutdown")
    close()

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
