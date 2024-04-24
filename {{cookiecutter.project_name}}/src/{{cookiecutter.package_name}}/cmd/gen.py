import os
import click
from loguru import logger
from {{ cookiecutter.package_name }}.cmd.generators import *
from {{ cookiecutter.package_name }}.config import get_project_dir


@click.command()
@click.argument('template', type=click.Choice(['fastapi', 'flask']), help='选择模板')
@click.option('--override', default=False, help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main(template: str, override: bool) -> None:
    """代码生成命令行工具"""
    project_dir = get_project_dir()
    package_dir = project_dir + os.sep + 'src' + os.sep + '{{cookiecutter.package_name}}'
    if template == 'fastapi':
        logger.info('开始生成[fastapi]模板代码')
        generate_fastapi(project_dir, package_dir, override=override)
        logger.success('生成[fastapi]模板代码完成')
    elif template == 'flask':
        logger.info('开始生成[flask]模板代码')
        generate_flask(project_dir, package_dir, override=override)
        logger.success('生成[flask]模板代码完成')


if __name__ == "__main__":
    main()
