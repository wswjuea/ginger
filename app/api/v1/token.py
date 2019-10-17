
from flask import current_app, jsonify, session
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
# 加密算法
from app.libs.token_auth import auth
from app.libs.enums import ClientTypeEnum
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm
from app.view_models.redict import SuccessViewModel

api = Redprint('token')

@api.route('', methods=['POST'])
# 用GET方法会将密码放置在url上,作为查询参数,不安全,用POST方法可以将密码放在http的body中传递
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify
    }
    identity = promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.secret.data
    )
    # Token
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identity['uid'],
                                form.type.data,
                                identity['scope'],
                                expiration)
    t = {
        'token': token.decode('ascii')
    }# 转化字符串类型
    # return jsonify(t), 201
    return SuccessViewModel.redict(t)

@api.route('/logout')
@auth.login_required
def logout():
    t = {
        'token': ''
    }
    session.clear()

    return SuccessViewModel.redict(t)

def generate_auth_token(uid, ac_type, scope=None,
                        expiration=7200):
    # expiration令牌有效期,默认2小时
    """生成令牌"""
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'scope': scope
    })