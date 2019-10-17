from datetime import datetime
from wtforms import StringField, IntegerField, FloatField, DateField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, length, Email, Regexp, NumberRange, EqualTo
from wtforms import ValidationError
from flask_wtf import FlaskForm

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form
from app.view_models.redict import getday


class ClientForm(Form):
    account = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=5, max=32
    )])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()], default=100)
    # 默认type为100,不需要输入

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
            #数字转化为枚举类型,指代不同的注册方式
        except ValueError as e:
            raise e
        self.type.data = client

# 楼盘筛选传入验证
class FilterForm(Form):
    opening_date_min = DateField(
        # validators=[DataRequired()],
        default=getday.get180daysago()
    )
    opening_date_max = DateField(
        # validators=[DataRequired()],
        default=getday.getYesterday()
    )
    # FloatField中的default必须用""
    huxing_area_min = FloatField(
        # validators=[DataRequired()],
        default="0"
    )
    huxing_area_max = FloatField(
        # validators=[DataRequired()],
        default="30000"
    )
    houses_average_min = FloatField(
        # validators=[DataRequired()],
        default="0"
    )
    houses_average_max = FloatField(
        # validators=[DataRequired()],
        default="200000"
    )
    commercial_average_min = FloatField(
        # validators=[DataRequired()],
        default="0"
    )
    commercial_average_max = FloatField(
        # validators=[DataRequired()],
        default="200000"
    )
    view_type_choose = StringField(
        validators=[DataRequired()],
        default='1'
    )
    data_level = IntegerField(
        validators=[DataRequired()],
        default=8
    )
    hist_region_choose = StringField(
        validators=[DataRequired()],
        default='1'
    )
    # 日期,浮点型,字符串,整型设置和数据模型及数据库内容相呼应
    building_search = StringField()
    page = IntegerField()
    per_page = IntegerField(default=15)
    order_ad = StringField(
        default='1'
    )
    order_basis = StringField(
        default='2'
    )

class HistSearchForm(Form):
    building_search = StringField(validators=[DataRequired()])

class LandSearchForm(Form):
    land_search = StringField(validators=[DataRequired()])

class FilterFormId(Form):
    id = IntegerField(validators=[DataRequired()])

class FilterFormLand(Form):
    plotnum = StringField(validators=[DataRequired("请输入地块编号")])

# 单室根据预售证号获取数据
class SingleroomFilterForm(Form):
    presale_license_number = StringField(
        validators=[DataRequired("请输入预售证号")]
    )
    page = IntegerField()
    per_page = IntegerField(default=15)
    order_ad = StringField(
        default='1'
    )
    order_basis = StringField(
        default='3'
    )



# 二手房根据预售证号获取数据
class SechandhouseFilterForm(Form):
    presale_license_number = StringField(
        validators=[DataRequired("请输入预售证号")]
    )
    page = IntegerField()
    per_page = IntegerField(default=15)

class SechandhouseFormLand(Form):
    plotnum = StringField(validators=[DataRequired("请输入地块编号")])
    page = IntegerField()
    per_page = IntegerField(default=15)

# 土地地块筛选传入验证
class LandFilterForm(Form):
    land_view_type_choose = StringField(
        validators=[DataRequired()],
        default='1'
    )
    data_level = IntegerField(
        validators=[DataRequired()],
        default=8
    )

    land_search = StringField()

    listing_start_date_min = DateField(
        # validators=[DataRequired()],
        default=getday.get180daysago()
    )
    listing_start_date_max = DateField(
        # validators=[DataRequired()],
        default=getday.getYesterday()
    )
    total_land_area_min = FloatField(
        # validators=[DataRequired()],
        default="0"
    )
    total_land_area_max = FloatField(
        # validators=[DataRequired()],
        default="99999999999"
    )
    price_min = FloatField(
        # validators=[DataRequired()],
        default="0"
    )
    price_max = FloatField(
        # validators=[DataRequired()],
        default="99999999999"
    )
    deal_date_min = DateField(
        # validators=[DataRequired()],
        default="0000-00-00"
    )
    deal_date_max = DateField(
        # validators=[DataRequired()],
        default=getday.getYesterday()
    )
    deal_price_min = FloatField(
        # validators=[DataRequired()],
        default="0"
    )
    deal_price_max = FloatField(
        # validators=[DataRequired()],
        default="99999999999"
    )
    land_region_choose = StringField(
        validators=[DataRequired()],
        default='1'
    )
    land_usage_type_choose = StringField(
        validators=[DataRequired()],
        default='1'
    )
    land_block_status_choose = StringField(
        validators=[DataRequired()],
        default='1'
    )
    page = IntegerField()
    per_page = IntegerField(default=15)
    order_ad = StringField(
        default='1'
    )
    order_basis = StringField(
        default='1'
    )

class LandFilterFormId(Form):
    id = IntegerField(validators=[DataRequired()])

class LandFileDn(Form):
    pn = StringField(validators=[DataRequired()])
    ft = StringField(validators=[DataRequired()])

class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')#6到22个字符
    ])
    nickname = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()
        # 根据方法名,自动对应email的验证

class BookSearchForm(Form):
    q = StringField(validators=[DataRequired()])

class LatlngSearchForm(Form):
    pname = StringField(validators=[DataRequired()])
    # DataRequired()需要数据,否则报错;validators是一个list,可以传入多个验证

class BuildingSearchForm(Form):
    b = StringField(validators=[DataRequired()])

class UserFeedbackForm(Form):
    title = StringField(validators=[DataRequired()])
    text = TextAreaField(validators=[DataRequired()])

