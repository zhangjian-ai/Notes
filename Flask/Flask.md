##  一、基础入门

1. **Django 和 Flask 的区别**
   
   - Django是一个内部扩展全面的框架，Flask 是一个轻量级的框架。
   - Django 内部提供了非常多的组件：orm/session/cookie/admin/form/modelform/路由/视图/模版/中间件/分页/auth/缓存/信号/多数据库连接 等。
   - Flask 框架本身只是一个框架，没什么扩展，主要就是：路由/视图/模板(jinja2)/session/中间件等，但是第三方组件非常丰富。
   - <font color='red'>Django 的请求是逐一封装并传递到对应的函数来处理；Flask 的请求是利用上下文管理来实现的。</font>
   
2. **Flask 的快速使用**

   ``` python
   pip3 install flask
   
   '''
   依赖模块说明：
   	- Jinja2 ：Flask 模版渲染基于 Jinja2 来实现，自己本身没有模版组件
   	- Werkzeug ：充当wsgi（Web Server Gateway Interface）服务器网关接口，Flask和Django一样没有wsgi，利用第三方模块实现
   '''
   ```

   - 依赖模块Werkzeug	封装成 Flask 逻辑演示

   ``` python
   from werkzeug.serving import run_simple
   
   def func(environ, start_response):
       print("来了老弟！")
       pass
   
   if __name__ == '__main__':
       run_simple('127.0.0.1', 5000, func)  # 启动服务器，访问接口时直接调用func函数
   ```

   ``` python
   from werkzeug.serving import run_simple
   
   class Flask:
       def __call__(self, environ, start_response):
           return 'xx'
   
   app = Flask()
   
   if __name__ == '__main__':
       run_simple('127.0.0.1', 5000, app)
   ```

   ``` Python
   from werkzeug.serving import run_simple
   
   class Flask:
       def __call__(self, environ, start_response):
           return 'xx'
       
       def run(self):
           run_simple('127.0.0.1', 5000, self)
   
   app = Flask()
   
   if __name__ == '__main__':
       app.run()
   ```

   

   - 快速使用Flask

   ``` python
   from flask import Flask
   
   app = Flask(__name__)
   
   @app.route('/index')
   def index():
       return 'hello world!'
   
   if __name__ == '__main__':
       app.run()  # 默认port：5000  内部就是使用的Werkzeug模块
   ```

   

3. **用户登录&用户操作**

   ``` Python
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
   
   
   @app.route('/delete/<int:nid>')  # 获取路由传参。前面的int可以不加，默认接收到的数值类型是str,加了就把参数转换成int类型，中间不能有空格
   @auth
   def delete(nid):
       del DATA_DICT[nid]
       return redirect(url_for('home'))  # 通过别名重定向
   
   
   if __name__ == '__main__':
       app.run('127.0.0.1', 4999)

4. **蓝图**

   > 蓝图是用来帮助实现业务功能可拆分的目录结构，类似于 Django 中的app，都用来做业务拆分。
   >
   > project_name
   >
   > ｜-- blue_print
   >
   > ​	｜-- user	# 一个 user 的蓝图文件夹。其他 蓝图继续同级创建即可
   >
   > ​		｜-- templates
   >
   > ​		｜-- static
   >
   > ​		｜-- views.py	# 蓝图对象在这里创建
   >
   > ​	｜-- `__init.py__`	# 蓝图管理目录，所有的 蓝图 都注册到 该 init 文件
   >
   > ｜-- `__init.py__`
   >
   > ｜-- manage.py	# 启动 flask app

   ``` python
   # manage.py
   from blue_print import create_app
   
   app = create_app()
   
   if __name__ == '__main__':
       app.run(port=4998)
   ```

   ``` python
   # 蓝图管理目录的 init 文件
   from flask import Flask
   
   
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
   ```

   ``` python
   # user.views.py
   from flask import Blueprint
   
   user = Blueprint('user', __name__, static_folder='static', template_folder='templates', static_url_path='/user')
   '''
   参数说明：
       user：为Blueprint对象取一个名字。
       __name__：和Flask对象一致，传入当前蓝图所在文件名。把该目录作为 一个蓝图的 根目录。蓝图私有的静态文件、模板都相对于该目录。
       static_folder、template_folder、static_url_path 在蓝图对象中是没有默认值的，需要使用时必须显示指定。
   '''
   
   # 创建路由接口，同flask对象
   @user.route('/name')
   def name():
       return '用户名称'
   ```



## 二、框架精讲

### 1. Flask 对象创建参数

``` python
from flask import Flask

