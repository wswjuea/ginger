from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
# HTTP传递账号密码规范
# HTTP的header传入信息Authorization:(basic base64(账号:密码))
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'ac_type', 'scope'])

@auth.verify_password
def verify_password(token, password):
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
        # g变量即代理模式的实现,类似request
        return True


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='非法token', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token过期', error_code=1003)
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    # request 访问的接口在这里也能确定
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    # request.endpoint返回当前请求要访问的视图函数
    return User(uid, ac_type, scope)