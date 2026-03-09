import streamlit as st
import time

def inject_fluent_design():
    st.markdown("""
    <style>
        /* Global Typography & Hide Default Elements */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Outfit:wght@400;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, sans-serif;
        }

        /* HIDE SIDEBAR & DEFAULT HEADER */
        [data-testid="collapsedControl"] { display: none !important; }
        section[data-testid="stSidebar"] { display: none !important; }
        header[data-testid="stHeader"] { display: none !important; }

        /* Dynamic Animated Gradient Background */
        .stApp {
            background: linear-gradient(-45deg, #09090b, #13151a, #0a1128, #150e28);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            color: #e6e6e6;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* --------------------------------- */
        /*  Custom Top Navigation Bar        */
        /* --------------------------------- */
        .top-nav {
            position: fixed;
            top: 0px;
            left: 0px;
            width: 100vw;
            height: 70px;
            background: rgba(15, 15, 20, 0.4);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            z-index: 999999;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        }

        .nav-btn-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .nav-btn {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.05);
            color: #b0b0b0;
            padding: 10px 24px;
            border-radius: 30px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            text-decoration: none;
            display: inline-block;
        }

        .nav-btn:hover {
            color: white;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(0, 198, 255, 0.4);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 198, 255, 0.2);
        }

        .nav-btn.active {
            background: linear-gradient(135deg, rgba(0, 120, 212, 0.9), rgba(0, 90, 158, 0.9));
            color: white;
            border: 1px solid rgba(0, 198, 255, 0.5);
            box-shadow: 0 4px 20px rgba(0, 120, 212, 0.4);
        }

        /* Shift overall app content down below the nav bar */
        .block-container {
            padding-top: 100px !important;
        }

        /* --------------------------------- */
        /*  Glassmorphism Cards (Metrics)    */
        /* --------------------------------- */
        [data-testid="stMetric"] {
            background: rgba(20, 22, 30, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            overflow: hidden;
            position: relative;
        }
        
        /* Inner glowing orb effect for Glassmorphism */
        [data-testid="stMetric"]::before {
            content: '';
            position: absolute;
            top: -50px; left: -50px;
            width: 100px; height: 100px;
            background: radial-gradient(circle, rgba(0,198,255,0.15) 0%, rgba(0,0,0,0) 70%);
            border-radius: 50%;
            transition: all 0.5s;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-6px) scale(1.02);
            box-shadow: 0 15px 45px rgba(0, 198, 255, 0.15);
            border: 1px solid rgba(0, 198, 255, 0.4);
            background: rgba(30, 32, 45, 0.4);
        }
        
        [data-testid="stMetric"]:hover::before {
            transform: translate(60px, 60px) scale(2);
        }
        
        [data-testid="stMetricValue"] {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 2.8rem;
            background: linear-gradient(120deg, #ffffff, #00C6FF, #0078D4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding-bottom: 2px;
            letter-spacing: -1px;
        }
        
        [data-testid="stMetricDelta"] svg { fill: #00C6FF; }

        /* Buttons Modernization - Liquid Hover */
        .stButton > button {
            border-radius: 30px;
            border: 1px solid rgba(255,255,255,0.1) !important;
            background: linear-gradient(135deg, rgba(0, 120, 212, 0.8), rgba(0, 198, 255, 0.8)) !important;
            backdrop-filter: blur(8px);
            color: white !important;
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.1rem;
            letter-spacing: 1px;
            padding: 0.8rem 2rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px rgba(0, 120, 212, 0.3);
            width: 100%;
            text-transform: uppercase;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #00C6FF, #0078D4) !important;
            box-shadow: 0 8px 25px rgba(0, 198, 255, 0.5) !important;
            transform: translateY(-3px) scale(1.02);
            border-color: rgba(255,255,255,0.4) !important;
        }

        /* Specific coloring for Reset Button */
        button[kind="secondary"].reset-btn, div:nth-child(3) > .stButton > button {
            background: linear-gradient(135deg, rgba(216, 59, 1, 0.8), rgba(168, 0, 0, 0.9)) !important;
            box-shadow: 0 4px 15px rgba(216, 59, 1, 0.3);
        }
        button[kind="secondary"].reset-btn:hover, div:nth-child(3) > .stButton > button:hover {
            background: linear-gradient(135deg, #ff5722, #d83b01) !important;
            box-shadow: 0 8px 25px rgba(255, 87, 34, 0.5) !important;
        }

        /* Input Fields */
        .stTextInput > div > div > input, .stSelectbox > div > div {
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background-color: rgba(0, 0, 0, 0.2);
            color: white;
            font-size: 1.1rem;
            padding: 12px;
            transition: all 0.3s;
            backdrop-filter: blur(12px);
        }
        .stTextInput > div > div > input:focus, .stSelectbox > div > div:focus-within {
            border-color: #00C6FF;
            box-shadow: 0 0 0 3px rgba(0, 198, 255, 0.3);
            background-color: rgba(0, 0, 0, 0.4);
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            background-color: rgba(10,12,18,0.5);
            border-radius: 12px;
            padding: 6px;
            border: 1px solid rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
        }
        .stTabs [data-baseweb="tab"] {
            color: #808080;
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            padding: 0.6rem 1.5rem;
            border-radius: 8px;
            transition: all 0.3s;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: white;
            background-color: rgba(255,255,255,0.05);
        }
        .stTabs [aria-selected="true"] {
            color: white !important;
            background: linear-gradient(90deg, rgba(0,198,255,0.2), rgba(0,120,212,0.2)) !important;
            border-bottom: none !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            border: 1px solid rgba(0,198,255,0.3);
        }

        /* Headers with pulsing glow animation */
        h1, h2, h3 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }
        
        h1 {
            background: linear-gradient(120deg, #ffffff, #00C6FF, #88c0d0);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fadeIn 0.8s ease-out, shineText 5s linear infinite;
            margin-bottom: 0.5rem;
            font-size: 3.5rem;
        }
        
        .stDivider > hr {
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            background: linear-gradient(90deg, transparent, rgba(0,198,255,0.5), transparent);
            height: 1px;
            border: none;
            margin: 3rem 0;
        }

        /* Custom Notification Bar */
        .custom-notification {
            position: fixed;
            top: 90px;
            right: 20px;
            z-index: 999999;
            background: rgba(20, 22, 30, 0.85);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.1);
            border-left: 5px solid #00C6FF;
            padding: 16px 28px;
            border-radius: 12px;
            color: white;
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6), 0 0 20px rgba(0,198,255,0.2);
            animation: slideInRight 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            display: flex;
            align-items: center;
            gap: 12px;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); filter: blur(10px); }
            to { opacity: 1; transform: translateY(0); filter: blur(0); }
        }
        
        @keyframes shineText {
            to { background-position: 200% center; }
        }

        @keyframes slideInRight {
            0% { opacity: 0; transform: translateX(100%) scale(0.9); }
            100% { opacity: 1; transform: translateX(0) scale(1); }
        }

        /* Virtual Game Lights Styling */
        .game-light {
            border-radius: 50%;
            width: 140px;
            height: 140px;
            margin: 30px auto;
            border: 4px solid rgba(255,255,255,0.05);
            box-shadow: 0 0 20px rgba(0,0,0,0.8) inset, 0 10px 20px rgba(0,0,0,0.4);
            transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .light-off {
            background: radial-gradient(circle at 30% 30%, #333, #0a0a0a);
        }
        .light-on {
            border: 4px solid #fff;
            background: radial-gradient(circle at 30% 30%, #5eff5e, #00ff00, #00aa00);
            box-shadow: 0 0 40px rgba(0, 255, 0, 0.8), 0 0 80px rgba(0, 255, 0, 0.5), inset 0 0 20px rgba(255,255,255,0.8);
            animation: popLight 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            transform: scale(1.05);
        }
        .light-miss {
            border: 4px solid #ff5e5e;
            background: radial-gradient(circle at 30% 30%, #ff5e5e, #ff0000, #aa0000);
            box-shadow: 0 0 40px rgba(255, 0, 0, 0.8), 0 0 80px rgba(255, 0, 0, 0.4);
            animation: shake 0.4s;
        }
        @keyframes popLight {
            0% { transform: scale(0.8); filter: brightness(0.5); }
            60% { transform: scale(1.15); filter: brightness(1.5); }
            100% { transform: scale(1.05); filter: brightness(1); }
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            20% { transform: translateX(-15px); }
            40% { transform: translateX(15px); }
            60% { transform: translateX(-15px); }
            80% { transform: translateX(15px); }
        }

    </style>
    """, unsafe_allow_html=True)

