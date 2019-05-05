# -*- coding:UTF-8 -*-
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Email,Length,EqualTo
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms import ValidationError

from app.models import User

class EditUserInfoForm(FlaskForm) :
    name = StringField(label='昵称',
                       validators=[
                           DataRequired(message='昵称必须填写'),
                           Length(1, 64, message='长度必须小于64')])
    location = StringField(label='位置')
    about_me = StringField(label='个性签名')
    password = PasswordField(label='密码', validators=[Length(0, 128)])
    password_again = PasswordField(label='确认密码',
                                   validators=[
                                       EqualTo('password', message='两次输入的密码不一致')
                                   ])
    submit = SubmitField(label='确认修改')

class CommentsForm(FlaskForm):
    body = TextAreaField(label='评论',validators=[DataRequired(),Length(1,128)])
    submit = SubmitField(label='提交')