app = Flask(import_name=__name__, static_url_path='/s', static_folder='static', template_folder='templates')
'''
import_name: 指Flask对象所在的文件，通常传入__name__即可。flask把import_name文件所在的目录作为工程根目录，后续的静态文件、模版相对于该目录寻找。
static_url_path: 客户端访问工程静态资源的url路径，默认值是'/static'。例如：'/s/123.jpg'。
static_folder: 静态资源文件相对于工程根目录的存放路径，默认值是'static'。客户端访问静态资源时，flask就到该路径下去找。
template_folder: 模版文件相对于工程根目录的存放路径，默认值是'/templates'
'''
```

### 2. Flask 配置参数

> Django 中的配置参数都放在 settings.py 文件中。
>
> Flask 的配置参数，保存在 app.config 配置类中，获取配置通过 app.config[key] 的方式，添加配置有以下三种方式

 - 参数配置类配置

   ``` python
   from flask import Flask
   
   # 配置类
   class Config:
       SECRET_KEY = 'hdsjat23u8dhbaj*bcsh$'
       DEBUG = True
   
   
   app = Flask(import_name=__name__)
   
   # 引入配置类
   app.config.from_object(Config)
   
   if __name__ == '__main__':
       print(app.config['SECRET_KEY'])  # hdsjat23u8dhbaj*bcsh$
       app.run()
       
   '''
   优点：
       - 可继承
   缺点：
       - 不安全，敏感信息暴露在代码明文中
       - 不灵活
   '''
   ```

- 配置文件配置

  ```python
  import os
  
  from flask import Flask
  
  app = Flask(import_name=__name__)
  
  # 引入配置文件
  path = os.path.join(os.path.abspath(__file__).rsplit('/', 1)[0], 'settings.py')
  app.config.from_pyfile(path)
  
  if __name__ == '__main__':
      print(app.config['SECRET_KEY'])  # dgsa263528dgsajgdt21
      app.run()
  
  '''
  优点：
      - 隐藏了敏感数据
  缺点：
      - 配置文件在项目中可见，还不够安全
  '''
  '''
  settings.py
  SECRET_KEY = 'dgsa263528dgsajgdt21'
  '''
  ```

- 环境变量配置

  ``` python
  from flask import Flask
  
  app = Flask(import_name=__name__)
  
  # 引入配置环境变量配置
  app.config.from_envvar('SETTINGS')
  
  if __name__ == '__main__':
      print(app.config['SECRET_KEY'])  # dgsa263528dgsajgdt21
      app.run()
  
  '''
  优点：
      - 隐藏了敏感数据，配置文件放在服务器上
  缺点：
      - 不方便，部署时需要添加对应的环境变量
      - export SETTINGS=/Users/zhangjian/PycharmProjects/Practice/settings.py
  '''

### 3. Flask 路由

 - 查询路由

   ``` python
   from flask import Flask
   
   app = Flask(import_name=__name__)
   
   
   @app.route('/')
   def index():
       return 'home'
   
   
   @app.route('/login')
   def login():
       return 'login'
   
   
   if __name__ == '__main__':
       rules = app.url_map  # 返回一个Map对象，调用 iter_rules() 迭代时返回一个 Rule 对象。Rule 对象中就包含了路由信息
       print(rules)  # Map([<Rule '/login' (GET, OPTIONS, HEAD) -> login>,<Rule '/' (GET, OPTIONS, HEAD) -> index>,<Rule '/static/<filename>' (GET, OPTIONS, HEAD) -> static>])
   
       urls = {rule.endpoint: rule.rule for rule in rules.iter_rules()}
       print(urls)  # {'login': '/login', 'index': '/', 'static': '/static/<path:filename>'}
   ```

- 指定请求方式

  ``` python
  from flask import Flask
  
  app = Flask(import_name=__name__)
  
  
  @app.route('/')  # 不指定时 默认请求方式 为 get。同时自带 options、head 两种请求方式。head 是简化版的get，只返回头部信息，没有响应体。
  def index():
      return 'home'
  
  
  @app.route('/login', methods=['POST'])  # 指定请求方式为post，此时仍然会带有 默认的 options。
  def login():
      return 'login'
  
  
  if __name__ == '__main__':
      rules = app.url_map
      print(
          rules)  # Map([<Rule '/login' (POST, OPTIONS) -> login>,<Rule '/' (HEAD, GET, OPTIONS) -> index>,<Rule '/static/<filename>' (HEAD, GET, OPTIONS) -> static>])
  
  ```

### 4. Flask 蓝图

> flask 中的 Flask 对象 对应到 Django 中的 Project；而 蓝图 就对应 Django 中的 一个app。

``` python
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
  
# 最后注册到 flask 对象中
# 蓝图目录结构：见基础入门 第四节
```

### 5. Flask 路由传参

- Url路径传参-默认转换器

  ``` python
  from flask import Flask
  
  app = Flask(import_name=__name__)
  
  
  @app.route('/index/<id>')  # <> 是一个转换器，可以匹配url中的参数，默认匹配string类型。同时返回str
  def index(id):
      return 'home'
  
  
  @app.route('/login/<int:id>')  # 匹配 int 类型的路由参数，同时 返回 int。 例如：'/login/123' 可以匹配成功；'/login/123aa' 匹配不成功。
  def login(id):
      return 'login'
  
  '''
  默认支持的参数类型：default、string、any、path、int、float、uuid
  '''
  ```

- Url路径传参-自定义转换器

  ``` python
  from flask import Flask
  from werkzeug.routing import BaseConverter
  
  
  # 自定义一个转换器
  class MobileConverter(BaseConverter):
      regex = '1[3-9]\d{9}'
  
  
  app = Flask(import_name=__name__)
  
  # 注册转化器
  app.url_map.converters['mobile'] = MobileConverter
  
  
  @app.route('/logon/<mobile:mobile_num>')  # 根据自定义的正则进行匹配
  def login(mobile_num):
      return mobile_num
  ```

### 6、Flask request 对象

