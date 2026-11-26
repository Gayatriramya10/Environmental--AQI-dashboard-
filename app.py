import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Environmental AQI Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Environmental AQI Dashboard")
st.subheader("Air Quality Monitoring and Prediction")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("aqi_sample_dataset_1000_records.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# Sidebar
st.sidebar.title("Dashboard Filters")

cities = ["All Cities"] + sorted(df["City"].unique().tolist())
selected_city = st.sidebar.selectbox("Select City", cities)

if selected_city == "All Cities":
    data = df.copy()
else:
    data = df[df["City"] == selected_city].copy()

# AQI Overview
st.header("📊 AQI Overview")

c1, c2, c3 = st.columns(3)

c1.metric("Average AQI", round(data["AQI"].mean(), 1))
c2.metric("Maximum AQI", int(data["AQI"].max()))
c3.metric("Minimum AQI", int(data["AQI"].min()))

# AQI Category
st.subheader("Air Quality Status")

def get_status(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    return "Severe"

average_aqi = data["AQI"].mean()
st.info("Current dataset average status: " + get_status(average_aqi))

# City Comparison
st.header("🏙️ City-wise AQI Comparison")

city_aqi = df.groupby("City")["AQI"].mean()
st.bar_chart(city_aqi)

# Pollutant Analysis
st.header("🧪 Pollutant Analysis")

pollutant = st.selectbox(
    "Select Pollutant",
    ["PM2.5 (µg/m³)", "PM10 (µg/m³)",
     "NO2 (µg/m³)", "SO2 (µg/m³)",
     "CO (mg/m³)", "O3 (µg/m³)"]
)

trend = data.sort_values("Date").set_index("Date")
st.line_chart(trend[pollutant])

# AQI Trend
st.header("📈 AQI Trend")

st.line_chart(
    data.sort_values("Date").set_index("Date")["AQI"]
)

# Simple Future Prediction
st.header("🔮 Future AQI Prediction")

if selected_city == "All Cities":
    st.warning("Select one city to view its estimated future AQI.")
else:
    prediction_days = st.slider(
        "Prediction days", 1, 7, 3
    )

    city_data = data.sort_values("Date")
    x = np.arange(len(city_data))
    y = city_data["AQI"].values

    slope, intercept = np.polyfit(x, y, 1)

    future_x = np.arange(
        len(city_data),
        len(city_data) + prediction_days
    )

    predictions = np.clip(
        slope * future_x + intercept, 0, 500
    )

    prediction_df = pd.DataFrame({
        "Day": [f"Day {i+1}" for i in range(prediction_days)],
        "Estimated AQI": np.round(predictions, 1)
    })

    st.dataframe(prediction_df, use_container_width=True)

    st.caption(
        "Demo trend-based estimates using sample data. "
        "These are not official AQI forecasts."
    )

# Dataset
st.header("📁 Dataset Preview")
st.dataframe(data.head(20), use_container_width=True)

st.caption(
    "Note: This project uses synthetic sample data "
    "for demonstration and educational purposes."
)

st.success("Environmental AQI Dashboard loaded successfully!")
                     
