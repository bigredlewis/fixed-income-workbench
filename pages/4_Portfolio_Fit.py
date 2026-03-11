"""
Portfolio Fit Analysis - Upload portfolio holdings, get an overview, and evaluate candidate bonds.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.calculations import RATING_SCALE, RATING_SCALE_REVERSE, numeric_to_rating
from utils.templates import create_portfolio_holdings_template

st.set_page_config(page_title="Portfolio Fit", page_icon="💼", layout="wide")
st.title("Portfolio Fit Analysis")
st.markdown(
    "Upload your portfolio holdings to get an overview, then evaluate how a candidate bond "
    "would impact duration, yield, credit quality, and sector concentration."
)

# --- Initialize session state ---
if "portfolio_holdings" not in st.session_state:
    st.session_state.portfolio_holdings = None
if "portfolio_stats" not in st.session_state:
    st.session_state.portfolio_stats = None

SECTORS = [
    "Financials", "Industrials", "Utilities", "Energy", "Technology",
    "Healthcare", "Consumer Staples", "Consumer Discretionary",
    "Telecom/Media", "Real Estate", "Other",
]

# =========================================================================
# SECTION 1: PORTFOLIO UPLOAD
# =========================================================================
st.subheader("1. Portfolio Holdings")

template_buf = create_portfolio_holdings_template()
st.download_button(
    "Download Holdings Template",
    data=template_buf,
    file_name="portfolio_holdings_template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

uploaded = st.file_uploader("Upload Portfolio Holdings (Excel)", type=["xlsx", "xls"], key="port_upload")

if uploaded is not None:
    try:
        df = pd.read_excel(uploaded)

        # Normalize column names for matching
        col_map = {}
        for c in df.columns:
            cl = str(c).lower().strip()
            if "issuer" in cl or "name" in cl or "company" in cl:
                col_map[c] = "Issuer"
            elif "cusip" in cl or "isin" in cl:
                col_map[c] = "CUSIP"
            elif "description" in cl or "desc" in cl or "bond" in cl:
                col_map[c] = "Description"
            elif "sector" in cl or "industry" in cl:
                col_map[c] = "Sector"
            elif "rating" in cl or "credit" in cl:
                col_map[c] = "Rating"
            elif "coupon" in cl:
                col_map[c] = "Coupon"
            elif "ytm" in cl or "yield" in cl:
                col_map[c] = "YTM"
            elif "duration" in cl or "dur" in cl:
                col_map[c] = "Duration"
            elif "spread" in cl or "oas" in cl:
                col_map[c] = "Spread"
            elif "par" in cl:
                col_map[c] = "Par"
            elif "market" in cl or "mv" in cl:
                col_map[c] = "MV"
            elif "weight" in cl or "wt" in cl or "%" in cl:
                col_map[c] = "Weight"

        df_mapped = df.rename(columns=col_map)

        st.markdown("**Uploaded Holdings:**")
        st.dataframe(df_mapped, use_container_width=True)

        if st.button("Load Portfolio", type="primary"):
            # Calculate weights if not provided
            if "Weight" not in df_mapped.columns and "MV" in df_mapped.columns:
                total_mv = df_mapped["MV"].sum()
                if total_mv > 0:
                    df_mapped["Weight"] = (df_mapped["MV"] / total_mv) * 100

            st.session_state.portfolio_holdings = df_mapped

            # Calculate portfolio-level stats
            weights = df_mapped.get("Weight", pd.Series([100 / len(df_mapped)] * len(df_mapped)))
            weight_sum = weights.sum()
            norm_weights = weights / weight_sum if weight_sum > 0 else weights

            stats = {}

            # Weighted average duration
            if "Duration" in df_mapped.columns:
                stats["duration"] = (df_mapped["Duration"].fillna(0) * norm_weights).sum()

            # Weighted average yield
            if "YTM" in df_mapped.columns:
                stats["yield"] = (df_mapped["YTM"].fillna(0) * norm_weights).sum()

            # Weighted average coupon
            if "Coupon" in df_mapped.columns:
                stats["coupon"] = (df_mapped["Coupon"].fillna(0) * norm_weights).sum()

            # Weighted average spread
            if "Spread" in df_mapped.columns:
                stats["spread"] = (df_mapped["Spread"].fillna(0) * norm_weights).sum()

            # Weighted average rating
            if "Rating" in df_mapped.columns:
                rating_nums = df_mapped["Rating"].map(RATING_SCALE).fillna(10)
                stats["avg_rating_numeric"] = (rating_nums * norm_weights).sum()
                stats["avg_rating"] = numeric_to_rating(stats["avg_rating_numeric"])

            # Sector weights
            if "Sector" in df_mapped.columns:
                sector_weights = {}
                for _, row in df_mapped.iterrows():
                    s = row.get("Sector", "Other")
                    w = row.get("Weight", 100 / len(df_mapped))
                    # Normalize
                    w_norm = (w / weight_sum * 100) if weight_sum > 0 else w
                    sector_weights[s] = sector_weights.get(s, 0) + w_norm
                stats["sector_weights"] = sector_weights

            # Total market value
            if "MV" in df_mapped.columns:
                stats["total_mv"] = df_mapped["MV"].sum()

            # Number of holdings
            stats["num_holdings"] = len(df_mapped)

            st.session_state.portfolio_stats = stats
            st.success(f"Loaded {len(df_mapped)} holdings")
            st.rerun()

    except Exception as e:
        st.error(f"Error reading file: {str(e)}")

# --- Portfolio Overview ---
holdings = st.session_state.portfolio_holdings
stats = st.session_state.portfolio_stats

if holdings is not None and stats is not None:
    st.markdown("---")
    st.subheader("Portfolio Overview")

    # Summary metrics
    mcol1, mcol2, mcol3, mcol4, mcol5 = st.columns(5)
    with mcol1:
        st.metric("Holdings", stats.get("num_holdings", 0))
    with mcol2:
        st.metric("Avg Duration", f"{stats.get('duration', 0):.2f}y")
    with mcol3:
        st.metric("Avg Yield", f"{stats.get('yield', 0):.2f}%")
    with mcol4:
        st.metric("Avg Rating", stats.get("avg_rating", "N/A"))
    with mcol5:
        st.metric("Avg Spread", f"{stats.get('spread', 0):.0f} bps")

    # Charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        sector_w = stats.get("sector_weights", {})
        if sector_w:
            filtered = {k: v for k, v in sector_w.items() if v > 0}
            fig_sector = go.Figure(go.Pie(
                labels=list(filtered.keys()),
                values=list(filtered.values()),
                textinfo="label+percent",
                hole=0.3,
            ))
            fig_sector.update_layout(title="Sector Allocation", height=400)
            st.plotly_chart(fig_sector, use_container_width=True)

    with chart_col2:
        if "Rating" in holdings.columns:
            rating_counts = holdings["Rating"].value_counts()
            # Sort by rating quality
            sorted_ratings = sorted(rating_counts.index,
                                     key=lambda r: RATING_SCALE.get(r, 99))
            fig_rating = go.Figure(go.Bar(
                x=sorted_ratings,
                y=[rating_counts[r] for r in sorted_ratings],
                marker_color="steelblue",
            ))
            fig_rating.update_layout(title="Rating Distribution",
                                      xaxis_title="Credit Rating",
                                      yaxis_title="Number of Holdings",
                                      height=400, template="plotly_white")
            st.plotly_chart(fig_rating, use_container_width=True)

    # Holdings table
    with st.expander("Full Holdings Table"):
        st.dataframe(holdings, use_container_width=True)

    # =========================================================================
    # SECTION 2: CANDIDATE BOND ANALYSIS
    # =========================================================================
    st.markdown("---")
    st.subheader("2. Evaluate Candidate Bond")
    st.markdown("Enter details of a bond you're considering adding to the portfolio.")

    bcol1, bcol2, bcol3 = st.columns(3)
    with bcol1:
        bond_issuer = st.text_input("Bond Issuer", placeholder="e.g., Company XYZ")
        bond_duration = st.number_input("Duration (years)", value=4.0, step=0.1, format="%.2f", key="bond_dur")
        bond_coupon = st.number_input("Coupon (%)", value=5.00, step=0.05, format="%.2f")
    with bcol2:
        bond_maturity = st.text_input("Maturity Date", placeholder="e.g., 06/2030")
        bond_yield = st.number_input("Yield to Maturity (%)", value=5.25, step=0.05, format="%.2f")
        bond_spread = st.number_input("OAS / Spread (bps)", value=150, step=5)
    with bcol3:
        bond_rating = st.selectbox("Credit Rating", list(RATING_SCALE.keys()), index=9, key="bond_rating")
        bond_sector = st.selectbox("Sector", SECTORS)
        allocation_pct = st.slider("Allocation (% of portfolio)", 0.5, 20.0, 2.0, 0.5)

    if st.button("Analyze Portfolio Impact", type="primary"):
        alloc = allocation_pct / 100.0
        remaining = 1.0 - alloc

        # Duration impact
        dur_before = stats.get("duration", 0)
        dur_after = dur_before * remaining + bond_duration * alloc
        dur_change = dur_after - dur_before

        # Yield impact
        yld_before = stats.get("yield", 0)
        yld_after = yld_before * remaining + bond_yield * alloc
        yld_change = yld_after - yld_before

        # Rating impact
        rat_before = stats.get("avg_rating_numeric", 10)
        rat_after = rat_before * remaining + RATING_SCALE[bond_rating] * alloc
        rat_change = rat_after - rat_before

        # Spread impact
        sprd_before = stats.get("spread", 0)
        sprd_after = sprd_before * remaining + bond_spread * alloc
        sprd_change = sprd_after - sprd_before

        st.markdown("---")
        st.subheader("Impact Analysis")

        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        with mcol1:
            st.metric("Duration", f"{dur_after:.2f}y", delta=f"{dur_change:+.2f}y", delta_color="inverse")
        with mcol2:
            st.metric("Yield", f"{yld_after:.2f}%", delta=f"{yld_change:+.2f}%")
        with mcol3:
            st.metric("Avg Rating", numeric_to_rating(rat_after),
                       delta=f"{rat_change:+.1f} notches", delta_color="inverse")
        with mcol4:
            st.metric("Avg Spread", f"{sprd_after:.0f} bps", delta=f"{sprd_change:+.0f} bps")

        # Sector impact
        sector_w = dict(stats.get("sector_weights", {}))
        new_sector_w = {k: v * remaining for k, v in sector_w.items()}
        new_sector_w[bond_sector] = new_sector_w.get(bond_sector, 0) + alloc * 100

        chart_c1, chart_c2 = st.columns(2)
        with chart_c1:
            # Before/After bar chart
            categories = ["Duration (yrs)", "Yield (%)", "Spread (bps/10)"]
            before = [dur_before, yld_before, sprd_before / 10]
            after = [dur_after, yld_after, sprd_after / 10]
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Before", x=categories, y=before, marker_color="lightsteelblue"))
            fig.add_trace(go.Bar(name="After", x=categories, y=after, marker_color="steelblue"))
            fig.update_layout(barmode="group", title="Portfolio Metrics: Before vs After",
                              height=400, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

        with chart_c2:
            filtered = {k: v for k, v in new_sector_w.items() if v > 0}
            colors = ["steelblue" if k == bond_sector else "lightsteelblue" for k in filtered]
            fig_s = go.Figure(go.Pie(
                labels=list(filtered.keys()), values=list(filtered.values()),
                marker=dict(colors=colors), textinfo="label+percent", hole=0.3))
            fig_s.update_layout(title="Sector Allocation (After)", height=400)
            st.plotly_chart(fig_s, use_container_width=True)

        # Risk flags
        st.markdown("---")
        st.subheader("Risk Flags")
        warnings = []

        sector_weight_after = new_sector_w.get(bond_sector, 0)
        if sector_weight_after > 25:
            warnings.append(f"**High Sector Concentration:** {bond_sector} would be {sector_weight_after:.1f}% of the portfolio (>25% threshold)")
        elif sector_weight_after > 15:
            warnings.append(f"**Elevated Sector Weight:** {bond_sector} would be {sector_weight_after:.1f}% of the portfolio")

        if abs(dur_change) > 0.5:
            warnings.append(f"**Duration Drift:** Portfolio duration changes by {dur_change:+.2f} years. Verify this aligns with your duration target.")

        if rat_change > 0.5:
            warnings.append(f"**Credit Quality Dilution:** Average credit quality moves from {numeric_to_rating(rat_before)} toward {numeric_to_rating(rat_after)}.")

        quality_gap = RATING_SCALE[bond_rating] - rat_before
        if quality_gap > 3:
            warnings.append(f"**Quality Gap:** This bond ({bond_rating}) is {quality_gap:.0f} notches below your portfolio average ({numeric_to_rating(rat_before)}).")

        if warnings:
            for w in warnings:
                st.warning(w)
        else:
            st.success("No significant risk flags. This bond appears compatible with the portfolio.")

        # Summary table
        st.markdown("---")
        with st.expander("Bond Details"):
            st.markdown(f"""
| Field | Value |
|---|---|
| **Issuer** | {bond_issuer or 'N/A'} |
| **Rating** | {bond_rating} |
| **Maturity** | {bond_maturity or 'N/A'} |
| **Coupon** | {bond_coupon:.2f}% |
| **YTM** | {bond_yield:.2f}% |
| **OAS** | {bond_spread} bps |
| **Duration** | {bond_duration:.2f}y |
| **Sector** | {bond_sector} |
| **Allocation** | {allocation_pct:.1f}% |
            """)

else:
    st.info("Upload your portfolio holdings above to get started. Download the template to see the expected format.")
