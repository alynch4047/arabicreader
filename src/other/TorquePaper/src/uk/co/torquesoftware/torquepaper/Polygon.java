package uk.co.torquesoftware.torquepaper;

import java.util.List;

import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Paint.Style;
import android.graphics.Path;


public class Polygon {
	
	private int numSides;
	private double angularStep;
	private Point centre;
	private double radius, innerCircleRadius;
	private double innerCircleRatio;
	private Point[] points ;
	private Point[]  innerCirclePoints ;
	private Point[]  intersectionPoints;
	private Point[] outerPoints;
	private Line[]  lines;
	public List<Polygon> relatedPolygons;
	public Line[] getLines() {
		return lines;
	}

	public void setLines(Line[] lines) {
		this.lines = lines;
	}

	private IDisplayProperties displayProperties;
	private double angularOffset;
	
	Polygon(int numSides, double centreX, double centreY, double radius,
			          double angularOffset, double innerCircleRatio) {
		this.numSides = numSides;
		this.angularOffset = angularOffset;
		this.radius = radius;
		points = new Point[numSides];
		 innerCirclePoints = new Point[numSides];
		 intersectionPoints = new Point[numSides];
		 outerPoints = new Point[numSides];		 
		 lines = new Line[numSides];		
		angularStep =2 * Math.PI/numSides;
		centre = new Point(centreX, centreY);
		setInnerCircleRatio(innerCircleRatio);
		initialisePoints();
		initialiseLines();
		initialiseInnerCirclePoints();
		displayProperties = new DisplayProperties(Color.argb(50,200, 200, 0), Color.argb(75, 0 , 80, 0),  2);
	}
	
	public void setDisplayProperties(IDisplayProperties displayProperties) {
		this.displayProperties = displayProperties;
	}
	
	public IDisplayProperties getDisplayProperties() {
		return displayProperties;
	}
	
	public double getRadius() {
		return radius;
	}
	
	private void initialisePoints() {
		double angle;
		for (int i = 0;  i < numSides;  i++) {
			angle = i * angularStep - angularStep / 2.0 + angularOffset;
			double x = centre.x + Math.cos(angle) * radius;
			double y = centre.y + Math.sin(angle) * radius;
			points[i] = new Point(x, y);
		}
	}
	
	public void setPoints(Point[] points, double innerCircleRatio) {
		/* Construct the polygon (irregular) from a list of points */
		this.points = points.clone();
		// estimate radius and centre
		double area = getArea();
		double approxRadius = Math.sqrt(area / (Math.PI * 2));
		radius = approxRadius;
		setInnerCircleRatio(0.5);
		innerCircleRadius = approxRadius *innerCircleRatio;
		int totalX = 0;
		int totalY = 0;
		for (Point point : points) {
			totalX += point.x;
			totalY += point.y;
		}
		int centreX = totalX / numSides;
		int centreY = totalY / numSides;
		centre = new Point(centreX, centreY);
		initialiseLines();
		// calculate angular offset by getting angle of radius to centre of line0
		Point centreLine0 = lines[0].getCentrePoint();
		Line radiusVector = new Line(centre, centreLine0);
		angularOffset = radiusVector.getAngle();
		initialiseInnerCirclePoints();
		
	}
	
	
	private double getArea() {
		float area = 0.0f;

		for (int i = 0; i < numSides - 1; ++i)
		  area += points[i].x * points[i+1].y - points[i+1].x * points[i].y;
		area += points[numSides-1].x * points[0].y - points[0].x * points[numSides-1].y;
		area /= 2.0f;
		return area;
	}
	
	public double getDistanceToCentreSide() {
		return radius * Math.cos(Math.PI / numSides);
	}

	private void initialiseInnerCirclePoints() {
		double angle;
		for (int i = 0;  i < numSides;  i++) {
			angle = i * angularStep + angularOffset;
			double x = centre.x + Math.cos(angle) * innerCircleRadius;
			double y = centre.y + Math.sin(angle) * innerCircleRadius;
			innerCirclePoints[i] = new Point(x, y);
		}
		for (int i = 0;  i < numSides;  i++) {
			int nextPointIndex = i + 1;
			if (nextPointIndex == numSides) nextPointIndex = 0;
			outerPoints[i] = lines[i].getCentrePoint();
		}		
		// calculate intersection points
		for (int i = 0;  i < numSides;  i++) {
			int previousIndex = i - 1;
			int nextIndex = i + 1;
			if (previousIndex == -1) previousIndex = numSides - 1;
			if (nextIndex == numSides) nextIndex = 0;
			Line line0 = new Line(innerCirclePoints[i], outerPoints[previousIndex]);
			Line line1 = new Line(innerCirclePoints[previousIndex], outerPoints[i]); 
			Point intersectionPoint = line0.intersection(line1);
			intersectionPoints[i] = intersectionPoint;
		}
	}
	