> falsk 中的request是基于上下文管理实现的，不会主动传递给接口函数，需要手动导入。
>
> Request 对象属性：
>
> - data: 记录请求中的数据，并转换成字符串
>
> - form: 记录请求中的表单数据，类型：MultiDict
> - args: 记录请求中的查询参数，类型：MultiDict
> - cookies: 记录请求中的cookie信息，类型：Dict
> - headers: 记录请求中的报文头，EnvironHeaders
> - method: 记录请求使用的http方式，GET/POST/PUT/DELETE等
> - url: 记录请求的URL地址，str
> - files: 记录请求上传的文件，二进制文件对象。

``` python
from flask import Flask, request

app = Flask(__name__)


@app.route('/index', methods=['GET', 'POST'])
def index():
    # http://127.0.0.1:4567/index?name=zhangjian
    print(request.args.get('name'))  # zhangjian
    print(request.data)  # zhangjian
    print(
        request.cookies)  # ImmutableMultiDict([('session', 'eyJ1c2VyIjoiemhhbmdqaWFuIn0.YUWi6A.yK9t7tBQnY-T_-XFlf7db2_nuSQ')])

    return 'xx'


@app.route('/home', methods=['POST'])
def home():
    print(request.form.get('name'))  # zhangjian
    print(request.url)  # http://127.0.0.1:4567/home

    return 'aaa'


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['pic']
    print(file)  # <FileStorage: '321321.jpeg' ('image/jpeg')>
    file.save('girl.jpg')  # flask 保存的文件对象提供了保存方法，不需要 在手动 创建文件保存

    return 'hello'


if __name__ == '__main__':
    app.run(port=4567)
```

### 7、Flask 构造响应信息

> flask 中接口函数可以创建响应对象，直接返回字符串即可，框架会自动封装成Response对象返回。

``` python
from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response

app = Flask(__name__)


@app.route('/index', methods=['GET', 'POST'])
def index():
    # return 'string'  # 直接返回字符串
    # return jsonify(name='zhangjian', age=18)  # {"age": 18,"name": "zhangjian"}  返回json字符串
    # return render_template('index.html', name='zhangjian', info={'age': 18})  # 返回html页面
    # return redirect('/home')  # 通过路由重定向
    return redirect(url_for('other_home'))  # 通过别名重定向


@app.route('/home', endpoint='other_name')  # endpoint 别名
def home():
    # ----------------------important------------------------
    # 直接修改响应状态码及 response header 字段。
    # 格式：return body, status_code, tuple(tuple(key, value),..)
    return '主页', 206, (('Ak', 'abs'), ('Bk', '123'))


@app.route('/goods')
def home():
    # ----------------------important------------------------
    # 通过 make_response 自定义响应
    response = make_response('勇士，你好呀！')  # 创建响应对象，传入响应体
    response.headers['token'] = '251637gdajhdgasyhdfags'  # 添加头部信息
    response.status_code = '403 Permission Denied'  # 修改状态码。此处修改不仅要协状态码，还要写上状态名称
    response.set_cookie('sos', 'help!!!')  # 设置cookie
    
    return response


if __name__ == '__main__':
    app.run(port=4567)
```

### 8、Flask Cookie和Session

> cookie: flask中设置cookie 和django中一样，调用response对象的set_cookie方法
>
> session：flask中的session跟随cookie保存到本地浏览器，服务器不做存储；Django 默认将 session 保存在数据库中

``` python
from flask import Flask, request, make_response, session

app = Flask(__name__)
app.secret_key = 'dhsud^9237bxhdsjag6232hr3ba'


@app.route('/set')
def set_sh():
    # ----------------------important------------------------
    # 通过 make_response 自定义响应
    response = make_response('勇士，你好呀！')  # 创建响应对象，传入响应体

    """Sets a cookie.

    A warning is raised if the size of the cookie header exceeds
    :attr:`max_cookie_size`, but the header will still be set.

    :param key: the key (name) of the cookie to be set.
    :param value: the value of the cookie.
    :param max_age: should be a number of seconds, or `None` (default) if
                    the cookie should last only as long as the client's
                    browser session.
    :param expires: should be a `datetime` object or UNIX timestamp.
    :param path: limits the cookie to a given path, per default it will
                 span the whole domain.
    :param domain: if you want to set a cross-domain cookie.  For example,
                   ``domain=".example.com"`` will set a cookie that is
                   readable by the domain ``www.example.com``,
                   ``foo.example.com`` etc.  Otherwise, a cookie will only
                   be readable by the domain that set it.
    :param secure: If ``True``, the cookie will only be available
        via HTTPS.
    :param httponly: Disallow JavaScript access to the cookie.
    :param samesite: Limit the scope of the cookie to only be
        attached to requests that are "same-site".
    """
    response.set_cookie('sos', 'help!!!')  # 设置cookie，原理就是在响应头中新增键值对，Set-Cookies: sos=help!!!&...
    response.set_cookie('name', 'zhangjian', max_age=3600)

    # response.delete_cookie('name')  # 原理也是设置cookie，只不过将过期时间 设置到当前时间之前，让其自动在浏览器过期。

    session['score'] = 100  # 设置session，session是加密保存在浏览器的，所以 依赖 secret_key

    return response


@app.route('/get')
def get_sh():
    cookie = request.cookies
    name = request.cookies.get('name')  # 获取客户端cookie
    print(cookie)

    score = session['score']  # 获取session中的信息。flask会自动为其解密。
    print(score)

    return 'OK'


if __name__ == '__main__':
    app.run(port=4567)
```

