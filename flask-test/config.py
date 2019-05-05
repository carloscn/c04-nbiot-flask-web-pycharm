# -*- coding:UTF-8 -*-
class Config :
    #表单需要
    CSRF_ENABLED = True
    SECRET_KEY = 'www.embsky.com'

    # 邮件需要
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = '25'
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'ws1017968224@163.com'
    MAIL_PASSWORD = 'violin1314ws'

    #数据库需要
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopConfig(Config) :
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:nihao@localhost/develop_db'

class TestConfig(Config) :
    TEST = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:nihao@localhost/test_db'

class ProductConfig(Config) :
    SQLALCHEMY_DATABASE_URI = 'mysql://root:nihao@localhost/product_db'

config = {
    'develop':DevelopConfig,
    'test':TestConfig,
    'product':ProductConfig,
    'default':DevelopConfig,
}
