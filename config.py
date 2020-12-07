

class Config(object):
    '''配置信息'''
    SECRET_KEY = 'HELLOESTELL0113%'
    # 数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://estellekk@127.0.0.1:3306/renting'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # reids 参数信息
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    # flask-session 配置信息
    # SESSION_TYPE: specifies which type of session interface to use 
    SESSION_TYPE = 'redis' 
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 对cookie 中的session id 进行隐藏
    SESSION_USE_SINGER = True
    PERMANENT_SESSION_LIFETIME = 86400 # session 数据的有效期 单位秒 1天

class DevelopmentConfig(Config):
    '''开发模式的配置信息'''
    DEBUG = True

class ProductionConfig(Config):
    '''生产环境的配置信息'''
    pass

config_map = {
    'develop': DevelopmentConfig,
    'product': ProductionConfig
}