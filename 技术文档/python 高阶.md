### 1、详解`__new__`、`__init__`、`__call__`及对象创建过程

`__new__`： 对象的创建，是一个静态方法，第一个参数是cls，返回一个实例好的空对象。
`__init__`： 对象的初始化， 是一个实例方法，第一个参数是self，为对象加载初始值。
`__call__`： 对象可call，注意不是类，一定是对象。

类：理解为是元类(type)的实例对象，所以当运行	类()  时，元类中的`__call__`函数将会被调用。

type中`__call__`函数的实现逻辑：

```python
    def __call__(self, *args, **kwargs):
        obj = self.__new__(self, *args, **kwargs)
        # 返回对象是类的实例才执行__init__
        if isinstance(obj, self):
            # self.__init__(obj, *args, **kwargs)
            obj.__init__(*args, **kwargs)
        return obj
```



有了上面的理解，那么实例化对象的逻辑就出来：

	- instance = class()
	- class 作为元类的实例对象，运行class()时，即调用元类type中的`__call__`方法，依次调用class中`__new__`和`__init__`方法，最终返回一个当前class类的实例对象。



### 2、 Python生成器send的应用场景

``` python
# 生成器是一种使用普通函数语法定义(包含yield关键字即可)的迭代器，迭代器的有点是可以按需获取序列值，而不需要构建出一整个列表
# send是实现外部访问生成器内部的方法。send()的两个功能：1.传值，接受一个参数(传递给生成器的消息，可以是对象)；2.next()。
# 应用场景：1、实现一个交互式的计算器(没啥用) 2、实现协程

# yield本身就是一种在单线程下可以保存任务运行状态的方法
#   - 1、yiled可以保存状态，yield的状态保存与操作系统的保存线程状态很像，但是yield是代码级别控制的，更轻量级
#   - 2、send可以把一个函数的结果传给另外一个函数，以此实现单线程内程序之间的切换
import time

def decorator(func):
    """实现一个装饰器来开启协程"""

    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        res.__next__()
        # 而这完全等价
        # next(res)
        return res

    return wrapper

@decorator
def consumer(n):
    """
    生成器首次迭代不能直接使用send(value)
    必须使用next()或者send(None)
    这里借助装饰器完成第一次调用以开启协程模式
    """
    info = ''
    while True:
        time.sleep(n)
        msg = yield info
        print(f"current consuming msg : {msg}")
        info = f"第 {msg} 次等待中 ..."

def producer(c1, c2):
    """
    producer和consumer函数在一个线程内执行，通过调用send方法和yield互相切换，实现协程的功能。
    """
    n = 1
    while n < 5:
        print(f"current producing msg : {n}")
        print(c1.send(n))
        print(c2.send(n))
        n += 1

if __name__ == '__main__':
    c1 = consumer(2)
    c2 = consumer(3)

    producer(c1, c2)
```

### 3、Python动态创建类

``` python
# -------------动态导入模块中的类------------
'''
1. 首先import相关模块`import importlib`

2. 加载你想要加载的模块`model = importlib.import_module(模块名称)`

3. 获取类对象`api_class = getattr(model, 类名)`

4. 创建类对象的实例`api_instance = api_class()`

5. 调用类对象的函数`api_instance.get_response(data)`
'''

# -------------type()函数动态创建类------------
# type()函数语法说明
# 第一种语法格式用来查看某个变量（类对象）的具体类型，obj 表示某个变量或者类对象。
# 第二种语法格式用来创建类:
#   - name 表示类的名称，必传字段；
#   - bases 表示一个元组，其中存储的是该类的父类，可以是一个空元组，表示创建一个无继承的类；
#   - dict 表示一个字典，用于表示类内定义的属性或者方法，可以是一个空字典，表示创建一个无属性(方法)的类；
# python中类创建的本质：
#   - 我们使用class创建类，当你使用class关键字时，Python解释器自动创建这个对象。
#   - 而底层其实使用的是type函数(type函数也可以查看实例所属类型)来创建类的。所以我们可以直接使用type()函数来手动实现动态创建类。
type(obj) 
type(name, bases, dict)

# type查看对象类型不再赘述，这里看一个动态创建类的例子
# 示例一：
    #定义一个实例方法
    def say(self):
        print("我要学 Python！")
        
    #定义一个类方法
    @classmethod
    def wudi(cls):
        print("i love you")
        
    #使用 type() 函数创建类
    #注意，Python 元组语法规定，当 (object,) 元组中只有一个元素时，最后的逗号（,）不能省略。
    CLanguage = type("CLanguage",(object,),dict(say = say, name = "C语言中文网", wudi = wudi))
    
    #创建一个 CLanguage 实例对象
    clangs = CLanguage()
    
    #调用 say() 方法和 name 属性
    clangs.say()
    print(clangs.name)
    
# 总结：
#   - 通过type添加的属性是类属性，并不是实例属性
#   - 通过type可以给类添加普通方法，静态方法，类方法，效果跟class一样
#   - type创建类的效果，包括继承等的使用性质和class创建的类一样。本质class创建类的本质就是用type创建。

# 理解元类：
#   - 元类就是类的类，python中函数type实际上是一个元类。
#   - type就是Python在背后用来创建所有类的元类。Python中所有的东西都是对象。这包括整数、字符串、函数以及类。
#   - 所有对象，都是从一个类创建而来，这个类就是type。type就是Python的内建元类，当然了，也可以创建自己的元类(基于metaclass实现单例)

```

