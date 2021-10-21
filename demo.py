import hashlib

username = 'zhangjian'
password = b"\xa1\xcf\x0c\xf8'V\xf6\xcf\x05-\xf26\xbf\xcf\xa2\xfe"

# 把用户名字节码当作盐加到对象中，加强密码的安全性
# 返回一个新的类
md5 = hashlib.md5(username.encode('utf-8'))
# 添加要加密的字节码
md5.update(password)
# 获得密文
content = md5.digest()

print(content)
