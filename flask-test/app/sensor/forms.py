# -*- coding:UTF-8 -*-
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Length
from wtforms import StringField,SubmitField,SelectField,TextAreaField,FloatField
from wtforms import ValidationError

class SensorForm(FlaskForm) :
    name = StringField(label='昵称',validators=[DataRequired(message='昵称必须填写')])
    desc = TextAreaField(label='描述',validators=[DataRequired(message='昵称必须填写'),])
    unit = SelectField(label='数据单位',coerce=int, choices=[(0,"个"),(1,"米"),(2,"摄氏度")])
    maxDate = FloatField(label="最大值",validators=[DataRequired()])
    minDate = FloatField(label="最小值", validators=[DataRequired()])
    submit = SubmitField(label='添加传感器')

class EditSensorForm(FlaskForm):
    name = StringField(label='昵称', validators=[DataRequired(message='昵称必须填写')])
    desc = TextAreaField(label='描述', validators=[DataRequired(message='昵称必须填写'), ])
    unit = SelectField(label='数据单位', coerce=int, choices=[(0,"个"),(1,"米"),(2,"摄氏度")])
    maxDate = FloatField(label="最大值", validators=[DataRequired()])
    minDate = FloatField(label="最小值", validators=[DataRequired()])
    submit = SubmitField(label='确认修改')
