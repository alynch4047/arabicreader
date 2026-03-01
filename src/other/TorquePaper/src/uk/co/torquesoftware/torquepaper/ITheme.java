package uk.co.torquesoftware.torquepaper;

public interface ITheme {
	
	IDisplayProperties []  getDisplayProperties();
	
	void setDisplayProperties(IDisplayProperties[]  displayPropertiesArray);
	
	int getTouchX();
	
	int getTouchY();
	
	float getCyclePercentage();

}
