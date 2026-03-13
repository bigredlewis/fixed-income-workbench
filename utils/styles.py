"""
Shared styling utilities for the Fixed Income Analyst Workbench.
Provides consistent CSS theme and color palette across all pages.
"""

import streamlit as st

# --- Unified color palette for charts ---
CHART_COLORS = {
    "primary": "#1B3A5C",       # Deep navy
    "secondary": "#2E6B9E",     # Medium blue
    "accent": "#4CA1D9",        # Light blue
    "highlight": "#E8913A",     # Warm amber
    "positive": "#2D8B57",      # Green
    "negative": "#C44E52",      # Red
    "warning": "#E8913A",       # Amber
    "muted": "#8FAABE",         # Muted blue-grey
    "light": "#D6E4F0",         # Very light blue
    "bg_card": "#F7F9FC",       # Card background
}

CHART_SEQUENCE = [
    CHART_COLORS["primary"],
    CHART_COLORS["highlight"],
    CHART_COLORS["secondary"],
    CHART_COLORS["positive"],
    CHART_COLORS["accent"],
    CHART_COLORS["negative"],
    CHART_COLORS["muted"],
]

PLOTLY_LAYOUT = dict(
    template="plotly_white",
    font=dict(family="Inter, -apple-system, BlinkMacSystemFont, sans-serif", size=13),
    title_font=dict(size=16, color=CHART_COLORS["primary"]),
    colorway=CHART_SEQUENCE,
    margin=dict(t=50, b=40, l=50, r=20),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)


