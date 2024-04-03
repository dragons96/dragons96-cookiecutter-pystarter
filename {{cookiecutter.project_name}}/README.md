# {{ cookiecutter.friendly_name }}

### 项目仓库地址: https://{{cookiecutter.git_type}}.com_/{{cookiecutter.git_user}}/{{ cookiecutter.project_name }}

## 安装依赖
1. pip install poetry
2. poetry lock
3. 开发环境安装依赖：poetry install (若出现哪个包安装不了先单独pip install 某个包再执行poetry install)
4. 正式环境安装依赖：poetry install --only main (若出现哪个包安装不了先单独pip install 某个包再执行poetry install)
5. 需要安装新增的依赖, 以sqlalchemy为例, `poetry add sqlalchemy`
6. 安装的依赖仅本地环境需要而正式环境不需要则可使用--group dev参数, 以pyinstaller为例, `poetry add --group dev pyinstaller`

## 运行
1. 运行 `poetry run main`, 对应 `src/{{ cookiecutter.package_name }}/cmd/main.py` (见`pyproject.toml`的`[tool.poetry.scripts]`配置)

## 实践指南
1. 开发cmd命令行工具推荐从`src/{{cookiecutter.package_name}}/cmd/main.py`复制一个新文件作为业务cmd命令行入口进行开发
2. 每开发一个新的cmd命令行工具需在`pyproject.toml`文件的`[tool.poetry.scripts]`下新配置一个poetry命令工具
3. 使用`poetry run xxx`执行开发的cmd命令行工具

## FastAPI 配置
1. poetry add fastapi uvicorn[standard]
2. 运行 `poetry run fastapi_main`, 对应 `src/{{ cookiecutter.package_name }}/cmd/fastapi_main.py`

PS: 若不需要可删除`src/{{cookiecutter.package_name}}/cmd/fastapi_main.py`文件与`src/{{cookiecutter.package_name}}/fastapi`包

## Flask 配置
1. poetry add flask uvicorn[standard]
2. 运行 `poetry run flask_main`, 对应 `src/{{ cookiecutter.package_name }}/cmd/flask_main.py`

PS: 若不需要可删除`src/{{cookiecutter.package_name}}/cmd/flask_main.py`文件与`src/{{cookiecutter.package_name}}/flask`包

## 环境变量
1. PROJECT_DIR: 项目路径, 通常无需设置, 打包后需设置
2. dragons96_tools包提供的ENV: 当前环境, dev=开发环境, test=测试环境, pro=生产环境

## 功能说明
### 1.配置管理
1. `config/application.yml` 配置内容, `src/{{ cookiecutter.package_name }}/models/config.py` 里更新`Config`类对应的属性
2. 使用方式如下:
```python
# cfg 为 {{ cookiecutter.package_name }}.models.config.Config 实例
from {{ cookiecutter.package_name }}.config import cfg

print(cfg().project_name)
```

## 拓展
本项目集成[dragons96_tools](https://gitee.com/dragons96/py_dragons96_tools)工具框架

## 部署


## 打包
### 一、使用pyinstaller打包
安装 `poetry add -D pyinstaller`
#### 1. 打包普通命令行任务
1. 打包, `pyinstaller --onefile ./src/{{cookiecutter.package_name}}/cmd/main.py --name {{cookiecutter.project_name}}`
2. 运行, `./dist/{{cookiecutter.project_name}}.exe --project_dir .` 或 `./dist/{{cookiecutter.project_name}} --project_dir .`
#### 2. 打包FastAPI命令行任务
1. 打包, `pyinstaller --onefile ./src/{{cookiecutter.package_name}}/cmd/fastapi_main.py --hidden-import "{{cookiecutter.package_name}}.fastapi.app" --name fastapi_{{cookiecutter.project_name}}`
2. 运行, `./dist/fastapi_{{cookiecutter.project_name}}.exe --project_dir .` 或 `./dist/fastapi_{{cookiecutter.project_name}} --project_dir .` (更多参数执行`./dist/fastapi_{{cookiecutter.project_name}}.exe -h` 或 `./dist/fastapi_{{cookiecutter.project_name}} -h`)
#### 3. 打包Flask命令行任务
1. 打包, `pyinstaller --onefile ./src/{{cookiecutter.package_name}}/cmd/flask_main.py --hidden-import "{{cookiecutter.package_name}}.flask.app" --name flask_{{cookiecutter.project_name}}`
2. 运行, `./dist/flask_{{cookiecutter.project_name}}.exe --project_dir .` 或 `./dist/flask_{{cookiecutter.project_name}} --project_dir .` (更多参数执行`./dist/flask_{{cookiecutter.project_name}}.exe -h` 或 `./dist/flask_{{cookiecutter.project_name}} -h`)
