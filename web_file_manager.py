"""
web文件管理

created by feather
2019/09/24
"""

import view_func              # 导入该文件, 是为了运行该文件的代码, 注册视图函数
import api                         # 注册api视图函数
import hook                     # 注册钩子
from exts import app

if __name__ == '__main__':
    app.run()
