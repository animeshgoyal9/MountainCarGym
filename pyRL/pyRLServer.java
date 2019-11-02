package pyRL;

import java.io.IOException;

import burlap.domain.singleagent.mountaincar.MountainCar;
import io.grpc.Server;
import io.grpc.ServerBuilder;

public class pyRLServer {
	public static void main(String[] args) throws IOException, InterruptedException {
		Server server = ServerBuilder.forPort(9090).addService(
				new PyRL()).build();
		server.start();
		
		System.out.println("Server started at " + server.getPort());
		
		new MountainCar().Run();
		
		server.awaitTermination();
				
	} 
}
