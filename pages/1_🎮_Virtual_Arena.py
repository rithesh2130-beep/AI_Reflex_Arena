import streamlit as st
import time
import random
import pandas as pd
import sys
import os
import plotly.express as px
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui_core import inject_fluent_design, show_notification, render_top_nav, apply_modern_theme

st.set_page_config(page_title="Virtual Reflex Arena", page_icon="🎮", layout="wide")
inject_fluent_design()
render_top_nav(active_page="virtual")

DATA_FILE = "players_data.csv"

# -----------------------------
# SESSION STATE
# -----------------------------
if "virtual_state" not in st.session_state:
    st.session_state.virtual_state = "idle" # idle, waiting_for_light, waiting_for_click, finished
if "current_light" not in st.session_state:
    st.session_state.current_light = None
if "turn_on_time" not in st.session_state:
    st.session_state.turn_on_time = 0
if "virtual_round" not in st.session_state:
    st.session_state.virtual_round = 0
if "virtual_reaction_times" not in st.session_state:
    st.session_state.virtual_reaction_times = []
if "virtual_correct_hits" not in st.session_state:
    st.session_state.virtual_correct_hits = []
if "false_starts" not in st.session_state:
    st.session_state.false_starts = 0
if "virtual_telemetry" not in st.session_state:
    st.session_state.virtual_telemetry = []

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<h1>🎮 Virtual Simulation Arena</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #88c0d0; font-size: 1.1rem; margin-bottom: 2rem;'>Test your cognitive responsiveness in the digital domain.</p>", unsafe_allow_html=True)

# -----------------------------
# GAME CONTROL
# -----------------------------
c1, c2, c3 = st.columns([4, 1, 1])

with c1:
    player = st.text_input("Operator Designation (Player Name)", placeholder="Enter your alias...", key="p_name")

with c2:
    st.write("") 
    if st.button("▶ INITIATE SEQUENCE", key="start_btn"):
        if not player.strip():
            show_notification("Operator Designation required.", "⚠️")
        else:
            show_notification("Sequence Initiated.", "🚀")
            st.session_state.virtual_state = "waiting_for_light"
            st.session_state.virtual_round = 0
            st.session_state.virtual_reaction_times = []
            st.session_state.virtual_correct_hits = []
            st.session_state.virtual_telemetry = []
            st.session_state.false_starts = 0
            time.sleep(1) # Let the notification render before jumping
            st.rerun()

with c3:
    st.write("")
    if st.button("⏹ ABORT", key="abort_btn"):
        st.session_state.virtual_state = "idle"
        st.rerun()

st.divider()

# -----------------------------
# GAME LOGIC & RENDER
# -----------------------------
arena_col1, arena_col2, arena_col3 = st.columns([1,1,1])
columns = [arena_col1, arena_col2, arena_col3]

score_col = st.empty()

if st.session_state.virtual_state == "idle":
    st.info("Awaiting initialization. Enter your Operator Designation and press Initiate Sequence.")

elif st.session_state.virtual_state == "waiting_for_light":
    score_col.markdown(f"**Round: {st.session_state.virtual_round + 1} / 10**")
    
    # Render all 3 lights as dark
    for col in columns:
        col.markdown("<div class='game-light light-off'></div>", unsafe_allow_html=True)
    
    # Random wait time between 1 and 4 seconds
    delay = random.uniform(1.0, 3.5)
    with st.spinner("Calibrating Neural Sync..."):
        time.sleep(delay)
    
    # Assign new target and switch state
    st.session_state.current_light = random.randint(0, 2)
    st.session_state.turn_on_time = time.time()
    st.session_state.virtual_state = "waiting_for_click"
    st.rerun()