### 9、Flask 异常处理

- abort 抛出异常

  - 抛出一个给定的状态码的 HTTPExption 或者 指定响应，例如想要用一个页面未找到来终止请求，就可以调用 abort(404)。
  - 参数
    - code - HTTP 的错误状态码，状态码必须是协议中规定的状态码。

  ``` python
  from flask import Flask, abort, make_response
  
  app = Flask(__name__)
  
  
  @app.route('/sms/<mobile>')
  def set_sh(mobile):
      if len(mobile) != 11:
          # abort(400)  # 返回指定错误状态码
          abort(400, '手机号错误')  # 返回指定错误状态码，同时可传入一些错误描述信息，flask会将其加到错误页面一同返回给前端
          # abort(make_response('手机号错误'))  # 返回一个指定的响应
  
      return '验证码已发送'
  
  
  if __name__ == '__main__':
      app.run(port=4567)
  ```

- errorhandler 装饰器 异常处理

  - 注册一个错误处理程序，当程序抛出错误状态码的时候，就会调用该装饰器所装饰的方法。
  - 参数
    - code_or_exception  HTTP错误状态码或者指定的异常类

  ``` python
  from flask import Flask, abort, make_response
  
  app = Flask(__name__)
  
  
  @app.errorhandler(500)  # 针对 HTTP 500 异常注册一个处理函数
  def server_err(e):
      return '服务器报 500 啦'
  
  
  @app.errorhandler(ZeroDivisionError)  # 为指定异常注册一个处理函数
  def zero_division_error(e):
      # print(e)
      # return '被除数不能是 0 ！'
      response = make_response('被除数不能是 0 ！')
      response.status_code = '403 Request Bad'
      return response  # 返回处理后的响应对象
  
  
  @app.route('/sms/<mobile>')
  def set_sh(mobile):
      if len(mobile) != 11:
          abort(500)  # 抛出一个500错误
  
      return '验证码已发送'
  
  
  @app.route('/math')
  def math():
      a = 1 / 0
      return a
  
  
  if __name__ == '__main__':
      app.run(port=4567)
  ```



### 10、Flask hook

在客户端和服务器交互过程中，有些准备工作和扫尾工作需要处理，例如：

		- 请求开始时，建立数据库连接
		- 请求开始时，进行用户身份认证、权限校验
		- 请求结束时，封装指定格式的响应数据

为了避免每个视图函数重复编写相同的功能代码，Flask 提供了通用的设施功能，即请求钩子。

Flask 请求钩子通过装饰器实现，目前支持如下四种钩子。

- before_first_request
  - 在处理第一个请求前执行
- before_request
  - 在每次请求前执行
  - 如果在被装饰的函数中返回了一个响应，那么视图函数将不再被执行
- after_request
  - 如果视图函数没有抛出异常，那么在视图函数处理完成后，将会被调用
  - 接受一个参数：视图函数返回的响应
  - 在该钩子中可以对响应数据做最后一次修改
  - 返回一个参数：被修改后的响应
- teardown_request
  - 在每次请求后执行
  - 接受一个参数：错误信息，如果有相关错误抛出



**示例：**

``` python
import time

from flask import Flask

app = Flask(__name__)


@app.before_first_request
def before_first_request():
    print("首次请求调用")


# 在每一次调用视图函数之前执行，此时已经生成request请求对象。
# 在这里一般进行身份认证、权限校验等。如果校验不通过，则可以直接 return，之后便不在调用 视图函数。
@app.before_request
def before_request():
    print("每次请求前调用")


# 在视图函数执行完之后调用，对响应对象做最后的处理并返回。
@app.after_request
def after_request(response):
    print("视图函数之后执行")
    return response


# 在每次请求结束之后都会调用（在前面的return之后），接受一个参数，参数是服务器出现的错误信息
# 此时响应对象还没有发送给前端，需要等待该钩子执行完之后再发送
@app.teardown_request
def teardown_request(error):
    time.sleep(5)
    print("每次请求结束后调用")


@app.route('/sms/<mobile>')
def set_sh(mobile):
    print('验证码已发送')

    return '验证码已发送'


if __name__ == '__main__':
    app.run(port=4567)
```



### 11、Flask current_app 全局上下文对象

> current_app 就是当前运行的Flask app，在代码中不方便直接操作flask 的 app 对象时，可以操作 current_app ，就等价于操作 flask 的 app 对象。

``` python
from flask import Blueprint, current_app

user = Blueprint('user', __name__, static_folder='static', template_folder='templates', static_url_path='/goods')


# 创建路由接口，同flask对象
@user.route('/name')
def name():
    return current_app.secret_key  # 通过 current_app 获取 app 的 secret_key
```



### 12、Flask g 全局临时对象

> g 作为 flask 应用 全局的一个临时对象，充当中间媒介的作用，我们可以通过它在一次请求调用多个函数间传递一些数据。每次请求都会重置这个对象。

