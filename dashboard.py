import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from city_loader import get_all_cities, get_coords
from aqi_api import fetch_aqi_history
from utils import safe_value, get_aqi_category, get_aqi_color, health_recommendation

LINKEDIN_URL = "https://www.linkedin.com/in/aman-agarwal0309/"

# --- Page Config ---
st.set_page_config(
    page_title="AQI Monitor",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Global Modern CSS (Dark Theme + Force Sidebar Visible) ---
st.markdown(
    """
    <style>

        /* Dark Background */
        .stApp {
            background-color: #0E1117 !important;
            color: #FAFAFA !important;
        }

        /* Sidebar Always Visible + Modern Dark Look */
        [data-testid="stSidebar"] {
            background-color: #111B1E !important;
            width: 22rem !important;
            transform: translateX(0px) !important;
            visibility: visible !important;
            border-right: 1px solid #203335 !important;
        }

        /* Sidebar Text */
        [data-testid="stSidebar"] * {
            color: #FAFAFA !important;
            font-size: 15px;
        }

        /* Dropdown Styling */
        .stSelectbox>div>div {
            background-color: #0F262A !important;
            color: white !important;
            border-radius: 6px;
        }

        /* Buttons */
        .stButton>button {
            background-color: #0a84ff !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
        }

        /* LinkedIn Icon Position */
        .top-right-icon {
            position: absolute;
            top: 20px;
            right: 35px;
            z-index: 999;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar ---
st.sidebar.title("AQI Monitor")

all_cities = get_all_cities()
selected_city = st.sidebar.selectbox(
    "Select City",
    all_cities,
    index=all_cities.index("New Delhi")
)

st.sidebar.write("---")
st.sidebar.write("Air Quality Analysis Dashboard")

st.session_state['selected_city'] = selected_city

# --- Top LinkedIn Icon ---
st.markdown(
    f"""
    <div class="top-right-icon">
        <a href="{LINKEDIN_URL}" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="32"/>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Main App Title ---
st.markdown("# India AQI Analyzer 🇮🇳")

# --- Fetch AQI Data ---
lat, lon = get_coords(selected_city)
end = datetime.utcnow()
start = end - timedelta(hours=24)

with st.spinner(f"Fetching real-time AQI data for {selected_city}..."):
    df = fetch_aqi_history(lat, lon, past_days=1)

# Clean Data
df['pm2_5'] = df['pm2_5'].apply(safe_value)
current_pm = df['pm2_5'].iloc[-1]
category = get_aqi_category(current_pm)
color = get_aqi_color(current_pm)

# --- Gauge Chart ---
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=current_pm,
    title={'text': "PM2.5 AQI"},
    gauge={
        'axis': {'range': [0, 400]},
        'bar': {'color': color},
        'steps': [
            {'range': [0, 50], 'color': "#2ECC71"},
            {'range': [50, 100], 'color': "#F1C40F"},
            {'range': [100, 200], 'color': "#E67E22"},
            {'range': [200, 400], 'color': "#E74C3C"}
        ]
    }
))
fig_gauge.update_layout(height=350, margin=dict(l=20, r=20))

# --- PM2.5 Trend Chart ---
fig_trend = px.area(
    df,
    x="time",
    y="pm2_5",
    title="PM2.5 Level (Last 24 Hours)",
)
fig_trend.update_traces(line_color='#E67E22')
fig_trend.update_layout(
    height=350,
    plot_bgcolor="#111B1E",
    paper_bgcolor="#0E1117",
    font_color="white",
    margin=dict(l=10, r=10)
)

# --- Layout ---
left, right = st.columns([1, 1])
with left:
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown(f"### Status: **{category}**")

with right:
    st.plotly_chart(fig_trend, use_container_width=True)

# --- Pollutant Breakdown ---
st.markdown("## Pollutant Breakdown")

cols = st.columns(4)
pollutants = ["pm2_5", "pm10", "o3", "no2"]

for i, pollutant in enumerate(pollutants):
    with cols[i]:
        st.metric(
            pollutant.upper(),
            f"{safe_value(df[pollutant].iloc[-1])}"
        )

# --- End of File ---
