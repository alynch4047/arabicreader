package uk.co.torquesoftware.torquepaper;

import android.graphics.Canvas;
import android.graphics.Paint;

public class Line {

	private Point startPoint, endPoint;	
	
	public Line(Point startPoint, Point endPoint) {
		super();
		this.startPoint = startPoint;
		this.endPoint = endPoint;
	}	
	
	public Point getStartPoint() {
		return startPoint;
	}

	public void setStartPoint(Point startPoint) {
		this.startPoint = startPoint;
	}

	public Point getEndPoint() {
		return endPoint;
	}

	public void setEndPoint(Point endPoint) {
		this.endPoint = endPoint;
	}

	public double getAngle() {
		return Math.atan2(endPoint.y - startPoint.y, endPoint.x - startPoint.x);
	}

	public void draw(Canvas canvas, Paint paint) {
		for (int i=0; i<8; i++){
			canvas.drawLine(getStartPoint().x,	getStartPoint().y, getEndPoint().x, getEndPoint().y, paint);
		}	
	}
	
	public Point getCentrePoint() {
		return new Point((startPoint.x + endPoint.x) / 2.0, (startPoint.y + endPoint.y) / 2.0); 
	}
	
	private double getSlope() {
		if (endPoint.x == startPoint.x) return 1e8;
		return ((double) (endPoint.y - startPoint.y)) / ((double) (endPoint.x - startPoint.x));
	}
	
	private double getIntercept() {
		return (double) startPoint.y - getSlope() * (double) startPoint.x;
	}

	public Point intersection(Line line1) {
		double m = getSlope();
		double c = getIntercept();
		double n = line1.getSlope();
		double d = line1.getIntercept();
		double  x = (d - c) / (m - n);
		double y = m*x + c;
		return new Point(x, y);
	}

}