def render_top_nav(active_page="home"):
    # Generate the top navbar HTML.
    # We will use Streamlit st.page_link which provides native fast routing, styled manually above!
    st.markdown('<div class="top-nav"><div class="nav-btn-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🏠 Command Center", use_container_width=True, type="primary" if active_page=="home" else "secondary"):
            st.switch_page("reflex_dashboard.py")
    with col2:
        if st.button("🎮 Virtual Arena", use_container_width=True, type="primary" if active_page=="virtual" else "secondary"):
            st.switch_page("pages/1_🎮_Virtual_Arena.py")
    with col3:
        if st.button("📊 Intelligence", use_container_width=True, type="primary" if active_page=="analytics" else "secondary"):
            st.switch_page("pages/2_📊_Analytics.py")
    with col4:
        if st.button("⚙️ Hardware Link", use_container_width=True, type="primary" if active_page=="hardware" else "secondary"):
            st.switch_page("pages/3_⚙️_Hardware_Arena.py")
            
    st.markdown('</div></div>', unsafe_allow_html=True)

def apply_modern_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Outfit, Inter, sans-serif", color="#c0c0c0"),
        hovermode="x unified",
        margin=dict(l=10, r=10, t=50, b=10),
        title_font=dict(size=22, color="#ffffff", family="Outfit, Inter"),
        xaxis=dict(showgrid=False, zeroline=False, gridcolor="rgba(255,255,255,0.03)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.03)", zeroline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor="rgba(0,0,0,0)")
    )
    # Add a soft glow onto line charts
    fig.update_traces(line=dict(width=4), selector=dict(type='scatter'))
    return fig

def show_notification(message, icon="ℹ️"):
    html = f"""
    <div class="custom-notification" id="notif-{time.time()}">
        <span style="font-size: 1.8rem;">{icon}</span>
        <span>{message}</span>
    </div>
    <script>
        setTimeout(function() {{
            var el = document.getElementById("notif-{time.time()}");
            if(el) {{
                el.style.opacity = '0';
                el.style.transform = 'translateX(100%) scale(0.9)';
                el.style.transition = 'all 0.4s ease';
            }}
        }}, 3500);
    </script>
    """
    st.markdown(html, unsafe_allow_html=True)
