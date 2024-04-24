import os
from {{ cookiecutter.package_name }}.cmd.generator.common import mkdir, create_file


def generate_fastapi(package_dir: str, override: bool = False):
    """生成fastapi代码模板"""
    def gen_fastapi_dir():
        """生成fastapi目录"""
        fastapi_dir = package_dir + os.sep + 'fastapi'
        fastapi_init_py = fastapi_dir + os.sep + '__init__.py'
        fastapi_app_py = fastapi_dir + os.sep + 'app.py'
        mkdir(fastapi_dir)
        create_file(fastapi_init_py, override=override)
        create_file(fastapi_app_py, """from fastapi import FastAPI
from dragons96_tools.fastapi import wrapper_exception_handler
from dragons96_tools.models import R
from {{cookiecutter.package_name}}.logger import setup, setup_uvicorn
from {{cookiecutter.package_name}}.fastapi.routers.api import api_router
from loguru import logger

# 设置日志文件
setup('fastapi_{{ cookiecutter.project_name }}.log')
setup_uvicorn('fastapi_uvicorn_{{ cookiecutter.project_name }}.log')
app = FastAPI()


@app.get('/')
def hello():
    logger.info('Hello {{ cookiecutter.project_name }} by FastAPI!')
    return R.ok(data='Hello {{ cookiecutter.project_name }} by FastAPI!')


app = wrapper_exception_handler(app)
app.include_router(api_router)
""", override=override)
        routers_dir = fastapi_dir + os.sep + 'routers'
        router_init_py = routers_dir + os.sep + '__init__.py'
        mkdir(routers_dir)
        create_file(router_init_py, override=override)

    def gen_fastapi_cmd():
        """生成fastapi命令行工具"""
        cmd_dir = package_dir + os.sep + 'cmd'
        fastapi_cmd_main_py = cmd_dir + os.sep + 'fastapi_main.py'
        create_file(fastapi_cmd_main_py, '''import os
import multiprocessing
import click
from loguru import logger
from {{cookiecutter.package_name}}.config import cfg
from {{cookiecutter.package_name}}.logger import setup, setup_uvicorn
from dragons96_tools.env import get_env
from typing import Optional
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
         host: Optional[str] = '127.0.0.1',
         port: Optional[int] = 8000,
         workers: Optional[int] = 1,
         env: Optional[str] = 'dev',
         log_level: Optional[str] = 'INFO',
         reload: Optional[bool] = None) -> None:
    """{{cookiecutter.friendly_name}} FastAPI cmd."""
    if project_dir:
        os.environ['PROJECT_DIR'] = project_dir
    if env:
        os.environ['ENV'] = env
    if reload is None:
        reload = get_env().is_dev()
    setup('fastapi_{}.log'.format(cfg().project_name), level=log_level)
    setup_uvicorn('fastapi_uvicorn_{}.log'.format(cfg().project_name), level=log_level)
    logger.info('运行成功, 当前项目: {}', cfg().project_name)
    uvicorn.run('{{cookiecutter.package_name}}.fastapi.app:app', host=host, port=port, workers=workers, reload=reload)


if __name__ == "__main__":
    # windows 多进程需要执行该方法, linux 与 mac 执行无效不影响
    multiprocessing.freeze_support()
    main()
''', override=override)

    gen_fastapi_dir()
    gen_fastapi_cmd()
