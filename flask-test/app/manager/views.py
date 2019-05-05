# coding: utf-8
from . import manager
from ..models import User,Posts,Device
from flask import render_template,redirect,url_for,flash,request,abort
from .forms import FindUserForm,EditPostInfoForm,PostForm,EditUserForm
from sqlalchemy import or_
from app import db
from flask_login import  current_user
@manager.route('manager_user',methods=['GET','POST'])
def manager_user():
    form = FindUserForm()
    users = User.query.all()

    return render_template('manager/manager_user.html',users=users,form=form)

@manager.route('/edit_user',methods=['GET','POST'])
def edit_user():
    form = EditUserForm()
    id = request.args.get('id')
    user = User.query.filter_by(id=id).first()
    if form.validate_on_submit():
        user.name = form.name.data
        user.location=form.location.data
        user.about_me = form.about_me.data

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.manager_user',id=current_user.id))
    return render_template('manager/edituser.html',form=form)

@manager.route('delete_user')
def delete_user():
    id = request.args.get('id')
    if id is None :
        abort(404)
    user = User.query.filter_by(id=id).first()
    if user is None :
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('.manager_user',id=current_user.id))

@manager.route('/edit_post',methods = ['GET','POST'])
def edit_post():
    form=EditPostInfoForm()
    id = request.args.get('id')
    if id is None :
        abort(404)
    post=Posts.query.filter_by(id=id).first()
    if post is None :
        abort(404)
    if form.validate_on_submit():
        post.title=form.title.data
        post.body=form.content.data
        post.timestamp=datetime.now()
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.manager_posts'))
    return render_template('manager/edit_post.html',form=form)


from ..models import Posts,Comment
from .forms import PostForm
@manager.route('/manager_posts')
def manager_posts():

    posts = Posts.query.all()

    return render_template('manager/manager_posts.html',posts = posts,)



from datetime import datetime
@manager.route('/add_post',methods=['GET','POST'])
def add_post():
    form = PostForm()
    post = Posts()
    if form.validate_on_submit():
        post.title=form.title.data
        post.body=form.content.data
        post.timestamp=datetime.now()
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.manager_posts'))
    return render_template('manager/add_post.html',form=form)

@manager.route('/delete_post')
def delete_post():
    id = request.args.get('id')
    if id is None:
        abort(404)
    post = Posts.query.filter_by(id=id).first()
    if post is None:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('.manager_posts'))


@manager.route('/manager_devices')
def manager_devices():
    devices = Device.query.all()
    users = User.query.all()
    return render_template('manager/manager_devices.html',devices=devices,users=users)

@manager.route('/delete_device')
def delete_device():
    id = request.args.get('id')
    if id is None:
        abort(404)
    device = Device.query.filter_by(id=id).first()
    if device is None:
        abort(404)
    db.session.delete(device)
    db.session.commit()
    return redirect(url_for('.manager_devices'))

@manager.route('/manager')
def manager():
    return render_template('manager.html')


