
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from config import config_map
import redis

# 创建数据库实例
db = SQLAlchemy()
# 创建redis连接对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
# 开发模式
def create_app(config_name):    

    app = Flask(__name__)
    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)
    # 将配置信息导图app中
    app.config.from_object(config_class)
    # 使用app初始化db
    db.init_app(app)
    return app