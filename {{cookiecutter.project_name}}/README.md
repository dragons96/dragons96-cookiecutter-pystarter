# {{ cookiecutter.friendly_name }}

### 项目仓库地址: https://{{cookiecutter.git_type}}.com_/{{cookiecutter.git_user}}/{{ cookiecutter.project_name }}

## 安装依赖
1. pip install poetry
2. poetry lock --no-update
3. 开发环境安装依赖：poetry install (若出现哪个包安装不了先单独pip install 某个包再执行poetry install)
4. 正式环境安装依赖：poetry install --only main (若出现哪个包安装不了先单独pip install 某个包再执行poetry install)

## 运行
1. 运行 `poetry run main`, 对应 `src/{{ cookiecutter.package_name }}/cmd/main.py` (见`pyproject.toml`的`[tool.poetry.scripts]`配置)

## fastapi 配置
1. poetry add fastapi uvicorn[standard]
2. 运行 `poetry run fastapi_main`, 对应 `src/{{ cookiecutter.package_name }}/cmd/fastapi_main.py`

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
1. 安装, `poetry add --dev pyinstaller`
2. 打包, `pyinstaller --onefile ./src/{{cookiecutter.package_name}}/__main__.py`
3. 运行, `./dist/{{cookiecutter.package_name}}.exe --project_dir .` 或 `./dist/{{cookiecutter.package_name}} --project_dir .`
