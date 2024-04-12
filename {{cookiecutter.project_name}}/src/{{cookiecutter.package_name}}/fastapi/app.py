from fastapi import FastAPI
from dragons96_tools.fastapi import wrapper_exception_handler
from dragons96_tools.models import R
from {{ cookiecutter.package_name }}.logger import setup, setup_uvicorn
from {{cookiecutter.package_name}}.fastapi.routers.api import api_router
from loguru import logger

# 设置日志文件
setup('fastapi_{{ cookiecutter.project_name }}.log')
setup_uvicorn('fastapi_uvicorn_{{ cookiecutter.project_name }}.log')
app = FastAPI()


@app.get('/')
def hello():
    logger.info('Hello {{cookiecutter.project_name}} by FastAPI!')
    return R.ok(data='Hello {{cookiecutter.project_name}} by FastAPI!')


app = wrapper_exception_handler(app)
app.include_router(api_router)
