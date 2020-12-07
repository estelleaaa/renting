from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
import redis

app = Flask(__name__)

class Config(object):
    '''配置信息'''
    DEBUG = True
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


# 将配置信息导图app中
app.config.from_object(Config)
# 创建数据库实例
db = SQLAlchemy(app)
# 创建redis连接对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
# 利用flask session 将session数据保存到redis中
Session(app)
# 为flask补充csrf防护机制
CSRFProtect(app)

@app.route("/index")
def index():
    return "index page"

if __name__ == '__main__':
    app.run()