import os
from loguru import logger
from {{cookiecutter.package_name}}.models.config import Config
from dragons96_tools.env import get_env
from dragons96_tools.files import AutoDataFileLoader
from typing import Optional

_cfg: Optional[Config] = None


def _load_config(project_dir: str):
    """
    加载配置
    :param project_dir: 项目目录地址
    """
    # 配置目录
    config_dir = project_dir + os.sep + 'config'
    # 当前项目的配置文件 (若需要做多环境配置自行修改, 推荐使用dragons96_tools.env环境工具)
    config_file_path = config_dir + os.sep + f'application.yml'
    env_config_file_path = config_dir + os.sep + f'application-{get_env().name}.yml'
    exist_config_file_path, exist_env_config_file_path = os.path.exists(config_file_path), os.path.exists(env_config_file_path)
    global _cfg
    if not exist_config_file_path and not exist_env_config_file_path:
        logger.error('未找到配置文件[{}]或[{}], 无法加载配置, 程序终止', config_file_path, env_config_file_path)
        exit(1)
    _data_file_loader = AutoDataFileLoader()
    # 配置对象_cfg
    _cfg_dict = None
    if exist_config_file_path:
        _cfg_dict = _data_file_loader.load_file(config_file_path,
                                                encoding='utf-8')
        logger.info('加载[{}]配置文件', config_file_path)
    if exist_env_config_file_path:
        if _cfg_dict:
            _cfg_dict = _merge_config(_cfg_dict, _data_file_loader.load_file(env_config_file_path,
                                                                             encoding='utf-8'))
        else:
            _cfg_dict = _data_file_loader.load_file(env_config_file_path,
                                                    encoding='utf-8')
        logger.info('加载[{}]配置文件', env_config_file_path)
    _cfg = Config(**_cfg_dict)


def _merge_config(cfg1: dict, cfg2: dict) -> dict:
    """ 合并两个配置, 重复的key用cfg2覆盖cfg1 """
    if not cfg2:
        return cfg1
    for key, value in cfg2.items():
        if key in cfg1 and isinstance(cfg1[key], dict) and isinstance(value, dict):
            _merge_config(cfg1[key], value)
        else:
            cfg1[key] = value
    return cfg1


def get_project_dir() -> str:
    """
    获取项目目录位置
    Returns:
        项目目录路径
    """
    return os.environ.get('PROJECT_DIR', os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def cfg() -> Config:
    """
    获取配置对象
    Returns:
        配置对象
    """
    global _cfg
    if not _cfg:
        project_dir = get_project_dir()
        logger.debug('项目目录: [{}]', project_dir)
        _load_config(project_dir)
    return _cfg
