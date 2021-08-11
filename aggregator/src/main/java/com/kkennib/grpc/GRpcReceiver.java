package com.kkennib.grpc;

import io.grpc.Server;
import io.grpc.ServerBuilder;

import java.io.IOException;

public class GRpcReceiver {

    public void receive() {
        try {
            Server server = ServerBuilder.forPort(8084)
                    .addService(new WorkProtocolServiceImpl())
                    .build();

            server.start();

            System.out.println("Publisher Receiving Packets...");
            server.awaitTermination();

        } catch(IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
