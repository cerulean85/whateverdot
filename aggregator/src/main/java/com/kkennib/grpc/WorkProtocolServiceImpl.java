package com.kkennib.grpc;

import io.grpc.stub.StreamObserver;

import java.util.List;

public class WorkProtocolServiceImpl extends WorkProtocolServiceGrpc.WorkProtocolServiceImplBase{

    @Override
    public void greeting(WorkProtocolServiceOuterClass.Work request,
                         StreamObserver<WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {

        String message = request.getMessage();
        System.out.print(message);
        WorkProtocolServiceOuterClass.WorkResponse response = WorkProtocolServiceOuterClass.WorkResponse.newBuilder()
                .setState("success")
                .build();

        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }

    @Override
    public void aggregate(WorkProtocolServiceOuterClass.Work request,
                        StreamObserver<WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {

        System.out.println("Aggregate...");
    }

    @Override
    public void report(WorkProtocolServiceOuterClass.Work request,
                          StreamObserver<WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {

        System.out.println("Report...");
    }

    @Override
    public void procReduceResult(WorkProtocolServiceOuterClass.Work request,
                       StreamObserver<WorkProtocolServiceOuterClass.WorkResponse> responseObserver) {

        System.out.println("procReduceResult...");
    }


}
