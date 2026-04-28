# 🏠 HDB Resale Data Analysis (Singapore)
An interactive data application that analyzes Singapore HDB resale transactions using data directly from [data.gov.sg](https://data.gov.sg/) public API.

Built with **Streamlit**, this app allows users to explore recent market activity through dynamic filtering, summary insights, and visualizations.

## 🌐 Live Demo
Access the app instantly (no installation required):  
[hdb-resale-analytics.streamlit.app](https://hdb-resale-analytics.streamlit.app/)

Explore HDB resale trends, compare flat types, and analyze market activity directly in your browser.

## 🔍 Overview
This project fetches recent HDB resale transaction data from a public API and transforms it into an intuitive, user-friendly interface.

Users can
- Explore resale price trends over recent months
- Compare average prices across flat types
- Analyze transaction activity by town
- Interact with data dynamically through filters

## 🚀 Features
### Interactive Filters
- Adjustable **lookback period** (1–5 months)
- Filter by **town** and **flat type**

### Summary Snapshot
- Dynamic time range display based on selected lookback period
- Highest transaction
- Average resale price by town (bar chart)

### Price Trends by Flat Type
- Line chart showing **average resale price trends** across flat types
- Clean visualization for comparing price movements over time

### Data Handling & Reliability 
- API integration with retry handling for rate limits
- Graceful fallback for partial data scenarios
- Caching by `@st.cache_data` to reduce API load and improve performance

## 🔧 Tech Stack
- Python 3.11+
- Streamlit (UI framework)
- pandas (data processing)
- requests (API calls)

## 📦 Installation
1. Install Python

    Ensure **Python 3.11+** is installed.
    
    You can check your version with `python --version`.

    If you don't have it, download it from [python.org/downloads](https://www.python.org/downloads/).

2. Clone this repository

    ```
    git clone https://github.com/bryancworks/hdb-resale-analytics.git
    
    cd hdb-resale-analytics
    ```

3. Create a virtual environment (recommended)

    ```
    python -m venv venv
    source venv/bin/activate    # macOS/Linux
    venv\Scripts\activate       # Windows
    ```

4. Install dependencies

    ```
    pip install -r requirements.txt
    ```

## 💻 Usage

### Option 1: Use the Live App
Access the deployed application directly:  
[hdb-resale-analytics.streamlit.app](https://hdb-resale-analytics.streamlit.app/)

---

### Option 2: Run locally
```
streamlit run app.py
```
It should open the site automatically, else 

## ⚠️ Notes
- This app is deployed using **Streamlit Community Cloud**
- Data is sourced from a public API and may be subject to:
    - rate limits
    - temporary unavailability
- In such cases, the app will:
    - retry requests
    - gracefully handle incomplete data

## 🎯 Key Highlights
This project demonstrates:
- API integration with real-world constraints (rate limiting)
- Data transformation and aggregation using pandas
- Building interactive data applications with Streamlit
- Designing user-friendly data exploration tools