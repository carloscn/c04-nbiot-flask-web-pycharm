# -*- coding:UTF-8 -*-
from flask import Flask
from config import config

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail



#pip install flask-bootstrap
#pip install flask-moment

from flask_bootstrap import Bootstrap
from flask_moment import Moment

from flask_login import LoginManager


login_manager = LoginManager()

                            #蓝本.视图
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'



#这个变量必须叫做moment,moment可以把utc时间转换成当地时间
moment = Moment()
#这个变量必须叫做bootstrap
bootstrap = Bootstrap()

mail = Mail()
db = SQLAlchemy()
def create_app(config_name) :
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    #绑定app
    db.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    #以后在此注册蓝本
    from .main import main as main_bp
    app.register_blueprint(main_bp)
    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from .device import device as device_bp
    app.register_blueprint(device_bp, url_fix='/device')
    from .sensor import sensor as sensor_bp
    app.register_blueprint(sensor_bp,url_prefix='/sensor')
    from .manager import manager as manager_bp
    app.register_blueprint(manager_bp, url_prefix='/manager')
    from .api_1_0 import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/1.0')


    return app
