package uk.co.torquesoftware.torquepaper;

import java.util.ArrayList;
import java.util.List;

public class PolygonLayout {
	
	static List<Polygon> createOctagonalPolygonsWithSquares(Point topLeft, Point bottomRight,
			       int polygonWidth, ITheme theme, double innerCircleRatioOctagon, double innerCircleRatioSquare){
		int numAcross = (int) ((bottomRight.x - topLeft.x) / polygonWidth) + 1;
		int numDown = (int) ((bottomRight.y - topLeft.y) / polygonWidth) + 1;
		double angularStep = 2 * Math.PI/8;
		double radius = (polygonWidth / 2.0) / Math.cos(angularStep / 2.0) ;
		Polygon[][] polygons = new Polygon[numAcross][numDown];
		List<Polygon> allPolygons = new ArrayList<Polygon>();
		for (int i = 0; i < numAcross; i++) {
			for (int j = 0; j < numDown; j++) {
				Polygon octagon = new Polygon(8,  topLeft.x + polygonWidth * i, topLeft.y + polygonWidth * j,  radius, 
																					  0, innerCircleRatioOctagon);
				octagon.setDisplayProperties(theme.getDisplayProperties()[0]);
				allPolygons.add(octagon);
				polygons[i][j] = octagon;
			}
		}

		for (int i = 0; i < numAcross - 1; i++) {
			for (int j = 0; j < numDown - 1; j++) {
				Polygon square = PolygonBuilder.buildSquareFromTwoOctagons(polygons[i][j], polygons[i+1][j+1], 
																																		                innerCircleRatioSquare);
				square.setDisplayProperties(theme.getDisplayProperties()[1]);
				allPolygons.add(square);
			}
		}
		return allPolygons;
	}

	public static List<Polygon> createDecagonalPolygonsWithPentagons(
				Point topLeft, Point bottomRight, double decagonRadius,
				double innerCircleRatioDecagon, double innerCircleRatioPentagon, double innerCircleRatioHexagon, ITheme theme) {

		List<Polygon> allPolygons = new ArrayList<Polygon>();
		
		int numAcross = (int) ((bottomRight.x - topLeft.x) / (decagonRadius * 2)) + 1;
		int numDown = (int) ((bottomRight.y - topLeft.y) / (decagonRadius * 2)) + 1;		
		Polygon[][] polygons = new Polygon[numAcross][numDown];
		
		for (int i = 0; i < numAcross; i++) {
			for (int j = 0; j < numDown; j++) {
				double angle = Math.PI * 2 / 10;
				double offsetA = decagonRadius * 2 + 2  * decagonRadius * Math.sin(Math.PI / 10.0) ;
				double offsetX = 2 * offsetA * Math.sin(angle);
				double offsetY = offsetA * Math.cos(angle);
				double extraOffsetX = offsetA * Math.sin(angle);
				if (j%2 == 0) extraOffsetX = 0;
				Polygon decagon = createDecagonWithPentagons(decagonRadius, allPolygons,
															topLeft.x + (offsetX * i) + extraOffsetX, topLeft.y + (offsetY * j),
															innerCircleRatioDecagon, innerCircleRatioPentagon, theme);
				polygons[i][j] = decagon;
			}
		}		
		
		for (int i = 0; i < numAcross - 1; i++) {
			for (int j = 1; j < numDown - 1; j++) {
				Polygon hexagon;
				if (j%2 == 0) {
				hexagon = PolygonBuilder.buildHexagonFromDecagons(polygons[i][j], polygons[i+1][j],
																																	 polygons[i][j - 1], innerCircleRatioHexagon, theme);
				} 
				else {
				hexagon = PolygonBuilder.buildHexagonFromDecagons(polygons[i][j], polygons[i+1][j],
																																	 polygons[i + 1][j - 1], innerCircleRatioHexagon, theme);
				}
				allPolygons.add(hexagon);
			}
		}
		return allPolygons;
	}

	private static Polygon createDecagonWithPentagons(double decagonRadius,
			List<Polygon> allPolygons, double x, double y,
			double innerCircleRatioDecagon, double innerCircleRatioPentagon, ITheme theme) {
		Polygon decagon = new Polygon(10,  x, y,  decagonRadius, 0, innerCircleRatioDecagon);
		decagon.setDisplayProperties(theme.getDisplayProperties()[0]);
		allPolygons.add(decagon);
		
		double pentagonRadius = decagonRadius * (Math.sin(Math.PI / 10.0) / Math.sin(Math.PI / 5.0));
		
		double distanceBetweenCentres = decagonRadius * Math.cos(Math.PI / 10.0) + 
																			      pentagonRadius * Math.cos(Math.PI / 5.0) ;
		
		decagon.relatedPolygons = new ArrayList<Polygon>();
		
		for (int i = 1; i < 5; i++) {
			double alpha = i * Math.PI / 5.0;
			double rotation = Math.PI / 5.0 + alpha;
			double pentagonXCentre = x + distanceBetweenCentres * Math.cos(alpha);
			double pentagonYCentre = y + distanceBetweenCentres * Math.sin(alpha);
			
			Polygon pentagon = new Polygon(5,  pentagonXCentre,  pentagonYCentre,
																			        pentagonRadius, rotation, innerCircleRatioPentagon);
			pentagon.setDisplayProperties(theme.getDisplayProperties()[1]);
			decagon.relatedPolygons.add(pentagon);

			allPolygons.add(pentagon);
		}
		return decagon;
	}
	


}
