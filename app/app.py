from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from app.libs.error_code import ServerError
from datetime import date
from decimal import Decimal


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        # python不能序列化的对象要特殊处理
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, Decimal):
            return o.__float__()
        raise ServerError()

class Flask(_Flask):
    json_encoder = JSONEncoder