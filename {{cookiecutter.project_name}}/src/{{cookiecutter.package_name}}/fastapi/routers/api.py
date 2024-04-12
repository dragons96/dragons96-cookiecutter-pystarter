from fastapi import APIRouter
from {{cookiecutter.package_name}}.fastapi.routers.demo import demo_router


api_router = APIRouter(prefix='/api')

# 在这里添加api路由
api_router.include_router(demo_router)
