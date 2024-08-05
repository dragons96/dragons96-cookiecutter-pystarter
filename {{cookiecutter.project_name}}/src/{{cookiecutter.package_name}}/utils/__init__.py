

def is_pyinstaller_env():
    """判断是否是pyinstaller环境"""
    import sys
    return hasattr(sys, 'frozen')