def inject_custom_css():
    """Inject the global custom CSS theme into the Streamlit app."""
    st.markdown("""
    <style>
    /* === GLOBAL TYPOGRAPHY === */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* === SMOOTH TRANSITIONS === */
    *, *::before, *::after {
        transition: background-color 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }

    /* === PAGE BACKGROUND === */
    .stApp {
        background: linear-gradient(180deg, #F7F9FC 0%, #F0F4F8 50%, #FFFFFF 100%);
    }

    /* === MAIN TITLE === */
    h1 {
        color: #1B3A5C !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        padding-bottom: 0.2em !important;
    }

    /* === SECTION HEADERS === */
    h2 {
        color: #1B3A5C !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #D6E4F0;
        padding-bottom: 0.4em !important;
        margin-top: 1.5em !important;
    }

    h3 {
        color: #2E6B9E !important;
        font-weight: 600 !important;
    }

    /* === STYLED DIVIDERS === */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #D6E4F0, transparent) !important;
        margin: 1.5em 0 !important;
    }

    /* === SIDEBAR === */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B3A5C 0%, #152D47 100%);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span {
        color: #E8EEF4 !important;
    }

    section[data-testid="stSidebar"] hr {
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
    }

    section[data-testid="stSidebar"] .stTextInput input {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: white !important;
        border-radius: 8px !important;
    }

    section[data-testid="stSidebar"] .stTextInput input:focus {
        border-color: rgba(255,255,255,0.5) !important;
        box-shadow: 0 0 0 2px rgba(255,255,255,0.1) !important;
    }

    /* === METRIC CARDS === */
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: all 0.25s ease !important;
    }

    [data-testid="stMetric"]:hover {
        box-shadow: 0 4px 12px rgba(27, 58, 92, 0.08);
        border-color: #D6E4F0;
        transform: translateY(-1px);
    }

    [data-testid="stMetric"] label {
        color: #64748B !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #1B3A5C !important;
        font-weight: 700 !important;
    }

    /* === BUTTONS === */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #1B3A5C, #2E6B9E) !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        padding: 0.5em 1.5em !important;
        transition: all 0.25s ease !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        background: linear-gradient(135deg, #152D47, #1B3A5C) !important;
        box-shadow: 0 4px 16px rgba(27, 58, 92, 0.35) !important;
        transform: translateY(-2px) !important;
    }

    .stButton > button[kind="primary"]:active,
    .stButton > button[data-testid="stBaseButton-primary"]:active {
        transform: translateY(0) !important;
        box-shadow: 0 2px 6px rgba(27, 58, 92, 0.2) !important;
    }

    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="stBaseButton-secondary"] {
        border: 1px solid #D6E4F0 !important;
        border-radius: 8px !important;
        color: #2E6B9E !important;
        font-weight: 500 !important;
        transition: all 0.25s ease !important;
    }

    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="stBaseButton-secondary"]:hover {
        background: #F0F7FF !important;
        border-color: #2E6B9E !important;
    }

    /* === DOWNLOAD BUTTONS === */
    .stDownloadButton > button {
        border: 1px solid #D6E4F0 !important;
        border-radius: 8px !important;
        color: #2E6B9E !important;
        font-weight: 500 !important;
        transition: all 0.25s ease !important;
    }

    .stDownloadButton > button:hover {
        background: #F0F7FF !important;
        border-color: #2E6B9E !important;
        box-shadow: 0 2px 8px rgba(46, 107, 158, 0.12) !important;
    }

    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 2px solid #E2E8F0;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 500;
        color: #64748B;
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #1B3A5C;
        background: #F7F9FC;
    }

    .stTabs [aria-selected="true"] {
        background: white !important;
        border-bottom: 3px solid #1B3A5C !important;
        color: #1B3A5C !important;
        font-weight: 600 !important;
    }

    /* === EXPANDERS === */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        color: #1B3A5C !important;
        border-radius: 8px !important;
    }

    /* === DATA FRAMES === */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }

    /* === FILE UPLOADER === */
    [data-testid="stFileUploader"] {
        border-radius: 12px;
    }

    [data-testid="stFileUploader"] section {
        border-radius: 12px !important;
        border: 2px dashed #D6E4F0 !important;
        transition: all 0.25s ease !important;
    }

    [data-testid="stFileUploader"] section:hover {
        border-color: #2E6B9E !important;
        background: #F8FBFF !important;
    }

    /* === INFO/SUCCESS/WARNING/ERROR BOXES === */
    .stAlert {
        border-radius: 10px !important;
    }

    /* === INPUTS === */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        border-radius: 8px !important;
        border-color: #D6E4F0 !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #2E6B9E !important;
        box-shadow: 0 0 0 3px rgba(46, 107, 158, 0.12) !important;
    }

    /* === MULTISELECT === */
    .stMultiSelect {
        border-radius: 8px;
    }

    /* === CAPTION === */
    .stCaption, caption {
        color: #94A3B8 !important;
    }

    /* === PAGE LINK BUTTONS === */
    [data-testid="stPageLink"] a {
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stPageLink"] a:hover {
        transform: translateX(4px);
    }

    /* === CUSTOM SCROLLBAR === */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }

    ::-webkit-scrollbar-track {
        background: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background: #C1D0E0;
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #94A3B8;
    }

    /* === FADE-IN ANIMATION === */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .main .block-container {
        animation: fadeInUp 0.4s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)


def feature_card(icon, title, description, page_link, link_label):
    """Render a styled feature card on the home page."""
    st.markdown(f"""
    <div class="fi-feature-card" style="
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 28px 28px 22px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(27, 58, 92, 0.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        min-height: 200px;
        cursor: default;
        position: relative;
        overflow: hidden;
    "
    onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 24px rgba(27,58,92,0.1)'; this.style.borderColor='#B8D4F0';"
    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(27,58,92,0.04)'; this.style.borderColor='#E2E8F0';"
    >
        <div style="
            font-size: 2rem;
            margin-bottom: 12px;
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #F0F7FF, #E8F0FE);
            border-radius: 12px;
        ">{icon}</div>
        <div style="
            font-size: 1.15rem;
            font-weight: 600;
            color: #1B3A5C;
            margin-bottom: 10px;
        ">{title}</div>
        <div style="
            color: #64748B;
            font-size: 0.9rem;
            line-height: 1.65;
        ">{description}</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link(page_link, label=link_label, icon=icon)


def styled_header(text, subtitle=None):
    """Render a styled page header."""
    st.markdown(f"""
    <div style="margin-bottom: 0.5em;">
        <h1 style="margin-bottom: 0 !important;">{text}</h1>
    </div>
    """, unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"""
        <p style="color: #64748B; font-size: 1.05rem; margin-top: -0.5em; margin-bottom: 1.5em;">
            {subtitle}
        </p>
        """, unsafe_allow_html=True)
