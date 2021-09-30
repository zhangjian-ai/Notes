### socket 模块

- 创建套接字

  ``` python
  import socket
  
  # 创建socket对象
  server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # 此处为默认值
  
  # 源码
  class socket(_socket.socket):
  
      """A subclass of _socket.socket adding the makefile() method."""
  
      __slots__ = ["__weakref__", "_io_refs", "_closed"]
  
      def __init__(self, family=-1, type=-1, proto=-1, fileno=None):
          # For user code address family and type values are IntEnum members, but
          # for the underlying _socket.socket they're just integers. The
          # constructor of _socket.socket converts the given argument to an
          # integer automatically.
          if fileno is None:
              if family == -1:
                  family = AF_INET
              if type == -1:
                  type = SOCK_STREAM
              if proto == -1:
                  proto = 0
          _socket.socket.__init__(self, family, type, proto, fileno)
          self._io_refs = 0
          self._closed = False
  ```

- 参数说明

  - family：协议簇。
    - AF_UNIX（本机通信）
    - AF_INET（TCP/IP – IPv4）
    - AF_INET6（TCP/IP – IPv6）
  - type：套接字类型。
    - SOCK_STREAM（TCP流）
    - SOCK_DGRAM（UDP数据报）
    - SOCK_RAW（原始套接字）
  - proto： **“proto”一般设置为“0”**，也就是当确定套接字使用的协议簇和类型时，这个参数的值就为0，但是有时候创建原始套接字时，并不知道要使用的协议簇和类型，也就是domain参数未知情况下，这时protocol这个参数就起作用了，它可以确定协议的种类。

