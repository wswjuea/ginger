from flask import Blueprint
from app.api.v1 import user, book, client, token, gift, latlng, histsup, singleroom, sechandhouse, land


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    #视图函数的初始化注册
    user.api.register(bp_v1)
    book.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    gift.api.register(bp_v1)
    latlng.api.register(bp_v1)
    histsup.api.register(bp_v1)
    singleroom.api.register(bp_v1)
    sechandhouse.api.register(bp_v1)
    land.api.register(bp_v1)
    return bp_v1