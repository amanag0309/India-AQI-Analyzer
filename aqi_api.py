import requests
import pandas as pd
from datetime import datetime
import pytz

def fetch_aqi_history(lat, lon, past_days=7):
    """
    Fetches hourly AQI data from Open-Meteo.
    Returns a DataFrame with 'time' index and pollutant columns.
    Filters out future timestamps.
    """
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    
    # We ask for past_days + forecast (default 0 forecast days usually, but API gives some)
    # We will filter strictly by current time.
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,ozone,sulphur_dioxide",
        "timezone": "Asia/Kolkata",
        "past_days": past_days
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        hourly = data.get("hourly", {})
        if not hourly or "time" not in hourly:
            return pd.DataFrame()

        df = pd.DataFrame(hourly)
        df['time'] = pd.to_datetime(df['time'])
        
        # Filter out future dates
        # Open-Meteo returns local time string, we parsed it.
        # We compare against naive local now or aware now depending on parsing.
        # pd.to_datetime usually creates naive timestamps if no utc=True.
        # We'll assume naive local time (IST) as requested by timezone param.
        
        now = datetime.now()
        df = df[df['time'] <= now]
        
        # Set index
        df.set_index('time', inplace=True)
        df.sort_index(inplace=True)
        
        # Rename columns to match our internal standard if needed, 
        # but Open-Meteo names are good: pm2_5, pm10, carbon_monoxide, etc.
        # Let's map them to shorter names for convenience
        rename_map = {
            "carbon_monoxide": "co",
            "nitrogen_dioxide": "no2",
            "sulphur_dioxide": "so2",
            "ozone": "o3"
        }
        df.rename(columns=rename_map, inplace=True)
        
        return df

    except Exception as e:
        print(f"API Error: {e}")
        return pd.DataFrame()
