import streamlit as st
from ui_core import inject_fluent_design, render_top_nav

st.set_page_config(
    page_title="AI Reflex Arena", 
    page_icon="⚡", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

inject_fluent_design()
render_top_nav(active_page="home")

# -----------------------------
# LANDING PAGE HEADER
# -----------------------------
st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-top: 5rem;'>⚡ AI Reflex Arena</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #88c0d0; font-size: 1.5rem; margin-bottom: 4rem;'>Select a module from the top navigation menu to begin.</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: rgba(30,32,40,0.4); border-radius: 12px; padding: 30px; border: 1px solid rgba(255,255,255,0.05); text-align: center; height: 100%;">
        <h2 style="color: #00C6FF; font-size: 2.5rem; margin-bottom: 10px;">🎮</h2>
        <h3>Virtual Arena</h3>
        <p style="color: #a0a0a0;">Test your cognitive responsiveness in the digital domain using your mouse or touchscreen. No hardware required.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: rgba(30,32,40,0.4); border-radius: 12px; padding: 30px; border: 1px solid rgba(255,255,255,0.05); text-align: center; height: 100%;">
        <h2 style="color: #00C6FF; font-size: 2.5rem; margin-bottom: 10px;">📊</h2>
        <h3>Intelligence & Analytics</h3>
        <p style="color: #a0a0a0;">View the global telemetry, performance radar matrices, leaderboards, and detailed operator dossiers.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: rgba(30,32,40,0.4); border-radius: 12px; padding: 30px; border: 1px solid rgba(255,255,255,0.05); text-align: center; height: 100%;">
        <h2 style="color: #00C6FF; font-size: 2.5rem; margin-bottom: 10px;">⚙️</h2>
        <h3>Hardware Training</h3>
        <p style="color: #a0a0a0;">Synchronize with external Arduino arrays for rigorous physical and sensory testing.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='min-height: 200px;'></div>", unsafe_allow_html=True)