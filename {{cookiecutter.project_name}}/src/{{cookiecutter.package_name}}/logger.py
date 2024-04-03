from loguru import logger
from {{cookiecutter.package_name}}.config import cfg
from dragons96_tools.logger import setup as _setup


def setup(file_name,
          rotation="1 days",
          serialize=True,
          backtrace=True,
          diagnose=False,
          retention="3 days",
          level='INFO'):
    logger.configure(extra={'project_name': cfg().project_name})
    _setup(f'./logs/{file_name}',
           rotation=rotation,
           serialize=serialize,
           backtrace=backtrace,
           diagnose=diagnose,
           retention=retention,
           level=level)
