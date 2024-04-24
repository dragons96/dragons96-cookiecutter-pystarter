import os
from {{cookiecutter.package_name}}.cmd.generators.common import mkdir, create_file, extract_names


def generate_task(project_dir: str, package_dir: str, override: bool = False,
                  task_class: str = None,
                  task_name: str = None,
                  is_async: bool = False,
                  *args, **kwargs):
    """生成任务代码模板"""
    task_dir = package_dir + os.sep + 'tasks'
    task_init_py = task_dir + os.sep + '__init__.py'
    mkdir(task_dir)
    create_file(task_init_py, override=override)

    names = extract_names(task_class)
    task_py = task_dir + os.sep + '_'.join(names) + '.py'
    custom_task_class = ''.join([(name[0].upper() + name[1:]) if len(name) > 1 else name.upper() for name in names])
    create_file(task_py, '''from typing import Any
from dragons96_tools.task import {base_task_class}

class {custom_task_class}(base_task_class):
    """自定义任务"""

    {async_def_prefix}def _run(self, *args, **kwargs) -> Any:
        # todo: 任务具体逻辑
        pass

    def _task_name(self) -> str:
        # todo: 任务名称
        return {task_name}
'''.format(base_task_class='AsyncTask' if is_async else 'Task', custom_task_class=custom_task_class,
           async_def_prefix='async ' if is_async else '', task_name=task_name))
