import streamlit as st
import pandas as pd
import logging

from fetcher import fetch_hdb_data
from analysis import (
    get_summary_snapshot,
    get_town_ranking,
    get_avg_prices_by_month_and_flat_type
)

logging.basicConfig(level=logging.INFO)

MAX_MONTHS = 5
api_key = st.secrets.get("API_KEY")

# Fetch data
@st.cache_data(ttl=600)  # cache data for 10 minutes to avoid rate limits and improve responsiveness
def load_data():
    df, fetched_months = fetch_hdb_data(MAX_MONTHS, api_key)
    df['resale_price'] = pd.to_numeric(df['resale_price'], errors='coerce')
    return df, fetched_months

try:
    df, fetched_months = load_data()
except Exception:
    st.error("Error fetching data. Please try again later.")
    st.stop()

if df is None or df.empty:
    st.error("No data available. Please try again later.")
    st.stop()

st.title("HDB Resale Analytics")

# Filters
st.subheader("Filters")
months = st.slider(
    "Lookback Period (months)", 
    min_value=1, 
    max_value=5, 
    value=3 
)

months_sorted = sorted(df["month"].unique())

selected_months = months_sorted[-months:]
logging.info(f"Selected months: {selected_months}")
missing_months = set(selected_months) - set(fetched_months)

if missing_months:
    st.warning(
        f"⚠️ Data for the following month(s) could not be fetched and will be excluded from analysis: {', '.join(sorted(missing_months))}"
    )

filtered_df = df[df["month"].isin(selected_months)]

town = st.selectbox("Select Town", ["All"] + sorted(filtered_df['town'].unique()))
flat_type = st.selectbox("Select Flat Type", ["All"] + sorted(filtered_df['flat_type'].unique()))

if town != "All":
    filtered_df = filtered_df[filtered_df["town"] == town]

if flat_type != "All":
    filtered_df = filtered_df[filtered_df["flat_type"] == flat_type]

# --- SUMMARY ---
st.subheader("Summary Snapshot")

start_month = filtered_df['month'].min()
end_month = filtered_df['month'].max()
start_month_fmt = pd.to_datetime(start_month).strftime("%b %Y")
end_month_fmt = pd.to_datetime(end_month).strftime("%b %Y")
st.caption(f"Based on filters and lookback period of {months} months: {start_month_fmt} → {end_month_fmt}")

avg_price, top_txn = get_summary_snapshot(filtered_df)

st.markdown("#### 💰 Highest Transaction")
st.write(
    f"{top_txn['town']} — S${int(top_txn['resale_price']):,} "
    f"({top_txn['flat_type']}, {top_txn['month']})"
)

# --- AVG PRICES ---
st.markdown("#### 🏙️ Average Resale Price by Town")
st.bar_chart(avg_price.set_index("Town"))

st.markdown("#### 🏢 Average Resale Price by Flat Type")
chart_data = get_avg_prices_by_month_and_flat_type(filtered_df)
st.line_chart(chart_data)

# --- RANKING ---
st.markdown("#### 🏆 Top Towns by No. of Transactions")
st.caption("Capped at 5 towns")
ranking = get_town_ranking(filtered_df)
st.bar_chart(ranking)
