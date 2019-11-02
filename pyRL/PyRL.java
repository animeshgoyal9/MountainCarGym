package pyRL;

import io.grpc.stub.StreamObserver;
import pyRL.PyRLGrpc.PyRLImplBase;
import pyRL.PyRLProto.Action;
import pyRL.PyRLProto.Obs;

public class PyRL extends PyRLImplBase{
	
	@Override
	public void getObs(Action request, StreamObserver<Obs> responseObserver) {
		Observation.setFlag(1);
		Observation.setAction(request.getAction());
		
		Obs.Builder resp = Obs.newBuilder();
		
		resp.setX(Observation.getX()).setV(Observation.getV());
		
		responseObserver.onNext(resp.build());
		responseObserver.onCompleted();
	}
	
}
