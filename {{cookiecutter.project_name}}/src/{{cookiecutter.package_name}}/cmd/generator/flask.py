import os
from {{ cookiecutter.package_name }}.cmd.generator.common import mkdir, create_file


def generate_flask(package_dir: str, override: bool = False):
    """生成flask代码模板"""
    def gen_flask_dir():
        """生成flask目录"""
        flask_dir = package_dir + os.sep + 'flask'
        flask_init_py = flask_dir + os.sep + '__init__.py'
        flask_app_py = flask_dir + os.sep + 'app.py'
        mkdir(flask_dir)
        create_file(flask_init_py, override=override)
        create_file(flask_app_py, '''from flask import Flask
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
''', override=override)

    def gen_flask_cmd():
        """生成flask命令行工具"""
        cmd_dir = package_dir + os.sep + 'cmd'
        flask_cmd_main_py = cmd_dir + os.sep + 'flask_main.py'
        create_file(flask_cmd_main_py, '''import os
import multiprocessing
import click
from loguru import logger
from {{ cookiecutter.package_name }}.config import cfg
from {{ cookiecutter.package_name }}.logger import setup, setup_uvicorn
from typing import Optional
from dragons96_tools.env import get_env
import uvicorn


@click.command()
@click.option('--project_dir', default=None, help='项目目录, 未打包无需传该参数, 自动基于项目树检索')
@click.option('--env', default='dev', help='运行环境, dev=测试环境, test=测试环境, pro=正式环境, 默认: dev')
@click.option('--log_level', default='INFO',
              help='日志级别, DEBUG=调试, INFO=信息, WARNING=警告, ERROR=错误, CRITICAL=严重, 默认: INFO')
@click.option('--host', default='127.0.0.1', help='服务允许访问的ip, 若允许所有ip访问可设置0.0.0.0')
@click.option('--port', default=8000, help='服务端口')
@click.option('--workers', default=1, help='工作进程数')
@click.option('--reload', default=None, help='是否热重启服务器, 默认情况下dev环境开始热重启, test与pro环境不热重启, true: 开启, false: 不开启')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main(project_dir: Optional[str] = None,
         env: Optional[str] = 'dev',
         log_level: Optional[str] = 'INFO',
         host: Optional[str] = '127.0.0.1',
         port: Optional[int] = 8000,
         workers: Optional[int] = 1,
         reload: Optional[bool] = None) -> None:
    """Demo FastAPI cmd."""
    if project_dir:
        os.environ['PROJECT_DIR'] = project_dir
    if env:
        os.environ['ENV'] = env
    if reload is None:
        reload = get_env().is_dev()
    setup('flask_{}.log'.format(cfg().project_name), level=log_level)
    setup_uvicorn('flask_uvicorn_{}.log'.format(cfg().project_name), level=log_level)
    logger.info('运行成功, 当前项目: {}', cfg().project_name)
    uvicorn.run('{{cookiecutter.package_name}}.flask.app:asgi_app', host=host, port=port, workers=workers, reload=reload)


if __name__ == "__main__":
    # windows 多进程需要执行该方法, linux 与 mac 执行无效不影响
    multiprocessing.freeze_support()
    main()
''', override=override)

    gen_flask_dir()
    gen_flask_cmd()
