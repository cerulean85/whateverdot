package com.kkennib.grpc;

import static io.grpc.MethodDescriptor.generateFullMethodName;
import static io.grpc.stub.ClientCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ClientCalls.asyncClientStreamingCall;
import static io.grpc.stub.ClientCalls.asyncServerStreamingCall;
import static io.grpc.stub.ClientCalls.asyncUnaryCall;
import static io.grpc.stub.ClientCalls.blockingServerStreamingCall;
import static io.grpc.stub.ClientCalls.blockingUnaryCall;
import static io.grpc.stub.ClientCalls.futureUnaryCall;
import static io.grpc.stub.ServerCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ServerCalls.asyncClientStreamingCall;
import static io.grpc.stub.ServerCalls.asyncServerStreamingCall;
import static io.grpc.stub.ServerCalls.asyncUnaryCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedStreamingCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.24.0)",
    comments = "Source: WorkProtocolService.proto")
public final class WorkProtocolServiceGrpc {

  private WorkProtocolServiceGrpc() {}

  public static final String SERVICE_NAME = "com.kkennib.grpc.WorkProtocolService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
      com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getGreetingMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "greeting",
      requestType = com.kkennib.grpc.WorkProtocolServiceOuterClass.Work.class,
      responseType = com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
      com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getGreetingMethod() {
    io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work, com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getGreetingMethod;
    if ((getGreetingMethod = WorkProtocolServiceGrpc.getGreetingMethod) == null) {
      synchronized (WorkProtocolServiceGrpc.class) {
        if ((getGreetingMethod = WorkProtocolServiceGrpc.getGreetingMethod) == null) {
          WorkProtocolServiceGrpc.getGreetingMethod = getGreetingMethod =
              io.grpc.MethodDescriptor.<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work, com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "greeting"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.kkennib.grpc.WorkProtocolServiceOuterClass.Work.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse.getDefaultInstance()))
              .setSchemaDescriptor(new WorkProtocolServiceMethodDescriptorSupplier("greeting"))
              .build();
        }
      }
    }
    return getGreetingMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
      com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getCollectMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "collect",
      requestType = com.kkennib.grpc.WorkProtocolServiceOuterClass.Work.class,
      responseType = com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
      com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getCollectMethod() {
    io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work, com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getCollectMethod;
    if ((getCollectMethod = WorkProtocolServiceGrpc.getCollectMethod) == null) {
      synchronized (WorkProtocolServiceGrpc.class) {
        if ((getCollectMethod = WorkProtocolServiceGrpc.getCollectMethod) == null) {
          WorkProtocolServiceGrpc.getCollectMethod = getCollectMethod =
              io.grpc.MethodDescriptor.<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work, com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "collect"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.kkennib.grpc.WorkProtocolServiceOuterClass.Work.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse.getDefaultInstance()))
              .setSchemaDescriptor(new WorkProtocolServiceMethodDescriptorSupplier("collect"))
              .build();
        }
      }
    }
    return getCollectMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
      com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getAggregateMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "aggregate",
      requestType = com.kkennib.grpc.WorkProtocolServiceOuterClass.Work.class,
      responseType = com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
      com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getAggregateMethod() {
    io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work, com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getAggregateMethod;
    if ((getAggregateMethod = WorkProtocolServiceGrpc.getAggregateMethod) == null) {
      synchronized (WorkProtocolServiceGrpc.class) {
        if ((getAggregateMethod = WorkProtocolServiceGrpc.getAggregateMethod) == null) {
          WorkProtocolServiceGrpc.getAggregateMethod = getAggregateMethod =
              io.grpc.MethodDescriptor.<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work, com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "aggregate"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.kkennib.grpc.WorkProtocolServiceOuterClass.Work.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse.getDefaultInstance()))
              .setSchemaDescriptor(new WorkProtocolServiceMethodDescriptorSupplier("aggregate"))
              .build();
        }
      }
    }
    return getAggregateMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
      com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getReportMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "report",
      requestType = com.kkennib.grpc.WorkProtocolServiceOuterClass.Work.class,
      responseType = com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
      com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getReportMethod() {
    io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work, com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getReportMethod;
    if ((getReportMethod = WorkProtocolServiceGrpc.getReportMethod) == null) {
      synchronized (WorkProtocolServiceGrpc.class) {
        if ((getReportMethod = WorkProtocolServiceGrpc.getReportMethod) == null) {
          WorkProtocolServiceGrpc.getReportMethod = getReportMethod =
              io.grpc.MethodDescriptor.<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work, com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "report"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.kkennib.grpc.WorkProtocolServiceOuterClass.Work.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse.getDefaultInstance()))
              .setSchemaDescriptor(new WorkProtocolServiceMethodDescriptorSupplier("report"))
              .build();
        }
      }
    }
    return getReportMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
      com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getReduceMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "reduce",
      requestType = com.kkennib.grpc.WorkProtocolServiceOuterClass.Work.class,
      responseType = com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
      com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getReduceMethod() {
    io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work, com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getReduceMethod;
    if ((getReduceMethod = WorkProtocolServiceGrpc.getReduceMethod) == null) {
      synchronized (WorkProtocolServiceGrpc.class) {
        if ((getReduceMethod = WorkProtocolServiceGrpc.getReduceMethod) == null) {
          WorkProtocolServiceGrpc.getReduceMethod = getReduceMethod =
              io.grpc.MethodDescriptor.<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work, com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "reduce"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.kkennib.grpc.WorkProtocolServiceOuterClass.Work.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse.getDefaultInstance()))
              .setSchemaDescriptor(new WorkProtocolServiceMethodDescriptorSupplier("reduce"))
              .build();
        }
      }
    }
    return getReduceMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
      com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getProcReduceResultMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "procReduceResult",
      requestType = com.kkennib.grpc.WorkProtocolServiceOuterClass.Work.class,
      responseType = com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
      com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getProcReduceResultMethod() {
    io.grpc.MethodDescriptor<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work, com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> getProcReduceResultMethod;
    if ((getProcReduceResultMethod = WorkProtocolServiceGrpc.getProcReduceResultMethod) == null) {
      synchronized (WorkProtocolServiceGrpc.class) {
        if ((getProcReduceResultMethod = WorkProtocolServiceGrpc.getProcReduceResultMethod) == null) {
          WorkProtocolServiceGrpc.getProcReduceResultMethod = getProcReduceResultMethod =
              io.grpc.MethodDescriptor.<com.kkennib.grpc.WorkProtocolServiceOuterClass.Work, com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "procReduceResult"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.kkennib.grpc.WorkProtocolServiceOuterClass.Work.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse.getDefaultInstance()))
              .setSchemaDescriptor(new WorkProtocolServiceMethodDescriptorSupplier("procReduceResult"))
              .build();
        }
      }
    }
    return getProcReduceResultMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static WorkProtocolServiceStub newStub(io.grpc.Channel channel) {
    return new WorkProtocolServiceStub(channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static WorkProtocolServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    return new WorkProtocolServiceBlockingStub(channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static WorkProtocolServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    return new WorkProtocolServiceFutureStub(channel);
  }

  /**
   */
  public static abstract class WorkProtocolServiceImplBase implements io.grpc.BindableService {

    /**
     */
    public void greeting(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request,
        io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {
      asyncUnimplementedUnaryCall(getGreetingMethod(), responseObserver);
    }

    /**
     */
    public void collect(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request,
        io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {
      asyncUnimplementedUnaryCall(getCollectMethod(), responseObserver);
    }

    /**
     */
    public void aggregate(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request,
        io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {
      asyncUnimplementedUnaryCall(getAggregateMethod(), responseObserver);
    }

    /**
     */
    public void report(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request,
        io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {
      asyncUnimplementedUnaryCall(getReportMethod(), responseObserver);
    }

    /**
     */
    public void reduce(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request,
        io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {
      asyncUnimplementedUnaryCall(getReduceMethod(), responseObserver);
    }

    /**
     */
    public void procReduceResult(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request,
        io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {
      asyncUnimplementedUnaryCall(getProcReduceResultMethod(), responseObserver);
    }

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
          .addMethod(
            getGreetingMethod(),
            asyncUnaryCall(
              new MethodHandlers<
                com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
                com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>(
                  this, METHODID_GREETING)))
          .addMethod(
            getCollectMethod(),
            asyncUnaryCall(
              new MethodHandlers<
                com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
                com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>(
                  this, METHODID_COLLECT)))
          .addMethod(
            getAggregateMethod(),
            asyncUnaryCall(
              new MethodHandlers<
                com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
                com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>(
                  this, METHODID_AGGREGATE)))
          .addMethod(
            getReportMethod(),
            asyncUnaryCall(
              new MethodHandlers<
                com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
                com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>(
                  this, METHODID_REPORT)))
          .addMethod(
            getReduceMethod(),
            asyncUnaryCall(
              new MethodHandlers<
                com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
                com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>(
                  this, METHODID_REDUCE)))
          .addMethod(
            getProcReduceResultMethod(),
            asyncUnaryCall(
              new MethodHandlers<
                com.kkennib.grpc.WorkProtocolServiceOuterClass.Work,
                com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>(
                  this, METHODID_PROC_REDUCE_RESULT)))
          .build();
    }
  }

  /**
   */
  public static final class WorkProtocolServiceStub extends io.grpc.stub.AbstractStub<WorkProtocolServiceStub> {
    private WorkProtocolServiceStub(io.grpc.Channel channel) {
      super(channel);
    }

    private WorkProtocolServiceStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected WorkProtocolServiceStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new WorkProtocolServiceStub(channel, callOptions);
    }

    /**
     */
    public void greeting(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request,
        io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(getGreetingMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void collect(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request,
        io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(getCollectMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void aggregate(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request,
        io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(getAggregateMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void report(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request,
        io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(getReportMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void reduce(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request,
        io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(getReduceMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void procReduceResult(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request,
        io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(getProcReduceResultMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   */
  public static final class WorkProtocolServiceBlockingStub extends io.grpc.stub.AbstractStub<WorkProtocolServiceBlockingStub> {
    private WorkProtocolServiceBlockingStub(io.grpc.Channel channel) {
      super(channel);
    }

    private WorkProtocolServiceBlockingStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected WorkProtocolServiceBlockingStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new WorkProtocolServiceBlockingStub(channel, callOptions);
    }

    /**
     */
    public com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse greeting(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request) {
      return blockingUnaryCall(
          getChannel(), getGreetingMethod(), getCallOptions(), request);
    }

    /**
     */
    public com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse collect(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request) {
      return blockingUnaryCall(
          getChannel(), getCollectMethod(), getCallOptions(), request);
    }

    /**
     */
    public com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse aggregate(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request) {
      return blockingUnaryCall(
          getChannel(), getAggregateMethod(), getCallOptions(), request);
    }

    /**
     */
    public com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse report(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request) {
      return blockingUnaryCall(
          getChannel(), getReportMethod(), getCallOptions(), request);
    }

    /**
     */
    public com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse reduce(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request) {
      return blockingUnaryCall(
          getChannel(), getReduceMethod(), getCallOptions(), request);
    }

    /**
     */
    public com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse procReduceResult(com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request) {
      return blockingUnaryCall(
          getChannel(), getProcReduceResultMethod(), getCallOptions(), request);
    }
  }

  /**
   */
  public static final class WorkProtocolServiceFutureStub extends io.grpc.stub.AbstractStub<WorkProtocolServiceFutureStub> {
    private WorkProtocolServiceFutureStub(io.grpc.Channel channel) {
      super(channel);
    }

    private WorkProtocolServiceFutureStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected WorkProtocolServiceFutureStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new WorkProtocolServiceFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> greeting(
        com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request) {
      return futureUnaryCall(
          getChannel().newCall(getGreetingMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> collect(
        com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request) {
      return futureUnaryCall(
          getChannel().newCall(getCollectMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> aggregate(
        com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request) {
      return futureUnaryCall(
          getChannel().newCall(getAggregateMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> report(
        com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request) {
      return futureUnaryCall(
          getChannel().newCall(getReportMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> reduce(
        com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request) {
      return futureUnaryCall(
          getChannel().newCall(getReduceMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse> procReduceResult(
        com.kkennib.grpc.WorkProtocolServiceOuterClass.Work request) {
      return futureUnaryCall(
          getChannel().newCall(getProcReduceResultMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_GREETING = 0;
  private static final int METHODID_COLLECT = 1;
  private static final int METHODID_AGGREGATE = 2;
  private static final int METHODID_REPORT = 3;
  private static final int METHODID_REDUCE = 4;
  private static final int METHODID_PROC_REDUCE_RESULT = 5;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final WorkProtocolServiceImplBase serviceImpl;
    private final int methodId;

    MethodHandlers(WorkProtocolServiceImplBase serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_GREETING:
          serviceImpl.greeting((com.kkennib.grpc.WorkProtocolServiceOuterClass.Work) request,
              (io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>) responseObserver);
          break;
        case METHODID_COLLECT:
          serviceImpl.collect((com.kkennib.grpc.WorkProtocolServiceOuterClass.Work) request,
              (io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>) responseObserver);
          break;
        case METHODID_AGGREGATE:
          serviceImpl.aggregate((com.kkennib.grpc.WorkProtocolServiceOuterClass.Work) request,
              (io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>) responseObserver);
          break;
        case METHODID_REPORT:
          serviceImpl.report((com.kkennib.grpc.WorkProtocolServiceOuterClass.Work) request,
              (io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>) responseObserver);
          break;
        case METHODID_REDUCE:
          serviceImpl.reduce((com.kkennib.grpc.WorkProtocolServiceOuterClass.Work) request,
              (io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>) responseObserver);
          break;
        case METHODID_PROC_REDUCE_RESULT:
          serviceImpl.procReduceResult((com.kkennib.grpc.WorkProtocolServiceOuterClass.Work) request,
              (io.grpc.stub.StreamObserver<com.kkennib.grpc.WorkProtocolServiceOuterClass.WorkResponse>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  private static abstract class WorkProtocolServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    WorkProtocolServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return com.kkennib.grpc.WorkProtocolServiceOuterClass.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("WorkProtocolService");
    }
  }

  private static final class WorkProtocolServiceFileDescriptorSupplier
      extends WorkProtocolServiceBaseDescriptorSupplier {
    WorkProtocolServiceFileDescriptorSupplier() {}
  }

  private static final class WorkProtocolServiceMethodDescriptorSupplier
      extends WorkProtocolServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final String methodName;

    WorkProtocolServiceMethodDescriptorSupplier(String methodName) {
      this.methodName = methodName;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (WorkProtocolServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new WorkProtocolServiceFileDescriptorSupplier())
              .addMethod(getGreetingMethod())
              .addMethod(getCollectMethod())
              .addMethod(getAggregateMethod())
              .addMethod(getReportMethod())
              .addMethod(getReduceMethod())
              .addMethod(getProcReduceResultMethod())
              .build();
        }
      }
    }
    return result;
  }
}
