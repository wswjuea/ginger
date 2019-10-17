from app.libs.redprint import Redprint
from app.libs.token_auth import auth

from app.validators.forms import LatlngSearchForm
from app.models.latlng import Latlng

from app.view_models.redict import SuccessViewModel

api = Redprint('latlng')


# @api.route('/all')
# @auth.login_required
# def all():
#     SQL = 'select * from latlng'
#     engine = sqlalchemy.create_engine('mysql+pymysql://root:1234@47.104.104.31/ginger')
#     latlng = pd.read_sql(SQL, con=engine)
#     engine.dispose()
#     return latlng.to_json(orient='index')

@api.route('/all')
@auth.login_required
# def all():
#     latlngs = Latlng.query.all()
#     result = []
#     for latlng in latlngs:
#         result.append(latlng.to_json())
#     return str(result)
def all():
    latlngs = Latlng.query.all()#字典
    # dict = {"lists": latlngs,
    #         "code": Success().code,
    #         "msg": Success().msg,
    #         "error_code": Success().error_code}
    return SuccessViewModel.redict(latlngs)
# jsonify会将头部带上content-type:application/json,但是panda.to_json只是将对象转化成json格式,所以需要设置response.headers


@api.route('/search')
@auth.login_required
def search():
    form = LatlngSearchForm().validate_for_api()
    pname = '%' + form.pname.data + '%'
    # 获取传入的pname
    # pname <class 'str'>
    latlngs = Latlng.query.filter(
        Latlng.project_name.like(pname)
    ).all()
    return SuccessViewModel.redict(latlngs)

@api.route('/id/<id>/detail')
@auth.login_required
def get_latlng(id):
    latlngs = Latlng.query.filter_by(id=id).first_or_404()
    # if status == '':
    #     status = 1
    # latlngs = Latlng.query.filter(
    #     Latlng.status == status
    # ).all()
    return SuccessViewModel.redict(latlngs)