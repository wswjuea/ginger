from flask import jsonify, g, request, render_template, redirect, flash, url_for, session

from app.libs.error_code import DeleteSuccess, AuthFailed
from app.view_models.redict import SuccessViewModel
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.user import User
from app.models.feedback import Feedback
from app.validators.forms import UserFeedbackForm
from flask_login import login_user, login_required, logout_user, current_user
import datetime


api = Redprint('user')

# 管理员查询普通用户
@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
# 被保护的接口,进入app.libs.token_auth的@auth.verify_password验证账号密码
def super_get_user(uid):
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)

@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    uid = g.user.uid
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)

# 管理员删除普通用户
@api.route('/<int:uid>', methods=['DELETE'])
def super_delete_user(uid):
    pass

@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    # 超权问题,普通权限的用户可以获取token直接删除其他用户
    # 通过用户使用的token中携带的uid来进行删除,不可以随意设置uid
    uid = g.user.uid
    # g变量是线程隔离的,两个用户同时删除,不会出现线程错乱的问题
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()


@api.route('/feedback', methods=['POST'])
@auth.login_required
def feedback():
    form = UserFeedbackForm().validate_for_api()
    uid = g.user.uid
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    title = form.title.data
    text = form.text.data
    Feedback.feedback(uid=uid, create_time=create_time, title=title, text=text)
    return SuccessViewModel.redict(dicts=[])


