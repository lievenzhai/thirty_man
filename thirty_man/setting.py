import os, sys


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig():
    # 配置密钥
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')
    # 配置主题
    BLOG_THEMES = {'cerulean_bootstrap': 'blue', 'darkly_bootstrap': 'dark'}


    # 配置邮件相关
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Bluelog Admin', MAIL_USERNAME)

    THIRTY_MAN_POST_PER_PAGE = 4
    THIRTY_MAN_EMAIL = os.getenv('THIRTY_MAN_EMAIL')
    THIRTY_MAN_MANAGE_POST_PER_PAGE = 15
    THIRTY_MAN_COMMENT_PER_PAGE = 15

    SQLALCHEMY_POOL_RECYCLE = 280

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    SSL_DISABLED = True



class TestingConfig(BaseConfig):
    ...


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))
    SSL_DISABLED = False


config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}