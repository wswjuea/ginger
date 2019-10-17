from flask import jsonify
from sqlalchemy import and_, or_, desc

from app.libs.redprint import Redprint
from app.libs.token_auth import auth

from app.view_models.redict import SuccessViewModel
from app.view_models.histsup import HistsupViewModel
from app.validators.forms import FilterForm, FilterFormId, FilterFormLand, HistSearchForm
from app.models.histsup import Histsup
from app.config.setting import VIEW_TYPE, HIST_REGION, HIST_SEARCH_ATTRI
from app.view_models.redict import DataLayer, MultiSelect, PageChoose, isempty, histsup_order_ad, DateIsEmpty

api = Redprint('histsup')

# 全量查询
@api.route('/all')
@auth.login_required
def all():
    histsups = Histsup.query.all()
    histsups = [dict(histsup) for histsup in histsups]
    # 显示状态码
    for histsup in histsups:
        histsup["display_code"] = 0
    histsups[0]["display_code"] = 1
    return SuccessViewModel.redict(histsups)


# 四图层选择数据
# @api.route('/<viewtype>')
# @auth.login_required
# def view_four(viewtype):
#     housesaves = Histsup.query.all()
#     re_view = [HistsupViewModel.re_data(x, viewtype) for x in housesaves]
#     return SuccessViewModel.redict(re_view)

# POST筛选
@api.route('/filter', methods=['POST'])
@auth.login_required
def filter():
    form = FilterForm().validate_for_api()
    ad = form.order_ad.data
    present = form.order_basis.data
    # 多条件筛选
    building_search = '%' + form.building_search._value().replace(" ", "") + '%'
    #区域多选
    region_choose = \
        MultiSelect.MultiSelect(string=form.hist_region_choose.data, dic=HIST_REGION)

    histsups = Histsup.query.filter(and_(
        Histsup.opening_date >= DateIsEmpty.dateisempty(form.opening_date_min),
        Histsup.opening_date <= isempty.IsEmpty(form.opening_date_max),
        Histsup.huxing_area >= isempty.IsEmpty(form.huxing_area_min),
        Histsup.huxing_area <= isempty.IsEmpty(form.huxing_area_max),
        Histsup.houses_average >= isempty.IsEmpty(form.houses_average_min),
        Histsup.houses_average <= isempty.IsEmpty(form.houses_average_max),
        Histsup.commercial_average >= isempty.IsEmpty(form.commercial_average_min),
        Histsup.commercial_average <= isempty.IsEmpty(form.commercial_average_max),
        or_(
            Histsup.building_promotion_name.like(building_search),
            Histsup.building_name.like(building_search),
            Histsup.presale_license_number.like(building_search),
            Histsup.building_address.like(building_search)
        ),
        or_(
            *[Histsup.region.like(r) for r in region_choose]
        )
    )).order_by(histsup_order_ad.Histsup_Order_Ad(ad=ad, present=present))

    total = len(histsups.all())
    # 如果有page传入则分页,其他不分页
    page = form.page.data
    per_page = form.per_page.data
    histsups = PageChoose.PageChoose(page=page, per_page=per_page, data=histsups)

    # 视图层转化
    histsups = [HistsupViewModel.re_data(histsup, VIEW_TYPE[form.view_type_choose.data])
                for histsup in histsups]

    # 添加levels字段
    hisrange = [histsup[VIEW_TYPE[form.view_type_choose.data]] for histsup in histsups]
    level = form.data_level.data
    for histsup in histsups:
        for i in range(level):
            if histsup[VIEW_TYPE[form.view_type_choose.data]] <= \
                    DataLayer.DataLayer(lists=hisrange, degree=i+1, level=level):
                histsup['levels'] = i + 1
                break
    # 显示状态码
    if len(histsups) > 0:
        for histsup in histsups:
            histsup["display_code"] = 0
        histsups[0]["display_code"] = 1

    return SuccessViewModel.redict_page(histsups, page=page, total=total)

@api.route('/id', methods=['POST'])
@auth.login_required
def search_id():
    form = FilterFormId().validate_for_api()
    idents = Histsup.query.filter(
        Histsup.id == form.id.data
    ).first()
    idents = HistsupViewModel.histsearchbyid(idents)
    return SuccessViewModel.redict(idents)


@api.route('/loca', methods=['POST'])
@auth.login_required
def search_latlng():
    form = FilterFormId().validate_for_api()
    lat, lng = Histsup.query.with_entities(Histsup.lat, Histsup.lng).filter(
        Histsup.id == form.id.data
    ).first()
    histsups = Histsup.query.filter(
        and_(
            Histsup.lat == lat,
            Histsup.lng == lng
        )
    ).order_by(Histsup.opening_date.desc()).all()
    histsups = [HistsupViewModel.histsearchbylatlng(histsup) for histsup in histsups]
    return SuccessViewModel.redict(histsups)


@api.route('/land_histsup', methods=['POST'])
@auth.login_required
def land_histsup():
    form = FilterFormLand().validate_for_api()
    plotnum = form.plotnum.data
    histsups = Histsup.query.filter(
        Histsup.plotnum == plotnum
    ).first()
    if histsups is not None:
        histsups = HistsupViewModel.histsearchbylandid(histsups)
    else:
        histsups = []

    return SuccessViewModel.redict(histsups)

@api.route('/hist_search', methods=['POST'])
@auth.login_required
def histsearch():
    keyword_completes = []
    form = HistSearchForm().validate_for_api()
    building_search = '%' + form.building_search._value().replace(" ", "") + '%'
    # for attri in HIST_SEARCH_ATTRI:
    #     keyword_completes_building_promotion_name = Histsup.query.filter(
    #         or_(
    #             Histsup.building_promotion_name.like(building_search),
    #             Histsup.building_name.like(building_search),
    #             Histsup.presale_license_number.like(building_search),
    #             Histsup.building_address.like(building_search)
    #         )
    #     ).all()
    #     for keyword_complete in keyword_completes_building_promotion_name:
    #         keyword_completes.append(
    #             HistsupViewModel.histsearch(keyword_complete, attri)
    #         )

    keyword_completes_building_promotion_name = Histsup.query.filter(
        Histsup.building_promotion_name.like(building_search)
    ).all()
    for keyword_complete in keyword_completes_building_promotion_name:
        keyword_completes.append(
            HistsupViewModel.histsearch(keyword_complete, "building_promotion_name")
        )

    keyword_completes_building_name = Histsup.query.filter(
        Histsup.building_name.like(building_search)
    ).all()
    for keyword_complete in keyword_completes_building_name:
        keyword_completes.append(
            HistsupViewModel.histsearch(keyword_complete, "building_name")
        )

    keyword_completes_presale_license_number = Histsup.query.filter(
        Histsup.presale_license_number.like(building_search)
    ).all()
    for keyword_complete in keyword_completes_presale_license_number:
        keyword_completes.append(
            HistsupViewModel.histsearch(keyword_complete, "presale_license_number")
        )

    keyword_completes_building_address = Histsup.query.filter(
        Histsup.building_address.like(building_search)
    ).all()
    for keyword_complete in keyword_completes_building_address:
        keyword_completes.append(
            HistsupViewModel.histsearch(keyword_complete, "building_address")
        )

    keyword_completes = list(set(keyword_completes))
    return SuccessViewModel.redict(keyword_completes)
