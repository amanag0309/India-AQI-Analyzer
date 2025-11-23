import requests
import pandas as pd
import time
import os

def fetch_cities_overpass():
    """
    Fetches cities, towns, and major localities in India using the Overpass API.
    """
    # Overpass Query
    # We query for nodes with place tags in the area of India (ID 3600304716)
    # We include: city, town, municipality, municipal_corporation
    query = """
    [out:json][timeout:180];
    area["ISO3166-1"="IN"]->.searchArea;
    (
      node["place"~"city|town|municipality|municipal_corporation"](area.searchArea);
      node["admin_level"="8"](area.searchArea); 
    );
    out body;
    """
    
    url = "https://overpass-api.de/api/interpreter"
    
    print("Fetching data from Overpass API... (This may take a few seconds)")
    try:
        response = requests.post(url, data={'data': query})
        response.raise_for_status()
        data = response.json()
        
        elements = data.get('elements', [])
        print(f"Received {len(elements)} raw elements.")
        
        cities = []
        for el in elements:
            tags = el.get('tags', {})
            name = tags.get('name')
            if not name:
                continue
                
            cities.append({
                'city': name,
                'lat': el.get('lat'),
                'lon': el.get('lon')
            })
            
        df = pd.DataFrame(cities)
        
        # Clean up
        df.drop_duplicates(subset=['city'], inplace=True)
        
        # Filter out non-English names if possible (optional, but good for consistency)
        # For now, just basic cleaning
        df['city'] = df['city'].str.strip()
        
        return df
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def main():
    df = fetch_cities_overpass()
    
    if df.empty:
        print("No cities found or API error.")
        return
        
    print(f"Processed {len(df)} unique cities.")
    
    # Save
    output_file = "India_Cities.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved to {output_file}")
    
    # Preview
    print(df.head())
    print(f"Total Count: {len(df)}")

if __name__ == "__main__":
    main()
