import math

def safe_value(x, default=0.0):
    """
    Safely converts a value to float. Returns default if None or NaN.
    """
    if x is None:
        return default
    try:
        val = float(x)
        if math.isnan(val):
            return default
        return val
    except (ValueError, TypeError):
        return default

def get_aqi_category(pm25):
    """
    Determines the AQI category based on PM2.5 concentration.
    """
    val = safe_value(pm25, default=-1)
    
    if val < 0: return "Unknown"
    if val <= 30: return "Good"
    if val <= 60: return "Satisfactory"
    if val <= 90: return "Moderate"
    if val <= 120: return "Poor"
    if val <= 250: return "Very Poor"
    return "Severe"

def get_aqi_color(category):
    """
    Returns a color code for the AQI category.
    """
    colors = {
        "Good": "#00B050",          # Green
        "Satisfactory": "#92D050",  # Light Green
        "Moderate": "#FFFF00",      # Yellow
        "Poor": "#FF9900",          # Orange
        "Very Poor": "#FF0000",     # Red
        "Severe": "#C00000",        # Dark Red
        "Unknown": "#808080"        # Grey
    }
    return colors.get(category, "#808080")

def health_recommendation(pm25):
    """
    Returns health recommendation based on PM2.5.
    """
    val = safe_value(pm25, default=-1)
    if val < 0: return "No data available."
    
    if val <= 30: return "Air quality is good. Enjoy your outdoor activities!"
    if val <= 60: return "Air quality is acceptable. Sensitive groups should consider reducing heavy exertion."
    if val <= 90: return "Members of sensitive groups may experience health effects. The general public is not likely to be affected."
    if val <= 120: return "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."
    if val <= 250: return "Health warnings of emergency conditions. The entire population is more likely to be affected."
    return "Health alert: everyone may experience more serious health effects. Avoid all outdoor exertion."