``` python
from flask import Flask, request, g

app = Flask(__name__)


def get_sum():
    return g.a + g.b  # 直接使用保存的参数


@app.route('/index')
def index():
    a = request.args.get('a')  # 查询参数取出来是 str 类型
    b = request.args.get('b')

    # 把参数添加到 g 对象中
    g.a = a
    g.b = b

    res = get_sum()
    return res


if __name__ == '__main__':
    app.run(port=4567)
```



### 13、 综合认证设计实现

> 身份认证：利用钩子函数在请求之前完成身份信息校验。
>
> 权限校验：利用 装饰器 实现局部视图的权限校验。

``` python
import functools

from flask import Flask, request, g

app = Flask(__name__)


@app.before_request
def check_user():
    # 在这里进行身份信息认证。
    # Cookie、Session JWT 等
    user_id = request.args.get('id')
    if user_id:
        g.user_id = user_id
    else:
        return "身份信息未提供"  # 钩子函数返回后，将不再调用视图函数


def auth(func):  # 认证装饰器
    @functools.wraps(func)
    def inner(*args, **kwargs):
      if int(g.user_id) == 10:
        res = func(*args, **kwargs)
        return res
      return "sorry， you no permission to operation"

    return inner


@app.route('/index')
def index():
    return "首页"


@app.route('/user/manage')
@auth  # 通过装饰器对局部视图进行权限校验
def user_manage():
        return "欢迎来到用户管理中心"


if __name__ == '__main__':
    app.run(port=4567)
```



## 三、Flask 全局上下文  源码分析

**上下文**：即语境、语意。在程序中可以理解为在代码执行到某一时刻，根据之前代码所做的操作，可以决定在接下来即将执行的操作中，我们可以使用到那些对象、变量、属性等，或者理解为我们可以完成哪些事。

**Flask 上下文对象：**分为两种。请求上下文和应用上下文。

- 请求上下文(request context)

  > 请求上下文本质上针对每一个请求独立创建的一个request对象，多个request之间数据相互隔离，当request处理完成之后，该 request 便被回收释放，结束其生命周期。

  - request
    - 封装了HTTP请求的内容，包括cookie、form、args等属性。详见：框架精讲 > 6、Flask request 对象
  - session
    - 用来记录请求会话中的信息。详见：框架精讲 > 6、Flask Cookie和Session

- 应用上下文(application context)

  > 应用上下文不是一直存在的，他只是 request context 中的一个对app 代理，local proxy。它的主要作用就是帮助 request 获取到当前的应用，它伴 request 而生，随 request 而亡。所以不同的 request 中 使用的 应用上下文 并不是同一个。

  - current_app
    - 应用上下文用于存储应用程序中的变量、工具类、数据库连接对象等。可以通过 current_app.name 打印当前 app 的名称。同时也可以读取 current_app 中保存的变量。
  - g
    - g 作为 flask 应用 全局的一个临时对象，充当中间媒介的作用，我们可以通过它在一次请求调用多个函数间传递一些数据。每次请求都会重置这个对象。



**request 上下文 实现源码分析：**

- flask.globals.py 部分代码

  ``` python
  def _lookup_req_object(name):
      top = _request_ctx_stack.top
      if top is None:
          raise RuntimeError('working outside of request context')
      return getattr(top, name)
   
  _request_ctx_stack = LocalStack()
  request = LocalProxy(partial(_lookup_req_object, 'request'))
  session = LocalProxy(partial(_lookup_req_object, 'session'))
  ```

  可以看到不管request还是session最后都是通过getattr(top, name)获取的，也就是说肯定有一个上下文对象同时保持request和session。我们只要一处导入request，在任何视图函数中都可以使用request，关键是每次的都是不同的request对象，说明获取request对象肯定是一个动态的操作，不然肯定都是相同的request。

  这里的魔法就是_lookup_req_object函数和LocalProxy组合完成的。

- LocalProxy是werkzeug.local.py中定义的一个代理对象，它的作用就是将所有的请求都发给内部的_local对象

  ``` python
  class LocalProxy(object):
    	
      # 使用__slots__指定类的属性，而不会创建__dict__数据结构，以此来节约memery
      __slots__ = ("__local", "__name", "__wrapped__")
      
      def __init__(self, local, name=None):
          #LocalProxy的代码被我给简化了，这里的local不一定就是local.py中定义的线程局部对象，也可以是任何可调用对象
          #在我们的request中传递的就是_lookup_req_object函数
          object.__setattr__(self, "_LocalProxy__local", local)
          object.__setattr__(self, "_LocalProxy__name", name)
   
      def _get_current_object(self):
          #很明显，_lookup_req_object函数没有__release_local__
          if not hasattr(self.__local, '__release_local__'):
              return self.__local()
          try:
              return getattr(self.__local, self.__name__)
          except AttributeError:
              raise RuntimeError('no object bound to %s' % self.__name__)
      
      # 这里仅仅是代码实现逻辑，源码中__getattr__是调用了另一个对象，获取__call__的返回值。
      def __getattr__(self, name):
          return getattr(self._get_current_object(), name)
  ```

  对request的任何调用都是对_lookup_req_object返回对象的调用。
  既然每次request都不同，要么调用top = _request_ctx_stack.top返回的top不同，要么top.request属性不同，在flask中每次返回的top是不一样的，所以request的各个属性都是变化的。

