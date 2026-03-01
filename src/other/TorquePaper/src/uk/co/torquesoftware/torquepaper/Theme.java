package uk.co.torquesoftware.torquepaper;

public class Theme implements ITheme {

	IDisplayProperties [] displayProperties;	
	
	int touchX, touchY;
	float cyclePercentage;
	
	public Theme(IDisplayProperties[] displayProperties, int touchX, int touchY, float cyclePercentage) {
		this.displayProperties = displayProperties;
		this.touchX = touchX;
		this.touchY = touchY;
		this.cyclePercentage = cyclePercentage;
	}

	@Override
	public IDisplayProperties[] getDisplayProperties() {
		DisplayProperties[] displayPropertiesCopy = new DisplayProperties[3];
		displayPropertiesCopy[0] = displayProperties[0].copy();
		displayPropertiesCopy[1] = displayProperties[1].copy();
		displayPropertiesCopy[2] = displayProperties[2].copy();
		return displayPropertiesCopy;
	}

	@Override
	public void setDisplayProperties(IDisplayProperties[] displayPropertiesArray) {
		displayProperties = displayPropertiesArray;
	}

	@Override
	public int getTouchX() {
		return touchX;
	}

	@Override
	public int getTouchY() {
		return touchY;
	}

	@Override
	public float getCyclePercentage() {
		return cyclePercentage;
	}

}
