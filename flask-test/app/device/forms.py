# -*- coding:UTF-8 -*-
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Length
from wtforms import SubmitField,StringField,TextField
from app.models import Device

class Add_device(FlaskForm):
    name = StringField(label='设备名字',  validators=[Length(1,64)])
    desc = TextField(label='设备描述',validators=[] )
    addr = StringField(label='设备地址',validators=[ Length(1,256)])
    submit=SubmitField(label='提交')

class  Modify_device(FlaskForm):
    name = StringField(label='设备名字', validators=[ Length(1,64)])
    desc = TextField(label='设备描述', validators=[])
    addr = StringField(label='设备地址', validators=[ Length(1,256)])
    submit = SubmitField(label='提交')
