import proto.WorkProtocolService_pb2
import proto.WorkProtocolService_pb2_grpc
import modules.Collector
import modules.Divider


# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./proto/WorkProtocolService.proto
class WorkProtocol(proto.WorkProtocolService_pb2_grpc.WorkProtocolServiceServicer):

    def echo(self, request, context):
        print("ECHO:", request.message)
        return proto.WorkProtocolService_pb2.WorkResponse(state="Hello!!")

    def collectUrls(self, request, context):
        print("Collect:")
        print(request)
        # divider
        # c = modules.Collector()
        # c.collect_urls(request)
        return proto.WorkProtocolService_pb2.WorkResponse(message="requested")

    def collectDocs(self, request, context):
        print("Collect:", request.message)
        c = modules.Collector()
        c.collect_docs(request)
        return proto.WorkProtocolService_pb2.WorkResponse(state="Hello!!")

    # def collect(self, request, context):
    #     Collector().collect_urls(request)
    #     return proto.WorkProtocolService_pb2.WorkResponse(state="Hello!!")

    # def requestAggregate(self, request, context):
    #     print(request.message)
    #     return proto.WorkProtocolService_pb2.WorkResponse(state="Hello!!")
    #
    # def responseAggregate(self, request, context):
    #     print(request.message)
    #     return proto.WorkProtocolService_pb2.WorkResponse(state="Hello!!")
    #
    # def requestReport(self, request, context):
    #     print(request.message)
    #     return proto.WorkProtocolService_pb2.WorkResponse(state="Hello!!")
    #
    # def responseReport(self, request, context):
    #     print(request.message)
    #     return proto.WorkProtocolService_pb2.WorkResponse(state="Hello!!")
    #
    # def requestReduce(self, request, context):
    #     print(request.message)
    #     return proto.WorkProtocolService_pb2.WorkResponse(state="Hello!!")
