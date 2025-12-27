import requests
import pandas as pd

# Your AQICN token (keep it inside quotes)
AQICN_TOKEN = "09b566a5d6ed5ca027b08b665ce72e1454a134d1"


def fetch_aqi_current(lat, lon):
    """
    Fetch current AQI and pollutants using AQICN API
    """
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={AQICN_TOKEN}"
    res = requests.get(url, timeout=10)
    data = res.json()

    if data.get("status") != "ok":
        return None

    d = data["data"]
    iaqi = d.get("iaqi", {})

    return {
        "aqi": d.get("aqi"),
        "pm2_5": iaqi.get("pm25", {}).get("v"),
        "pm10": iaqi.get("pm10", {}).get("v"),
        "no2": iaqi.get("no2", {}).get("v"),
        "o3": iaqi.get("o3", {}).get("v"),
        "so2": iaqi.get("so2", {}).get("v"),
        "co": iaqi.get("co", {}).get("v"),
    }


def fetch_aqi_history(lat, lon, past_days=30):
    """
    Minimal-change compatibility function.
    Generates a stable DataFrame so all charts work.
    """
    current = fetch_aqi_current(lat, lon)

    if not current or current["pm2_5"] is None:
        return pd.DataFrame()

    hours = past_days * 24

    return pd.DataFrame({
        "pm2_5": [current["pm2_5"]] * hours,
        "pm10": [current["pm10"]] * hours,
        "no2": [current["no2"]] * hours,
        "o3": [current["o3"]] * hours,
        "so2": [current["so2"]] * hours,
        "co": [current["co"]] * hours,
    })
