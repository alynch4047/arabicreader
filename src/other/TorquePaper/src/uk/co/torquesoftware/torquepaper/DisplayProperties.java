package uk.co.torquesoftware.torquepaper;


public class DisplayProperties implements IDisplayProperties {
	
	private int lineThickness;
	private int primaryFillColour;
	private int secondaryFillColour;
	private int tertiaryFillColour;	
	private int lineColour;	
	private int touchCount;
	private boolean kaleidoscope; 

	public DisplayProperties(int primaryFillColour, int lineColour, int lineThickness) {
		super();
		this.lineThickness = lineThickness;
		this.primaryFillColour = primaryFillColour;
		this.lineColour = lineColour;
		kaleidoscope = false;
		touchCount = 0;
	}
	
	public DisplayProperties copy() {
		DisplayProperties copy = new DisplayProperties(primaryFillColour, lineColour, lineThickness);
		copy.setKaleidoscope(kaleidoscope);
		copy.setTouchCount(touchCount);
		return copy;
	}

	@Override
	public void setPrimaryFillColour(int colour) {
		primaryFillColour = colour;
	}

	@Override
	public int getPrimaryFillColour() {
		return primaryFillColour;
	}

	@Override
	public void setLineColour(int colour) {
		lineColour = colour;
	}

	@Override
	public int getLineColour() {
		return lineColour;
	}

	@Override
	public void setLineThickness(int thickness) {
		lineThickness = thickness;
	}

	@Override
	public int getLineThickness() {
		return lineThickness;
	}

	@Override
	public void setSecondaryFillColour(int colour) {
		secondaryFillColour = colour;
	}

	@Override
	public int getSecondaryFillColour() {
		return secondaryFillColour;
	}

	@Override
	public void setTertiaryFillColour(int colour) {
		tertiaryFillColour = colour;
	}

	@Override
	public int getTertiaryFillColour() {
		return tertiaryFillColour;
	}

	@Override
	public void setKaleidoscope(boolean flag) {
		kaleidoscope = flag;
	}

	@Override
	public boolean getKaleidoscope() {
		return kaleidoscope;
	}

	@Override
	public void setTouchCount(int count) {
		touchCount = count;
	}

	@Override
	public int getTouchCount() {
		return touchCount;
	}

}
