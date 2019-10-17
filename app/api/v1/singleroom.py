
from app.libs.redprint import Redprint
from app.models.singleroom import Singleroom
from app.view_models.redict import SuccessViewModel, PageChoose, singleroom_order_ad
from app.validators.forms import SingleroomFilterForm, BuildingSearchForm
from app.libs.token_auth import auth
from flask import send_from_directory
from app.view_models.singleroom import SingleroomViewModel
import pandas as pd

api = Redprint('singleroom')


@api.route('/all')
@auth.login_required
def all():
    singleroom = Singleroom.query.all()
    return SuccessViewModel.redict(singleroom)


@api.route('/prelic', methods=['POST'])
@auth.login_required
def prelic():
    form = SingleroomFilterForm().validate_for_api()
    ad = form.order_ad.data
    present = form.order_basis.data

    prelic = form.presale_license_number.data
    singlerooms = Singleroom.query.filter(
        Singleroom.presale_license_number == prelic
        # ,
        # Singleroom.state != '非销售房产'
    ).order_by(singleroom_order_ad.Singleroom_Order_Ad(ad=ad, present=present))

    total = len(singlerooms.all())
    # 分页
    page = form.page.data
    per_page = form.per_page.data
    singlerooms = PageChoose.PageChoose(page=page, per_page=per_page, data=singlerooms)

    singlerooms = [SingleroomViewModel.singleroomviewmodel(singleroom) for singleroom in singlerooms]
    # 总价无法计算是因为对象返回时list,未通过其他视图层转化成字典对象
    return SuccessViewModel.redict_page(dicts=singlerooms, page=page, total=total)

# 导出数据api
@api.route('/prelic/download')
# @auth.login_required
def prelic_dls():
    singlerooms_to_xlsx = pd.DataFrame()
    form = BuildingSearchForm().validate_for_api()
    prelic = form.b.data
    singlerooms = Singleroom.query.filter(
        Singleroom.presale_license_number == prelic
    ).all()
    singlerooms = [SingleroomViewModel.singleroomdw(singleroom) for singleroom in singlerooms]

    if len(singlerooms) > 0:
        singlerooms = [dict(singleroom) for singleroom in singlerooms]
        singlerooms_to_xlsx = pd.DataFrame(
            singlerooms, columns=list(singlerooms[0].keys())
        ).rename(columns={
            'presale_license_number': '预售许可证号',
            'building_promotion_name': '项目名称',
            'building_name': '项目备案名',
            'build_name': '幢名',
            'room_number': '室号',
            'state': '属性',
            'overall_floorage': '总建筑面积(㎡)',
            'sold_date': '销售日期',
            'room_price': '单价(元/㎡)',
            'total_price': '总价(元)'
        })

    singlerooms_to_xlsx.to_excel("/home/work/ginger/downloads/singlerooms.xlsx", index=False)
    return send_from_directory("/home/work/ginger/downloads/", filename="singlerooms.xlsx",
                               as_attachment=True)
# C:/Users/33066/Desktop/ginger/downloads/
# /home/work/ginger/downloads/
