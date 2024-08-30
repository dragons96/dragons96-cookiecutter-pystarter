from typing import Union
from dragons96_tools.sqlalchemy import SqlAlchemyClient, AsyncSqlAlchemyClient
from dragons96_tools.env import get_env
from {{cookiecutter.package_name}}.config import cfg
from {{cookiecutter.package_name}}.models.config import CommonDBConfig
from sqlalchemy import URL
from loguru import logger

__db_map = {}


def db_select(_id: Union[str, CommonDBConfig]) -> Union[SqlAlchemyClient, AsyncSqlAlchemyClient]:
    """
    DB客户端选择器
    Args:
        _id: 在{{cookiecutter.package_name}}.models.config.Config.db 中定义的名称属性名称 或者 数据库配置对象
            假设配置了一个sqlite的数据源, 定义属性名称为sqlite_xxx_db, 示例:
                class MultiDBConfig(BaseModel):
                    sqlite_xxx_db: Optional[CommonDBConfig] = CommonDBConfig()
            则可通过 db_select('sqlite_xxx_db') 或 db_select(cfg().db.sqlite_xxx_db) 获取对应的DB客户端
    Returns:
        SqlAlchemyClient|AsyncSqlAlchemyClient: DB客户端, 根据配置的is_async决定返回同步还是异步客户端
    """
    if isinstance(_id, str):
        db_config = cfg().db
        try:
            config: CommonDBConfig = getattr(db_config, _id)
        except AttributeError:
            raise ValueError('未配置名称为[{}]的DB配置'.format(_id))
    else:
        config, _id = _id, str(__gen_sqlalchemy_url(_id))
    client = __db_map.get(_id)
    if client:
        return client
    return __new_sqlalchemy_client(config, _id)


def __gen_sqlalchemy_url(config: CommonDBConfig):
    return URL.create(config.sqlalchemy_schema,
                      host=config.host,
                      port=config.port,
                      username=config.user,
                      password=config.password,
                      database=config.db)


def __new_sqlalchemy_client(config: CommonDBConfig, _id: str) -> Union[SqlAlchemyClient, AsyncSqlAlchemyClient]:
    url = __gen_sqlalchemy_url(config)
    logger.info('初始化ID[{}]的SqlAlchemyClient, 连接串[{}]', _id, url)
    client_cls = AsyncSqlAlchemyClient if config.is_async else SqlAlchemyClient
    # hive 需要额外处理
    if config.sqlalchemy_schema == 'hive':
        try:
            from pyhive import hive
        except ImportError as e:
            logger.error('未安装pyhive依赖, sqlalchemy无法配置hive')
            raise e
        client = client_cls(url=url, echo=not get_env().is_pro(),
                                  creator=lambda: hive.Connection(
                                      host=config.host, port=config.port, username=config.user, database=config.db)
                                  )
    else:
        client = client_cls(url=url, echo=not get_env().is_pro())
    __db_map[_id] = client
    return client
