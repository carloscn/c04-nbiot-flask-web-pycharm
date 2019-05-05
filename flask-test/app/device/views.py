# coding: utf-8
from flask import render_template,redirect,url_for,flash,request,abort
from app import db
from . import device
from .forms import Add_device,Modify_device
from flask_login import login_required,current_user
from app.models import Device,User,Sensor
from flask_login import current_user


@device.route('/devices')
def devices():
    user_id=request.args.get('id')


    all_device = Device.query.filter_by(user_id=user_id).all()

    return render_template('/device/devices.html',all_device=all_device,id=user_id)


@device.route('/device_id',methods=['GET','POST'])
def device_id():
    sensor = Sensor()
    did = request.args.get('id')
    if id is None:
        abort(404)
    dev = Device.query.filter_by(id=did).first()
    if device is None:
        abort(404)
    all_sensors=Sensor.query.filter_by(device_id=did).all()

    return render_template('/device/device_id.html',id=did,dev=dev,all_sensors=all_sensors)


@device.route('/add_device',methods=['GET','POST'])
def add_device():

    form=Add_device()
    id=request.args.get('id')


    if form.validate_on_submit():
        device = Device()
        device.name = form.name.data
        device.desc = form.desc.data
        device.addr = form.addr.data
        device.user_id=id
        db.session.add(device)
        db.session.commit()
        return redirect(url_for('.devices',id=id))
    return render_template('/device/add_device.html',form=form)


@device.route('/modify_device',methods=['GET', 'POST'])
def modify_device():
    form = Modify_device()
    id = request.args.get('id')
    if id is None:
        abort(404)
    device= Device.query.filter_by(id=id).first()

    if device is None:
        abort(404)
    if form.validate_on_submit():
        device.name = form.name.data
        device.desc = form.desc.data
        device.addr = form.addr.data
        db.session.add(device)
        db.session.commit()
        return redirect(url_for('.devices',id=id))
    return render_template('/device/modify_device.html',form=form,id=id)


@device.route('/delete_device')
def delete_device():
    id = request.args.get('id')
    if id is None:
        abort(404)
    d = Device.query.filter_by(id=id).first()
    if device is None:
        abort(404)
    db.session.delete(d)
    db.session.commit()
    return redirect(url_for('device.devices'))


@device.route('/set_default_time_device',methods=['GET','POST'])
def set_default_time_device():
    sensor = Sensor()
    did = 9
    if id is None:
        abort(404)
    dev = Device.query.filter_by(id=did).first()
    if device is None:
        abort(404)
    all_sensors=Sensor.query.filter_by(device_id=did).all()
    data = request.args.get('data')
    if data == 8:
        print('default time')
    return render_template('/device/device_id.html',id=did,dev=dev,all_sensors=all_sensors)



@device.route('/set_temp_time_device',methods=['GET','POST'])
def set_temp_time_device():
    sensor = Sensor()
    did = 9
    if id is None:
        abort(404)
    dev = Device.query.filter_by(id=did).first()
    if device is None:
        abort(404)
    all_sensors=Sensor.query.filter_by(device_id=did).all()
    data = request.args.get('data')
    if data == 8:
        print('temp time')
    return render_template('/device/device_id.html',id=did,dev=dev,all_sensors=all_sensors)

@device.route('/dataFromAjax')
def dataFromAjax():
    htmlStr = request.args.get('mydata')
    filename = "/home/delvis/test.file"
    with open(filename, 'w') as file_object:
        file_object.write(htmlStr)
    print("write data to " + filename)
    return 'dataFromAjax'

@device.route('/dataFromAjaxSetNormalMode')
def dataFromAjaxSetNormalMode():
    htmlStr = request.args.get('mydata')
    filename = "/home/ubuntu/python/cache.i"
    #filename = "/home/delvis/test.file"
    with open(filename, 'w') as file_object:
        file_object.write('1')
    return 'dataFromAjaxSetNormalMode'

@device.route('/dataFromAjaxSetHighMode')
def dataFromAjaxSetHighMode():
    htmlStr = request.args.get('mydata')
    filename = "/home/ubuntu/python/cache.i"
    #filename = "/home/delvis/test.file"
    with open(filename, 'w') as file_object:
        file_object.write('2')
    return 'dataFromAjaxSetHighMode'
