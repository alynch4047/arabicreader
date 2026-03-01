package uk.co.torquesoftware.torquepaper;

public interface IDisplayProperties {
	
	public void setKaleidoscope(boolean flag);
	public boolean getKaleidoscope();
	
	public void setTouchCount(int count);
	public int getTouchCount();	
	
	public void setLineThickness(int thickness);
	public int getLineThickness();
	
	public void setPrimaryFillColour(int colour);
	public int getPrimaryFillColour();
	
	public void setSecondaryFillColour(int colour);
	public int getSecondaryFillColour();
	
	public void setTertiaryFillColour(int colour);
	public int getTertiaryFillColour();	
	
	public void setLineColour(int colour);
	public int getLineColour();
	public DisplayProperties copy();

}
