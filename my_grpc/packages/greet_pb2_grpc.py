# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import my_grpc

import my_grpc.packages.greet_pb2 as greet__pb2


class GreetServiceStub(object):
    """定义服务
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.sayHello = channel.unary_unary(
                '/packages.GreetService/sayHello',
                request_serializer=greet__pb2.helloRequest.SerializeToString,
                response_deserializer=greet__pb2.helloResponse.FromString,
                )


class GreetServiceServicer(object):
    """定义服务
    """

    def sayHello(self, request, context):
        """定义借口和数据类型
        """
        context.set_code(my_grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GreetServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'sayHello': my_grpc.unary_unary_rpc_method_handler(
                    servicer.sayHello,
                    request_deserializer=greet__pb2.helloRequest.FromString,
                    response_serializer=greet__pb2.helloResponse.SerializeToString,
            ),
    }
    generic_handler = my_grpc.method_handlers_generic_handler(
            'packages.GreetService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GreetService(object):
    """定义服务
    """

    @staticmethod
    def sayHello(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return my_grpc.experimental.unary_unary(request, target, '/packages.GreetService/sayHello',
                                                greet__pb2.helloRequest.SerializeToString,
                                                greet__pb2.helloResponse.FromString,
                                                options, channel_credentials,
                                                insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
