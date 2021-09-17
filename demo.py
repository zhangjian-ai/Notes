import sys
import weakref


class A:
    def __init__(self, name):
        self.name = name


# 创建 值是弱引用 的字典
weak_dict = weakref.WeakValueDictionary()
key = 'test1'
value = A("zhangjian")  # value 强引用到实例对象上面

weak_dict[key] = value  # 弱引用字典的赋值取值等操作和dict类一致。其本身就是dict的子类

print(weak_dict[key])  # <__main__.A object at 0x100a3c550>

# 删除对象的唯一引用，那么字典里的键值对就被回收了
del value
# print(weak_dict[key])  # KeyError: 'test1'
print(weak_dict.get(key, "default"))  # default
