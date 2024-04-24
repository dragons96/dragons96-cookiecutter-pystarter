import os
from loguru import logger


def mkdir(dir_path: str):
    """创建目录"""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        logger.success('创建目录: {}', dir_path)
        return
    logger.warning('目录已存在: {}, 忽略', dir_path)


def create_file(filepath: str, content='', encoding='utf-8', override=False):
    """创建文件"""
    exists = os.path.exists(filepath)
    if override and exists:
        os.remove(filepath)
        exists = False
        logger.info('删除文件: {}', filepath)
    if not exists:
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
        logger.success('创建文件: {}', filepath)
        return
    logger.warning('文件已存在: {}, 忽略', filepath)


def add_poetry_script(project_idr: str, script: str):
    """新增poetry启动脚本"""
    pyproject_toml = project_idr + os.sep + 'pyproject.toml'
    if not os.path.exists(pyproject_toml):
        logger.error('pyproject.toml文件不存在, 无法添加poetry执行脚本')
        return
    with open(pyproject_toml, 'r', encoding='utf-8') as f:
        content = f.read()
    if script in content:
        logger.warning('脚本[{}]已存在, 无需重复添加', script)
        return
    content = content.replace('[tool.poetry.scripts]', f'[tool.poetry.scripts]\n{script}')
    with open(pyproject_toml, 'w', encoding='utf-8') as f:
        f.write(content)
    logger.success('新增poetry执行脚本: [poetry run {}]', script.split('=')[0].strip())
