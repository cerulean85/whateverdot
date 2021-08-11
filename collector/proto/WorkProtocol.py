import proto.WorkProtocolService_pb2
import proto.WorkProtocolService_pb2_grpc
from modules import Collector


# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./proto/WorkProtocolService.proto
class WorkProtocol(proto.WorkProtocolService_pb2_grpc.WorkProtocolServiceServicer):
    def greeting(self, request, context):
        print(request.message)
        return proto.WorkProtocolService_pb2.WorkResponse(state="Hello!!")

    def collect(self, request, context):
        Collector().test()
        print(request.message)
        return proto.WorkProtocolService_pb2.WorkResponse(state="Hello!!")

    def aggregate(self, request, context):
        print(request.workList)
        return proto.WorkProtocolService_pb2.WorkResponse(state="Hello!!")

    def report(self, request, context):
        print(request.workList)
        return proto.WorkProtocolService_pb2.WorkResponse(state="Hello!!")

    def reduce(self, request, context):
        print(request.workList)
        return proto.WorkProtocolService_pb2.WorkResponse(state="Hello!!")

    def procReduceResult(elf, request, context):
        print(request.workList)
        return proto.WorkProtocolService_pb2.WorkResponse(state="Hello!!")