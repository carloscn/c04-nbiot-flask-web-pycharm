# -*- coding:UTF-8 -*-
from . import api
from flask_httpauth import HTTPBasicAuth
from flask import jsonify
from flask import g
from flask_login import login_required
from app.models import User
from app import db
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
    if len(email_or_token) == 0:
        return False
    if len(password) == 0:
        g.current_user = User.check_api_token(email_or_token)
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    return user.check_user_password(password)

@auth.error_handler
def error_handler():
    return jsonify({'static':401})

@api.route('/')
@auth.login_required
def test_devices():
    return 'devices'





@api.route('/token')
@auth.login_required
def token():
    return jsonify({'token': g.current_user.api})


@api.route('/devices')
@auth.login_required
def devices():
    ds = g.current_user.devices
    ds_list = []
    for d in ds:
        ds_list.append(d.to_json())
    return jsonify({'status': 200, 'devices' : ds_list})


@api.route('/device/<int:id>')
def device(id):
    pass

@api.route('/device/<int:id>/sensors')
def sensors(id):
    pass

@api.route('/device/<int:device_id>/sensor/<int:sensor_id>')
def sensor(device_id,sensor_id):
    pass
@api.route('/device/<int:device_id>/sensor/<int:sensor_id>/datas')
def datas(device_id,sensor_id):
    pass
from app.models import Data,Device,Sensor
from flask import request
@api.route('/device/<int:device_id>/sensor/<int:sensor_id>/data',methods=['GET','POST'])
def data(device_id,sensor_id):
    dev = Device.query.filter_by(id=device.id).first()
    if dev is None:
        return jsonify({'status': 404,'info':'device not found'})
    sen = dev.sensors.filter_by(id = sensor_id).first()
    if sen is None:
        return jsonify({'status': 404, 'info': 'sensor not found'})


    if request.method =='POST':
        upload_data = request.json
        if 'data' in upload_data.keys():
            data = Data()
            data.data= upload_data['data']
            data.sensor_id = sen.id
            db.session.add(data)
            db.session.commit()

            #baojingchuli

            return jsonify({'status':200})
        else:
            return jsonify({'status':404,'info':'data not found'})
    else:
        return jsonify({'status': 200})

