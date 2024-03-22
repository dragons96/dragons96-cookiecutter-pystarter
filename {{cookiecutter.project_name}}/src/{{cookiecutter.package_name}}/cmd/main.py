import os
import click
from loguru import logger
from {{ cookiecutter.package_name }}.config import cfg
from typing import Optional


@click.command()
@click.option('--project_dir', default=None, help='项目目录, 未打包无需传该参数, 自动基于项目树检索')
@click.option('--env', default='dev', help='运行环境, dev=测试环境, test=测试环境, pro=正式环境')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main(project_dir: Optional[str] = None,
         env: Optional[str] = 'dev') -> None:
    """{{cookiecutter.friendly_name}} cmd."""
    if project_dir:
        os.environ['PROJECT_DIR'] = project_dir
    if env:
        os.environ['ENV'] = env
    logger.info('运行成功, 当前项目: {}', cfg().project_name)


if __name__ == "__main__":
    main()
