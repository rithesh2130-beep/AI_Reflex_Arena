import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui_core import inject_fluent_design, apply_modern_theme, render_top_nav

st.set_page_config(page_title="Global Analytics", page_icon="📊", layout="wide")
inject_fluent_design()
render_top_nav(active_page="analytics")

DATA_FILE = "players_data.csv"

# -----------------------------
# LOAD DATA
# -----------------------------
if os.path.exists(DATA_FILE):
    try:
        db = pd.read_csv(DATA_FILE)
    except:
        db = pd.DataFrame()
else:
    db = pd.DataFrame()

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<h1>📊 Global Telemetry & Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #88c0d0; font-size: 1.1rem; margin-bottom: 2rem;'>Comprehensive performance diagnostics across all operators.</p>", unsafe_allow_html=True)

# -----------------------------
# GLOBAL ANALYTICS
# -----------------------------
if not db.empty:
    col1, col2, col3, col4 = st.columns(4)

    best_reaction = db['AvgReaction'].min()
    best_score = int(db['Score'].max())
    
    # Calculate some deltas (e.g. comparing latest to average)
    latest_reaction = db['AvgReaction'].iloc[-1]
    avg_reaction_global = db['AvgReaction'].mean()
    reaction_delta = avg_reaction_global - latest_reaction # Positive is better (faster)
    
    latest_acc = db['Accuracy'].iloc[-1]
    avg_acc_global = db['Accuracy'].mean()
    acc_delta = latest_acc - avg_acc_global

    col1.metric("Registered Operators", len(db["Player"].unique()))
    col2.metric("Apex Reaction Time", f"{best_reaction:.0f} ms", delta=f"{reaction_delta:.1f} ms vs avg", delta_color="inverse")
    col3.metric("Peak Synchronization (Score)", best_score)
    col4.metric("Mean Precision", f"{avg_acc_global:.1f}%", delta=f"{acc_delta:.1f}% vs avg", delta_color="normal")

    st.write("")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 Leaderboard", "📊 Distribution", "🎯 Accuracy vs Speed", "📈 Performance Radar"])

    with tab1:
        leaderboard = db.sort_values("AvgReaction").drop_duplicates("Player").head(10).reset_index(drop=True)
        leaderboard.index += 1
        st.dataframe(leaderboard, use_container_width=True)

    with tab2:
        fig = px.histogram(
            db, 
            x="AvgReaction", 
            nbins=30, 
            color_discrete_sequence=['#00C6FF'],
            marginal="box",
            title="Neurological Response Distribution"
        )
        fig.update_traces(opacity=0.8)
        st.plotly_chart(apply_modern_theme(fig), use_container_width=True)

    with tab3:
        fig = px.scatter(
            db, 
            x="AvgReaction", 
            y="Accuracy", 
            size="Score", 
            color="Player",
            hover_name="Player", 
            title="Speed vs Precision Matrix",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(apply_modern_theme(fig), use_container_width=True)
        
    with tab4:
        # Radar charts comparing average stats of top 5 players
        top_players = leaderboard.head(5)['Player'].tolist()
        radar_data = db[db['Player'].isin(top_players)].groupby('Player')[['Score', 'AvgReaction', 'Accuracy', 'PerformanceIndex']].mean().reset_index()
        
        fig = go.Figure()
        
        for i, row in radar_data.iterrows():
            # Normalize data for radar chart visual clarity
            max_r = db['AvgReaction'].max()
            norm_reaction = abs((row['AvgReaction'] / max_r) * 100 - 100) # faster is higher score
            
            fig.add_trace(go.Scatterpolar(
                r=[row['Accuracy'], norm_reaction, (row['Score']/db['Score'].max())*100, (row['PerformanceIndex']/db['PerformanceIndex'].max())*100, row['Accuracy']],
                theta=['Precision', 'Speed (Normalized)', 'Score', 'Overall Performance', 'Precision'],
                fill='toself',
                name=row['Player']
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)"),
                bgcolor="rgba(0,0,0,0)"
            ),
            showlegend=True,
            title="Top Operator Signatures",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e6e6e6", family="Segoe UI")
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

# -----------------------------
# PLAYER SPECIFIC ANALYTICS
# -----------------------------
    st.markdown("<h3>Operator Dossier</h3>", unsafe_allow_html=True)

    selected_player = st.selectbox(
        "Select Operator Designation",
        db["Player"].unique()
    )

    player_df = db[db["Player"] == selected_player].copy()
    player_df["Session"] = range(1, len(player_df) + 1)
    
    # Calculate rolling averages for smooth trend line
    player_df["RollingReaction"] = player_df["AvgReaction"].rolling(window=3, min_periods=1).mean()

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=player_df["Session"], y=player_df["AvgReaction"], 
            mode='lines+markers', name='Raw Reaction',
            line=dict(color='rgba(0, 198, 255, 0.4)', dash='dot')
        ))
        fig.add_trace(go.Scatter(
            x=player_df["Session"], y=player_df["RollingReaction"], 
            mode='lines', name='Trend (3-MA)',
            line=dict(color='#0078D4', width=3, shape='spline')
        ))
        fig.update_layout(title="Cognitive Response Trend")
        st.plotly_chart(apply_modern_theme(fig), use_container_width=True)

    with col2:
        fig = px.bar(
            player_df, 
            x="Session", 
            y="Score", 
            title="Synchronization Score History",
            color="Score",
            color_continuous_scale="Blues"
        )
        fig.update_traces(marker_line_width=0, opacity=0.9)
        st.plotly_chart(apply_modern_theme(fig), use_container_width=True)

else:
    st.info("No telemetry data found. Go run some simulations in the Arena first!")
