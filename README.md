# 🇮🇳 India AQI Analyzer  
A real-time Air Quality Index (AQI) monitoring dashboard for Indian cities, built using **Python**, **Streamlit**, **Plotly**, and the **Open-Meteo Air Quality API** (no API key required).

This project provides clean, interactive visualizations that help users explore pollution levels, track trends, and understand the health impact of air quality across India.

---

## 🚀 Features

- 🔴 **Real-time AQI data** for PM2.5, PM10, NO₂, SO₂, CO, and O₃  
- 🌆 **Search any Indian city** and view instant AQI analysis  
- 📊 **Interactive Plotly charts** for 24-hour, 7-day, and 30-day trends  
- 🟩 **Color-coded AQI categories** with a modern dark theme  
- 🧠 **Health recommendations** based on AQI  
- 📁 **Bulk data processing** using the built-in CLI tool  
- 🌐 **No API key required** — uses Open-Meteo’s free public API.

---

## 🧰 Tech Stack

- Python  
- Streamlit  
- Plotly  
- Pandas  
- Open-Meteo Air Quality API  

---

## Project Structure
```
India_AQI_Analyzer/
├── aqi_api.py             # API integration module
├── city_loader.py         # City data loader
├── utils.py               # Helper functions (AQI logic)
├── app.py                 # CLI application
├── dashboard.py           # Streamlit dashboard
├── India_Cities.csv       # Input dataset
├── India_All_Cities_AQI.csv # Output dataset (generated)
└── README.md              # Documentation
```

## Installation

Install dependencies:
   ```bash
   pip install pandas requests streamlit plotly
   ```

## Usage

### 1. CLI Mode (Batch Processing)
Run the script to fetch data for all cities and generate the report.
```bash
python app.py
```
- This will create `India_All_Cities_AQI.csv`.
- It will also print the Top 10 Most Polluted and Cleanest cities to the console.

### 2. Dashboard Mode (Interactive UI)
Launch the Streamlit dashboard.
```bash
streamlit run dashboard.py
```
- View real-time data for specific cities.
- Compare cities using interactive charts.
- View the full dataset.

## API Used
- **Open-Meteo Air Quality API**: [https://open-meteo.com/en/docs/air-quality-api](https://open-meteo.com/en/docs/air-quality-api)
- No API key required for non-commercial use.

## ✨ Author & Maintainer

**Aman Agarwal**  
[🔗 LinkedIn Profile](https://www.linkedin.com/in/aman-agarwal0309/)


## License
Open Source.
