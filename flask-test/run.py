# -*- coding:UTF-8 -*-
import jinja2
from os import abort

import pymysql
import socketio
import threading
import SocketServer
from app.device import device
from multiprocessing import Process
pymysql.install_as_MySQLdb()
import psutil
import time
import thread
from flask_script import Manager, Shell
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit
import socket
from app import create_app
from app import db
from flask_migrate import Migrate, MigrateCommand
from app.models import Role
from app.models import User, Device, Role
import sys
from app.models import Device, User, Sensor
from time import ctime
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
app = create_app('develop')

red_state = 0
yellow_state = 0
green_state = 0
manager = Manager(app)
app = Flask(__name__)
migrate = Migrate(app=app, db=db)

manager.add_command('db', MigrateCommand)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def make_shell_context():
    return dict(app=app, db=db, Device=Device, Role=Role, User=User)


manager.add_command('shell', Shell(make_context=make_shell_context))

DB = app.config.get('DEBUG')
if DB:
    print('debug:app will start')

def render_without_request(template_name, **context):
    """
    用法同 flask.render_template:

    render_without_request('template.html', var1='foo', var2='bar')
    """
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('package','templates')
    )
    template = env.get_template(template_name)
    return template.render(**context)


# python run.py test
@manager.command
def test():
    import unittest
    t = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(t)


@manager.command
def init():
    Role.create_roles()
    user = User()
    user.email = 'root@embsky.com'
    user.name = 'admin'
    user.confirmed = True
    user.password = 'admin'
    user.role = Role.query.filter_by(name='admin').first()
    db.session.add(user)
    db.session.commit()



if __name__ == '__main__':


    # p=Process(target=read_sensor,args=())
    # p.start()
    # server1需放在p.start后启动不然会阻塞进程，server2无法启动
    manager.run()

    # p.join()