- _request_ctx_stack

  ``` python
  class LocalStack:
        def __init__(self) -> None:
          self._local = Local()
          
        def push(self, obj: t.Any) -> t.List[t.Any]:
          """Pushes a new item to the stack"""
          rv = getattr(self._local, "stack", []).copy()
          rv.append(obj)
          self._local.stack = rv
          return rv  # type: ignore
  
        def pop(self) -> t.Any:
            """Removes the topmost item from the stack, will return the
            old value or `None` if the stack was already empty.
            """
            stack = getattr(self._local, "stack", None)
            if stack is None:
                return None
            elif len(stack) == 1:
                release_local(self._local)
                return stack[-1]
            else:
                return stack.pop()
  
        @property
        def top(self) -> t.Any:
            """The topmost item on the stack.  If the stack is empty,
            `None` is returned.
            """
            try:
                return self._local.stack[-1]
            except (AttributeError, IndexError):
                return None
  ```

  ``` python
  class Local(object):  # 此处仅是Local的实现原理
      __slots__ = ('__storage__', '__ident_func__')
   
      def __init__(self):
          object.__setattr__(self, '__storage__', {})
          object.__setattr__(self, '__ident_func__', get_ident)
      def __getattr__(self, name):
          return self.__storage__[self.__ident_func__()][name]
      def __setattr__(self, name, value):
        	thread_dict = self.__storage__.setdefault(self.__ident_func__(), {})
          thread_dict[name] = value
  ```

  _request_ctx_stack = LocalStack()，LocalStack其实就是简单的模拟了堆栈的基本操作，push,top,pop，内部保存的线程本地变量是在多线程中request不混乱的关键。

  查看Local的代码，`__storage__`在内部是一个字典对象，以 thread.get_ident 作为每个线程数据信息的键，来保存和取出数据。

  -------  至此，我们可以明确一点，每个请求都是隔离保存或者取出来的。

- _request_ctx_stack堆栈是在哪里push的

  - 从app.run()开始

    ``` python
    class Flask(_PackageBoundObject):
        def run(self, host=None, port=None, debug=None, **options):
            from werkzeug.serving import run_simple
            run_simple(host, port, self, **options)
    ```

    使用的是werkzeug的run_simple，根据wsgi规范，app是一个接口，并接受两个参数,即，application(environ, start_response)

  - werkzeug.servering 的 run_wsgi我们可以清晰的看到调用过程

    ``` python
        def run_wsgi(self):
            environ = self.make_environ()
        
            def start_response(status, response_headers, exc_info=None):
                if exc_info:
                    try:
                        if headers_sent:
                            reraise(*exc_info)
                    finally:
                        exc_info = None
                elif headers_set:
                    raise AssertionError('Headers already set')
                headers_set[:] = [status, response_headers]
                return write
     
            def execute(app):
                application_iter = app(environ, start_response)
                #environ是为了给request传递请求的
                #start_response主要是增加响应头和状态码，最后需要werkzeug发送请求
                try:
                    for data in application_iter: #根据wsgi规范，app返回的是一个序列
                        write(data) #发送结果
                    if not headers_sent:
                        write(b'')
                finally:
                    if hasattr(application_iter, 'close'):
                        application_iter.close()
                    application_iter = None
     
            try:
                execute(self.server.app)
            except (socket.error, socket.timeout) as e:
                pass
    ```

  - flask中通过定义`__call__`方法适配wsgi规范

    ``` python
    class Flask(_PackageBoundObject):
        def __call__(self, environ, start_response):
            """Shortcut for :attr:`wsgi_app`."""
            return self.wsgi_app(environ, start_response)
     
        def wsgi_app(self, environ, start_response):
            ctx = self.request_context(environ)
            #这个ctx就是我们所说的同时有request,session属性的上下文
            ctx.push()
            error = None
            try:
                try:
                    response = self.full_dispatch_request()
                except Exception as e:
                    error = e
                    response = self.make_response(self.handle_exception(e))
                return response(environ, start_response)
            finally:
                if self.should_ignore_error(error):
                    error = None
                ctx.auto_pop(error)
     
        def request_context(self, environ):  # 当请求进来时，会调用该方法
            return RequestContext(self, environ)
    ```

  - RequestContext是保持一个请求的上下文的类，之前我们`_request_ctx_stack`一直是空的，当一个请求来的时候调用ctx.push()将向_request_ctx_stack中push ctx。

    ``` python
    class RequestContext(object):
        def __init__(self, app, environ, request=None):
            self.app = app
            if request is None:
                request = app.request_class(environ) #根据环境变量创建request
            self.request = request
            self.session = None
     
        def push(self):
            _request_ctx_stack.push(self) #将ctx push进 _request_ctx_stack
            # Open the session at the moment that the request context is
            # available. This allows a custom open_session method to use the
            # request context (e.g. code that access database information
            # stored on `g` instead of the appcontext).
            self.session = self.app.open_session(self.request)
            if self.session is None:
                self.session = self.app.make_null_session()
     
        def pop(self, exc=None):
            rv = _request_ctx_stack.pop()
         
        def auto_pop(self, exc):
            if self.request.environ.get('flask._preserve_context') or \
               (exc is not None and self.app.preserve_context_on_exception):
                self.preserved = True
                self._preserved_exc = exc
            else:
                self.pop(exc)
    ```

    ctx.push操作将ctx push到`_request_ctx_stack`，所以当我们调用request时将调用_lookup_req_object。 top此时就是ctx上下文对象，而getattr(top, "request")将返回ctx的 request 对象，而这个request就是在 RequestContext 的`__init__`中根据环境变量创建的。

    

