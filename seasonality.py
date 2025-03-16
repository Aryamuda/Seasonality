import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image
import requests
from io import BytesIO

base_dir = Path(__file__).parent / "Seasonality"
excel_path = Path(__file__).parent / "TP_SL_Data.xlsx"

# List of currency pairs
currency_pairs = ["AUDUSD", "EURUSD", "GBPJPY", "GBPUSD", "NZDUSD", "USDCAD", "USDJPY", "XAUUSD"]
months = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

def load_image(file_path, github_url):
    """Load image from local file or GitHub if missing."""
    if file_path.exists():
        return Image.open(file_path)
    else:
        response = requests.get(github_url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            return None

def load_tp_sl_data():
    """Load TP/SL data from GitHub Excel file."""
    github_url = "https://github.com/Aryamuda/Seasonality/raw/main/TP_SL_Data.xlsx"

    try:
        response = requests.get(github_url)
        response.raise_for_status()  # Raise error if request fails
        df = pd.read_excel(BytesIO(response.content), engine="openpyxl")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        return df.dropna(subset=["Date"])  # Drop rows with invalid dates
    except Exception as e:
        st.error(f"Failed to load TP/SL data: {e}")
        return pd.DataFrame(columns=["Date", "Pair", "Probability Up", "Probability Down", "Type"])


# Sidebar
seasonality_type = st.sidebar.radio("Select Analysis Type", ["Monthly Seasonality", "Daily Seasonality", "View by Month"])

# **View by Month Page**
if seasonality_type == "View by Month":
    st.title("View by Month")
    selected_month = st.selectbox("Choose a month:", list(months.keys()))
    month_num = months[selected_month]
    st.subheader(f"Bullish Probabilities for {selected_month}")
    
    tp_sl_data = load_tp_sl_data()
    
    for pair in currency_pairs:
        file_path = base_dir / pair / f"{pair} bullish_probability_month_{month_num}.png"
        github_url = f"https://raw.githubusercontent.com/Aryamuda/Seasonality/main/Seasonality/{pair}/{pair} bullish_probability_month_{month_num}.png"
        
        image = load_image(file_path, github_url)
        if image:
            st.image(image, caption=f"{pair} - {selected_month}", use_container_width=True)
            st.markdown("---")
        else:
            st.warning(f"Image not found: {file_path}")
        
        # Filter TP/SL Data for this month and pair
        filtered_data = tp_sl_data[(tp_sl_data["Date"].dt.month == month_num) & (tp_sl_data["Pair"] == pair)]
        if not filtered_data.empty:
            with st.expander(f"TP/SL for {pair} in {selected_month}"):
                st.table(filtered_data[["Date", "Pair", "Probability Up", "Probability Down", "Type"]])
