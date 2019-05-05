# -*- coding:UTF-8 -*-
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Email,Length,EqualTo
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms import ValidationError

from app.models import User

class LoginForm(FlaskForm) :
    email = StringField(label='邮箱',
                        validators=[DataRequired(message='邮箱必须填写'),
                                    Length(1, 128, message='长度必须是1-128'),
                                    Email(message='邮箱格式不对')])
    password = PasswordField(label='密码',
                             validators=[DataRequired(message='密码必须填写'),
                                         Length(1, 128, message='长度必须是1-128')])
    submit = SubmitField(label='登陆')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is None:
            raise ValidationError('此邮箱没有注册')

class RegisterForm(FlaskForm):
    name = StringField(label='昵称', validators=[DataRequired(), Length(1, 64)])
    email = StringField(label='邮箱',
                        validators=[DataRequired(message='邮箱必须填写'),
                                    Length(1, 128, message='长度必须是1-128'),
                                    Email(message='邮箱格式不对')])
    password = PasswordField(label='密码',
                             validators=[DataRequired(message='密码必须填写'),
                                         Length(1, 128, message='长度必须是1-128')])
    password_again = PasswordField(label='确认密码',
                             validators=[EqualTo('password', message='两次密码输入不一致')])

    submit = SubmitField(label='注册')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError('此邮箱已经被使用')


