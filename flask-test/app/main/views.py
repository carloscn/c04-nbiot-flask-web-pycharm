# -*- coding:UTF-8 -*-
from . import main
from flask import render_template
from flask import abort, request
from flask_login import login_required
from app.models import User,Posts
from flask_login import current_user
from ..manager.forms import EditPostInfoForm
from flask import request
from flask import session
from flask import make_response
from .forms import EditUserInfoForm,CommentsForm
from app import db
from flask import redirect, url_for
from ..models import Posts,Comment,AnonymousUserMixin
@main.route('/index')
def index():
    return render_template('main/index.html')
#没有添加前端页面
@main.route('/user_info')
def user_info():

    id = request.args.get('id')
    if id is None:
        abort(404)
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    posts= Posts.query.all()
    return render_template('main/user_info.html',user=user,posts=posts,all=False)

@main.route('/show_post')
def show_post():
    id = request.args.get('id')
    post = Posts.query.filter_by(id=id).first()
    return render_template('main/show_post.html',all=True,post=post)

@main.route('/post_comments',methods=['GET','POST'])
def post_comments():
    u_id = request.args.get('uid')
    p_id = request.args.get('pid')
    if u_id is None:
        abort(404)
    if p_id is None:
        abort(404)
    form = CommentsForm()
    comment=Comment()
    comment.user_id = u_id
    comment.post_id = p_id
    if form.validate_on_submit():
        comment.body = form.body.data
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.show_post',id = p_id))
    return render_template('main/post_comments.html',form=form)

@main.route('/edit_user_info',methods=['GET','POST'])
def edit_user_info():
    form = EditUserInfoForm()
    if form.validate_on_submit():
        current_user.name=form.name.data
        current_user.location=form.location.data
        current_user.about_me=form.about_me.data
        if not form.password.data is None:
            current_user.password=form.password.data
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('main.user_info',id=current_user.id))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('main/edit_user_info.html',form=form)


