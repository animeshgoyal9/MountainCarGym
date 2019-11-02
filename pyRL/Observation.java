package pyRL;

public class Observation {
	static int action = 0;
	static int x = 0;
	static int v = 0;
	static int flag = 0; 
	
	public static int getAction() {
		return action;
	}
	
	public static void setAction(int action) {
		Observation.action = action;
	}
	
	public static int getX() {
		return x;
	}
	
	public static void setX(int x) {
		Observation.x = x;
	}
	
	public static int getV() {
		return v;
	}
	
	public static void setV(int v) {
		Observation.v = v;
	}

	public static int getFlag() {
		return flag;
	}

	public static void setFlag(int flag) {
		Observation.flag = flag;
	}
}
