# coding: utf-8
from . import sensor
from flask import redirect,render_template,abort,url_for,request,flash
from .forms import SensorForm,EditSensorForm
from app.models import Sensor
from app import db
from flask_login import  current_user
from app.models import Device

@sensor.route("/add_sensor",methods=["GET","POST"])
def add_sensor():
    form = SensorForm()
    id = request.args.get('id')
    if id is None:
        abort(404)
    if form.validate_on_submit():
        sensor = Sensor()
        sensor.name = form.name.data
        sensor.desc = form.desc.data
        sensor.unit = form.unit.data
        sensor.maxData = form.maxDate.data
        sensor.minData = form.minDate.data
        sensor.device_id = id
        db.session.add(sensor)
        db.session.commit()
        return redirect(url_for("device.device_id",id=id))
    return render_template("sensor/add_sensor.html",form=form)

@sensor.route("edit_sensor",methods=["GET","POST"])
def edit_sensor():
    form = EditSensorForm()
    sensor = Sensor()
    id = request.args.get("id")
    if id is None:
        abort(404)
    sensor = Sensor.query.filter_by(id=id).first()
    if sensor is None:
        abort(404)
    if form.validate_on_submit():
        sensor.name = form.name.data
        sensor.desc = form.desc.data
        sensor.unit = form.unit.data
        db.session.add(sensor)
        db.session.commit()
        return redirect(url_for("sensor.index"))
    return render_template("sensor/edit_sensor.html",form=form)

@sensor.route("delete_sensor")
def delete_sensor():
    sid = request.args.get("id")
    print(sid)
    if id is None:
        abort(404)
    sensor = Sensor.query.filter_by(id=sid).first()

    if sensor is None:
        abort(404)
    did = sensor.device_id

    db.session.delete(sensor)
    db.session.commit()
    return redirect(url_for("device.device_id",id=did))

@sensor.route('/sensor_data')
def sensor_data():
    sensor = Sensor()
    did = request.args.get('id')
    if id is None:
        abort(404)
    dev = Device.query.filter_by(id=did).first()
    all_sensors=Sensor.query.all()
    fp = open('/home/ubuntu/python/cache.ii', 'r+w+a+')
    ss = fp.readline()
    fp.truncate()
    fp.close()
    
    if ss.strip()=="":
	red_state = 2
        yellow_state = 2
	green_state = 2
    else:
        if ss[0] == '0':
            red_state = 0
        else:
            red_state = 1
        if ss[1] == '0':
            yellow_state = 0
        else:
            yellow_state = 1
        if ss[2] == '0':
            green_state = 0
        else:
            green_state = 1
    mm = [red_state, yellow_state, green_state]
    print(mm)
    return render_template('sensor/sensor_data.html', mm=mm,id=did,dev=dev,all_sensors=all_sensors)
