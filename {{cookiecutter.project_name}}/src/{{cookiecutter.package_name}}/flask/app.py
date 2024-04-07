from flask import Flask
from dragons96_tools.models import R
from uvicorn.middleware.wsgi import WSGIMiddleware
from {{ cookiecutter.package_name }}.logger import setup, setup_uvicorn
from loguru import logger

# 设置日志文件
setup('flask_{{ cookiecutter.project_name }}.log')
setup_uvicorn('flask_uvicorn_{{ cookiecutter.project_name }}.log')
app = Flask(__name__)


@app.get('/')
def hello():
    logger.info('Hello {{cookiecutter.project_name}} by Flask!')
    return R.ok(data='Hello {{cookiecutter.project_name}} by Flask!')


# wsgi 转 asgi
asgi_app = WSGIMiddleware(app)
