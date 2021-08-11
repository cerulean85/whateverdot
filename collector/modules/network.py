import time
import grpc
from kafka import KafkaProducer
from concurrent import futures
from proto import WorkProtocol
from proto import WorkProtocolService_pb2
from proto import WorkProtocolService_pb2_grpc


def start_rpc_server():
    print("Started gRPC Server...")
    proc = WorkProtocol()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    WorkProtocolService_pb2_grpc.add_WorkProtocolServiceServicer_to_server(proc, server)
    server.add_insecure_port('localhost:8083')
    server.start()
    server.wait_for_termination()


def batch_to_queue(kafka_topic_name, data_list):
    start_time = time.time()
    producer = KafkaProducer(acks=0, compression_type='gzip', bootstrap_servers=['localhost:9092'],
                             api_version=(0, 10, 1),
                             value_serializer=lambda x: x.encode('euc-kr'))

    for data in data_list:
        producer.send(kafka_topic_name, value=data)

    producer.flush()
    producer.close()

    end = time.time()
    print("수행 시간: {} ms".format((end - start_time)))


def response_reduce_result():
    channel = grpc.insecure_channel('localhost:8084')
    stub = WorkProtocolService_pb2_grpc.WorkProtocolServiceStub(channel)
    stub.procReduceResult(WorkProtocolService_pb2.Work(
        message="ㅋㅋㅋ"
    ))