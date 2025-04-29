import my_grpc

from packages.greet_pb2 import helloRequest
from packages.greet_pb2_grpc import GreetServiceStub


def run():
    # 使用上下文管理，自动关闭链接
    with my_grpc.insecure_channel('localhost:50000') as channel:
        # 客户端通过 stub 来实现 rpc 通信
        stub = GreetServiceStub(channel)
        # 调用服务端接口
        res = stub.sayHello(helloRequest(name='zhangjian'))

    print('server message:', res.msg)


if __name__ == '__main__':
    run()
