import os
import requests
import pandas as pd
from datetime import datetime

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not OPENWEATHER_API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY not set")


def fetch_aqi_history(lat, lon, past_days=5):
    """
    Fetch real hourly air pollution data (geo-based)
    Free tier supports up to 5 days
    """
    end = int(datetime.utcnow().timestamp())
    start = end - past_days * 24 * 3600

    url = (
        "https://api.openweathermap.org/data/2.5/air_pollution/history"
        f"?lat={lat}&lon={lon}&start={start}&end={end}&appid={OPENWEATHER_API_KEY}"
    )

    res = requests.get(url, timeout=10).json()

    if "list" not in res:
        return pd.DataFrame()

    rows = []
    for item in res["list"]:
        c = item["components"]
        rows.append({
            "timestamp": datetime.utcfromtimestamp(item["dt"]),
            "pm2_5": c.get("pm2_5"),
            "pm10": c.get("pm10"),
            "no2": c.get("no2"),
            "o3": c.get("o3"),
            "so2": c.get("so2"),
            "co": c.get("co"),
        })

    df = pd.DataFrame(rows)
    df = df.set_index("timestamp").sort_index()
    # Normalize to hourly data so charts change with range selection
    df = df.resample("1H").mean().interpolate()
    return df
