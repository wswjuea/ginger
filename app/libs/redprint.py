class Redprint:
    def __init__(self, name):
        self.name = name
        self.mound = []

    # route函数|装饰器,接收了一组参数,调用了其中的方法,完成视图函数向蓝图注册
    def route(self, rule, **options):
        # f即定义的方法,装饰器作用的方法;实现了视图函数向蓝图注册的过程;route()带参数的装饰器的实现
        def decorator(f):
            self.mound.append((f, rule, options))
            return f
        return decorator

    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = '/' + self.name
        for f, rule, options in self.mound:
            endpoint = self.name + '+' + options.pop("endpoint", f.__name__)
            #pop()即取endpoint对应的值,如果endpoint的值不存在则用视图函数的名字作为endpoint的值
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
            #必须用**options,上面传入的也是**options