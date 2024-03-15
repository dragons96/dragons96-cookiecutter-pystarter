# {{ cookiecutter.friendly_name }}

### 项目仓库地址: https://{{cookiecutter.git_type}}.com_/{{cookiecutter.git_user}}/{{ cookiecutter.project_name }}

## 安装依赖
1. pip install poetry
2. poetry lock --no-update
3. 开发环境安装依赖：poetry install (若出现哪个包安装不了先单独pip install 某个包再执行poetry install)
4. 正式环境安装依赖：poetry install --only main (若出现哪个包安装不了先单独pip install 某个包再执行poetry install)

## 运行
1. poetry run {{ cookiecutter.project_name }}

## fastapi 配置
1. poetry add fastapi uvicorn
2. 编辑src/{{ cookiecutter.package_name }}/__main__.py文件, 示例如下
```python
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def main():
    return "{{cookiecutter.project_name}}"
```
3. 运行 `poetry run uvicorn {{cookiecutter.package_name}}.__main__:app --host 0.0.0.0 --port 8000`

## 功能说明
### 1.配置管理
1. `config/application.yml` 配置内容, `src/{{ cookiecutter.package_name }}/models/config.py` 里更新`Config`类对应的属性
2. 使用方式如下:
```python
# cfg 为 {{ cookiecutter.package_name }}.models.config.Config 实例
from {{ cookiecutter.package_name }}.config import cfg

print(cfg.project_name)
```

## 拓展
本项目集成[dragons96_tools](https://gitee.com/dragons96/py_dragons96_tools)工具框架

## 部署
