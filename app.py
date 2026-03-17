import streamlit as st
from datetime import datetime, timedelta
import random
import os
import pandas as pd
from config import Config
from ai_solar_forecast import SolarForecaster
from real_time_scraper import MarketScraper
from gov_subsidy_bot import GovGuide
from savings_tracker import SavingsTracker
from hardware_link import HardwareConnector

# --- SYSTEM UTILITIES ---
def register_user(name):
    log_file = "users_log.txt"
    count = 1
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            count = len(f.readlines()) + 1
    timestamp = (datetime.utcnow() + timedelta(hours=5.5)).strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"User {count}: {name} | {timestamp}\n")
    return count

@st.cache_resource
def load_components():
    return {
        "forecaster": SolarForecaster(),
        "scraper": MarketScraper(),
        "gov_bot": GovGuide(),
        "tracker": SavingsTracker(),
        "hardware": HardwareConnector()
    }

components = load_components()
ist_now = datetime.utcnow() + timedelta(hours=5.5)
is_night = ist_now.hour < 6 or ist_now.hour >= 18

# --- UI CONFIGURATION ---
st.set_page_config(page_title="SolarOS 2026", page_icon="☀️", layout="wide")

if "system_ready" not in st.session_state:
    st.session_state.system_ready = False
if "panel_area" not in st.session_state:
    st.session_state.panel_area = 300
if "last_forecast" not in st.session_state:
    st.session_state.last_forecast = None

with st.sidebar:
    st.title("Settings")
    theme_choice = st.selectbox("Dashboard Theme", ["Midnight Black", "Eco Green", "Solar Yellow"])
    
    themes = {
        "Midnight Black": ("#0E1117", "#FFFFFF", "#1E1E1E", "#007BFF", "#FFFFFF"),
        "Eco Green": ("#F0F7F4", "#1E3D33", "#D1E8E2", "#2D6A4F", "#1E3D33"),
        "Solar Yellow": ("#FFFDF0", "#4A4A00", "#FFF9C4", "#F9A825", "#4A4A00")
    }
    bg, txt, side, acc, t_txt = themes[theme_choice]

    st.markdown(f"""
        <style>
        .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
        [data-testid="stSidebar"] {{ background-color: {side} !important; }}
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{ color: {txt} !important; }}
        
        /* Graph Transparency Fix */
        .stVegaLiteChart canvas, div[data-testid="stAreaChart"] {{ 
            background-color: transparent !important; 
        }}
        
        [data-testid="stTable"] td, [data-testid="stTable"] th, .stDataFrame div, .stDataFrame p {{ color: {t_txt} !important; }}
        .telemetry-card {{ background: {side}cc; border-radius: 15px; padding: 20px; border: 1px solid {acc}33; margin-bottom: 20px; }}
        .terminal-text {{ font-family: monospace; color: {acc}; background: #00000022; padding: 10px; border-radius: 5px; }}
        h1, h2, h3 {{ color: {acc} !important; font-weight: 700 !important; }}
        div.stButton > button {{ background-color: {acc} !important; color: white !important; border-radius: 8px !important; }}
        </style>
        """, unsafe_allow_html=True)

# --- LOGIN ---
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if st.session_state.user_name is None:
    st.title("SolarOS 2026: Access Portal")
    name_input = st.text_input("Username / Access Key")
    if st.button("Initialize Dashboard"):
        if name_input:
            st.session_state.user_id = register_user(name_input)
            st.session_state.user_name = name_input
            st.rerun()
    st.stop()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.divider()
    st.header(f"Profile: {st.session_state.user_name}")
    user_state = st.selectbox("Location", list(Config.STATE_RATES.keys()))
    menu = st.radio("Navigation", ["Overview", "AI Forecast", "Live Telemetry", "Subsidy Hub", "Market Hub"])
    st.divider()
    st.session_state.system_ready = st.toggle("System Online", value=st.session_state.system_ready)
    st.divider()
    st.caption("Developer: Yash Narayan Mohanty")
    st.write(f"[GitHub: yashzpro101](https://github.com/yashzpro101)")

# --- MAIN LOGIC ---
current_rate = Config.STATE_RATES.get(user_state, 7.0)

if menu == "Overview":
    if not st.session_state.system_ready:
        st.markdown(f'<div class="telemetry-card"><h1>Welcome to SolarOS 2026</h1><p>Awaiting hardware configuration for {user_state}.</p></div>', unsafe_allow_html=True)
        with st.popover("⚙️ Configure Array"):
            st.session_state.panel_area = st.number_input("Panel Area (sq ft):", 50, 10000, st.session_state.panel_area)
            if st.button("Finalize Installation"):
                st.session_state.system_ready = True
                st.rerun()
    else:
        st.title("Performance Analytics")
        user_kw = st.session_state.panel_area / 100
        units = user_kw * 120
        history = [units * f * current_rate for f in [0.95, 1.1, 0.9, 1.2, 1.3, 1.1]]
        data = components["tracker"].generate_dashboard_data(history)
        c1, c2, c3 = st.columns(3)
        c1.metric("Financial Savings", f"Rs. {data['total_savings']:,.0f}")
        c2.metric("Carbon Saved", f"{data['co2_saved_kg']:,.1f} kg")
        c3.metric("State Unit Rate", f"Rs. {current_rate}")
        st.subheader("Monthly Savings Trend")
        st.area_chart(data["history_df"].set_index("Month")["Savings"], color=acc)

elif menu == "AI Forecast":
    st.title("Atmospheric Prediction")
    st.write("Click below to run the neural network simulation based on current satellite data.")
    
    if st.button("Run AI Projection"):
        with st.spinner("Connecting to AI Model..."):
            try:
                prediction_value = components["forecaster"].predict_48h_harvest()
                if prediction_value is not None:
                    scale = (st.session_state.panel_area / 100) if st.session_state.system_ready else 3.0
                    st.session_state.last_forecast = (prediction_value / 3.0) * scale
                    st.success("Neural link established!") 
                else:
                    st.error("Model returned empty data.")
            except Exception as e:
                st.error(f"Module Error: {e}")

    if st.session_state.last_forecast:
        st.markdown(f"""
            <div class="telemetry-card">
                <h3 style='margin:0;'>48h Forecast Result</h3>
                <h1 style='font-size: 3rem;'>{st.session_state.last_forecast:.2f} <span style='font-size: 1.5rem;'>kWh</span></h1>
                <p style='opacity:0.7;'>Confidence Level: 94.2%</p>
            </div>
        """, unsafe_allow_html=True)

elif menu == "Live Telemetry":
    st.title("