## 四、拓展实践

### 请求表单

flask框架下表单，推荐使用 flask-wtf。

安装模块：

```shell
pip install flask-wtf
```

实践案例：

```python
class MetaForm(Form):
    """
    元表单
    增强默认表单能力
    """
    def __init__(self):
        data = request.get_json()
        args = request.args.to_dict()
        super(MetaForm, self).__init__(data=data, **args)
        self.request_data = dict(**data, **args)

    @property
    def valid_data(self) -> dict:
        """
        过滤表单中的None值
        返回非控制的字段的一个dict
        """
        data = {}
        for key, val in self.data.items():
            if val is not None:
                data[key] = val
        return data

    def validate(self, extra_validators=None):
        """
        重写父类校验方法
        增加对请求中多余字段的校验，不允许有不相关字段
        """
        other = []
        for key in self.request_data.keys():
            if key not in self._fields:
                other.append(key)
        if other:
            self.form_errors.append(f"Illegal fields: {' '.join(other)}")
            return False
        return super().validate(extra_validators)

def validate_data(cls):
    """
    实现一个装饰器，作用在视图函数上
    统一校验数据的合法性
    cls：MetaForm的子类，实际的请求表单
	"""
    def outer(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            form = cls()
            if not form.validate():
                response = make_response({"code": -1, "msg": form.errors})
                response.status_code = 400
                return response
            kwargs["form"] = form
            return func(*args, **kwargs)
        return inner
    return outer
```

创建表单：

```python
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired

class DemoForm(MetaForm):
    id = IntegerField(validators=[DataRequired()])
```



### ORM框架

flask开发框架下，推荐使用sqlalchemy库。

安装模块：

```python
 pip install -i https://pypi.tuna.tsinghua.edu.cn/simple sqlalchemy
```

sqlalchemy是一个开源的ORM框架，不再过多赘诉，下面给一些实践代码。

**工具封装**

```python
class ORMTool:
    base = declarative_base()
    table_extend_args = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}
    engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?"charset=utf8mb4", echo=False, pool_size=20, max_overflow=10, pool_timeout=30, pool_recycle=360, pool_pre_ping=True)

		# 创建数据库
    if not database_exists(engine.url):
        create_database(engine.url)

    # 会话maker
    sm = sessionmaker(bind=engine, expire_on_commit=False)

    @classmethod
    def flush_table(cls):
        cls.base.metadata.create_all(cls.engine)
		
    # 配合 dataclass 可以将对象序列化为json
    @staticmethod
    def to_dict(row: base):
        data = asdict(row)
        for key, val in data.items():
            if isinstance(val, datetime):
                data[key] = val.strftime("%Y-%m-%d %H:%M:%S")
        return data

    class SessionContext:
        def __init__(self, commit=True):
            self.commit = commit

        def __enter__(self):
            self.session = scoped_session(ModelTool.sm)
            return self.session

        def __exit__(self, exc_type, exc_val, exc_tb: traceback):
            try:
              if any([exc_type, exc_val, exc_tb]):
                  self.session.rollback()
                  raise exc_type(exc_val)
              if self.commit:
                  self.session.commit()
            except Exception as e:
              raise e
            finally:
              self.s.close()
```



**定义模型**

```python
from dataclasses import dataclass
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, func

@dataclass
class Demo(ModelTool.base):
    __tablename__ = "demo"
    __table_args__ = {"comment": "示例数据表"}

    id: int = Column(Integer, primary_key=True, autoincrement=True, comment="主键id 也是task_id")
    name: str = Column(String(32), nullable=False, unique=True, comment="名称")
    type: str = Column(Enum('0', '1', '2'), default='0')
    sub_id: int = Column(Integer, ForeignKey("sub.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=True)
    create_time: str = Column(DateTime, default=func.now(), comment="创建时间")
    update_time: str = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    sub = relationship("Sub", backref="task")
```



### 定时任务

flask开发框架下，推荐使用apscheduler库来实现定时任务的管理。
安装模块：
```shell
 pip install -i https://pypi.tuna.tsinghua.edu.cn/simple apscheduler
```

#### 基础模块

##### 调度器

Apscheduler提供的调度器有7种：

- BlockingScheduler : 调度器在当前进程的主线程中运行，会阻塞当前线程。
- BackgroundScheduler : 调度器在后台线程中运行，不会阻塞当前线程。
- AsyncIOScheduler : 结合 asyncio 模块（一个异步框架）一起使用。
- GeventScheduler : 程序中使用 gevent（高性能的Python并发框架）作为IO模型，和 GeventExecutor 配合使用。
- TornadoScheduler : 程序中使用 Tornado（一个web框架）的IO模型，用 ioloop.add_timeout 完成定时唤醒。
- TwistedScheduler : 配合 TwistedExecutor，用 reactor.callLater 完成定时唤醒。
- QtScheduler : Qt 应用，需使用QTimer完成定时唤醒。

##### 执行器

用于设置线程池、进程池、协程池等，Apscheduler提供的执行器有6种：

