from typing import Optional
from dragons96_tools.models import BaseModel


class CommonDBConfig(BaseModel):
    """通用 DB 配置"""
    host: Optional[str] = ''
    port: Optional[int] = 0
    user: Optional[str] = ''
    password: Optional[str] = ''
    db: Optional[str] = None
    # sqlalchemy的schema, 仅使用sqlalchemy需要配置, 例如:sqlite, mysql+pymysql等等
    sqlalchemy_schema: Optional[str] = None


class MysqlConfig(CommonDBConfig):
    """Mysql 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 3306
    user: Optional[str] = 'root'
    sqlalchemy_schema: Optional[str] = 'mysql+pymysql'


class RedisConfig(CommonDBConfig):
    """Redis 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 6379


class HiveConfig(CommonDBConfig):
    """Hive 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 10000
    sqlalchemy_schema: Optional[str] = 'hive'


class ImpylaConfig(CommonDBConfig):
    """Impala 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 21050
    sqlalchemy_schema: Optional[str] = 'impala'


class ClickhouseConfig(CommonDBConfig):
    """Clickhouse 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 8123
    user: Optional[str] = 'root'
    sqlalchemy_schema: Optional[str] = 'clickhouse'


class MultiDBConfig(BaseModel):
    """多 DB 配置"""


class Config(BaseModel):
    """ 自定义配置项, 与config/application.yml 保持一致 """
    project_name: Optional[str] = 'undefined_project_name'
    log_dir: Optional[str] = './logs'
    db: Optional[MultiDBConfig] = MultiDBConfig()
