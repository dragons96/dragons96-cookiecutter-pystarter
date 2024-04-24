import os
from loguru import logger


def mkdir(dir_path: str):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        logger.success('创建目录: {}', dir_path)
        return
    logger.warning('目录已存在: {}, 忽略', dir_path)


def create_file(filepath: str, content='', encoding='utf-8', override=False):
    exists = os.path.exists(filepath)
    if override and exists:
        os.remove(filepath)
        exists = False
        logger.warning('删除文件: {}', filepath)
    if not exists:
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
        logger.success('创建文件: {}', filepath)
        return
    logger.warning('文件已存在: {}, 忽略', filepath)
