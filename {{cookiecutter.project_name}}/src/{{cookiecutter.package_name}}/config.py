import os
from loguru import logger
from {{cookiecutter.package_name}}.models.config import Config

_cfg = None


def load_config(project_dir: str):
    """
    加载配置
    :param project_dir: 项目目录地址
    """
    # 配置目录
    config_dir = project_dir + os.sep + 'config'
    # 当前项目的配置文件 (若需要做多环境配置自行修改, 推荐使用dragons96_tools.env环境工具)
    config_file_path = config_dir + os.sep + f'application.yml'
    global _cfg
    if not os.path.exists(config_file_path):
        logger.warning('未找到配置文件[{}], 忽略配置', config_file_path)
        _cfg = Config()
        return
    # 配置对象 cfg
    logger.debug('开始尝试使用[dragons96_tools]包加载系统配置文件[{}]', config_file_path)
    try:
        from dragons96_tools.files import AutoDataFileLoader
        _data_file_loader = AutoDataFileLoader()
        # 配置对象
        _cfg = _data_file_loader.load_file(config_file_path,
                                          encoding='utf-8',
                                          modelclass=Config) or Config()
        logger.debug('使用[dragons96_tools]包加载配置成功')
    except ImportError:
        logger.debug('当前未导入[dragons96_tools]包, 开始尝试使用[pyyaml]加载配置[{}]', config_file_path)
        try:
            import yaml
            with open(config_file_path, encoding='utf-8') as f:
                config_data = f.read()
            _cfg = Config(**(yaml.safe_load(config_data)))
            logger.debug('使用[pyyaml]包加载配置成功')
        except ImportError:
            logger.warning('当前未导入[pyyaml]包, 无法加载系统配置')
            _cfg = Config()


def cfg() -> Config:
    """
    获取配置对象
    Returns:
        配置对象
    """
    global _cfg
    if not _cfg:
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        logger.debug('未设置项目目录, 自动设置项目目录: [{}]', project_dir)
        load_config(project_dir)
    return _cfg
