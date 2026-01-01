import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta

# Local modules
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

# --- Custom CSS (Dark Theme) ---
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Hide Streamlit Toolbar and GitHub Button */
    .stAppDeployButton {display:none;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    footer {visibility: hidden !important;}

    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #021a1a;
        border-right: 1px solid #1E2D2D;
    }
    
    /* Card Container */
    .metric-card {
        background-color: #061E1E;
        border: 1px solid #1E2D2D;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Typography */
    h1, h2, h3, h4, p, span {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 {
        color: #FAFAFA !important;
    }
    
    .big-aqi {
        font-size: 4rem;
        font-weight: 800;
        margin: 0;
    }
    .aqi-label {
        font-size: 1.2rem;
        font-weight: 500;
    }
    
    /* Progress Bars */
    .stProgress > div > div > div > div {
        background-color: #00B050;
    }
    
    /* Inputs */
    .stSelectbox > div > div {
        background-color: #061E1E !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Init ---
if 'selected_city' not in st.session_state:
    st.session_state['selected_city'] = "New Delhi"

# --- Header with LinkedIn Icon ---
st.markdown(
    f'''
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 20px;">
        <h1 style="margin:0; font-size: 2.5rem;">India AQI Analyzer 🇮🇳</h1>
        <a href="{LINKEDIN_URL}" target="_blank" style="text-decoration:none;">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg"
                 alt="LinkedIn"
                 style="width:32px;height:32px;">
        </a>
    </div>
    ''',
    unsafe_allow_html=True
)

# --- Sidebar ---
st.sidebar.title("AQI Monitor")


# City Selection
cities = get_all_cities()
if st.session_state['selected_city'] in cities:
    default_city_idx = cities.index(st.session_state['selected_city'])
else:
    default_city_idx = 0

selected_city = st.sidebar.selectbox(
    "Select City", 
    cities, 
    index=default_city_idx
)

# Update Session State
st.session_state['selected_city'] = selected_city

st.sidebar.button("+ Add Location") # Mock button

# --- Data Fetching ---
lat, lon = get_coords(selected_city)
if lat is None:
    st.error("City coordinates not found.")
    st.stop()

df = fetch_aqi_history(lat, lon)

if df is None or df.empty:
    st.error("No data available for this location.")
    st.stop()



# Latest Data (from OpenWeather history)
latest_row = df.iloc[-1]

current_pm25 = safe_value(latest_row.get('pm2_5'))

current_pm10 = safe_value(latest_row.get('pm10'))
current_no2  = safe_value(latest_row.get('no2'))
current_o3   = safe_value(latest_row.get('o3'))
current_so2  = safe_value(latest_row.get('so2'))
current_co   = safe_value(latest_row.get('co'))

category = get_aqi_category(current_pm25)
color = get_aqi_color(category)



# --- Layout ---
col_left, col_right = st.columns([1, 2.5])

# --- Left Column ---
with col_left:
    # Gauge Chart
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = current_pm25,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "PM2.5 AQI", 'font': {'color': 'white', 'size': 20}},
        number = {'font': {'color': color}},
        gauge = {
            'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "#1E2D2D",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50], 'color': "#00B050"},
                {'range': [50, 100], 'color': "#92D050"},
                {'range': [100, 200], 'color': "#FFFF00"},
                {'range': [200, 300], 'color': "#FF9900"},
                {'range': [300, 400], 'color': "#FF0000"},
                {'range': [400, 500], 'color': "#C00000"}
            ],
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=250,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown(f'<p style="text-align: center; color: {color}; font-weight: bold; margin-top: -20px;">{category}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Pollutants Grid
    st.markdown("### Pollutant Breakdown")
    
    # CSS for Pollutant Cards
    st.markdown("""
    <style>
        .pollutant-card {
            background-color: #161b22;
            border-radius: 8px;
            padding: 15px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
            border: 1px solid #30363d;
            position: relative;
            overflow: hidden;
        }
        .pollutant-card::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background-color: var(--card-color);
        }
        .pollutant-info {
            display: flex;
            flex-direction: column;
        }
        .pollutant-label {
            color: #8b949e;
            font-size: 0.85rem;
            font-weight: 500;
        }
        .pollutant-value {
            color: #f0f6fc;
            font-size: 1.5rem;
            font-weight: 700;
        }
        .pollutant-unit {
            color: #8b949e;
            font-size: 0.75rem;
            margin-left: 4px;
        }
        .pollutant-icon {
            font-size: 1.5rem;
            opacity: 0.7;
        }
    </style>
    """, unsafe_allow_html=True)

    def pollutant_card(label, value, unit, max_val):
        val_safe = safe_value(value)
        # Determine color
        pct = min(val_safe / max_val, 1.0) * 100
        if pct < 20: color = "#00B050"      # Good
        elif pct < 40: color = "#92D050"    # Satisfactory
        elif pct < 60: color = "#FFFF00"    # Moderate
        elif pct < 80: color = "#FF9900"    # Poor
        elif pct < 90: color = "#FF0000"    # Very Poor
        else: color = "#C00000"             # Severe
        
        return f"""
        <div class="pollutant-card" style="--card-color: {color};">
            <div class="pollutant-info">
                <span class="pollutant-label">{label}</span>
                <div>
                    <span class="pollutant-value">{int(val_safe)}</span>
                    <span class="pollutant-unit">{unit}</span>
                </div>
            </div>
            <div class="pollutant-icon" style="color: {color};">
                ☁️
            </div>
        </div>
        """

    # Grid Layout
    pc1, pc2 = st.columns(2)
    
    with pc1:
        st.markdown(pollutant_card("Particulate Matter (PM2.5)", current_pm25, "µg/m³", 250), unsafe_allow_html=True)
        st.markdown(pollutant_card("Sulfur Dioxide (SO2)", current_so2, "ppb", 200), unsafe_allow_html=True)
        st.markdown(pollutant_card("Ozone (O3)", current_o3, "ppb", 180), unsafe_allow_html=True)
        
    with pc2:
        st.markdown(pollutant_card("Particulate Matter (PM10)", current_pm10, "µg/m³", 400), unsafe_allow_html=True)
        st.markdown(pollutant_card("Nitrogen Dioxide (NO2)", current_no2, "ppb", 200), unsafe_allow_html=True)
        st.markdown(pollutant_card("Carbon Monoxide (CO)", current_co, "ppb", 4000), unsafe_allow_html=True)

# --- Right Column ---
with col_right:
    # Header
    c_head1, c_head2 = st.columns([3, 1])
    with c_head1:
        st.markdown(f"## AQI for {selected_city}")
    with c_head2:
        range_opt = st.selectbox("Range", ["24 Hours", "7 Days", "Last 5 Days"], label_visibility="collapsed")
    
    # Chart Logic
    if range_opt == "24 Hours":
        plot_df = df.tail(24)
    elif range_opt == "7 Days":
        plot_df = df.tail(24 * 5)  # OpenWeather free tier (max 5 days)
    else:
        plot_df = df


    
    # Dynamic Color for Chart
    max_val = plot_df['pm2_5'].max()
    chart_color = get_aqi_color(get_aqi_category(max_val))
        
    # Trend Chart (PM2.5)
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("#### PM2.5 Trend")
    
    fig = px.area(plot_df, x=plot_df.index, y='pm2_5', 
                  template="plotly_dark",
                  color_discrete_sequence=[chart_color])
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        height=280,
        xaxis_title="",
        yaxis_title="PM2.5",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Multi-Pollutant Chart
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("#### Multi-Pollutant Comparison")
    
    fig_multi = go.Figure()
    fig_multi.add_trace(go.Scatter(x=plot_df.index, y=plot_df['pm2_5'], mode='lines', name='PM2.5', line=dict(color='#FF9900')))
    fig_multi.add_trace(go.Scatter(x=plot_df.index, y=plot_df['pm10'], mode='lines', name='PM10', line=dict(color='#FFFF00')))
    fig_multi.add_trace(go.Scatter(x=plot_df.index, y=plot_df['no2'], mode='lines', name='NO2', line=dict(color='#00B050')))
    
    fig_multi.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        height=280,
        xaxis_title="",
        yaxis_title="Concentration (µg/m³)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_multi, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bottom Cards
    bc1, bc2, bc3 = st.columns(3)
    
    # 24h Avg
    last_24h = df.tail(24)
    avg_24h = safe_value(last_24h['pm2_5'].mean())
    
    # Previous 24h (for comparison)
    if len(df) >= 48:
        prev_24h = df.iloc[-48:-24]['pm2_5'].mean()
        diff = avg_24h - safe_value(prev_24h)
        diff_str = f"{diff:+.1f}"
    else:
        diff_str = "-"

    with bc1:
        st.markdown(f"""
        <div class="metric-card">
            <p style="color: #888; font-size: 0.8rem; margin:0;">🕒 24h Average</p>
            <h2 style="margin: 5px 0;">{int(avg_24h)}</h2>
            <p style="color: #ccc; font-size: 0.8rem; margin:0;">vs prev: {diff_str}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with bc2:
        peak_val = safe_value(last_24h['pm2_5'].max())
        st.markdown(f"""
        <div class="metric-card">
            <p style="color: #888; font-size: 0.8rem; margin:0;">📈 Peak (24h)</p>
            <h2 style="margin: 5px 0;">{int(peak_val)}</h2>
            <p style="color: #FF7F50; margin:0;">PM2.5</p>
        </div>
        """, unsafe_allow_html=True)
        
    with bc3:
        rec = health_recommendation(current_pm25)
        st.markdown(f"""
        <div class="metric-card">
            <p style="color: #888; font-size: 0.8rem; margin:0;">🛡️ Recommendation</p>
            <p style="font-size: 0.85rem; margin-top: 5px; line-height: 1.4;">{rec}</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")

