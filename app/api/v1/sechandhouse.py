from flask import send_from_directory

from app.libs.redprint import Redprint
from app.models.sechandhouse import Sechandhouse
from app.view_models.redict import SuccessViewModel, PageChoose
from app.validators.forms import SechandhouseFilterForm, BuildingSearchForm, SechandhouseFormLand
from app.libs.token_auth import auth
import pandas as pd
from app.view_models.sechandhouse import SechandhouseViewModel

api = Redprint('sechandhouse')

@api.route('/all')
@auth.login_required
def all():
    sechandhouse = Sechandhouse.query.all()
    return SuccessViewModel.redict(sechandhouse)

@api.route('/prelic', methods=['POST'])
@auth.login_required
def prelic():
    form = SechandhouseFilterForm().validate_for_api()

    prelic = form.presale_license_number.data
    sechandhouses = Sechandhouse.query.filter(
        Sechandhouse.presale_license_number == prelic
    )
    total = len(sechandhouses.all())
    # 分页
    page = form.page.data
    per_page = form.per_page.data
    sechandhouses = PageChoose.PageChoose(page=page, per_page=per_page, data=sechandhouses)

    sechandhouses = \
        [SechandhouseViewModel.secviewmodel(sechandhouse) for sechandhouse in sechandhouses]

    return SuccessViewModel.redict_page(dicts=sechandhouses, page=page, total=total)

# 导出数据api
@api.route('/prelic/download')
# @auth.login_required
def prelic_dls():
    sechandhouses_to_xlsx = pd.DataFrame()
    form = BuildingSearchForm().validate_for_api()
    prelic = form.b.data
    sechandhouses = Sechandhouse.query.filter(
        Sechandhouse.presale_license_number == prelic
    ).all()
    sechandhouses = \
        [SechandhouseViewModel.secdw(sechandhouse) for sechandhouse in sechandhouses]

    if len(sechandhouses) > 0:
        sechandhouses = [dict(sechandhouse) for sechandhouse in sechandhouses]
        sechandhouses_to_xlsx = pd.DataFrame(
            sechandhouses, columns=list(sechandhouses[0].keys())
        ).rename(columns={
            'title': '标题',
            'building_promotion_name': '项目名称',
            'huxing': '房屋户型',
            'on_floor': '所在楼层',
            'overall_floorage': '建筑面积(㎡)',
            'house_orientation': '房屋朝向',
            'decoration': '装修情况',
            'tier_house_ratio': '梯户比例',
            'elevator': '配备电梯',
            'listing_date': '挂牌时间',
            'transaction_ownership': '交易权属',
            'room_price': '单价(元/㎡)',
            'total_price': '总价(万元)'
        })

    sechandhouses_to_xlsx.to_excel("/home/work/ginger/downloads/sechandhouses.xlsx", index=False)
    return send_from_directory("/home/work/ginger/downloads/", filename="sechandhouses.xlsx",
                               as_attachment=True)

# @api.route('/land_sec', methods=['POST'])
# @auth.login_required
# def land_sec():
#     form = SechandhouseFormLand().validate_for_api()
#     plotnum = form.plotnum.data
#     sechandhouses = Sechandhouse.query.filter(
#         Sechandhouse.plotnum == plotnum
#     )
#
#     total = len(sechandhouses.all())
#     # 分页
#     page = form.page.data
#     per_page = form.per_page.data
#     sechandhouses = PageChoose.PageChoose(page=page, per_page=per_page, data=sechandhouses)
#
#     sechandhouses = \
#         [SechandhouseViewModel.secviewmodel(sechandhouse) for sechandhouse in sechandhouses]
#     return SuccessViewModel.redict_page(dicts=sechandhouses, page=page, total=total)