	private void initialiseLines() {
		for (int i = 0;  i < numSides;  i++) {
			int nextPointIndex = i + 1;
			if (nextPointIndex == numSides) nextPointIndex = 0;
			lines[i] = new Line(points[i], points[nextPointIndex]);
		}
	}

	public Point getCentre() {
		return centre;
	}
	
	public Point[] getPoints() {
		return points;
	}

	public void setCentre(Point centre) {
		this.centre = centre;
	}
	
	public void drawLines(Canvas canvas) {
		for (int i=0; i<numSides; i++){
			canvas.save();
			Paint paint = new Paint();
			paint.setStrokeCap(Paint.Cap.ROUND);
			paint.setColor(displayProperties.getLineColour());
			paint.setStrokeWidth(displayProperties.getLineThickness());			
			Line line = lines[i];
			line.draw(canvas, paint);
		}
		canvas.restore();
	}
	
	public void fillPolygons(Canvas canvas) {
		for (int i=0; i<numSides; i++){
			int previousIndex = i - 1;
			int nextIndex = i + 1;
			if (previousIndex == -1) previousIndex = numSides - 1;
			if (nextIndex == numSides) nextIndex = 0;
			Paint paint = new Paint();
			paint.setStyle(Style.FILL);
			if (! displayProperties.getKaleidoscope()) {
			paint.setColor(displayProperties.getPrimaryFillColour());
			} else {
				int colourIndex = i;
				colourIndex += displayProperties.getTouchCount();
				if (colourIndex > numSides) colourIndex -= numSides;
				float hue = (float) colourIndex / (float) numSides * 360f;
				float saturation = 0.9f;
				float value = 0.5f;
				float[] hsv = { hue, saturation, value };
				int color = Color.HSVToColor(hsv);
				color &= 0x00FFFFFF;
				int alpha = displayProperties.getPrimaryFillColour() & 0xFF000000;
				color |= alpha;
				paint.setColor(color);
			}
			
			fillPolygon(canvas, innerCirclePoints[i], intersectionPoints[i], outerPoints[i], intersectionPoints[nextIndex],
					paint);
		}
	}

	private void fillPolygon(Canvas canvas, Point point, Point point2, Point point3,
			Point point4, Paint paint) {
		Path wallpath = new Path();
		wallpath.reset(); // only needed when reusing this path for a new build
		wallpath.moveTo(point.x, point.y); // used for first point
		wallpath.lineTo(point2.x, point2.y);
		wallpath.lineTo(point3.x, point3.y);
		wallpath.lineTo(point4.x, point4.y);
		canvas.drawPath(wallpath, paint);
	}

	public void draw(Canvas canvas) {
		canvas.save();
		Paint paint = new Paint();
		paint.setStrokeCap(Paint.Cap.ROUND);
		paint.setColor(displayProperties.getLineColour());
		paint.setStrokeWidth(displayProperties.getLineThickness());
		
		for (int i = 0;  i < numSides;  i++) {
			int adjacentLineIndex1 = i - 1;
			if (adjacentLineIndex1 == -1) adjacentLineIndex1 = numSides - 1;
			int adjacentLineIndex2 = i + 1;
			if (adjacentLineIndex2 == numSides) adjacentLineIndex2 = 0;
			Line adjacentLine1 = lines[adjacentLineIndex1];
			Line adjacentLine2 = lines[adjacentLineIndex2];
			Line newLine1 = new Line(innerCirclePoints[i] , adjacentLine1.getCentrePoint());
			Line newLine2 = new Line(innerCirclePoints[i] , adjacentLine2.getCentrePoint());
			newLine1.draw(canvas, paint);
			newLine2.draw(canvas, paint);
		}
		canvas.restore();
	};
	
	public void drawPoints(Canvas canvas) {
		canvas.save();
		Paint paint = new Paint();
		
		paint.setStrokeCap(Paint.Cap.ROUND);
		paint.setColor(Color.GREEN);
		paint.setTextSize(12);
		paint.setStrokeWidth(displayProperties.getLineThickness());
		for (int i=0; i<numSides; i++){
			Point point = innerCirclePoints[i];
			canvas.drawText(String.valueOf(i), point.x, point.y, paint);
		}
		paint.setColor(Color.YELLOW);
		for (int i=0; i<numSides; i++){
			Point point = outerPoints[i];
			canvas.drawText(String.valueOf(i), point.x, point.y, paint);
		}
		paint.setColor(Color.WHITE);
		for (int i=0; i<numSides; i++){
			Point point = intersectionPoints[i];
			canvas.drawText(String.valueOf(i), point.x, point.y, paint);
		}			
		canvas.restore();
	};	
	
	public double getInnerCircleRatio() {
		return innerCircleRatio;
	}

	public void setInnerCircleRatio(double innerCircleRatio) {
		this.innerCircleRatio = innerCircleRatio;
		innerCircleRadius = radius * innerCircleRatio; 
	}

	public int getNumSides() {
		return numSides;
	}
	


}
