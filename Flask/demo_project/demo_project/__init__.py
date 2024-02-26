from flask import Flask

from .apps import *


def create_app():
    app = Flask(__name__)

    # 加载配置文件
    app.config.from_pyfile(filename="settings.py")

    # 注册蓝图
    app.register_blueprint(home)
    app.register_blueprint(user)

    return app
