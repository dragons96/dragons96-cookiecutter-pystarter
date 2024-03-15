import click
from loguru import logger
from {{ cookiecutter.package_name }}.config import load_config, cfg
from typing import Optional


@click.command()
@click.option('--project_dir', default=None, help='项目目录, 未打包无需传该参数, 自动基于项目树检索')
@click.version_option(version="1.0.0")
def main(project_dir: Optional[str] = None) -> None:
    """{{cookiecutter.friendly_name}}."""
    if project_dir:
        load_config(project_dir)
    logger.info('运行成功, 当前项目: {}', cfg().project_name)


if __name__ == "__main__":
    main()
