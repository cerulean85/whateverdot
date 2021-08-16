import proto.WorkProtocolService_pb2
import proto.WorkProtocolService_pb2_grpc
import modules.collect.Collector
# import modules.Divider


# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./proto/WorkProtocolService.proto
class WorkProtocol(proto.WorkProtocolService_pb2_grpc.WorkProtocolServiceServicer):

    def echo(self, request, context):
        print("ECHO:", request.message)
        return proto.WorkProtocolService_pb2.WorkResponse(state="Hello!!")

    def collectUrls(self, request, context):
        work_list = []
        for i in range(len(request.workList)):
            work = request.workList[i]
            work_list.append({
                "channel": work.channels[0],
                "keyword": work.keywords[0],
                "start_dt": work.collectionDates[0][0:10],
                "end_dt": work.collectionDates[1][0:10],
                "work_type": "collect_url",
                "work_group_no": work.groupNo,
                "work_no": work.no
            })
        collect = modules.Collector()
        collect.collect_urls(work_list)
        return proto.WorkProtocolService_pb2.WorkResponse(message="requested")

    def collectDocs(self, request, context):
        work_list = []
        for i in range(len(request.workList)):
            work = request.workList[i]
            work_list.append({
                "channel": work.channels[0],
                "keyword": work.keywords[0],
                "start_dt": work.collectionDates[0][0:10],
                "end_dt": work.collectionDates[1][0:10],
                "work_type": "collect_doc",
                "work_group_no": work.groupNo,
                "work_no": work.no
            })
        collect = modules.Collector()
        collect.collect_docs(work_list)
        return proto.WorkProtocolService_pb2.WorkResponse(state="requested")

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
