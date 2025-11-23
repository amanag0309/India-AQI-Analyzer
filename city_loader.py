import pandas as pd
import os

_cities_df = None

def load_cities(file_path="India_Cities.csv"):
    """
    Loads city data from a CSV file.
    """
    global _cities_df
    if _cities_df is not None:
        return _cities_df

    if not os.path.exists(file_path):
        # Fallback empty DF if file missing
        return pd.DataFrame(columns=['city', 'lat', 'lon'])
    
    try:
        df = pd.read_csv(file_path)
        # Ensure columns exist
        required = ['city', 'lat', 'lon']
        if not all(col in df.columns for col in required):
            return pd.DataFrame(columns=required)
        
        # Clean data
        df['city'] = df['city'].astype(str).str.strip()
        
        _cities_df = df
        return df
    except Exception:
        return pd.DataFrame(columns=['city', 'lat', 'lon'])

def get_all_cities():
    df = load_cities()
    if df.empty: return []
    return sorted(df['city'].unique().tolist())

def get_coords(city_name):
    df = load_cities()
    if df.empty: return None, None
    row = df[df['city'] == city_name]
    if row.empty: return None, None
    return row.iloc[0]['lat'], row.iloc[0]['lon']
