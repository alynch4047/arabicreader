package uk.co.torquesoftware.torquepaper;

public class Point {
	
	public int x, y;

	public Point(int x, int y) {
		this.x = x;
		this.y = y;
	}

	public Point(double x, double y) {
		this.x = (int) x;
		this.y = (int) y;
	}
	
	public Point minus(Point point) {
		return new Point(x - point.x, y - point.y);
	}

}