### 4、Python类属性和实例属性的区别

``` python
'''
理解类属性:
    - 类属性就相当与全局变量，实例对象共有的属性，实例对象的属性为实例对象自己私有。
    - 类属性就是类对象（Tool）所拥有的属性，它被所有类对象的实例对象(实例方法)所共有，在内存中只存在一个副本，这个和C++中类的静态成员变量有点类似。
    - 对于公有的类属性，在类外可以通过类对象和实例对象访问。
    
调用类属性:
    - 果需要在类外修改类属性，必须通过类对象去引用然后进行修改。
    - 如果通过实例对象去引用，会产生一个同名的实例属性，这种方式修改的是实例属性，不会影响到类属性，
      并且之后如果通过实例对象去引用该名称的属性，实例属性会强制屏蔽掉类属性，即引用的是实例属性，除非删除了该实例属性。
'''
```

### 5、Python动态创建函数

``` python
# lambda 动态创建匿名函数
```

### 6、socket如何解决粘包问题（待解决）

**A、为什么会发生TCP粘包、拆包**

1. 应用程序写入的数据大于套接字缓冲区大小，这将会发生拆包。

2. 应用程序写入数据小于套接字缓冲区大小，网卡将应用多次写入的数据发送到网络上，这将会发生粘包。

3. 进行MSS（最大报文长度）大小的TCP分段，当TCP报文长度-TCP头部长度>MSS的时候将发生拆包。

4. 接收方法不及时读取套接字缓冲区数据，这将发生粘包。

**B、如何处理粘包、拆包**

1. 使用带消息头的协议、消息头存储消息开始标识及消息长度信息，服务端获取消息头的时候解析出消息长度，然后向后读取该长度的内容。

2. 设置定长消息，服务端每次读取既定长度的内容作为一条完整消息，当消息不够长时，空位补上固定字符。

3. 设置消息边界，服务端从网络流中按消息编辑分离出消息内容，一般使用‘\n’。



### 7、socket断点续传如何实现（待解决）



### 8、导包方式总结及.pyc文件介绍

```
sys.path 系统导包路径列表说明：
	- import/from 模块名  中的模块必须是在sys.path列表中的路径下才可以被导入。
	- sys.path 列表中的第一个路径，总是当前执行文件的父级路径。所以我们执行文件时，总是可以基于当前路径导入同级模块或同级以下的模块。
```

　　**方式一：from 包名  import  模块名**

　          使用时：模块名.函数名()

　　**方式二：from 包名.模块名  import 函数名**

　　        使用时：函数名()

　　**方式三 ：import  包名.模块名   ** 

　　        使用时:  包名.模块名.函数名()

　　**方式四：from  包名  import  *   **

　　        前提是：将 `__init__.py`  文件中写入`__all__`列表变量，写入当前路径下级模块名

​                   导入哪个模块，不写则什么都不导入

　　        使用时：模块名.函数名()

　　**方式五：import 包名**   

　　        前提是：在包里面的`__init__.py`  文件里写入   from . import  模块名`__init__.py`  里面导入哪个模块

​                   通过本方式就能使用哪个模块

　　        使用时：模块名.函数名()

**.pyc文件的介绍：**

> ​		导入时会产生一个.pyc的字节码文件，此文件是当第一次导入时python解释器会将被导入的模块预解释成字节码的文件，下次再导入时python解释器则不会做预解释而是直接拿.pyc文件使用，这样就不会每次导入时做解释的操作，节省时间，当修改模块文件的内容时，python解释器会根据.pyc文件和模块的修改时间判断有没有对模块做修改，如果模块的修改时间比.pyc文件的晚说明模块已经被修改  Python解释器会将模块重新解释成.pyc文件。

