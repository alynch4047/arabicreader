package uk.co.torquesoftware.torquepaper;

import java.util.List;

import android.content.SharedPreferences;
import android.content.res.Resources;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.os.Handler;
import android.service.wallpaper.WallpaperService;
import android.util.DisplayMetrics;
import android.util.FloatMath;
import android.util.Log;
import android.view.Display;
import android.view.MotionEvent;
import android.view.SurfaceHolder;
import android.view.WindowManager;

public class TorquePaper extends WallpaperService
{

	public static final String SHARED_PREFS_NAME	= "torquepapersettings";

	@Override
	public void onCreate()
	{
		super.onCreate();
	}

	@Override
	public void onDestroy()
	{
		super.onDestroy();
	}

	@Override
	public Engine onCreateEngine()
	{
		return new GeometryPatternEngine();
	}

	class GeometryPatternEngine extends Engine implements
											SharedPreferences.OnSharedPreferenceChangeListener
	{
		private final Handler handler	= new Handler();
		private float touchX = -1;
		private float touchY = -1;
		private int touchCount = 0;
		private final Paint mPaint			= new Paint();
		private final Runnable drawPatternRunnable	= new Runnable()
				{
					public void run()
					{
						drawFrame();
					}
				};
		private boolean 	mVisible;
		private SharedPreferences	preferences;

		private Rect	rectFrame;

		// private
		private int	frameCount	= 0;
		private int maxFrameCount;
		private String pattern= "Dodecagonal Pattern";
		private String size	= "Medium";
		private int primaryColour;
		private int secondaryColour;
		private int tertiaryColour;
		private int transparency, alpha;
		private boolean rotateColours;
		private boolean expanding;
		private int expansionCount;
		float cyclePercentage;
		private boolean inDestroy = false;
		
		private int rotateColour() {

			float hue = cyclePercentage * 360.0f;
			float saturation = 0.9f;
			float value = 0.5f;
			float[] hsv = { hue, saturation, value };
			int color = Color.HSVToColor(hsv);
			color &= 0x00FFFFFF;

			return alpha | color;
		}
		
		GeometryPatternEngine()
		{
//			Log.d(WALLPAPER_SERVICE, "create engine");
			final Paint paint = mPaint;
			paint.setColor(0xffffffff);
			paint.setAntiAlias(true);
			paint.setStrokeWidth(2);
			paint.setStrokeCap(Paint.Cap.ROUND);
			paint.setStyle(Paint.Style.STROKE);
			cyclePercentage = 0;
			expanding = false;
			expansionCount = 0;

			preferences = TorquePaper.this.getSharedPreferences(SHARED_PREFS_NAME, 0);
			preferences.registerOnSharedPreferenceChangeListener(this);
			onSharedPreferenceChanged(preferences, null);
	
		}

		public void onSharedPreferenceChanged(SharedPreferences prefs,
				String key)
		{
			Resources res = getResources();
//			System.out.println("Preferences changed");
			pattern = prefs.getString("torquepaper_pattern", 
					res.getStringArray(R.array.torquepaper_pattern_names)[1]);
			size = prefs.getString("torquepaper_size", res.getStringArray(R.array.torquepaper_sizes)[0]);
			primaryColour = prefs.getInt("primary_colour", res.getInteger(R.integer.COLOR_BLUE));
			secondaryColour = prefs.getInt("secondary_colour", res.getInteger(R.integer.COLOR_BLUE_2));
			tertiaryColour = prefs.getInt("tertiary_colour", res.getInteger(R.integer.COLOR_BLUE_3));
			transparency = 255 - (prefs.getInt("transparency", 40) * 255 / 100);
			alpha = transparency << 24;
			rotateColours = prefs.getBoolean("torquepaper_rotatecolours", false);
			
			// set transparency which is the alpha part (0x AA RR GG BB) of the color integer
			primaryColour &= 0x00FFFFFF ;
			secondaryColour &= 0x00FFFFFF;
			tertiaryColour&= 0x00FFFFFF;
			
			primaryColour += alpha;
			secondaryColour += alpha;
			tertiaryColour += alpha;
		}

		@Override
		public void onCreate(SurfaceHolder surfaceHolder)
		{
			super.onCreate(surfaceHolder);
			setTouchEventsEnabled(true);
		}

		@Override
		public void onDestroy()
		{
			inDestroy = true;
			super.onDestroy();
//			Log.d(WALLPAPER_SERVICE, "destroy");
			handler.removeCallbacks(drawPatternRunnable);
		}

		@Override
		public void onVisibilityChanged(boolean visible)
		{
//			Log.d(WALLPAPER_SERVICE, "visibility changed");
			mVisible = visible;
			if (visible)
			{
				drawFrame();
			}
			else
			{
				handler.removeCallbacks(drawPatternRunnable);
			}
		}

		@Override
		public void onSurfaceChanged(SurfaceHolder holder, int format,
				int width, int height)
		{
			super.onSurfaceChanged(holder, format, width, height);
//			Log.d(WALLPAPER_SERVICE, "surface changed");
			initFrameParams();
			drawFrame();
		}

		@Override
		public void onSurfaceCreated(SurfaceHolder holder)
		{
			super.onSurfaceCreated(holder);
//			Log.d(WALLPAPER_SERVICE, "surface created");
		}

		@Override
		public void onSurfaceDestroyed(SurfaceHolder holder)
		{
			super.onSurfaceDestroyed(holder);
//			Log.d(WALLPAPER_SERVICE, "surface destroyed");
			mVisible = false;
			handler.removeCallbacks(drawPatternRunnable);
		}

		@Override
		public void onOffsetsChanged(float xOffset, float yOffset, float xStep,
				float yStep, int xPixels, int yPixels)
		{
			drawFrame();
		}

		@Override
		public void onTouchEvent(MotionEvent event)
		{
			if (event.getAction() == MotionEvent.ACTION_DOWN)
			{
				touchX = event.getX();
				touchY = event.getY();
				touchCount = 0;
			}
			super.onTouchEvent(event);
		}

		void drawFrame()
		{
			if (inDestroy)  {
//				Log.d(WALLPAPER_SERVICE, "don't draw - in destroy!");
				return;
			}
			final SurfaceHolder holder = getSurfaceHolder();

			Canvas c = null;
			try
			{
				c = holder.lockCanvas();
				if (c != null)
				{
					drawPattern(c);
				}
			}
			finally
			{
				if (c != null && ! inDestroy)
						holder.unlockCanvasAndPost(c);
			}

			handler.removeCallbacks(drawPatternRunnable);
			if (mVisible)
			{
				handler.postDelayed(drawPatternRunnable, 750);
			}
		}

		void drawPattern(Canvas canvas) {
			canvas.save();
			canvas.drawColor(0xff000000);
			frameCount++;
			cyclePercentage = (frameCount % 50) / 50.0f;

			maxFrameCount = rectFrame.right;
			if (frameCount > maxFrameCount) frameCount = 0;
			
			// set radius and innerCircleRatio based on preferences and rfameCount
			int polygonRadius;
			Resources res = getResources();
			String[] sizes = res.getStringArray(R.array.torquepaper_sizes);
			if (size.equals(sizes[2])) {
				polygonRadius = (int) (rectFrame.width() / 2.0);
			} else if (size.equals( sizes[1]))  {
				polygonRadius = (int) (rectFrame.width() / 3.0);
			} else {
				polygonRadius = (int) (rectFrame.width() / 5.0);
			}
			
			if (expanding) 	{
				expansionCount ++;
				if (expansionCount > 19) expanding = ! expanding;
			}
			else {
				expansionCount--;
				if (expansionCount < 0)  expanding = ! expanding;
			}
			
			double innerCircleRatioDecagon = 0.3, innerCircleRatioPentagon = 0.2, innerCircleRatioHexagon = 0.2;
			innerCircleRatioDecagon += expansionCount/20.0 * 0.4;
			innerCircleRatioPentagon += expansionCount/20.0 * 0.5;
			innerCircleRatioHexagon += expansionCount/20.0 * 0.5 ;
			
			double innerCircleRatioOctagon = 0.3, innerCircleRatioSquare= 0.2;
			innerCircleRatioOctagon += expansionCount/20.0 * 0.4;
			innerCircleRatioSquare += expansionCount/20.0 * 0.5;
			
			// move image 
			int offset = (frameCount % (polygonRadius / 2)) * 2;
			Point topLeft = new Point(-polygonRadius + offset, -polygonRadius + offset);
			Point bottomRight = new Point(rectFrame.width() + offset, rectFrame.height() + offset);
			
			if (rotateColours) {
				primaryColour = rotateColour();
				secondaryColour = rotateColour();
				tertiaryColour = rotateColour();
			}
			
			// set up theme
			IDisplayProperties[] displayProperties = new IDisplayProperties[3]; 
			// dodecagon
			displayProperties[0] = new DisplayProperties(primaryColour, Color.argb(75, 0 , 80, 0),  2);
			// pentagon
			displayProperties[1] = new DisplayProperties(secondaryColour, Color.argb(75, 0 , 80, 0),  2);
			// hexagon
			displayProperties[2] = new DisplayProperties(tertiaryColour, Color.argb(75, 0 , 80, 0),  2);
			ITheme theme = new Theme(displayProperties, (int) touchX, (int) touchY, cyclePercentage);
			
			List<Polygon> polygons;
			if (pattern.equals(res.getStringArray(R.array.torquepaper_pattern_names)[0])) {
				polygons = PolygonLayout.createOctagonalPolygonsWithSquares(topLeft, bottomRight, polygonRadius,
																																						theme, innerCircleRatioOctagon,
																																						innerCircleRatioSquare);
			}
			else {
			 polygons = PolygonLayout.createDecagonalPolygonsWithPentagons(topLeft, bottomRight, polygonRadius,
					 										innerCircleRatioDecagon, innerCircleRatioPentagon, innerCircleRatioHexagon,
					 										theme);
			}
			
			Polygon nearestPolygon = null;
			if (touchX != -1) {
				touchCount++;
				if (touchCount > 10) {
					touchCount = 0;
					touchX = -1;
					touchY = -1;
				}
				double nearestDistance =1e6;
				for (Polygon polygon : polygons) {
					Point centre = polygon.getCentre();
					double distance = FloatMath.sqrt((centre.x - touchX) * (centre.x - touchX)  + 
																					(centre.y - touchY) * (centre.y - touchY));
					if (distance < nearestDistance) {
						nearestDistance = distance;
						nearestPolygon = polygon;
					}
				}
			}
			
			// draw polygons
			for (Polygon polygon : polygons) {
//				polygon.draw(canvas);
//				polygon.drawPoints(canvas);
//				polygon.drawLines(canvas);				
				if (touchX != -1 && polygon == nearestPolygon) {
					IDisplayProperties displayProperties1 = polygon.getDisplayProperties();
					displayProperties1.setKaleidoscope(true);
					displayProperties1.setTouchCount(touchCount);
				}
				polygon.fillPolygons(canvas);
			}
			canvas.restore();
		}

		void initFrameParams()
		{
			DisplayMetrics metrics = new DisplayMetrics();
			Display display = ((WindowManager) getSystemService(WINDOW_SERVICE)).getDefaultDisplay();
			display.getMetrics(metrics);

			rectFrame = new Rect(0, 0, metrics.widthPixels, metrics.heightPixels);
		}
	}
}