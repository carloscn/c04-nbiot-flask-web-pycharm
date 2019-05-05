# -*- coding:UTF-8 -*-
from app import db
from . import auth
from flask import render_template
from .forms import LoginForm, RegisterForm
from app.models import User
from flask_login import login_user, logout_user, login_required
from flask import redirect, url_for,flash
from flask import request
from flask import abort
from flask_login import current_user
from app.email import send_mail
from flask import current_app
from app.models import Role

@auth.route('/logout')
@login_required
def logout() :
    #注销的是当前用户
    logout_user()
    return redirect(url_for('.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register() :
    form = RegisterForm()
    if form.validate_on_submit() :
        user = User()
        user.name = form.name.data
        user.password = form.password.data
        user.email = form.email.data

        #send_mail(subject='物联网云平台',
        #          recver=form.email.data,
        #          body='hahaha', html=None)

        if form.email.data == current_app.config['MAIL_USERNAME'] :
            user.role = Role.query.filter_by(name='admin').first()
        else :
            user.role = Role.query.filter_by(default=True).first()

        db.session.add(user)
        db.session.commit()

        user.generate_api_token()





        #渲染邮件模版
        html = render_template('email/register.html',
                               token=user.generate_token(),
                               name=user.name)
        #发送邮件
        send_mail('物联网云平台',
                  recver=form.email.data,
                  html=html, body=None)

        return redirect(url_for('.login'))

    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login() :
    form = LoginForm()
    if form.validate_on_submit() :
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user.check_user_password(password) :
            login_user(user)
            return redirect(url_for('main.user_info',id=user.id))
        else:
            flash('亲！账号或者密码错误！')

    return render_template('auth/login.html', form=form)

@auth.route('/resend_email')
@login_required
def resend_email() :
    # 渲染邮件模版
    token = current_user.generate_token()
    html = render_template('email/register.html',
                           token=token,
                           name=current_user.name)
    print(token)
    # 发送邮件
    send_mail('海淀区信息发布系统注册邮件',
              recver=current_user.email,
              html=html, body=None)

    return redirect(url_for('main.user_info', id=current_user.id))

#当用户点击邮箱中的  这里  时候调用，用来激活用户
@auth.route('/confirm')
@login_required
def confirm() :
    token = request.args.get('token')
    if not current_user.check_token(token) :
        return render_template('auth/email_again.html')
    return redirect(url_for('main.user_info', id=current_user.id))

@auth.route('/request_confirm')
def request_confirm() :
    return render_template('auth/request_confirm.html')

@auth.before_app_request
def before_app_request() :
    if current_user.is_authenticated :
        current_user.flush_access_time()


    if current_user.is_authenticated and \
        not current_user.confirm and \
        request.endpoint[:5] != 'auth.' and \
        request.endpoint != 'static':
        return redirect(url_for('auth.request_confirm'))

