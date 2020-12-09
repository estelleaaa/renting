# -*- coding: utf-8 -*-

from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import constants

class BaseModel(object):
    '''模型基类，为每个模型补充创建时间 更新时间'''

    create_time = db.Column(db.DateTime, default=datetime.now) # 记录创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now) # 记录更新时间

class User(BaseModel, db.Model):
    '''用户表'''
    __tablename__='renting_user_profile'

    id = db.Column(db.Integer, primary_key=True) #用户编号
    name = db.Column(db.String(32), unique=True, nullable=False) # 用户的昵称
    password_hash= db.Column(db.String(128), nullable=False) # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False) # 手机号码
    real_name = db.Column(db.String(32)) # 用户真实姓名
    id_card = db.Column(db.String(20)) # 身份证号码
    avatar_url = db.Column(db.String(128)) # 头像图片的url
    houses = db.relationship('House', backref='user') # 用户发布的房源
    orders = db.relationship('Order', backref='user') # 用户的订单信息

    # property 装饰器  将函数转换为以属性的方式进行调用
    @property
    def password(self):
        '''读取属性的函数行为'''
        raise AttributeError('this is noly can be set, cannot be read')

    @password.setter
    def password(self, value):
        '''
        设置属性 user.password = 'xxxxx'
        '''
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        '''检查密码的正确性'''
        return check_password_hash(self.password_hash,password)

    def to_dict(self):
        '''将对象转换为字典数据'''
        user_dict = {
            'user_id':self.id,
            'name':self.name,
            'mobile':self.mobile,
            'avatar':constants.QINIU_URL_DOMAIN + self.avatar_url if self.avatar_url else "",
            'create_time':self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return user_dict

    def auth_to_dict(self):
        '''将实名信息转换为字典数据'''
        auth_dict = {
            'user_id':self.id,
            'real_name':self.real_name,
            'id_card':self.id_card
        }
        return auth_dict
            