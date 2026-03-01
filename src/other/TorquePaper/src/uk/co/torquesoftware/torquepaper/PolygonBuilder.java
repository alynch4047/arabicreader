package uk.co.torquesoftware.torquepaper;

public class PolygonBuilder {
	
	public static Polygon buildFromPoints(Point[] points, double innerCircleRatio) {
		/* Build a polygon from a list of points */
		int numPoints = points.length;
		Polygon polygon = new Polygon(numPoints, 0, 0, 100, 0, innerCircleRatio);
		polygon.setPoints(points, innerCircleRatio);
		return polygon;
	}

	public static Polygon buildSquareFromTwoOctagons(Polygon octagon1,
			Polygon octagon2, double innerCircleRatio) {
		/***
		 *  Return a polygon (square) between by two opposite octagons 
		*   oct1
		*        square
		*              oct2 
		 ** */
    	Point[] points = {octagon1.getPoints()[1],
															octagon2.getPoints()[6],
															octagon2.getPoints()[5],
															octagon1.getPoints()[2],};
    	Polygon square = PolygonBuilder.buildFromPoints(points, innerCircleRatio);
		return square;
	}

	public static Polygon buildHexagonFromDecagons(Polygon polygon1,
			Polygon polygon2, Polygon polygon3, double innerCircleRatioHexagon, ITheme theme) {
		/***
		 *  Return a polygon (hexagon) from four decagons and their related polygons
		*   oct1
		*        square
		*              oct2 
		 ** */
    	Point[] points = {polygon2.getPoints()[5],
    			polygon2.relatedPolygons.get(3).getPoints()[1],
    			polygon1.relatedPolygons.get(0).getPoints()[3],
    			polygon1.getPoints()[0],
    			polygon3.relatedPolygons.get(2).getPoints()[4],
    			polygon3.relatedPolygons.get(1).getPoints()[0],};
    	Polygon hexagon = PolygonBuilder.buildFromPoints(points, innerCircleRatioHexagon);
    	hexagon.setDisplayProperties(theme.getDisplayProperties()[2]);
    	return hexagon;
	}

}
