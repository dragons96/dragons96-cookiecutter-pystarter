from typing import Optional
try:
    from dragons96_tools.models import BaseModel
except ImportError:
    from pydantic import BaseModel


class CommonDBConfig(BaseModel):
    """通用 DB 配置"""
    host: Optional[str] = ''
    port: Optional[int] = 0
    user: Optional[str] = ''
    password: Optional[str] = ''
    db: Optional[str] = None


class MysqlConfig(CommonDBConfig):
    """Mysql 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 3306
    user: Optional[str] = 'root'


class RedisConfig(CommonDBConfig):
    """Redis 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 6379


class ImpylaConfig(CommonDBConfig):
    """Impala 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 21050


class ClickhouseConfig(CommonDBConfig):
    """Clickhouse 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 8123
    user: Optional[str] = 'root'


class Config(BaseModel):
    """ 自定义配置项, 与config/application.yml 保持一致 """
    project_name: Optional[str] = 'undefined_project_name'