- ThreadPoolExecutor： 线程池执行器。
- ProcessPoolExecutor： 进程池执行器。
- GeventExecutor： Gevent程序执行器。
- TornadoExecutor： Tornado程序执行器。
-  TwistedExecutor： Twisted程序执行器。
- AsyncIOExecutor： asyncio程序执行器。

##### 任务存储器

任务默认是存储在内存里的，服务重启后，内存里的任务会丢失。将任务保存在数据库中，每次启动会读取数据库的信息，可以避免服务重启丢失信息的问题。

```python
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

# 数据持久化至Mysql，默认table名为apscheduler_jobs
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
jobstores = {'default': SQLAlchemyJobStore(url="mysql+pymysql://root:123456@127.0.0.1:3306/work")}

# 数据持久化至MongoDB
from apscheduler.jobstores.mongodb import MongoDBJobStore
jobstores = {'default': MongoDBJobStore(host="127.0.0.1",port=27017, database="TEST", collection="jobs")}

# 数据持久化至redis
from apscheduler.jobstores.redis import RedisJobStore
jobstores = {'default': RedisJobStore(host="127.0.0.1",port=6379, db=0)}

# 引入配置的方法，在创建类时加入配置项
scheduler = BackgroundScheduler(jobstores=jobstores)
def job1(a, b):  # 运行的定时任务的函数
    print(str(a) + ' ' + str(b))
```

##### 触发器

当你开始定时任务时，需要为定时策略选择一个触发器（设置  class Config 中 trigger 的值）。apscheduler 提供了三种类型的触发器。

- date:  一次性指定固定时间，只执行一次
- interval   间隔调度，隔多长时间执行一次
- cron  指定相对时间执行，比如：每月1号、每星期一执行

其他配置：
```python
defaults = {
    # 不合并执行
    'coalesce': False,
    # 同一时间同个任务最大执行次数为3
    'max_instances': 3,
    # 任务错过当前时间60s内，仍然可以触发任务
    'misfire_grace_time':60
}

# 创建类，导入配置
scheduler = BackgroundScheduler(job_defaults=defaults)
```

#### 使用方式

apscheduler有三种使用方式。

##### Config配置类

```python
# 步骤一： Config定义数据
class Config:
    JOBS = [
        {
            'id': '0001',
            'func': 'app.job.cron_job:job', # 如果需要应用其他文件的函数可以使用这种方法
            'args': (1, 2),  # 这个是函数对应的入参，如果函数没有参数则无需增加args参数
            'trigger': 'interval',
            'seconds': 2
        },
        {
            'id': '0002',
            'func': 'app.job.cron_job:job_cron',
            'trigger': 'cron',
            # 'day': 21,
            # "hour": 11,
            # "minute": 44,
            "second": 10
        }
    ]
    SCHEDULER_API_ENABLE = True
    SCHEDULER_TIMEZONE = "Asia/Shanghai"

# 步骤二： python文件app/job/cron_job.py 定义方法
def job(a, b):
    """定时任务执行函数"""
    print(a + b, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
def job_cron():
    print("====================")
```

##### 使用装饰器

```python
# 步骤一: 实例化APScheduler（一般放在app/__init__.py中）
scheduler = APScheduler()
# 步骤二： 修饰定时任务
@scheduler.task('interval', id='job_1', args=(1,2),seconds=5)
def job1(a, b):  # 运行的定时任务的函数
    print(str(a) + ' ' + str(b))
# 步骤三： 运行主类中启动框架
if __name__ == '__main__':
    app = Flask(__name__)  # 实例化flask
    scheduler.start()  # 启动任务列表
    app.debug=True
    app.run(host='0.0.0.0',port= 8000)  # 启动 flask
```

##### 使用API

```python
# 步骤一： 定义后台线程中运行的调度器
from apscheduler.schedulers.background import BackgroundScheduler
# 调度器在后台线程中运行，不会阻塞当前线程
# timezone 配置时区
scheduler = BackgroundScheduler(timezone="Asia/Shanghai")

# 步骤二： 定义定时任务函数
def job1(a, b):
    print(str(a) + ' ' + str(b))
    
# 步骤三： 使用API纳管
scheduler.scheduled_job(func=job1, args=("1","2"),id="job_1", trigger="interval", seconds=5, replace_existing=False)
'''
func：定时任务执行的函数名称。
args：任务执行函数的位置参数，若无参数可不填
id：任务id，唯一标识，修改，删除均以任务id作为标识
trigger：触发器类型，参数可选：date、interval、cron
replace_existing：将任务持久化至数据库中时，此参数必须添加，值为True。并且id值必须有。不然当程序重新启动时，任务会被重复添加。
'''

# 步骤四： 启动定时框架
if __name__ == '__main__':
    app = Flask(__name__)
    scheduler.start()
    app.debug=True
    app.run(host='0.0.0.0',port= 8000)

# 实例对象 scheduler 拥有增、删、改、查等基本用法：
新增任务：add_job()
编辑任务：modify_job()
删除任务：remove_job(id)（删除所有任务：remove_all_jobs()）
查询任务：get_job(id)（查询所有任务：get_jobs()）
暂停任务：pause_job(id)
恢复任务：resume_job(id)
运行任务：run_job(id)（立即运行，无视任务设置的时间规则）
```

