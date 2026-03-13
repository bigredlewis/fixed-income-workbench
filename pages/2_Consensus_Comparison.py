"""
Consensus Comparison page - Upload or enter your estimates vs Street consensus.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.ai_analysis import generate_variance_commentary
from utils.templates import create_consensus_template
from utils.pdf_export import create_analysis_pdf
from utils.styles import inject_custom_css, CHART_COLORS, PLOTLY_LAYOUT

st.set_page_config(page_title="Consensus Comparison", page_icon="🔄", layout="wide")
inject_custom_css()
st.title("Consensus Comparison")
st.markdown("""
<p style="color: #64748B; font-size: 1.05rem; margin-top: -0.5em; margin-bottom: 1em;">
    Upload an Excel file with your estimates and consensus estimates,
    or enter them manually. The tool flags variances and helps you understand the implications.
</p>
""", unsafe_allow_html=True)

# --- Initialize session state ---
if "consensus_data" not in st.session_state:
    st.session_state.consensus_data = {}

# --- Issuer & Period ---
col_issuer, col_period = st.columns(2)
with col_issuer:
    issuer = st.text_input("Issuer / Company Name", key="cons_issuer")
with col_period:
    period = st.text_input("Period (e.g., FY 2025, Q3 2025)", key="cons_period")

if not issuer or not period:
    st.info("Enter an issuer name and period to get started.")
    st.stop()

existing_key = f"{issuer}|{period}"

# --- Data Input: Upload or Manual ---
METRICS = [
    ("Revenue ($M)", "revenue"),
    ("EBITDA ($M)", "ebitda"),
    ("EBITDA Margin (%)", "ebitda_margin"),
    ("Net Income ($M)", "net_income"),
    ("EPS ($)", "eps"),
    ("Total Debt ($M)", "total_debt"),
    ("Leverage (Debt/EBITDA)", "leverage"),
    ("Interest Coverage (x)", "interest_coverage"),
    ("Free Cash Flow ($M)", "fcf"),
    ("Capex ($M)", "capex"),
    ("Revenue Growth (%)", "revenue_growth"),
]

input_tab1, input_tab2 = st.tabs(["Upload Excel", "Manual Entry"])

with input_tab1:
    st.markdown("Upload an Excel file with columns: **Metric**, **Your Estimate**, **Consensus**. Download the template to see the format.")

    template_buf = create_consensus_template()
    st.download_button(
        "Download Excel Template",
        data=template_buf,
        file_name="consensus_comparison_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    uploaded = st.file_uploader("Upload Estimates (Excel)", type=["xlsx", "xls"], key="cons_upload")

    if uploaded is not None:
        try:
            df = pd.read_excel(uploaded)
            st.markdown("**Preview:**")
            st.dataframe(df, use_container_width=True)

            if st.button("Import Estimates", type="primary", key="import_cons"):
                data = {}
                # Try to find the right columns
                cols = df.columns.tolist()
                metric_col = cols[0]  # First column is metric name
                yours_col = cols[1] if len(cols) > 1 else None
                cons_col = cols[2] if len(cols) > 2 else None

                for _, row in df.iterrows():
                    metric_name = str(row[metric_col]).strip()
                    # Match to our internal keys
                    matched_key = None
                    for display, key in METRICS:
                        if (display.lower().split("(")[0].strip() in metric_name.lower()
                                or metric_name.lower() in display.lower()):
                            matched_key = key
                            break
                    if matched_key is None:
                        # Try fuzzy match on key words
                        lower_name = metric_name.lower()
                        for display, key in METRICS:
                            if key.replace("_", " ") in lower_name or lower_name in key.replace("_", " "):
                                matched_key = key
                                break
                    if matched_key is None:
                        continue

                    yours_val = 0.0
                    cons_val = 0.0
                    if yours_col:
                        try:
                            yours_val = float(row[yours_col]) if pd.notna(row[yours_col]) else 0.0
                        except (ValueError, TypeError):
                            yours_val = 0.0
                    if cons_col:
                        try:
                            cons_val = float(row[cons_col]) if pd.notna(row[cons_col]) else 0.0
                        except (ValueError, TypeError):
                            cons_val = 0.0

                    data[matched_key] = {"yours": yours_val, "consensus": cons_val}

                st.session_state.consensus_data[existing_key] = data
                st.success(f"Imported {len(data)} metrics for {issuer} - {period}")
                st.rerun()
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

with input_tab2:
    existing_data = st.session_state.consensus_data.get(existing_key, {})

    with st.form("consensus_form"):
        st.markdown("**Enter your estimates and consensus for each metric:**")
        your_estimates = {}
        consensus_estimates = {}

        for display_name, key in METRICS:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{display_name}**")
            with col2:
                yours = st.number_input(
                    f"Your {display_name}",
                    value=existing_data.get(key, {}).get("yours", 0.0),
                    step=0.1, format="%.2f", key=f"yours_{key}",
                    label_visibility="collapsed",
                )
            with col3:
                cons = st.number_input(
                    f"Consensus {display_name}",
                    value=existing_data.get(key, {}).get("consensus", 0.0),
                    step=0.1, format="%.2f", key=f"cons_{key}",
                    label_visibility="collapsed",
                )
            your_estimates[key] = yours
            consensus_estimates[key] = cons

        submitted = st.form_submit_button("Save & Analyze", type="primary")

    if submitted:
        data = {}
        for _, key in METRICS:
            data[key] = {"yours": your_estimates[key], "consensus": consensus_estimates[key]}
        st.session_state.consensus_data[existing_key] = data
        st.success(f"Saved estimates for {issuer} - {period}")
        st.rerun()

# --- Display comparison ---
saved_data = st.session_state.consensus_data.get(existing_key, {})
if not saved_data:
    st.stop()

st.markdown("---")
st.subheader("Variance Analysis")

comparison_rows = []
yours_dict = {}
cons_dict = {}

for display_name, key in METRICS:
    entry = saved_data.get(key, {})
    yours_val = entry.get("yours", 0)
    cons_val = entry.get("consensus", 0)

    if yours_val == 0 and cons_val == 0:
        continue

    yours_dict[display_name] = yours_val
    cons_dict[display_name] = cons_val

    variance_pct = ((yours_val - cons_val) / abs(cons_val)) * 100 if cons_val != 0 else 0

    abs_var = abs(variance_pct)
    if abs_var <= 2:
        flag = "In-Line"
    elif abs_var <= 5:
        flag = "Slight Variance"
    elif abs_var <= 10:
        flag = "Notable Variance"
    else:
        flag = "Significant Variance"

    direction = "ABOVE" if variance_pct > 0 else "BELOW" if variance_pct < 0 else "AT"

    comparison_rows.append({
        "Metric": display_name,
        "Your Estimate": round(yours_val, 2),
        "Consensus": round(cons_val, 2),
        "Variance (%)": round(variance_pct, 1),
        "Direction": direction,
        "Assessment": flag,
    })

if comparison_rows:
    comp_df = pd.DataFrame(comparison_rows).set_index("Metric")

    def color_variance(val):
        if isinstance(val, str):
            if val == "In-Line":
                return "color: green"
            elif val == "Slight Variance":
                return "color: orange"
            elif "Variance" in val:
                return "color: red"
        if isinstance(val, (int, float)):
            if abs(val) <= 2:
                return "color: green"
            elif abs(val) <= 5:
                return "color: orange"
            else:
                return "color: red"
        return ""

    styled_df = comp_df.style.map(color_variance, subset=["Variance (%)", "Assessment"])
    st.dataframe(styled_df, use_container_width=True)

    # --- Charts ---
    st.markdown("---")
    st.subheader("Visual Comparison")

    chart_metrics = [r["Metric"] for r in comparison_rows]
    selected_metrics = st.multiselect("Select metrics to chart", chart_metrics, default=chart_metrics[:5])

    if selected_metrics:
        filtered = [r for r in comparison_rows if r["Metric"] in selected_metrics]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Your Estimate", x=[r["Metric"] for r in filtered],
                              y=[r["Your Estimate"] for r in filtered], marker_color=CHART_COLORS["primary"]))
        fig.add_trace(go.Bar(name="Consensus", x=[r["Metric"] for r in filtered],
                              y=[r["Consensus"] for r in filtered], marker_color=CHART_COLORS["highlight"]))
        fig.update_layout(barmode="group", title="Your Estimates vs. Consensus",
                          height=450, **PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    # Variance bar chart
    var_colors = [CHART_COLORS["positive"] if abs(r["Variance (%)"]) <= 2
                  else CHART_COLORS["warning"] if abs(r["Variance (%)"]) <= 5
                  else CHART_COLORS["negative"] for r in comparison_rows]
    var_fig = go.Figure()
    var_fig.add_trace(go.Bar(x=[r["Metric"] for r in comparison_rows],
                              y=[r["Variance (%)"] for r in comparison_rows],
                              marker_color=var_colors, name="Variance %"))
    var_fig.update_layout(title="Variance from Consensus (%)", yaxis_title="Variance %",
                          height=400, **PLOTLY_LAYOUT)
    var_fig.add_hline(y=5, line_dash="dash", line_color=CHART_COLORS["warning"], annotation_text="5% threshold")
    var_fig.add_hline(y=-5, line_dash="dash", line_color=CHART_COLORS["warning"])
    var_fig.add_hline(y=10, line_dash="dash", line_color=CHART_COLORS["negative"], annotation_text="10% threshold")
    var_fig.add_hline(y=-10, line_dash="dash", line_color=CHART_COLORS["negative"])
    st.plotly_chart(var_fig, use_container_width=True)

    # --- AI Commentary ---
    st.markdown("---")
    st.subheader("Variance Commentary")

    # Initialize session state for saving commentary
    if "consensus_commentary" not in st.session_state:
        st.session_state.consensus_commentary = {}

    commentary_key = f"{issuer}|{period}"

    if st.session_state.get("anthropic_api_key"):
        if st.button("Generate AI Commentary", type="primary"):
            with st.spinner("Analyzing variances with Claude..."):
                commentary = generate_variance_commentary(yours_dict, cons_dict)
                if commentary:
                    st.session_state.consensus_commentary[commentary_key] = commentary
                    st.rerun()
                else:
                    st.error("Failed to generate commentary. Check your API key.")
    else:
        st.info("Add your Anthropic API key in the sidebar (AI Settings) to enable AI-powered variance commentary.")

    # Display saved commentary and PDF download
    saved_commentary = st.session_state.consensus_commentary.get(commentary_key)
    if saved_commentary:
        st.markdown(saved_commentary)
        pdf_bytes = create_analysis_pdf(
            title=f"Consensus Variance Analysis: {issuer}",
            issuer=issuer,
            analysis_type=f"Consensus Comparison - {period}",
            content=saved_commentary,
        )
        st.download_button(
            "Download Commentary as PDF",
            data=pdf_bytes,
            file_name=f"{issuer}_{period}_variance_commentary.pdf",
            mime="application/pdf",
            key="pdf_consensus",
        )

    notes = st.text_area("Your Notes / Thesis",
                          placeholder="Explain why your estimates differ from consensus...", height=150)

    st.markdown("---")
    csv = comp_df.reset_index().to_csv(index=False)
    st.download_button("Export Comparison as CSV", data=csv,
                        file_name=f"{issuer}_{period}_consensus_comparison.csv", mime="text/csv")
