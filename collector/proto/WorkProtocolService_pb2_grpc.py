# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto import WorkProtocolService_pb2 as proto_dot_WorkProtocolService__pb2


class WorkProtocolServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.greeting = channel.unary_unary(
                '/com.kkennib.grpc.WorkProtocolService/greeting',
                request_serializer=proto_dot_WorkProtocolService__pb2.Work.SerializeToString,
                response_deserializer=proto_dot_WorkProtocolService__pb2.WorkResponse.FromString,
                )
        self.collect = channel.unary_unary(
                '/com.kkennib.grpc.WorkProtocolService/collect',
                request_serializer=proto_dot_WorkProtocolService__pb2.Work.SerializeToString,
                response_deserializer=proto_dot_WorkProtocolService__pb2.WorkResponse.FromString,
                )
        self.aggregate = channel.unary_unary(
                '/com.kkennib.grpc.WorkProtocolService/aggregate',
                request_serializer=proto_dot_WorkProtocolService__pb2.Work.SerializeToString,
                response_deserializer=proto_dot_WorkProtocolService__pb2.WorkResponse.FromString,
                )
        self.report = channel.unary_unary(
                '/com.kkennib.grpc.WorkProtocolService/report',
                request_serializer=proto_dot_WorkProtocolService__pb2.Work.SerializeToString,
                response_deserializer=proto_dot_WorkProtocolService__pb2.WorkResponse.FromString,
                )
        self.reduce = channel.unary_unary(
                '/com.kkennib.grpc.WorkProtocolService/reduce',
                request_serializer=proto_dot_WorkProtocolService__pb2.Work.SerializeToString,
                response_deserializer=proto_dot_WorkProtocolService__pb2.WorkResponse.FromString,
                )
        self.procReduceResult = channel.unary_unary(
                '/com.kkennib.grpc.WorkProtocolService/procReduceResult',
                request_serializer=proto_dot_WorkProtocolService__pb2.Work.SerializeToString,
                response_deserializer=proto_dot_WorkProtocolService__pb2.WorkResponse.FromString,
                )


class WorkProtocolServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def greeting(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def collect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def aggregate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def report(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def reduce(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def procReduceResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WorkProtocolServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'greeting': grpc.unary_unary_rpc_method_handler(
                    servicer.greeting,
                    request_deserializer=proto_dot_WorkProtocolService__pb2.Work.FromString,
                    response_serializer=proto_dot_WorkProtocolService__pb2.WorkResponse.SerializeToString,
            ),
            'collect': grpc.unary_unary_rpc_method_handler(
                    servicer.collect,
                    request_deserializer=proto_dot_WorkProtocolService__pb2.Work.FromString,
                    response_serializer=proto_dot_WorkProtocolService__pb2.WorkResponse.SerializeToString,
            ),
            'aggregate': grpc.unary_unary_rpc_method_handler(
                    servicer.aggregate,
                    request_deserializer=proto_dot_WorkProtocolService__pb2.Work.FromString,
                    response_serializer=proto_dot_WorkProtocolService__pb2.WorkResponse.SerializeToString,
            ),
            'report': grpc.unary_unary_rpc_method_handler(
                    servicer.report,
                    request_deserializer=proto_dot_WorkProtocolService__pb2.Work.FromString,
                    response_serializer=proto_dot_WorkProtocolService__pb2.WorkResponse.SerializeToString,
            ),
            'reduce': grpc.unary_unary_rpc_method_handler(
                    servicer.reduce,
                    request_deserializer=proto_dot_WorkProtocolService__pb2.Work.FromString,
                    response_serializer=proto_dot_WorkProtocolService__pb2.WorkResponse.SerializeToString,
            ),
            'procReduceResult': grpc.unary_unary_rpc_method_handler(
                    servicer.procReduceResult,
                    request_deserializer=proto_dot_WorkProtocolService__pb2.Work.FromString,
                    response_serializer=proto_dot_WorkProtocolService__pb2.WorkResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.kkennib.grpc.WorkProtocolService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WorkProtocolService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def greeting(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.kkennib.grpc.WorkProtocolService/greeting',
            proto_dot_WorkProtocolService__pb2.Work.SerializeToString,
            proto_dot_WorkProtocolService__pb2.WorkResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def collect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.kkennib.grpc.WorkProtocolService/collect',
            proto_dot_WorkProtocolService__pb2.Work.SerializeToString,
            proto_dot_WorkProtocolService__pb2.WorkResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def aggregate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.kkennib.grpc.WorkProtocolService/aggregate',
            proto_dot_WorkProtocolService__pb2.Work.SerializeToString,
            proto_dot_WorkProtocolService__pb2.WorkResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def report(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.kkennib.grpc.WorkProtocolService/report',
            proto_dot_WorkProtocolService__pb2.Work.SerializeToString,
            proto_dot_WorkProtocolService__pb2.WorkResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def reduce(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.kkennib.grpc.WorkProtocolService/reduce',
            proto_dot_WorkProtocolService__pb2.Work.SerializeToString,
            proto_dot_WorkProtocolService__pb2.WorkResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def procReduceResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.kkennib.grpc.WorkProtocolService/procReduceResult',
            proto_dot_WorkProtocolService__pb2.Work.SerializeToString,
            proto_dot_WorkProtocolService__pb2.WorkResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)