from flask import jsonify
from sqlalchemy import desc, asc

from app.libs.error_code import Success
from app.config.setting import LAND_VIEW_TYPE, LAND_USAGE_TYPE, LAND_REGION, LAND_BLOCK_STATUS, SINGLEROOM_ORDER, \
    ORDER_AD, HISTSUP_ORDER, LAND_ORDER
import datetime


class SuccessViewModel:
    code = Success().code
    msg = Success().msg
    error_code = Success().error_code

    @classmethod
    def redict(cls, dicts):
        success_json = {"lists": dicts,
                        "code": cls.code,
                        "msg": cls.msg,
                        "error_code": cls.error_code}
        return jsonify(success_json)

    @classmethod
    def redict_page(cls, dicts, page, total):
        if page is None:
            page = ""
        success_json = {"lists": dicts,
                        "code": cls.code,
                        "msg": cls.msg,
                        "page": page,
                        "total": total,
                        "error_code": cls.error_code}
        return jsonify(success_json)

    # @classmethod
    # def logout(cls, dicts):
    #     success_json = {"lists": dicts,
    #                     "code": 204,
    #                     "msg": "登出",
    #                     "error_code": cls.error_code}
    #     return jsonify(success_json)

    @classmethod
    def __cut_data(cls, dict):
        pass
    # 私有方法,只能在模块内使用


class getday:
    @classmethod
    def getYesterday(cls):
        cls.today = datetime.date.today()
        cls.oneday = datetime.timedelta(days=1)
        yesterday = cls.today - cls.oneday
        return yesterday

    @classmethod
    def get180daysago(cls):
        cls.today = datetime.date.today()
        cls.halfyear = datetime.timedelta(days=180)
        halfyearbefore = cls.today - cls.halfyear
        return halfyearbefore


class DataLayer:
    @classmethod
    def DataLayer(cls, lists, degree, level):
        cls.section = (max(lists) - min(lists)) / level
        ceiling = degree * cls.section + min(lists)
        # 以min(lists)为基底
        return ceiling


class MultiSelect:
    # 多选中的全选会把null记录给去除
    @classmethod
    def MultiSelect(cls, string, dic):
        if len(string) == 1 and int(string) == 1:
            return ["%%"]
        else:
            choice = string.replace(" ", "").split(",")
            lists = ['%' + dic[l] + '%' for l in choice]
            return lists


class PageChoose:
    @classmethod
    # 如果有page传入则分页,其他不分页
    def PageChoose(cls, page, per_page, data):
        if page is None or page == "" or page == 0:
            sqldata = data.all()
        else:
            sqldata = data.paginate(page=page, per_page=per_page, error_out=False).items
        return sqldata


class isempty:
    @classmethod
    def IsEmpty(cls, attri):
        return attri.data or attri.default

class DateIsEmpty:
    @classmethod
    def dateisempty(cls, attri):
        if attri.data is None or attri.data == "":
            return "1970-01-01"
        else:
            return attri.data


class singleroom_order_ad:
    @classmethod
    def Singleroom_Order_Ad(cls, ad, present):
        if ORDER_AD[ad] == "desc":
            return desc(SINGLEROOM_ORDER[present])
        else:
            return asc(SINGLEROOM_ORDER[present])


class histsup_order_ad:
    @classmethod
    def Histsup_Order_Ad(cls, ad, present):
        if ORDER_AD[ad] == "desc":
            return desc(HISTSUP_ORDER[present])
        else:
            return asc(HISTSUP_ORDER[present])


class land_order_ad:
    @classmethod
    def Land_Order_Ad(cls, ad, present):
        if ORDER_AD[ad] == "desc":
            return desc(LAND_ORDER[present])
        else:
            return asc(LAND_ORDER[present])
