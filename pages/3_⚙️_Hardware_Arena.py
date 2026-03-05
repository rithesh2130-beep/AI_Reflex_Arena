import streamlit as st
import pandas as pd
import time
import os
import serial
import plotly.express as px
import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui_core import inject_fluent_design, apply_modern_theme, show_notification, render_top_nav

st.set_page_config(page_title="Hardware Arena", page_icon="⚙️", layout="wide")
inject_fluent_design()
render_top_nav(active_page="hardware")

DATA_FILE = "players_data.csv"

# -----------------------------
# SESSION STATE
# -----------------------------
if "game_running" not in st.session_state:
    st.session_state.game_running = False

# -----------------------------
# CONNECT ARDUINO
# -----------------------------
@st.cache_resource
def connect_arduino():
    try:
        ser = serial.Serial("COM11", 9600, timeout=1)
        time.sleep(2)
        return ser
    except Exception as e:
        return None

arduino = connect_arduino()

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<h1>⚙️ Hardware Training Facility</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #88c0d0; font-size: 1.1rem; margin-bottom: 2rem;'>Synchronize with Arduino arrays for physical cognitive tests.</p>", unsafe_allow_html=True)

# -----------------------------
# GAME CONTROL
# -----------------------------
c1, c2, c3, c4 = st.columns([4, 1, 1, 1])

with c1:
    player = st.text_input("Operator Designation (Player Name)", placeholder="Enter your alias...")

with c2:
    st.write("") # Spacer
    start = st.button("▶ INITIALIZE")
    
with c3:
    st.write("")
    # Add a custom class wrapper using Streamlit markdown container hack or generic for reset
    reset = st.button("⟳ PURGE", key="btnP", type="secondary")
    
with c4:
    st.write("")
    export = st.button("⬇ EXPORT", key="btnE", type="primary")

if reset and os.path.exists(DATA_FILE):
    os.remove(DATA_FILE)
    show_notification("Databanks purged.", icon="🗑️")
    time.sleep(1)
    st.rerun()

if export and os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    st.download_button(
        "Download Telemetry (CSV)",
        data=df.to_csv(index=False),
        file_name="reflex_telemetry.csv",
        use_container_width=True
    )

st.divider()

# -----------------------------
# LIVE GAME AREA
# -----------------------------
st.markdown("<h3>Live Diagnostics</h3>", unsafe_allow_html=True)
live_metrics_col = st.empty()
chart_area = st.empty()
log_area = st.expander("Raw Serial Telemetry")

reaction_data = []
correct_data = []
logs = []

human_score = None
human_avg = None
category = None

# Custom pulse animation placeholder
if not st.session_state.game_running:
    with chart_area.container():
        st.info("Awaiting task execution. Initialize to begin recording diagnostics.")
        if arduino is None:
            st.error("Arduino Interface OFFLINE.")

# -----------------------------
# START GAME
# -----------------------------
if start:
    st.session_state.game_running = True

if st.session_state.game_running:

    if arduino is None:
        show_notification("System Failure: Arduino offline.", "⚠️")
        st.session_state.game_running = False
        st.stop()

    if player.strip() == "":
        show_notification("Operator Designation required to initialize.", "⚠️")
        st.session_state.game_running = False
        st.stop()

    show_notification(f"Simulation Active. Standby, Operator {player}.", "🚀")

    arduino.write(b"START\n")
    start_time = time.time()

    while True:

        if arduino.in_waiting:
            line = arduino.readline().decode("utf-8", errors="ignore").strip()
            logs.append(line)

            if "REACTION" in line:
                parts = line.split(",")

                if len(parts) >= 8:
                    reaction = int(parts[5])
                    correct = parts[7]

                    reaction_data.append(reaction)
                    correct_data.append(correct)

                    df = pd.DataFrame({
                        "Round": range(1, len(reaction_data) + 1),
                        "Reaction": reaction_data
                    })

                    # Live ECG-style visualization
                    fig = px.area(
                        df, 
                        x="Round", 
                        y="Reaction", 
                        title="Live Neural Telemetry (ms)",
                        color_discrete_sequence=['#00C6FF']
                    )
                    fig.update_traces(mode='lines+markers', line=dict(width=3, shape='spline'), fillcolor='rgba(0, 198, 255, 0.1)')
                    
                    chart_area.plotly_chart(apply_modern_theme(fig), use_container_width=True)

            if "HUMAN_SCORE" in line:
                try: human_score = int(line.split(",")[1])
                except: pass

            if "HUMAN_AVG" in line:
                try: human_avg = line.split(",")[1].replace("ms", "").strip()
                except: pass

            if "CATEGORY" in line:
                category = line.split(",")[1]

            if "GAME_COMPLETE" in line:
                break

        if time.time() - start_time > 120:
            st.warning("Simulation Timeout Exceeded.")
            break

    st.session_state.game_running = False
    show_notification("Simulation Concluded. Processing diagnostics...", "🏁")

    with log_area:
        st.code('\n'.join(logs), language='text')

# -----------------------------
# SAVE DATA
# -----------------------------
    if human_score and human_avg:

        if not os.path.exists(DATA_FILE):
            df_init = pd.DataFrame(columns=[
                "Player", "Score", "AvgReaction", "Accuracy", "PerformanceIndex", "Timestamp"
            ])
            df_init.to_csv(DATA_FILE, index=False)

        if len(correct_data) > 0:
            accuracy = (pd.Series(correct_data) == "1").mean() * 100
        else:
            accuracy = 0

        performance_index = (float(human_score) * 2) + (1000 / float(human_avg))

        new_entry = pd.DataFrame([{
            "Player": player + " [Physical]",
            "Score": int(human_score),
            "AvgReaction": float(human_avg),
            "Accuracy": accuracy,
            "PerformanceIndex": performance_index,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])

        existing = pd.read_csv(DATA_FILE)
        updated = pd.concat([existing, new_entry], ignore_index=True)
        updated.to_csv(DATA_FILE, index=False)

        st.balloons()
        show_notification(f"Operator {player} telemetry archived.", "💾")
