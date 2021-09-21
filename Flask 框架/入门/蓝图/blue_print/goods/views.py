from flask import Blueprint

goods = Blueprint('goods', __name__, static_folder='static', template_folder='templates', static_url_path='/goods')
'''
参数说明：
    goods：为Blueprint对象取一个名字。
    __name__：和Flask对象一致，传入当前蓝图所在文件名。把该目录作为 一个蓝图的 根目录。蓝图私有的静态文件、模板都相对于该目录。
    static_folder、template_folder、static_url_path 在蓝图对象中是没有默认值的，需要使用时必须显示指定。
'''


# 创建路由接口，同flask对象
@goods.route('/price')
def price():
    return '商品价格'
