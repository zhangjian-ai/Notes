from flask import Flask, request


def create_app():
    app = Flask(__name__)
    app.secret_key = "dghs$sga73#af)sva@vdsak!dfs6"

    @app.route('/index')
    def index():
        return '主页'

    # 蓝图：帮助构建业务功能可拆分的目录结构
    # 关联蓝图
    # 蓝图类似于 django 中的一个 app
    from .goods.views import goods
    from .user.views import user

    app.register_blueprint(goods)
    app.register_blueprint(user, url_prefix='/demo')  # url_prefix 为蓝图路由添加前缀。注册蓝图类似于 django 的路由分发

    return app
