from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    # 返回一个HTTPException对象,flask内部依然会读取get_body()和get_headers()
    code = 500
    msg = 'sorry,we make a mistake'
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None, headers=None):
        # 默认所有信息为None,如果存在则直接修改实例默认值,不需要对比,只需要有返回即修改为返回值
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        # 基类HTTPException的构造函数
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg = self.msg,
            error_code = self.error_code,
            request = request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [("Content-Type", "application/json")]
    # 访问整个类,返回头部信息,返回修改为json格式

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
        # 以?分割返回信息,取头链接