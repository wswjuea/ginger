from flask import send_from_directory
from sqlalchemy import and_, or_
import os, difflib

from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.config.setting import LAND_VIEW_TYPE, LAND_USAGE_TYPE, LAND_REGION, LAND_BLOCK_STATUS, LAND_FILE_TYPE

from app.view_models.redict import SuccessViewModel, isempty, land_order_ad
from app.models.land import Land
from app.view_models.land import LandViewModel
from app.validators.forms import LandFilterForm, LandFilterFormId, LandFileDn, LandSearchForm
from app.view_models.redict import DataLayer, MultiSelect, PageChoose, DateIsEmpty

api = Redprint('land')


@api.route('/all')
@auth.login_required
def all():
    lands = Land.query.all()
    lands = [LandViewModel.landviewmodel(land) for land in lands]
    # 显示状态码
    for land in lands:
        land["display_code"] = 0
    lands[0]["display_code"] = 1

    return SuccessViewModel.redict(lands)


# POST筛选
@api.route('/filter', methods=['POST'])
@auth.login_required
def filter():
    form = LandFilterForm().validate_for_api()
    ad = form.order_ad.data
    present = form.order_basis.data
    land_search = '%' + form.land_search._value().replace(" ", "") + '%'

    # 区域,土地用途,地块状态多选
    region_choose = \
        MultiSelect.MultiSelect(string=form.land_region_choose.data, dic=LAND_REGION)
    land_usage_choose = \
        MultiSelect.MultiSelect(string=form.land_usage_type_choose.data, dic=LAND_USAGE_TYPE)
    block_status_choose = \
        MultiSelect.MultiSelect(string=form.land_block_status_choose.data, dic=LAND_BLOCK_STATUS)

    lands = Land.query.filter(and_(
        Land.listing_start_date >= DateIsEmpty.dateisempty(form.listing_start_date_min),
        Land.listing_start_date <= isempty.IsEmpty(form.listing_start_date_max),
        Land.total_land_area >= isempty.IsEmpty(form.total_land_area_min),
        Land.total_land_area <= isempty.IsEmpty(form.total_land_area_max),
        Land.price >= isempty.IsEmpty(form.price_min),
        Land.price <= isempty.IsEmpty(form.price_max),
        Land.deal_date > isempty.IsEmpty(form.deal_date_min) if form.land_view_type_choose.data == '2'
        else Land.deal_date >= isempty.IsEmpty(form.deal_date_min),
        Land.deal_date <= isempty.IsEmpty(form.deal_date_max),
        Land.deal_price >= isempty.IsEmpty(form.deal_price_min),
        Land.deal_price <= isempty.IsEmpty(form.deal_price_max),
        or_(
            Land.plotnum.like(land_search),
            Land.block_name.like(land_search),
            Land.block_location.like(land_search),
            Land.competitive_unit.like(land_search),
            Land.deal_date.like(land_search)
        ),
        or_(
            *[Land.region.like(r) for r in region_choose]
        )
        ,
        or_(
            *[Land.land_usage.like(l) for l in land_usage_choose]
        ),
        or_(
            *[Land.block_status.like(b) for b in block_status_choose]
        )
    )).order_by(land_order_ad.Land_Order_Ad(ad=ad, present=present))

    total = len(lands.all())
    # 如果有page传入则分页,其他不分页
    page = form.page.data
    per_page = form.per_page.data
    lands = PageChoose.PageChoose(page=page, per_page=per_page, data=lands)

    # 视图层转化
    lands = [LandViewModel.landviewmodel(land, LAND_VIEW_TYPE[form.land_view_type_choose.data]) for land in lands]

    # 添加levels字段
    landrange = [land[LAND_VIEW_TYPE[form.land_view_type_choose.data]] for land in lands]
    level = int(form.data_level.data)
    for land in lands:
        for i in range(level):
            if land[LAND_VIEW_TYPE[form.land_view_type_choose.data]] <= \
                    DataLayer.DataLayer(lists=landrange, degree=i + 1, level=level):
                land['levels'] = i + 1
                break
    # 显示状态码
    if len(lands) > 0:
        for land in lands:
            land["display_code"] = 0
        lands[0]["display_code"] = 1

    return SuccessViewModel.redict_page(dicts=lands, page=page, total=total)

