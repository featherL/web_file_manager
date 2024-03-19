"""
不使用数据库
"""

import os

# 配置{

USERNAME = 'admin'  # 登录用户名
PASSWORD = '123456'  # 登录密码

HOME_PATH = '/home/guoyuh/projects/plantform'  # 文件管理的根目录

# }

HOME_PATH = os.path.abspath(HOME_PATH)  # 将路径转化为标准绝对路径
HOME_NAME = os.path.basename(HOME_PATH)  # 根目录的名字
