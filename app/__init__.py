
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from config import config_map
from app import api_v1_0
import redis

# 创建数据库实例
db = SQLAlchemy()
# 创建redis连接对象
redis_store = None
# 开发模式

def create_app(config_name):    
    # print(config_name,'---------name')
    app = Flask(__name__)
    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)
    # 使用app初始化db
    db.init_app(app)
    # 初始化redis工具
    global redis_store 
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST,port=config_class.REDIS_PORT)
    # 利用flask session 将session数据保存到redis中
    Session(app)
    # 为flask补充csrf防护机制
    CSRFProtect(app)
    # 注册蓝图
    app.register_blueprint(api_v1_0.api, url_prefix='/api/v1.0')
    return app