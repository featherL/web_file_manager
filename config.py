import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):    
    SECRET_KEY = os.urandom(24)    


class DevelopmentConfig(Config):
    ## 开发配置
    DEBUG = True
    SQLALCHEMY_DATABASE_URI  = 'sqlite:///webfilemanager.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS      = True
    SECRET_KEY                          = os.urandom(24)

class TestingConfig(Config):
    ## 测试配置
    TESTING = True

class ProductionConfig(Config):
    ## 部署配置
    DATABASE_URI = 'mysql://user@localhost/foo'

config = {
    'development'   : DevelopmentConfig,
    'testing'       : TestingConfig,
    'production'    : ProductionConfig,
    'default'       : DevelopmentConfig
}