elif st.session_state.virtual_state == "waiting_for_click":
    score_col.markdown(f"**Round: {st.session_state.virtual_round + 1} / 10**")
    
    clicked_btn = None
    for i, col in enumerate(columns):
        with col:
            # Draw Lights
            if i == st.session_state.current_light:
                st.markdown("<div class='game-light light-on'></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='game-light light-off'></div>", unsafe_allow_html=True)
            
            # Action Button
            if st.button(f"STRIKE {i+1}", key=f"strike_{i}"):
                clicked_btn = i

    if clicked_btn is not None:
        reaction = (time.time() - st.session_state.turn_on_time) * 1000
        st.session_state.virtual_reaction_times.append(reaction)
        
        target = st.session_state.current_light
        hit = 1 if clicked_btn == target else 0
        if hit:
            st.session_state.virtual_correct_hits.append(1)
            show_notification(f"Hit! {reaction:.0f}ms", "⚡")
        else:
            st.session_state.virtual_correct_hits.append(0)
            show_notification(f"Miss! Wrong Zone.", "❌")
            
        st.session_state.virtual_telemetry.append(f"ROUND {st.session_state.virtual_round + 1}: STRIKE {clicked_btn+1} | TARGET {target+1} | REACTION: {reaction:.0f}ms | HIT: {hit}")
        
        st.session_state.virtual_round += 1
        
        if st.session_state.virtual_round >= 10:
            st.session_state.virtual_state = "finished"
        else:
            st.session_state.virtual_state = "waiting_for_light"
        
        st.rerun()
    else:
        # Evaluate timeout only if no strike button was pressed
        current_time = time.time()
        if current_time - st.session_state.turn_on_time > 2.0:
            st.session_state.virtual_reaction_times.append(2000.0) # Penalty 2s
            st.session_state.virtual_correct_hits.append(0)
            st.session_state.virtual_telemetry.append(f"ROUND {st.session_state.virtual_round + 1}: TIMEOUT | TARGET {st.session_state.current_light+1} | REACTION: 2000ms | HIT: 0")
            
            show_notification("Missed Target (Timeout).", "❌")
            st.session_state.virtual_round += 1
            if st.session_state.virtual_round >= 10:
                st.session_state.virtual_state = "finished"
            else:
                st.session_state.virtual_state = "waiting_for_light"
            time.sleep(1)
            st.rerun()

elif st.session_state.virtual_state == "finished":
    st.success("Simulation Complete!")
    
    avg_reac = sum(st.session_state.virtual_reaction_times) / len(st.session_state.virtual_reaction_times)
    acc = (sum(st.session_state.virtual_correct_hits) / 10.0) * 100
    
    # Very basic score calculation prioritizing speed and accuracy
    raw_score = (1000 / avg_reac) * 100 if avg_reac > 0 else 0
    raw_score = raw_score * (acc / 100)
    perf_idx = raw_score * 1.5
    
    st.markdown("<h3>Session Diagnostics</h3>", unsafe_allow_html=True)
    rc1, rc2, rc3 = st.columns(3)
    rc1.metric("Average Reaction", f"{avg_reac:.0f} ms")
    rc2.metric("Accuracy", f"{acc:.0f}%")
    rc3.metric("Final Score", f"{int(raw_score)}")
    
    if st.button("💾 SAVE DIAGNOSTICS & RETURN TO IDLE"):
        if not os.path.exists(DATA_FILE):
            df_init = pd.DataFrame(columns=[
                "Player", "Score", "AvgReaction", "Accuracy", "PerformanceIndex", "Timestamp"
            ])
            df_init.to_csv(DATA_FILE, index=False)
            
        new_entry = pd.DataFrame([{
            "Player": player + " [Virtual]",
            "Score": int(raw_score),
            "AvgReaction": float(avg_reac),
            "Accuracy": acc,
            "PerformanceIndex": perf_idx,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])

        existing = pd.read_csv(DATA_FILE)
        updated = pd.concat([existing, new_entry], ignore_index=True)
        updated.to_csv(DATA_FILE, index=False)
        
        st.balloons()
        st.session_state.virtual_state = "idle"
        st.rerun()

st.divider()

st.markdown("<h3>Live Diagnostics</h3>", unsafe_allow_html=True)
chart_area = st.empty()
log_area = st.expander("Raw Telemetry")

if len(st.session_state.virtual_reaction_times) > 0:
    df = pd.DataFrame({
        "Round": range(1, len(st.session_state.virtual_reaction_times) + 1),
        "Reaction": st.session_state.virtual_reaction_times
    })

    fig = px.area(
        df, 
        x="Round", 
        y="Reaction", 
        title="Live Neural Telemetry (ms)",
        color_discrete_sequence=['#00C6FF']
    )
    fig.update_traces(mode='lines+markers', line=dict(width=3, shape='spline'), fillcolor='rgba(0, 198, 255, 0.1)')
    chart_area.plotly_chart(apply_modern_theme(fig), use_container_width=True)

    with log_area:
        st.code('\n'.join(st.session_state.get("virtual_telemetry", [])), language='text')
else:
    with chart_area.container():
        st.info("Awaiting task execution. Initialize to begin recording diagnostics.")
