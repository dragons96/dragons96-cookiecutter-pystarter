import os
from gen.generators.common import mkdir, create_file, extract_names, add_poetry_script, str_format, add_docker_compose_script


def generate_cmd(project_dir: str, package_dir: str, override: bool = False,
                 command: str = None):
    """生成poetry cmd命令"""
    cmd_dir = package_dir + os.sep + 'cmd'
    cmd_init_py = cmd_dir + os.sep + '__init__.py'
    mkdir(cmd_dir)
    # 该文件不覆盖, 防止影响其他逻辑
    create_file(cmd_init_py)
    names = extract_names(command)
    cmd_name = '_'.join(names)
    names.append('main')
    cmd_main_name = '_'.join(names)
    cmd_py = cmd_dir + os.sep + cmd_main_name + '.py'
    create_file(cmd_py, '''import os
import click
from loguru import logger
from {{ cookiecutter.package_name }}.config import cfg
from {{ cookiecutter.package_name }}.logger import setup
from typing import Optional


@click.command()
@click.option('--project_dir', default=None, help='项目目录, 未打包无需传该参数, 自动基于项目树检索')
@click.option('--env', default='dev', help='运行环境, dev=测试环境, test=测试环境, pro=正式环境, 默认: dev')
@click.option('--log_level', default='INFO',
              help='日志级别, DEBUG=调试, INFO=信息, WARNING=警告, ERROR=错误, CRITICAL=严重, 默认: INFO')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main(project_dir: Optional[str] = None,
         env: Optional[str] = 'dev',
         log_level: Optional[str] = 'INFO') -> None:
    """{{cookiecutter.friendly_name}} cmd."""
    if project_dir:
        os.environ['PROJECT_DIR'] = project_dir
    if env:
        os.environ['ENV'] = env
    # 设置日志文件
    file_name = cfg().project_name + '.' + os.path.basename(__file__).split('.')[0]
    setup('{}.log'.format(file_name), level=log_level)
    logger.info('运行成功, 当前项目: {}', cfg().project_name)


if __name__ == "__main__":
    main()
''', override=override)
    add_poetry_script(project_dir, command + str_format('${command} = "{{cookiecutter.package_name}}.cmd.${cmd_main_name}:main"',
                                                        command=command,
                                                        cmd_main_name=cmd_main_name))
    bin_dir = project_dir + os.sep + 'bin'
    bin_file = bin_dir + os.sep + cmd_name + '.sh'
    create_file(bin_file, str_format('''# 获取脚本文件目录
BIN_DIR=$(dirname "$(readlink -f "$0")")
# 获取项目目录
PROJECT_DIR=$(dirname "$BIN_DIR")
echo "当前项目路径: $PROJECT_DIR"
# 进入目录
cd "$PROJECT_DIR"
echo "切换到项目目录: $PROJECT_DIR"
echo "拉取最新项目代码"
git pull
echo "切换虚拟环境"
source venv/bin/activate
echo "开始安装生产环境依赖"
poetry install --only main
echo "安装生产环境依赖完成"
# 执行命令
echo "开始执行命令"
poetry run ${command} --env pro >> /dev/null 2>&1
echo "执行成功"
echo "退出虚拟环境"
deactivate
''', command=command), override=override)

    dockerfile_file = project_dir + os.sep + cmd_name + '.Dockerfile'
    create_file(dockerfile_file, str_format('''FROM python:3.9

WORKDIR /app

COPY . /app

# 系统时区改为上海
RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone

RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple pip

RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple poetry

RUN poetry lock

RUN poetry install --only main

CMD poetry run ${command} --env pro
''', command=command))
    add_docker_compose_script(project_dir, str_format('''  ${cmd_name}:
    container_name: {{cookiecutter.project_name}}_${cmd_name}
    build:
      context: .
      dockerfile: ${cmd_name}.Dockerfile
    image: {{cookiecutter.project_name}}_${cmd_name}:latest
    volumes:
      - ".:/app"
''', cmd_name=cmd_name))
