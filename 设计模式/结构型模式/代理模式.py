'''
代理模式：为其他对象提供一种代理，以控制对这个对象的访问。
角色：
    - 抽象实体(subject)
    - 实体(RealSubject)
    - 代理(Proxy)
场景：
    - 远程代理：可以隐藏对象位于远程空间的事实
    - 虚代理：优化对象的访问，例如 根据需要加载资源
    - 保护代理：允许在访问对象时有一些附加的内务处理，例如权限控制
'''

from abc import abstractmethod, ABCMeta


class Subject(metaclass=ABCMeta):
    @abstractmethod
    def get_content(self):
        pass

    @abstractmethod
    def set_content(self, content):
        pass


# 实体
class RealSubject(Subject):
    def __init__(self, filename):
        self.filename = filename
        f = open(self.filename, 'r', encoding='utf-8')
        self.content = f.read()
        f.close()

    def get_content(self):
        return self.content

    def set_content(self, content):
        f = open(self.filename, 'w', encoding='utf-8')
        f.write(content)
        f.close()


# 虚代理
class VirtualProxy(Subject):
    def __init__(self, filename):
        self.filename = filename
        self.obj = None

    def get_content(self):
        if not self.obj:
            self.obj = RealSubject(self.filename)
        return self.obj.get_content()

    def set_content(self, content):
        if not self.obj:
            self.obj = RealSubject(self.filename)
        self.obj.set_content(content)


# 保护代理
class ProtectProxy(Subject):
    def __init__(self, filename, user):
        self.filename = filename
        self.user = user
        self.obj = None

    def get_content(self):
        if not self.obj:
            self.obj = RealSubject(self.filename)
        return self.obj.get_content()

    def set_content(self, content):
        if self.user == 'admin':
            if not self.obj:
                self.obj = RealSubject(self.filename)
            self.obj.set_content(content)
        else:
            raise PermissionError('Permission Denied')


# client
pp = ProtectProxy('test.txt', 'dev')
print(pp.get_content())
pp.set_content('欢迎来到地下城！')
