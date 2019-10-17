from app.libs.error import APIException

class Success(APIException):
    code = 201
    msg = "ok"
    error_code = 0

class DeleteSuccess(Success):
    code = 202
    error_code = -1

class ServerError(APIException):
    code = 200
    msg = 'sorry, we made a mistake'
    error_code = 999

class ClientTypeError(APIException):
    # 400请求参数错误,401未授权,403禁止访问,404没有找到链接
    # 500服务器产生未知错误
    # 200查询成功,201创建|更新成功,204删除成功
    # 301重定向
    code = 400
    msg = "client is invalid"
    error_code = 1006

class PatameterException(APIException):
    code = 200
    msg = 'invalid parameter'
    error_code = 1000

class NotFound(APIException):
    code = 200
    msg = '当前账号不存在'
    error_code = 1001

class AuthFailed(APIException):
    code = 200
    error_code = 1005
    msg = '账号或密码错误'

class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = 'forbidden,not in scope'

class DuplicateGift(APIException):
    code = 400
    error_code = 2001
    msg = 'the current book has already in gift'
