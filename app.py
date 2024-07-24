"""
web文件管理

created by feather
2019/09/24
"""

import view_func              # 导入该文件, 是为了运行该文件的代码, 注册视图函数
import api                         # 注册api视图函数
import hook                     # 注册钩子
from exts import app
from models import db
from config import config
app.config.from_object(config['default'])
db.init_app(app)

if __name__ == '__main__':
    app.run(host='192.168.6.182', port=9094, debug=True)
