# -*- coding:UTF-8 -*-
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from datetime import datetime

from app import login_manager
#注销时用到的回调函数
@login_manager.user_loader
def user_loader(id) :
    return User.query.get(int(id))

class User(db.Model,UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128))
    confirm=db.Column(db.Boolean,default=False)
    location=db.Column(db.String(128))
    about_me=db.Column(db.Text())
    r_time=db.Column(db.DateTime,default=datetime.utcnow)
    a_time=db.Column(db.DateTime,default=datetime.utcnow)
    api_token=db.Column(db.String(256))
    isEnterprise=db.Column(db.Boolean,default=False)
    telephone1=db.Column(db.Integer)
    telephone2=db.Column(db.Integer)
    telephone3=db.Column(db.Integer)
    remain_msg_count=db.Column(db.Integer,default=0)
    verify_code=db.Column(db.String(4))
    telephone=db.Column(db.String(12))


    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    alerts=db.relationship('Alert',backref='user',lazy='dynamic')
    devices=db.relationship('Device',backref='user', cascade ='all, delete-orphan',lazy='dynamic')
    comments=db.relationship('Comment',backref='user',lazy='dynamic')

    api = db.Column(db.String(256))


    def generate_api_token(self):
        s=Serializer(secret_key=current_app.config['SECRET_KEY'], expires_in=10*365*24*60*60)
        self.api = s.dumps({'id':self.id})
        db.session.add(self)
        db.session.commit()

    def get_api_token(self):
        return self.api

    @staticmethod
    def check_api_token(token):
        s = Serializer(secret_key=current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return None
        if 'id' in data.keys():
            id = data['id']
            return User.query.filter_by(id=id).first()
        else:
            return None



    def flush_access_time(self):
        self.a_time = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('不好意思，密码不能读取')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_user_password(self, password):
        return check_password_hash(self.password_hash, password)
    # 生成token：发送邮件的时候用
    def generate_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=7200)
        return s.dumps({'id': self.id})
    # 用来验证token是否则正确：当用户点击邮箱中的连接验证时候调用
    def check_token(self, token):
        if token is None:
            return False
        token = token[2:-1]
        print(token)
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        id = data.get('id')
        if id is None:
            return False
        if id != self.id:
            return False
        self.confirm = True
        db.session.add(self)
        db.session.commit()
        return True

    def is_admin(self):
        return self.role.permissions == 0xff

    def is_moderator(self):
        return self.role.permissions == Permission.MODE_COMMENT

    def has_permission(self, permission):
        return self.role.permissions & permission == permission


class Permission():
    FOLLOW = 0x01
    CREATE = 0x02
    COMMENT = 0x04
    MODE_COMMENT = 0x08
    ADMIN = 0x80

class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    permission = db.Column(db.Integer, default=0)
    default = db.Column(db.Boolean, default=False)

    users=db.relationship('User',backref='role',lazy='dynamic')

    @staticmethod
    def create_roles():
        roles = {
            'user': [Permission.FOLLOW | Permission.CREATE, True],
            'moderator': [Permission.MODE_COMMENT, False],
            'admin': [0xff, False]
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role()
                role.name = r
            role.permission = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Sensor_Type(db.Model):
    __tablename__='sensor_types'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128))
    desc = db.Column(db.Text)
    default=db.Column(db.Boolean)

    sensor_id=db.Column(db.Integer,db.ForeignKey('sensors.id'))

class Device(db.Model):
    __tablename__='devices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    desc = db.Column(db.Text())
    addr = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    sensors = db.relationship('Sensor',backref='device', cascade='all, delete-orphan',lazy='dynamic')
    alerts = db.relationship('Alert',backref='device', lazy='dynamic')


    def to_json(self):
        json_data={
            'id':self.id,
            'name':self.name,
            'desc':self.desc,
            'addr':self.addr,
            'timestamp':self.timestamp,
            'user':self.user.name,
        }
        return json_sensor

class Sensor(db.Model):
    __tablename__='sensors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    desc = db.Column(db.Text())
    unit = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    maxData = db.Column(db.Float())
    minData = db.Column(db.Float())

    sensor_types=db.relationship('Sensor_Type',backref='sensor',lazy='dynamic')
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id', ondelete='CASCADE'))
    datas=db.relationship('Data',backref='sensor',cascade='all, delete-orphan')
    alerts=db.relationship('Alert',backref='sensor')

    def to_json(self):
        json_data={
            'id':self.id,
            'name':self.name,
            'desc':self.desc,
            'unit':self.unit,
            'timestamp':self.timestamp,
            'device':self.device.name,
            'maxData':self.maxData,
            'minData':self.minData,
        }
        return json_data

class Data(db.Model):
    __tablename__ = "datas"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sensor_id = db.Column(db.Integer, db.ForeignKey("sensors.id"),onupdate='CASCADE')
    alerts=db.relationship('Alert',backref='data')

    def to_json(self):
        json_data={
            'id':self.id,
            'data':self.data,
            'timestamp':self.timestamp,
            'sensor':self.sensor.name,
        }
        return json_data

class Alert(db.Model):
    __tablename__ = "alerts"
    id = db.Column(db.Integer, primary_key=True)
    isMsged = db.Column(db.Boolean)
    maxData = db.Column(db.Float)
    minData = db.Column(db.Float)
    alertInfo = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"))
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensors.id"))
    data_id = db.Column(db.Integer, db.ForeignKey("datas.id"))


class Posts(db.Model) :
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    body = db.Column(db.Text())
    # body_html = db.Column(db.Text())
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

    comments=db.relationship('Comment',backref='post',lazy='dynamic')

class Comment(db.Model) :
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text())
    body_html = db.Column(db.Text())
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    disable = db.Column(db.Boolean,default=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
from flask_login import AnonymousUserMixin
class AnonymousUser(AnonymousUserMixin) :


    name = '游客'

    def is_admin(self):
        return False

    def is_moderator(self):
        return False

    def has_permission(self, permission):
        return False