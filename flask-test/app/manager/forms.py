
# -*- coding:UTF-8 -*-
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Email,Length,EqualTo
from wtforms import StringField,PasswordField,BooleanField,SubmitField,SelectField,TextAreaField
from wtforms import ValidationError

from app.models import User
from app.models import Role

class FindUserForm(FlaskForm) :
    find_text = StringField(label='搜索', validators=[DataRequired()])
    submit = SubmitField(label='搜索')

class EditPostInfoForm(FlaskForm) :
    title = StringField(label='标题',
                        validators=[
                            DataRequired(message='标题必须填写'),
                            Length(1, 256, message='长度必须小于256')])
    content = TextAreaField(label='正文', validators=[
        DataRequired(message='文章必须由内容')
    ])

    submit = SubmitField(label='修改')

class PostForm(FlaskForm) :
    title = StringField(label='标题',
                       validators=[
                           DataRequired(message='标题必须填写'),
                           Length(1, 256, message='长度必须小于256')])
    content = TextAreaField(label='正文', validators=[
        DataRequired(message='文章必须由内容')
    ])

    submit = SubmitField(label='发表')

class EditUserForm(FlaskForm):
    name = StringField(label='昵称', validators=[ Length(1, 64)])

    location = StringField(label='位置')
    about_me = StringField(label='个性签名')
    submit = SubmitField(label='提交')