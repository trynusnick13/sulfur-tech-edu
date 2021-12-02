from fastapi import APIRouter
from app.Controllers import auth, ready, user, courses

router_auth = APIRouter(prefix='/auth')
router_auth.include_router(auth.auth_route, tags=['auth'])

router_user = APIRouter(prefix='/user')
router_user.include_router(user.user_route, tags=['user'])

router_courses = APIRouter(prefix='/course')
router_courses.include_router(courses.course_route, tags=['course'])

router_ready = APIRouter(prefix='/api')
router_ready.include_router(ready.ready_route, tags=['ready'])