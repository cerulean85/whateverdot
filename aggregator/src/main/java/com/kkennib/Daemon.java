package com.kkennib;

//import com.kkennib.grpc.WorkProtocolServiceGrpc;
//import com.kkennib.grpc.WorkProtocolServiceOuterClass;
//import com.kkennib.grpc.GRpcReceiver;
//import com.kkennib.kafka.KafakaConsumer;
//import com.kkennib.kafka.KafakaConsumer;
//import io.grpc.ManagedChannel;
//import io.grpc.ManagedChannelBuilder;

//import java.util.List;

//import com.kkennib.grpc.GRpcReceiver;
import com.kkennib.grpc.GRpcReceiver;
import com.kkennib.grpc.WorkProtocolServiceGrpc;
import com.kkennib.grpc.WorkProtocolServiceOuterClass;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

public class Daemon {

    private static Object List;

    public static void main(String[] args ) {

//        greeting();
//        req_reduce();
//        (new KafakaConsumer()).consume("test");
//        GRpcReceiver receiver = new GRpcReceiver();
//        receiver.receive();
        GRpcReceiver t = new GRpcReceiver();
        t.receive();
    }

    static void greeting() {
        final ManagedChannel channel = ManagedChannelBuilder.forTarget("localhost:8083")
                .usePlaintext(true)
                .build();
        WorkProtocolServiceGrpc.WorkProtocolServiceBlockingStub stub = WorkProtocolServiceGrpc.newBlockingStub(channel);
        WorkProtocolServiceOuterClass.Work work = WorkProtocolServiceOuterClass.Work.newBuilder()
                .setMessage("ㅋㅋㅋ").addChannels("zzz")
                .build();
        WorkProtocolServiceOuterClass.WorkResponse response = stub.greeting(work);

        channel.shutdownNow();
    }

    static void req_reduce() {
        final ManagedChannel channel = ManagedChannelBuilder.forTarget("localhost:8083")
                .usePlaintext(true)
                .build();

        WorkProtocolServiceGrpc.WorkProtocolServiceBlockingStub stub = WorkProtocolServiceGrpc.newBlockingStub(channel);
        WorkProtocolServiceOuterClass.Work work = WorkProtocolServiceOuterClass.Work.newBuilder()
                .addWorkList(1)
                .addWorkList(2)
                .addWorkList(3)
                .build();
        WorkProtocolServiceOuterClass.WorkResponse response = stub.reduce(work);

        channel.shutdownNow();
    }

}
