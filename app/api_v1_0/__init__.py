# api 称为后端的蓝图文件
# 定义蓝图 创建蓝图对象
from flask import Blueprint
# param:1 名字 
api = Blueprint('api_v1_0', __name__)
# 导入蓝图的视图函数
from . import demo