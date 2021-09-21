from flask import Blueprint, current_app

user = Blueprint('user', __name__, static_folder='static', template_folder='templates', static_url_path='/goods')


# 创建路由接口，同flask对象
@user.route('/name')
def name():
    return current_app.secret_key  # 通过 current_app 获取 app 的 secret_key
