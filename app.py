"""
Fixed Income Analyst Workbench
A tool for fundamental fixed income analysts to streamline credit analysis,
compare estimates to consensus, analyze sell-side reports, and evaluate portfolio fit.
"""

import streamlit as st
from utils.styles import inject_custom_css, feature_card

st.set_page_config(
    page_title="Fixed Income Analyst Workbench",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Inject global theme ---
inject_custom_css()

# --- Sidebar branding ---
st.sidebar.markdown("""
<div style="text-align: center; padding: 10px 0 6px 0;">
    <div style="font-size: 1.6rem; margin-bottom: 2px;">📊</div>
    <div style="font-size: 1.1rem; font-weight: 700; color: #E8EEF4; letter-spacing: 0.02em;">
        FI Analyst Workbench
    </div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "Navigate using the pages above. Each tool is designed to streamline "
    "a common fixed income analyst workflow."
)

# --- Check for API key in session state ---
if "anthropic_api_key" not in st.session_state:
    st.session_state.anthropic_api_key = ""

with st.sidebar.expander("AI Settings", expanded=False):
    api_key_input = st.text_input(
        "Anthropic API Key (optional)",
        value=st.session_state.anthropic_api_key,
        type="password",
        help="Required for AI-powered document analysis. Get a key at console.anthropic.com",
    )
    if api_key_input != st.session_state.anthropic_api_key:
        st.session_state.anthropic_api_key = api_key_input
        st.rerun()

    if st.session_state.anthropic_api_key:
        st.success("API key configured")
    else:
        st.info("No API key — AI features will use manual mode")

# --- Home page hero ---
st.markdown("""
<div style="
    background: linear-gradient(135deg, #1B3A5C 0%, #2E6B9E 50%, #4CA1D9 100%);
    border-radius: 16px;
    padding: 40px 44px;
    margin-bottom: 28px;
    color: white;
    position: relative;
    overflow: hidden;
">
    <div style="
        position: absolute;
        top: -20px;
        right: -20px;
        width: 200px;
        height: 200px;
        background: rgba(255,255,255,0.05);
        border-radius: 50%;
    "></div>
    <div style="
        position: absolute;
        bottom: -40px;
        right: 60px;
        width: 120px;
        height: 120px;
        background: rgba(255,255,255,0.03);
        border-radius: 50%;
    "></div>
    <div style="font-size: 2rem; margin-bottom: 8px;">📊</div>
    <h1 style="color: white !important; margin: 0 0 8px 0 !important; font-size: 2rem !important;">
        Fixed Income Analyst Workbench
    </h1>
    <p style="color: rgba(255,255,255,0.85); font-size: 1.1rem; margin: 0; line-height: 1.5; max-width: 600px;">
        Streamline your credit analysis workflow — from model building to portfolio fit.
    </p>
</div>
""", unsafe_allow_html=True)

# --- API Key callout ---
if not st.session_state.anthropic_api_key:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #F0F7FF, #E8F0FE);
        border: 1px solid #B8D4F0;
        border-left: 4px solid #2E6B9E;
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 24px;
    ">
        <div style="font-weight: 600; color: #1B3A5C; font-size: 1rem; margin-bottom: 6px;">
            Unlock AI-Powered Analysis
        </div>
        <div style="color: #4A6A8A; font-size: 0.92rem; line-height: 1.5;">
            For full AI functionality — including document analysis, credit commentary, and
            variance insights — enter your Anthropic API key below.
            Get one at <a href="https://console.anthropic.com" target="_blank" style="color: #2E6B9E; font-weight: 500;">console.anthropic.com</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    api_key_home = st.text_input(
        "Anthropic API Key",
        value="",
        type="password",
        placeholder="sk-ant-...",
        help="Your key is stored only in your browser session and never saved to disk.",
        key="api_key_home",
    )
    if api_key_home:
        st.session_state.anthropic_api_key = api_key_home
        st.rerun()
else:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #F0FAF4, #E6F5EC);
        border: 1px solid #A8D8B9;
        border-left: 4px solid #2D8B57;
        border-radius: 10px;
        padding: 16px 24px;
        margin-bottom: 24px;
    ">
        <div style="color: #1D6B3F; font-size: 0.92rem;">
            <strong>AI features are active.</strong> Claude-powered analysis is available across all tools.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- Feature cards ---
st.markdown("""
<div style="
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
">
    <div style="
        font-size: 1.1rem;
        font-weight: 600;
        color: #1B3A5C;
        letter-spacing: 0.02em;
    ">Tools & Features</div>
    <div style="
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, #D6E4F0, transparent);
    "></div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    feature_card(
        "📈", "Credit Analysis",
        "Build and track credit models with leverage ratios, interest coverage, "
        "free cash flow analysis, and margin trends across quarters.",
        "pages/1_Credit_Analysis.py", "Open Credit Analysis",
    )

    feature_card(
        "📄", "Document Analysis",
        "Upload sell-side reports and earnings transcripts to extract key data points, "
        "summarize insights, and translate views into model assumptions.",
        "pages/3_Document_Analysis.py", "Open Document Analysis",
    )

    feature_card(
        "📋", "3-Statement Model Summary",
        "Upload a 3-statement financial model and get a credit-focused summary with "
        "auto-calculated metrics, trend charts, and AI commentary.",
        "pages/5_Model_Summary.py", "Open Model Summary",
    )

with col2:
    feature_card(
        "🔄", "Consensus Comparison",
        "Compare your estimates against Street consensus with side-by-side comparison, "
        "variance analysis with visual flags, and AI-powered commentary.",
        "pages/2_Consensus_Comparison.py", "Open Consensus Comparison",
    )

    feature_card(
        "💼", "Portfolio Fit Analysis",
        "Evaluate how a bond fits your portfolio with duration and yield impact, "
        "credit quality assessment, and sector concentration analysis.",
        "pages/4_Portfolio_Fit.py", "Open Portfolio Fit",
    )

    feature_card(
        "📖", "Key Terms & Concepts",
        "Quick reference guide with 90+ fixed income terms covering bond basics, "
        "yield, spreads, credit ratios, and market terminology.",
        "pages/6_Key_Terms.py", "Open Key Terms",
    )

st.markdown("---")
st.markdown("""
<div style="
    text-align: center;
    padding: 16px 0 8px 0;
    color: #94A3B8;
    font-size: 0.85rem;
">
    <span style="letter-spacing: 0.03em;">
        Built with Streamlit &nbsp;&bull;&nbsp; AI powered by Claude &nbsp;&bull;&nbsp; Fixed Income Analyst Workbench
    </span>
</div>
""", unsafe_allow_html=True)
