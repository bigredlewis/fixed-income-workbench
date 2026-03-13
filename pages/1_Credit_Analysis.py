"""
Credit Analysis page - Build and track credit models with key metrics.
Upload Excel or enter data manually.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.calculations import calculate_credit_metrics, rate_metric
from utils.templates import create_credit_analysis_template
from utils.styles import inject_custom_css, CHART_COLORS, PLOTLY_LAYOUT

st.set_page_config(page_title="Credit Analysis", page_icon="📈", layout="wide")
inject_custom_css()
st.title("Credit Analysis Model")
st.markdown("""
<p style="color: #64748B; font-size: 1.05rem; margin-top: -0.5em; margin-bottom: 1em;">
    Upload an Excel file with quarterly financials or enter data manually to calculate key credit metrics.
</p>
""", unsafe_allow_html=True)

# --- Initialize session state ---
if "credit_data" not in st.session_state:
    st.session_state.credit_data = {}
if "current_issuer" not in st.session_state:
    st.session_state.current_issuer = ""

# --- Issuer selection ---
st.sidebar.subheader("Issuer")
issuer_name = st.sidebar.text_input("Issuer / Company Name", value=st.session_state.current_issuer)
if issuer_name:
    st.session_state.current_issuer = issuer_name
    if issuer_name not in st.session_state.credit_data:
        st.session_state.credit_data[issuer_name] = {}

if not issuer_name:
    st.info("Enter an issuer name in the sidebar to get started.")
    st.stop()

st.subheader(f"Credit Model: {issuer_name}")

# --- Column matching keywords (order = priority) ---
# Each internal field maps to a list of keywords to search for in column headers
COLUMN_KEYWORDS = {
    "revenue": ["revenue", "net sales", "total sales", "sales"],
    "ebitda": ["ebitda"],
    "depreciation": ["d&a", "depreciation", "amortization", "dep"],
    "total_debt": ["total debt", "debt"],
    "cash": ["cash"],
    "interest_expense": ["interest expense", "interest exp", "interest"],
    "capex": ["capital expenditure", "capex", "cap ex"],
    "taxes": ["cash taxes", "taxes", "tax"],
    "working_capital_change": ["working capital", "wc change", "wc"],
}


def match_columns(df_columns):
    """Match DataFrame columns to internal field names using keyword search."""
    mapping = {}
    used_cols = set()

    # First column is always assumed to be the period/label column
    mapping[df_columns[0]] = "period"
    used_cols.add(df_columns[0])

    # Match remaining columns by keywords
    for internal_key, keywords in COLUMN_KEYWORDS.items():
        for kw in keywords:
            for col in df_columns:
                if col in used_cols:
                    continue
                if kw in str(col).lower():
                    mapping[col] = internal_key
                    used_cols.add(col)
                    break
            if internal_key in mapping.values():
                break

    return mapping


def safe_sort_period(p):
    """Sort periods chronologically, handling various formats gracefully."""
    p = str(p).strip()
    parts = p.split()
    q_order = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4, "FY": 5}

    if len(parts) == 2:
        try:
            year = int(parts[1])
            q = q_order.get(parts[0].upper(), 0)
            return (year, q)
        except ValueError:
            pass

    # Try to extract any 4-digit year
    for part in parts:
        try:
            val = int(part)
            if 2000 <= val <= 2099:
                return (val, 0)
        except ValueError:
            continue

    # Fallback: sort alphabetically
    return (0, p)


# --- Data input: Upload or Manual ---
input_tab1, input_tab2 = st.tabs(["Upload Excel", "Manual Entry"])

with input_tab1:
    st.markdown("Upload an Excel file with quarterly financial data. Download the template to see the expected format.")

    template_buf = create_credit_analysis_template()
    st.download_button(
        "Download Excel Template",
        data=template_buf,
        file_name="credit_analysis_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    uploaded = st.file_uploader("Upload Financial Data (Excel)", type=["xlsx", "xls"], key="credit_upload")

    if uploaded is not None:
        try:
            uploaded.seek(0)
            df = pd.read_excel(uploaded)

            # Drop fully empty rows
            df = df.dropna(how="all").reset_index(drop=True)

            # Drop rows where the first column is NaN or looks like a note
            first_col = df.columns[0]
            df = df[df[first_col].notna()].reset_index(drop=True)
            # Filter out rows that start with "Note" or similar
            df = df[~df[first_col].astype(str).str.lower().str.startswith(("note", "-", "#"))].reset_index(drop=True)

            # Match columns
            col_mapping = match_columns(df.columns.tolist())

            # Show what was matched
            st.markdown("**Column Mapping:**")
            match_display = {orig: internal for orig, internal in col_mapping.items()}
            unmatched = [c for c in df.columns if c not in col_mapping]
            st.json(match_display)
            if unmatched:
                st.caption(f"Unmatched columns (ignored): {unmatched}")

            df_renamed = df.rename(columns=col_mapping)

            st.markdown("**Preview of uploaded data:**")
            st.dataframe(df_renamed.head(10), use_container_width=True)

            if st.button("Import All Quarters", type="primary"):
                imported = 0
                for _, row in df_renamed.iterrows():
                    period_val = str(row.get("period", "")).strip()
                    if not period_val or period_val == "nan" or period_val == "None":
                        continue

                    financials = {}
                    for internal_key in COLUMN_KEYWORDS.keys():
                        val = row.get(internal_key, 0)
                        try:
                            financials[internal_key] = float(val) if pd.notna(val) else 0.0
                        except (ValueError, TypeError):
                            financials[internal_key] = 0.0

                    st.session_state.credit_data[issuer_name][period_val] = financials
                    imported += 1

                if imported > 0:
                    st.success(f"Imported {imported} quarters for {issuer_name}")
                    st.rerun()
                else:
                    st.warning("No data rows found. Check that your file has data below the header row.")

        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.markdown("**Troubleshooting:**")
            st.markdown("- Make sure the file is a valid .xlsx file")
            st.markdown("- The first row should be column headers")
            st.markdown("- Data should start on row 2")
            st.markdown("- Download the template above for the expected format")

with input_tab2:
    with st.expander("Add / Edit Quarter Data", expanded=True):
        col_period, col_year = st.columns(2)
        with col_period:
            quarter = st.selectbox("Quarter", ["Q1", "Q2", "Q3", "Q4", "FY"])
        with col_year:
            year = st.number_input("Year", min_value=2015, max_value=2030, value=2025)

        period_key = f"{quarter} {year}"
        existing = st.session_state.credit_data[issuer_name].get(period_key, {})

        st.markdown("**Income Statement ($ millions)**")
        col1, col2, col3 = st.columns(3)
        with col1:
            revenue = st.number_input("Revenue", value=existing.get("revenue", 0.0), step=10.0, format="%.1f", key="rev")
        with col2:
            ebitda = st.number_input("EBITDA", value=existing.get("ebitda", 0.0), step=5.0, format="%.1f", key="ebitda")
        with col3:
            depreciation = st.number_input("D&A", value=existing.get("depreciation", 0.0), step=1.0, format="%.1f", key="da")

        st.markdown("**Balance Sheet & Cash Flow ($ millions)**")
        col4, col5, col6 = st.columns(3)
        with col4:
            total_debt = st.number_input("Total Debt", value=existing.get("total_debt", 0.0), step=10.0, format="%.1f", key="debt")
        with col5:
            cash = st.number_input("Cash & Equivalents", value=existing.get("cash", 0.0), step=5.0, format="%.1f", key="cash")
        with col6:
            interest_expense = st.number_input("Interest Expense", value=existing.get("interest_expense", 0.0), step=1.0, format="%.1f", key="int_exp")

        col7, col8, col9 = st.columns(3)
        with col7:
            capex = st.number_input("Capital Expenditures", value=existing.get("capex", 0.0), step=5.0, format="%.1f", key="capex")
        with col8:
            taxes = st.number_input("Cash Taxes", value=existing.get("taxes", 0.0), step=1.0, format="%.1f", key="taxes")
        with col9:
            wc_change = st.number_input("Working Capital Change", value=existing.get("working_capital_change", 0.0), step=1.0, format="%.1f", key="wc",
                                         help="Positive = cash used, Negative = cash generated")

        if st.button("Save Quarter", type="primary"):
            st.session_state.credit_data[issuer_name][period_key] = {
                "revenue": revenue, "ebitda": ebitda, "depreciation": depreciation,
                "total_debt": total_debt, "cash": cash, "interest_expense": interest_expense,
                "capex": capex, "taxes": taxes, "working_capital_change": wc_change,
            }
            st.success(f"Saved {period_key} data for {issuer_name}")
            st.rerun()

# --- Display saved data and metrics ---
issuer_data = st.session_state.credit_data.get(issuer_name, {})

if not issuer_data:
    st.info("No quarterly data yet. Upload an Excel file or enter data manually above.")
    st.stop()

st.markdown("---")
st.subheader("Credit Metrics Summary")

sorted_periods = sorted(issuer_data.keys(), key=safe_sort_period)

all_metrics = {}
for period in sorted_periods:
    all_metrics[period] = calculate_credit_metrics(issuer_data[period])

metric_display_names = {
    "gross_leverage": "Gross Leverage (Debt/EBITDA)",
    "net_leverage": "Net Leverage",
    "interest_coverage": "Interest Coverage (EBITDA/Int.Exp)",
    "ebitda_margin": "EBITDA Margin (%)",
    "free_cash_flow": "Free Cash Flow ($M)",
    "fcf_to_debt": "FCF / Debt (%)",
    "cash_to_debt": "Cash / Debt (%)",
    "net_debt": "Net Debt ($M)",
}

rows = []
for metric_key, display_name in metric_display_names.items():
    row = {"Metric": display_name}
    for period in sorted_periods:
        val = all_metrics[period].get(metric_key)
        row[period] = round(val, 2) if val is not None else "N/A"
    latest_val = all_metrics[sorted_periods[-1]].get(metric_key)
    row["Assessment"] = rate_metric(metric_key, latest_val)
    rows.append(row)

metrics_df = pd.DataFrame(rows).set_index("Metric")
st.dataframe(metrics_df, use_container_width=True)

# --- Trend Charts ---
st.markdown("---")
st.subheader("Trend Analysis")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig_lev = go.Figure()
    fig_lev.add_trace(go.Scatter(x=sorted_periods, y=[all_metrics[p]["gross_leverage"] for p in sorted_periods],
                                  mode="lines+markers", name="Gross Leverage", line=dict(color=CHART_COLORS["primary"])))
    fig_lev.add_trace(go.Scatter(x=sorted_periods, y=[all_metrics[p]["net_leverage"] for p in sorted_periods],
                                  mode="lines+markers", name="Net Leverage", line=dict(color=CHART_COLORS["accent"])))
    fig_lev.update_layout(title="Leverage Trend", yaxis_title="x EBITDA", height=350, **PLOTLY_LAYOUT)
    st.plotly_chart(fig_lev, use_container_width=True)

with chart_col2:
    fig_cov = go.Figure()
    fig_cov.add_trace(go.Scatter(x=sorted_periods, y=[all_metrics[p]["interest_coverage"] for p in sorted_periods],
                                  mode="lines+markers", name="Interest Coverage", line=dict(color=CHART_COLORS["positive"])))
    fig_cov.update_layout(title="Interest Coverage Trend", yaxis_title="x", height=350, **PLOTLY_LAYOUT)
    st.plotly_chart(fig_cov, use_container_width=True)

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    fig_margin = go.Figure()
    fig_margin.add_trace(go.Bar(x=sorted_periods, y=[all_metrics[p]["ebitda_margin"] for p in sorted_periods],
                                 name="EBITDA Margin", marker_color=CHART_COLORS["secondary"]))
    fig_margin.update_layout(title="EBITDA Margin Trend", yaxis_title="%", height=350, **PLOTLY_LAYOUT)
    st.plotly_chart(fig_margin, use_container_width=True)

with chart_col4:
    fcf_vals = [all_metrics[p]["free_cash_flow"] for p in sorted_periods]
    colors = [CHART_COLORS["positive"] if v >= 0 else CHART_COLORS["negative"] for v in fcf_vals]
    fig_fcf = go.Figure()
    fig_fcf.add_trace(go.Bar(x=sorted_periods, y=fcf_vals, name="FCF", marker_color=colors))
    fig_fcf.update_layout(title="Free Cash Flow Trend", yaxis_title="$ Millions", height=350, **PLOTLY_LAYOUT)
    st.plotly_chart(fig_fcf, use_container_width=True)

# --- Export & Manage ---
st.markdown("---")
with st.expander("Export / Manage Data"):
    export_rows = []
    for period in sorted_periods:
        row = {"Period": period}
        row.update(issuer_data[period])
        row.update({f"calc_{k}": v for k, v in all_metrics[period].items()})
        export_rows.append(row)
    export_df = pd.DataFrame(export_rows)
    csv = export_df.to_csv(index=False)
    st.download_button("Download as CSV", data=csv, file_name=f"{issuer_name}_credit_analysis.csv", mime="text/csv")

    st.markdown("---")
    del_period = st.selectbox("Delete a quarter", sorted_periods)
    if st.button("Delete Selected Quarter", type="secondary"):
        del st.session_state.credit_data[issuer_name][del_period]
        st.rerun()
