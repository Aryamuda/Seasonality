import streamlit as st
import os
from PIL import Image

# Define the base directory
base_dir = "/home/arya/project/Seasonality"

# List of currency pairs
currency_pairs = ["AUDUSD", "EURUSD", "GBPJPY", "GBPUSD", "NZDUSD", "USDCAD", "USDJPY", "XAUUSD"]

# Sidebar: Choose Seasonality Type
seasonality_type = st.sidebar.radio("Select Analysis Type", ["Monthly Seasonality", "Daily Seasonality"])

# 📅 **Monthly Seasonality Page**
if seasonality_type == "Monthly Seasonality":
    st.title("📊 Monthly Seasonality Overview")

    # Display Monthly Seasonality for All Pairs (1 row = 1 image)
    for pair in currency_pairs:
        monthly_seasonality_file = os.path.join(base_dir, pair, f"{pair}_monthly_seasonality.png")
        if os.path.exists(monthly_seasonality_file):
            st.image(Image.open(monthly_seasonality_file), caption=f"{pair} Monthly Seasonality", use_container_width=True)
            st.markdown("---")  # Add a separator between images

# 📈 **Daily Seasonality Page**
else:
    st.title("📅 Daily Seasonality Analysis")

    # Dropdown to select currency pair
    selected_pair = st.selectbox("Choose a currency pair:", currency_pairs)

    st.subheader(f"{selected_pair} Bullish Probabilities by Month")

    pair_dir = os.path.join(base_dir, selected_pair)

    if os.path.exists(pair_dir):
        for month in range(1, 13):
            file_path = os.path.join(pair_dir, f"{selected_pair} bullish_probability_month_{month}.png")
            if os.path.exists(file_path):
                st.image(Image.open(file_path), caption=f"{selected_pair} - Month {month}", use_container_width=True)
                st.markdown("---")  # Add separator for better spacing
