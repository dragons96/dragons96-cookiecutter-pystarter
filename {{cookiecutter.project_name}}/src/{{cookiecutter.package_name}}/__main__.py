import click
from loguru import logger
from {{ cookiecutter.package_name }}.config import cfg


@click.command()
@click.version_option(version="1.0.0")
def main() -> None:
    """{{cookiecutter.friendly_name}}."""
    logger.info('运行成功, 当前项目: {}', cfg.project_name)


if __name__ == "__main__":
    main()  # pragma: no cover
