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


class Area(BaseModel, db.Model):
    '''城区信息'''

    __tablename__ = 'renting_area_info'

    id = db.Column(db.Integer, primary_key=True) # 区域编号
    name = db.Column(db.String(32), nullable=False)# 区域名字
    houses = db.relationship('House', backref='area')

    def to_dict(self):
        '''将对象转换为字典'''
        d = {
            'aid':self.id,
            'aname':self.name
        }
        return d


# 房屋设施表，建立房屋与设施的多对的关系
house_facility = db.Table(
    'renting_house_facility',
    db.Column('house_id', db.Integer, db.ForeignKey('renting_house_info.id'), primary_key=True), # 房屋编号
    db.Column('facility_id', db.Integer, db.ForeignKey('renting_facility_info.id'), primary_key=True) # 设施编号
)
            
class House(BaseModel, db.Model):
    '''房屋信息'''

    __tablename__ = 'renting_house_info'

    id = db.Column(db.Integer, primary_key=True) # 房屋编号
    user_id = db.Column(db.Integer, db.ForeignKey('renting_user_profile.id'), nullable=False) # 房屋主人的用户编号
    area_id = db.Column(db.Integer, db.ForeignKey('renting_area_info.id'), nullable=False) # 归属地的区域编号
    title = db.Column(db.String(64), nullable=False) # 标题
    price = db.Column(db.Integer, default=0)# 单价 单位 分
    address = db.Column(db.String(512), default="") # 地址
    room_count = db.Column(db.Integer, default=0) # 房间数目
    acreage = db.Column(db.Integer, default=0) # 房屋面积
    unit = db.Column(db.String(32),default="") # 房屋单元  如几室几厅
    capacity = db.Column(db.Integer, default=1) # 房屋容纳的人数
    beds = db.Column(db.String(64), default="")# 房屋的床铺的配置
    deposit = db.Column(db.Integer, default=0)# 房屋押金
    min_days = db.Column(db.Integer, default=1) # 最少入住天数
    max_days = db.Column(db.Integer, default=0) # 最多入住天数 0 表示不限制
    order_count = db.Column(db.Integer, default=0)# 预定完成的该房屋的订单数
    index_image_url = db.Column(db.String(256), default="") # 房屋主图片的路径
    facilities = db.relationship('Facility', secondary=house_facility) # 房屋的设施
    images = db.relationship('HouseImage') # 房屋图片
    orders = db.relationship("Order", backref = 'house') # 房屋的订单

    def to_basic_dict(self):
        '''将基本信息转为字典数据'''
        house_dict = {
            'house_id':self.id,
            'title':self.title,
            'price':self.price,
            'area_name':self.area.name,
            'img_url':contants.QINIU_URL_DOMAIN + self.index_image_url if self.index_image_url else "",
            'room_count':self.room_count,
            'address':self.order_count,
            'user_avatar': constants.QINIU_URL_DOMAIN + self.user.avatar_url if self.user.avatar_url else "",
            'ctime':self.create_time.strftime("%Y-%m-%d")
        }
        return house_dict

    def to_full_dict(self):
        '''将详细信息转换为字典'''
        house_dict = {
            'hid':self.id,
            'user_id':self.user_id,
            'user_name':self.user.name,
            'user_avatar': constants.QINIU_URL_DOMAIN + self.user.avatar_url if self.user.avatar_url else "",
            'title':self.title,
            'price': self.price,
            'address':self.address,
            'room_count':self.room_count,
            'acreage':self.acreage,
            'unit':self.unit,
            'capacity':self.capacity,
            'beds': self.beds,
            'deposit':self.deposit,
            'min_days':self.min_days,
            'max_days':self.max_days
        }

        # 房屋图片
        img_urls = []
        for image in self.images:
            img_urls.append(constants.QINIU_URL_DOMAIN + image.url)
        house_dict['img_urls'] = img_urls

        # 房屋设施
        facilities = []
        for facility in self.facilities:
            facilities.append(facility.id)
        house_dict['facilities'] = facilities

        # 评论信息
        comments = []
        orders = Order.query.filter(Order.house_id == self.id, Order,status == 'COMPLETE', Order.comment != None)\
            .order_by(Order.update_time.desc()).limit(constants.HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS)
        for order in orders:
            comment = {
                'comment': order.comment, # 评论内容
                'user_name': order.user.name if order.user.name != order.user.mobile else '匿名用户', # 发表评论
                'ctime': order.update_time.strftime("Y%-%m-%d %H:%M:%S") # 评论时间
            }
            comments.append(comment)
        house_dict['comments'] = comments
        return house_dict

class Facility(BaseModel, db.Model):
    '''设施信息'''
    __tablename__ = 'renting_facility_info'

    id = db.Column(db.Integer, primary_key=True) # 设施编号
    name = db.Column(db.String(32), nullable=False) # 设施名字

class HouseImage(BaseModel, db.Model):
    '''房屋图片'''
    __tablename__ = 'renting_house_image'

    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('renting_house_info.id'), nullable=False) # 房屋编号
    url = db.Column(db.String(256), nullable=False) # 图片的路径

class Order(BaseModel, db.Model):
    '''订单'''
    __tablename__ = 'renting_order_info'

    id = db.Column(db.Integer, primary_key=True) # 订单编号
    user_id = db.Column(db.Integer, db.ForeignKey('renting_user_profile.id'), nullable=False) # 下订单的用户编号
    house_id = db.Column(db.Integer, db.ForeignKey('renting_house_info.id'), nullable=False) # 预定的房间编号
    begin_date = db.Column(db.DateTime, nullable=False) # 预订的起始时间
    end_time = db.Column(db.DateTime, nullable=False) # 预订的结束时间
    days = db.Column(db.Integer, nullable=False) # 预订的总天数
    house_price = db.Column(db.Integer, nullable=False) # 房屋的单价
    status = db.Column(#订单状态
        db.Enum( # 枚举 
            'WAIT_ACCEPT', # 待接单
            'WAIT_PAYMENT', # 待支付
            'PAID', # 已付款
            'WAIT_COMMENT', #待评价
            'COMPLETE', # 已完成
            'CANCELED', # 已取消
            'REJECTED' # 已拒单
        ),
        default='WAIT_ACCEPT', index=True)    # 指明在mysql中这个字段建立索引 加快查询速度
    comment = db.Column(db.Text) # 订单的评论信息或者拒单原因
    trade_no = db.Column(db.String(80)) # 订单交易流水号 支付宝的

    def to_dict(self):
        '''将订单信息转换为字典数据'''
        order_dict = {
            'order_id':self.id,
            'title':self.house.title,
            'img_url': constants.QINIU_URL_DOMAIN + self.house.index_image_url if self.house.index_imgae_url else "",
            'start_date': self.begin_date.strftime("%Y-%m-%d"),
            'end_date':self.end_date.strftime("%Y-%m-%d"),
            'ctime': self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'days':self.days,
            'amount':self.amount,
            'status':self.status,
            'comment':self.comment if self.comment else ""
        }            
        return order_dict