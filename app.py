import pandas as pd
import time
from city_loader import load_cities
from aqi_api import fetch_aqi_history
from utils import get_aqi_category, safe_value

def main():
    print("Loading cities...")
    cities_df = load_cities()
    
    if cities_df.empty:
        print("No cities found. Exiting.")
        return

    print(f"Found {len(cities_df)} cities. Fetching AQI data...")
    
    results = []
    
    for index, row in cities_df.iterrows():
        city = row['city']
        lat = row['lat']
        lon = row['lon']
        
        print(f"Fetching data for {city}...", end="\r")
        
        # Fetch just 1 day to get latest
        df = fetch_aqi_history(lat, lon, past_days=1)
        
        if not df.empty:
            latest = df.iloc[-1]
            pm25 = safe_value(latest.get('pm2_5'))
            
            record = {
                'city': city,
                'lat': lat,
                'lon': lon,
                'timestamp': latest.name,
                'pm2_5': pm25,
                'pm10': safe_value(latest.get('pm10')),
                'no2': safe_value(latest.get('no2')),
                'o3': safe_value(latest.get('o3')),
                'so2': safe_value(latest.get('so2')),
                'co': safe_value(latest.get('co')),
                'aqi_category': get_aqi_category(pm25)
            }
            results.append(record)
        
        # Respect API rate limits
        time.sleep(0.2)

    print("\nData fetching complete.")
    
    if not results:
        print("No data fetched.")
        return

    results_df = pd.DataFrame(results)
    
    output_file = "India_All_Cities_AQI.csv"
    results_df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")
    
    # Analysis
    print("\n--- Top 10 Most Polluted Cities (by PM2.5) ---")
    top_polluted = results_df.sort_values(by='pm2_5', ascending=False).head(10)
    print(top_polluted[['city', 'pm2_5', 'aqi_category']].to_string(index=False))
    
    print("\n--- Top 10 Cleanest Cities (by PM2.5) ---")
    top_cleanest = results_df.sort_values(by='pm2_5', ascending=True).head(10)
    print(top_cleanest[['city', 'pm2_5', 'aqi_category']].to_string(index=False))

if __name__ == "__main__":
    main()
