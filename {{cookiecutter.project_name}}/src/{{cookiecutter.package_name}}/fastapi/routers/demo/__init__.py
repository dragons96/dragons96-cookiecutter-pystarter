# 示例业务路由
from fastapi import APIRouter
from {{cookiecutter.package_name}}.fastapi.routers.demo.models import Demo


demo_router = APIRouter(prefix='/demo', tags=['示例模块'])


@demo_router.post("/create", response_model=Demo, summary="Create an demo")
async def create_demo(demo: Demo):
    """
    Create an demo with all the information:

    - **name**: each demo must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the demo doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this demo
    """
    return demo
