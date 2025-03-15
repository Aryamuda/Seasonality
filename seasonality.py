import streamlit as st
from pathlib import Path
from PIL import Image
import requests
from io import BytesIO

# Base directory (gunakan path relatif supaya fleksibel di deployment)
base_dir = Path(__file__).parent / "Seasonality"

# List of currency pairs
currency_pairs = ["AUDUSD", "EURUSD", "GBPJPY", "GBPUSD", "NZDUSD", "USDCAD", "USDJPY", "XAUUSD"]

# Sidebar: Choose Seasonality Type
seasonality_type = st.sidebar.radio("Select Analysis Type", ["Monthly Seasonality", "Daily Seasonality"])

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

# 📅 **Monthly Seasonality Page**
if seasonality_type == "Monthly Seasonality":
    st.title("📊 Monthly Seasonality Overview")

    # Display Monthly Seasonality for All Pairs
    for pair in currency_pairs:
        file_path = base_dir / pair / f"{pair}_monthly_seasonality.png"
        github_url = f"https://raw.githubusercontent.com/Aryamuda/Seasonality/main/Seasonality/{pair}/{pair}_monthly_seasonality.png"
        
        image = load_image(file_path, github_url)
        if image:
            st.image(image, caption=f"{pair} Monthly Seasonality", use_container_width=True)
            st.markdown("---")
        else:
            st.warning(f"⚠️ Image not found: {file_path}")

# 📈 **Daily Seasonality Page**
else:
    st.title("📅 Daily Seasonality Analysis")

    # Dropdown to select currency pair
    selected_pair = st.selectbox("Choose a currency pair:", currency_pairs)
    st.subheader(f"{selected_pair} Bullish Probabilities by Month")

    pair_dir = base_dir / selected_pair

    for month in range(1, 13):
        file_path = pair_dir / f"{selected_pair} bullish_probability_month_{month}.png"
        github_url = f"https://raw.githubusercontent.com/Aryamuda/Seasonality/main/Seasonality/{selected_pair}/{selected_pair} bullish_probability_month_{month}.png"
        
        image = load_image(file_path, github_url)
        if image:
            st.image(image, caption=f"{selected_pair} - Month {month}", use_container_width=True)
            st.markdown("---")
        else:
            st.warning(f"⚠️ Image not found: {file_path}")
