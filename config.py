import os

# debug模式
DEBUG = True

# session用的盐
SECRET_KEY = os.urandom(24)

# # 数据库配置{ 不使用数据库
# HOSTNAME = '127.0.0.1'
# PORT = '3306'
# USERNAME = 'root'
# PASSWORD = 'flask_test'
# DATABASE = 'web_file_manager'
# DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
#
# SQLALCHEMY_DATABASE_URI = DB_URI
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# }
