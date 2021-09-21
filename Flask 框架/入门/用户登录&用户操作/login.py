import functools

from flask import Flask, request, render_template, jsonify, redirect, url_for, session

app = Flask(__name__, template_folder='.')  # template_folder 指定模版路径，默认值是当前路径的 templates 下
app.secret_key = 'dhasddyuwqejqbwghjhchashjda'  # flask 需要手动配置secret_key，没有默认值

DATA_DICT = {
    1: {'name': 'zhangjian', 'age': 28},
    2: {'name': 'zhaoyun', 'age': 26}
}


def auth(func):  # 通过装饰器实现用户认证
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if session.get('user') == 'zhangjian':
            return func(*args, **kwargs)
        return redirect('/login')
    return inner


@app.route('/login', methods=['GET', 'POST'])  # methods 指定该路由允许的请求方式
def login():
    if request.method == 'GET':
        # code = request.args.get('code')  # 获取 get 路由参数
        # return render_template('login.html')  # django 中的 render
        # return jsonify({'code': 0, 'data': [1, 2, 3]})  # django 中的 JsonResponse
        return render_template('login.html')  # 返回 html

    user = request.form.get('user')  # 获取 post 表单参数
    pwd = request.form.get('pwd')
    if user == 'zhangjian' and pwd == '123':
        session['user'] = 'zhangjian'  # 设置session，flask的session跟随cookie保存在客户端，服务器不做保存。
        return redirect('/index')  # 路由重定向

    error = '用户名或密码错误'
    return render_template('login.html', error=error)


@app.route('/index', endpoint="home")  # endpoint 是别名。不指明的情况下默认值同函数名
@auth
def index():
    data_dict = DATA_DICT
    return render_template('index.html', data_dict=data_dict)


@app.route('/edit', methods=['GET', 'POST'])
@auth
def edit():
    nid = request.args.get('nid')
    nid = int(nid)

    if request.method == 'GET':
        data = DATA_DICT[nid]
        return render_template('edit.html', data=data)

    name = request.form.get('name')
    age = request.form.get('age')

    DATA_DICT[nid]['name'] = name
    DATA_DICT[nid]['age'] = age

    return redirect(url_for('home'))


@app.route('/delete/<int:nid>')  # 获取路由传参。前面的int可以不加，默认匹配参数类型是str,加了就匹配int类型，中间不能有空格
@auth
def delete(nid):
    del DATA_DICT[nid]
    return redirect(url_for('home'))  # 通过别名重定向


if __name__ == '__main__':
    app.run('127.0.0.1', 4999)
