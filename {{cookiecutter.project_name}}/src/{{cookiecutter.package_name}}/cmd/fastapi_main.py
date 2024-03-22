import os
import multiprocessing
import click
from loguru import logger
from {{ cookiecutter.package_name }}.config import cfg
from typing import Optional
import uvicorn


@click.command()
@click.option('--project_dir', default=None, help='项目目录, 未打包无需传该参数, 自动基于项目树检索')
@click.option('--port', default=8000, help='服务端口')
@click.option('--workers', default=1, help='工作进程数')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main(project_dir: Optional[str] = None,
         port: Optional[int] = 8000,
         workers: Optional[int] = 1) -> None:
    """{{cookiecutter.friendly_name}} FastAPI cmd."""
    if project_dir:
        os.environ['PROJECT_DIR'] = project_dir
    logger.info('运行成功, 当前项目: {}', cfg().project_name)
    uvicorn.run('{{cookiecutter.package_name}}.fastapi.app:app', host='0.0.0.0', port=port, workers=workers)


if __name__ == "__main__":
    # windows 多进程需要执行该方法, linux 与 mac 执行无效不影响
    multiprocessing.freeze_support()
    main()
