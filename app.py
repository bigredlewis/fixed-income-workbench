"""
Fixed Income Analyst Workbench
A tool for fundamental fixed income analysts to streamline credit analysis,
compare estimates to consensus, analyze sell-side reports, and evaluate portfolio fit.
"""

import streamlit as st

st.set_page_config(
    page_title="Fixed Income Analyst Workbench",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Sidebar branding ---
st.sidebar.title("FI Analyst Workbench")
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

# --- Home page content ---
st.title("Fixed Income Analyst Workbench")
st.markdown(
    """
    Welcome! This workbench helps fundamental fixed income analysts work more
    efficiently. Use the sidebar to navigate between tools.
    """
)

st.markdown("---")

# Feature cards
col1, col2 = st.columns(2)

with col1:
    st.subheader("Credit Analysis")
    st.markdown(
        """
        Build and track credit models with key metrics:
        - Leverage ratios (Debt/EBITDA)
        - Interest coverage
        - Free cash flow analysis
        - Margin trends across quarters
        """
    )
    st.page_link("pages/1_Credit_Analysis.py", label="Open Credit Analysis", icon="📈")

    st.markdown("---")

    st.subheader("Document Analysis")
    st.markdown(
        """
        Upload sell-side reports and earnings transcripts:
        - Extract key financial data points
        - Summarize qualitative insights
        - Translate qualitative views into model assumptions
        """
    )
    st.page_link("pages/3_Document_Analysis.py", label="Open Document Analysis", icon="📄")

with col2:
    st.subheader("Consensus Comparison")
    st.markdown(
        """
        Compare your estimates against Street consensus:
        - Side-by-side metric comparison
        - Variance analysis with visual flags
        - Track where you differ and why
        """
    )
    st.page_link("pages/2_Consensus_Comparison.py", label="Open Consensus Comparison", icon="🔄")

    st.markdown("---")

    st.subheader("Portfolio Fit Analysis")
    st.markdown(
        """
        Evaluate how a bond fits your portfolio:
        - Duration and yield impact
        - Credit quality and sector concentration
        - Risk contribution analysis
        """
    )
    st.page_link("pages/4_Portfolio_Fit.py", label="Open Portfolio Fit", icon="💼")

st.markdown("---")

# Third row - centered
col3, col4 = st.columns(2)
with col3:
    st.subheader("3-Statement Model Summary")
    st.markdown(
        """
        Upload a 3-statement financial model and get a credit-focused summary:
        - Auto-calculates leverage, coverage, and FCF metrics
        - Trend charts across historical periods
        - AI-powered credit commentary and rating estimate
        """
    )
    st.page_link("pages/5_Model_Summary.py", label="Open Model Summary", icon="📋")

with col4:
    st.subheader("Key Terms & Concepts")
    st.markdown(
        """
        Quick reference guide for fixed income analysts:
        - Bond basics, yield, spread, and duration concepts
        - Credit ratios and rating agency frameworks
        - Bond structures, covenants, and market terminology
        """
    )
    st.page_link("pages/6_Key_Terms.py", label="Open Key Terms", icon="📖")

st.markdown("---")
st.caption("Built with Streamlit | AI powered by Claude")
