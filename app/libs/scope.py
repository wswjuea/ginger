class Scope:
    allow_api = []
    allow_module = []
    forbidden = []

    def __add__(self, other):
        # 对象的相加行为,__add__是python内置的写法,可以直接用+代替object1.__add__(object2)
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))# 转化为集合去重

        self.allow_module = self.allow_module + other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))

        return self

class AdminScope(Scope):
    # 两种权限设置方式,设置模块权限或模块中视图的权限
    # allow_api = ['v1.user+super_get_user',
    #              'v1.user+super_delete_user']
    allow_module = ['v1.user']

    def __init__(self):
        self + UserScope()
        pass

# 普通用户的权限是最少的,不同级别的账号权限之间是子集,全包含的关系
class UserScope(Scope):
    allow_api = ['v1.user+get_user',
                 'v1.user+delete_user',
                 'v1.user+feedback',
                 'v1.latlng+all',
                 'v1.latlng+search',
                 'v1.latlng+get_latlng',
                 'v1.land+all',
                 'v1.land+filter',
                 'v1.land+search_id',
                 'v1.land+search_latlng',
                 'v1.land+landsearch',
                 'v1.histsup+all',
                 'v1.histsup+filter',
                 'v1.histsup+search_id',
                 'v1.histsup+search_latlng',
                 'v1.histsup+land_histsup',
                 'v1.histsup+histsearch',
                 'v1.singleroom+all',
                 'v1.singleroom+prelic',
                 'v1.singleroom+prelic_dls',
                 'v1.sechandhouse+all',
                 'v1.sechandhouse+prelic',
                 'v1.sechandhouse+prelic_dls',
                 'v1.sechandhouse+land_sec',
                 'v1.token+logout']

# 排除法,普通用户只是没有小部分视图查询的权限,拥有大部分和管理员一样的权限
# class UserScope(Scope):
#     forbidden = ['v1.user+super_get_user',
#                  'v1.user+super_delete_user']
#
#     def __init__(self):
#         self + AdminScope()


# 超级管理员权限
# class SuperScope(Scope):
#     allow_api = ['v1.C', 'v1.D']
#     allow_module = ['v1.user']
#
#     def __init__(self):
#         self + UserScope() + AdminScope()



def is_in_scope(scope, endpoint):
    # 反射,在python中用globals()获取全局变量的字典
    scope = globals()[scope]()
    # 将scope从字符串转变为对象
    # 期望endpoint包含v1.module_name+view_func
    # v1.red_name+view_func
    splits = endpoint.split('+')
    red_name = splits[0]
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False