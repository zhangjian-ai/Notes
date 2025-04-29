import time
from concurrent import futures

import my_grpc

from packages.greet_pb2 import helloResponse
from packages.greet_pb2_grpc import add_GreetServiceServicer_to_server, GreetServiceServicer


class Hello(GreetServiceServicer):
    # 实现接口
    def sayHello(self, request, context):
        print(f'{request.name} is coming')
        return helloResponse(msg='hello, %s' % request.name)


def serve():
    # 这里通过thread pool来并发处理server的任务
    server = my_grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 将对应的任务处理函数添加到rpc server中
    add_GreetServiceServicer_to_server(Hello(), server)

    # 这里使用的非安全接口，gRPC支持TLS/SSL安全连接，以及各种鉴权机制
    server.add_insecure_port('[::]:50000')
    server.start()

    try:
        while True:
            time.sleep(60 * 60)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    serve()
