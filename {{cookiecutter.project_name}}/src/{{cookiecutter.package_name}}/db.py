from dragons96_tools.sqlalchemy import SqlAlchemyClient
from dragons96_tools.env import get_env
from {{cookiecutter.package_name}}.config import cfg
from {{cookiecutter.package_name}}.models.config import CommonDBConfig
from loguru import logger

__db_map = {}


def db_select(_id: str) -> SqlAlchemyClient:
    """
    DB客户端选择器
    Args:
        _id: 在{{cookiecutter.package_name}}.models.config.Config.db 中定义的名称属性名称
            假设配置了一个sqlite的数据源, 定义属性名称为sqlite_xxx_db, 示例:
                class MultiDBConfig(BaseModel):
                    sqlite_xxx_db: Optional[CommonDBConfig] = CommonDBConfig()
            则可通过 db_select('sqlite_xxx_db') 获取对应的DB客户端
    Returns:
        SqlAlchemyClient: DB客户端
    """
    client = __db_map.get(_id)
    if client:
        return client
    db_config = cfg().db
    try:
        config: CommonDBConfig = getattr(db_config, _id)
    except AttributeError:
        raise ValueError('未配置名称为[{}]的DB配置'.format(_id))
    url = __gen_sqlalchemy_url(config)
    logger.info('初始化ID[{}]的SqlAlchemyClient, 连接串[{}]', _id, url)
    # hive 需要额外处理
    if config.schema == 'hive':
        try:
            from pyhive import hive
        except ImportError as e:
            logger.error('未安装pyhive依赖, sqlalchemy无法配置hive')
            raise e
        client = SqlAlchemyClient(url=url, echo=not get_env().is_pro(),
                                  creator=lambda: hive.Connection(
                                      host=config.host, port=config.port, username=config.user, database=config.db)
                                  )
    else:
        client = SqlAlchemyClient(url=url, echo=not get_env().is_pro())
    __db_map[_id] = client
    return client


def __gen_sqlalchemy_url(config: CommonDBConfig):
    up, hp = None, None
    if config.user:
        up = f'{config.user}:{config.password}'
    if config.host and config.port:
        hp = f'{config.host}:{config.port}'
    if hp and up:
        return f'{config.schema}://{up}@{hp}/{config.db}'
    if hp:
        return f'{config.schema}://{hp}/{config.db}'
    return f'{config.schema}:///{config.db}'
