from flask import request
from wtforms import Form
import json

from app.libs.error_code import PatameterException


class BaseForm(Form):
    def __init__(self):
        # data = request.form
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise PatameterException(msg=self.errors)
            # raise PatameterException(msg="账号密码错误")
        # 不抛出异常的特性,改为抛出异常
        return self