# @api.route('/keyword', methods=['POST'])
# @auth.login_required
# def keyword():
#     form = LandFilterForm().validate_for_api()
#     keyword = form.land_search.data


@api.route('/id', methods=['POST'])
@auth.login_required
def search_id():
    form = LandFilterFormId().validate_for_api()
    idents = Land.query.filter(
        Land.id == form.id.data
    ).first()
    idents = LandViewModel.landsearchbyid(idents)
    return SuccessViewModel.redict(idents)


@api.route('/loca', methods=['POST'])
@auth.login_required
def search_latlng():
    form = LandFilterFormId().validate_for_api()
    lat, lng = Land.query.with_entities(Land.lat, Land.lng).filter(
        Land.id == form.id.data
    ).first()
    lands = Land.query.filter(
        and_(
            Land.lat == lat,
            Land.lng == lng
        )
    ).all()
    lands = [LandViewModel.landsearchbylatlng(land) for land in lands]
    return SuccessViewModel.redict(lands)


@api.route('/isfile')
# @auth.login_required
def isfile():
    form = LandFileDn().validate_for_api()
    plotnum = form.pn.data
    file_type = form.ft.data
    directory = "/home/work/ginger/landfile/" + plotnum
    filelist = []

    if not os.path.exists(directory):
        return "False"
    else:
        for root, dirs, files in os.walk(directory):
            filelist = files
        a = difflib.get_close_matches(LAND_FILE_TYPE[file_type], filelist, 1)
        return "False" if not a else "True"


@api.route('/filedn')
# @auth.login_required
def filedn():
    form = LandFileDn().validate_for_api()
    plotnum = form.pn.data
    file_type = form.ft.data
    directory = "/home/work/ginger/landfile/" + plotnum
    filelist = []

    for root, dirs, files in os.walk(directory):
        filelist = files
    a = difflib.get_close_matches(LAND_FILE_TYPE[file_type], filelist, 1)
    return send_from_directory(directory=directory, filename=a[0],
                               as_attachment=True)


# C:/Users/33066/Desktop/土地1/
# /home/work/ginger/landfile/

@api.route('/land_search', methods=['POST'])
@auth.login_required
def landsearch():
    keyword_completes = []
    form = LandSearchForm().validate_for_api()
    land_search = '%' + form.land_search._value().replace(" ", "") + '%'
    keyword_completes_plotnum = Land.query.filter(
        Land.plotnum.like(land_search)
    ).all()
    for keyword_complete in keyword_completes_plotnum:
        keyword_completes.append(
            LandViewModel.landsearch(keyword_complete, "plotnum")
        )

    keyword_completes_block_location = Land.query.filter(
        Land.block_location.like(land_search)
    ).all()
    for keyword_complete in keyword_completes_block_location:
        keyword_completes.append(
            LandViewModel.landsearch(keyword_complete, "block_location")
        )

    keyword_completes_competitive_unit = Land.query.filter(
        Land.competitive_unit.like(land_search)
    ).all()
    for keyword_complete in keyword_completes_competitive_unit:
        keyword_completes.append(
            LandViewModel.landsearch(keyword_complete, "competitive_unit")
        )

    keyword_completes_deal_date = Land.query.filter(
        Land.deal_date.like(land_search)
    ).all()
    for keyword_complete in keyword_completes_deal_date:
        keyword_completes.append(
            LandViewModel.landsearch(keyword_complete, "deal_date")
        )

    keyword_completes = list(set(keyword_completes))
    return SuccessViewModel.redict(keyword_completes)
