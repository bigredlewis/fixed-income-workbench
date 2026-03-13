"""
3-Statement Model Summary - Upload a financial model and get a credit-focused summary.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
from utils.templates import create_three_statement_template
from utils.ai_analysis import get_client
from utils.pdf_export import create_analysis_pdf
from utils.styles import inject_custom_css, CHART_COLORS, PLOTLY_LAYOUT

st.set_page_config(page_title="3-Statement Model Summary", page_icon="📋", layout="wide")
inject_custom_css()
st.title("3-Statement Model Summary")
st.markdown("""
<p style="color: #64748B; font-size: 1.05rem; margin-top: -0.5em; margin-bottom: 1em;">
    Upload a 3-statement financial model (Income Statement, Balance Sheet, Cash Flow)
    and get an automated credit-focused summary with key metrics and trends.
</p>
""", unsafe_allow_html=True)

# --- Template download ---
template_buf = create_three_statement_template()
st.download_button(
    "Download 3-Statement Template",
    data=template_buf,
    file_name="three_statement_model_template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

# --- File upload ---
issuer_name = st.text_input("Issuer / Company Name", placeholder="e.g., Company XYZ")
uploaded = st.file_uploader("Upload 3-Statement Model (Excel)", type=["xlsx", "xls"], key="model_upload")

if not uploaded or not issuer_name:
    st.info("Enter an issuer name and upload an Excel file with Income Statement, Balance Sheet, and Cash Flow Statement sheets.")
    st.stop()


def read_all_sheets(uploaded_file):
    """Read all sheets from an uploaded Excel file at once to avoid file pointer issues."""
    uploaded_file.seek(0)
    file_bytes = uploaded_file.read()
    buf = BytesIO(file_bytes)

    xl = pd.ExcelFile(buf)
    sheet_names = xl.sheet_names

    sheets = {}
    for sheet in sheet_names:
        buf.seek(0)
        df = pd.read_excel(buf, sheet_name=sheet)
        # Set first column as index (row labels)
        if len(df.columns) > 0:
            df = df.set_index(df.columns[0])
            df.index = df.index.map(lambda x: str(x).strip() if pd.notna(x) else "")
            df = df[df.index != ""]
            df = df[df.index != "nan"]
            # Convert columns to numeric
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        sheets[sheet] = df

    return sheets, sheet_names


def find_sheet(sheets, sheet_names, keywords):
    """Find a sheet by matching keywords against sheet names."""
    for kw in keywords:
        for name in sheet_names:
            if kw.lower() in name.lower():
                return sheets[name]
    return None


def find_row(df, keywords):
    """Find a row in a dataframe by matching keywords in the index."""
    if df is None:
        return None
    for idx in df.index:
        idx_lower = str(idx).lower()
        for kw in keywords:
            if kw.lower() in idx_lower:
                return df.loc[idx]
    return None


def safe_val(series, col_idx=-1):
    """Get a value from a series by position."""
    if series is None:
        return None
    try:
        if isinstance(series, pd.DataFrame):
            series = series.iloc[0]
        vals = series.dropna()
        if len(vals) == 0:
            return None
        if col_idx == -1:
            return float(vals.iloc[-1])
        if col_idx < len(series):
            val = series.iloc[col_idx]
            if pd.notna(val):
                return float(val)
        return None
    except (IndexError, TypeError, ValueError):
        return None


try:
    # Read all sheets at once (avoids file pointer issues)
    sheets, sheet_names = read_all_sheets(uploaded)

    st.caption(f"Sheets found in file: {', '.join(sheet_names)}")

    # Match sheets to statements
    income_stmt = find_sheet(sheets, sheet_names, ["income", "p&l", "profit", "is"])
    balance_sheet = find_sheet(sheets, sheet_names, ["balance", "bs", "position"])
    cash_flow = find_sheet(sheets, sheet_names, ["cash flow", "cf"])

    # If cash flow wasn't found but "cash" exists, check it's not the balance sheet cash row
    if cash_flow is None:
        cash_flow = find_sheet(sheets, sheet_names, ["cash"])
        # Verify it looks like a cash flow statement (has "operations" or "investing" rows)
        if cash_flow is not None:
            has_cf_rows = any("operat" in str(idx).lower() or "invest" in str(idx).lower()
                             for idx in cash_flow.index)
            if not has_cf_rows:
                cash_flow = None

    found_sheets = []
    if income_stmt is not None:
        found_sheets.append("Income Statement")
    if balance_sheet is not None:
        found_sheets.append("Balance Sheet")
    if cash_flow is not None:
        found_sheets.append("Cash Flow Statement")

    if not found_sheets:
        st.error(
            "Could not match any sheets to financial statements. "
            f"Your file has sheets: {', '.join(sheet_names)}. "
            "Expected sheet names containing 'Income', 'Balance', or 'Cash Flow'."
        )
        st.stop()

    st.success(f"Matched: {', '.join(found_sheets)}")

    # Show raw data
    with st.expander("View Raw Data"):
        if income_stmt is not None:
            st.markdown("**Income Statement**")
            st.dataframe(income_stmt, use_container_width=True)
        if balance_sheet is not None:
            st.markdown("**Balance Sheet**")
            st.dataframe(balance_sheet, use_container_width=True)
        if cash_flow is not None:
            st.markdown("**Cash Flow Statement**")
            st.dataframe(cash_flow, use_container_width=True)

    # =========================================================================
    # EXTRACT KEY METRICS
    # =========================================================================
    st.markdown("---")
    st.subheader(f"Credit Summary: {issuer_name}")

    # Get period columns (years)
    ref_df = income_stmt if income_stmt is not None else (balance_sheet if balance_sheet is not None else cash_flow)
    periods = [str(c) for c in ref_df.columns]

    # Extract key line items from income statement
    revenue_row = find_row(income_stmt, ["revenue", "net sales", "total sales", "net revenue"])
    ebitda_row = find_row(income_stmt, ["ebitda"])
    ebit_row = find_row(income_stmt, ["ebit", "operating income", "operating profit"])
    da_row = find_row(income_stmt, ["depreciation", "d&a", "amortization"])
    interest_row = find_row(income_stmt, ["interest expense", "interest cost"])
    net_income_row = find_row(income_stmt, ["net income", "net profit", "net earnings"])
    gross_profit_row = find_row(income_stmt, ["gross profit"])

    # Also check cash flow for D&A if not in income statement
    if da_row is None:
        da_row = find_row(cash_flow, ["depreciation", "d&a", "amortization"])

    # Extract from balance sheet
    cash_bs_row = find_row(balance_sheet, ["cash", "cash & equiv", "cash and equiv"])
    total_debt_lt = find_row(balance_sheet, ["long-term debt", "lt debt", "long term debt"])
    total_debt_st = find_row(balance_sheet, ["short-term debt", "st debt", "short term debt", "current portion"])
    total_assets_row = find_row(balance_sheet, ["total assets"])
    total_equity_row = find_row(balance_sheet, ["total equity", "stockholder", "shareholder"])
    total_liab_row = find_row(balance_sheet, ["total liabilities"])

    # Extract from cash flow
    cfo_row = find_row(cash_flow, ["cash from operations", "operating activities", "cash from ops"])
    capex_row = find_row(cash_flow, ["capital expenditure", "capex", "purchases of property"])

    # Also look for net income in cash flow if not in income statement
    if net_income_row is None:
        net_income_row = find_row(cash_flow, ["net income", "net profit"])

    # Calculate derived metrics for each period
    metrics_by_period = {}
    for i, period in enumerate(periods):
        m = {}

        m["revenue"] = safe_val(revenue_row, i)
        m["ebitda"] = safe_val(ebitda_row, i)

        # Calculate EBITDA from EBIT + D&A if not directly available
        if m["ebitda"] is None and ebit_row is not None and da_row is not None:
            ebit_val = safe_val(ebit_row, i)
            da_val = safe_val(da_row, i)
            if ebit_val is not None and da_val is not None:
                m["ebitda"] = ebit_val + abs(da_val)

        m["ebit"] = safe_val(ebit_row, i)
        m["net_income"] = safe_val(net_income_row, i)
        m["interest_expense"] = safe_val(interest_row, i)
        m["da"] = safe_val(da_row, i)
        m["gross_profit"] = safe_val(gross_profit_row, i)

        # Balance sheet
        m["cash"] = safe_val(cash_bs_row, i)
        lt_debt = safe_val(total_debt_lt, i) or 0
        st_debt = safe_val(total_debt_st, i) or 0
        m["total_debt"] = lt_debt + st_debt if (lt_debt + st_debt) > 0 else None
        m["total_assets"] = safe_val(total_assets_row, i)
        m["total_equity"] = safe_val(total_equity_row, i)

        # Cash flow
        m["cfo"] = safe_val(cfo_row, i)
        m["capex"] = safe_val(capex_row, i)

        # --- Derived metrics ---
        if m["revenue"] and m["revenue"] != 0:
            if m["gross_profit"]:
                m["gross_margin"] = (m["gross_profit"] / m["revenue"]) * 100
            if m["ebitda"]:
                m["ebitda_margin"] = (m["ebitda"] / m["revenue"]) * 100
            if m["net_income"]:
                m["net_margin"] = (m["net_income"] / m["revenue"]) * 100

        if m["ebitda"] and m["ebitda"] != 0:
            if m["total_debt"]:
                m["gross_leverage"] = m["total_debt"] / m["ebitda"]
            net_debt = (m["total_debt"] or 0) - (m["cash"] or 0)
            m["net_debt"] = net_debt
            if m["ebitda"] != 0:
                m["net_leverage"] = net_debt / m["ebitda"]

        if m["interest_expense"] and m["interest_expense"] != 0 and m["ebitda"]:
            m["interest_coverage"] = m["ebitda"] / abs(m["interest_expense"])

        if m["cfo"] is not None and m["capex"] is not None:
            m["fcf"] = m["cfo"] - abs(m["capex"])
        elif m["cfo"] is not None:
            m["fcf"] = m["cfo"]

        if m.get("fcf") and m.get("total_debt") and m["total_debt"] != 0:
            m["fcf_to_debt"] = (m["fcf"] / m["total_debt"]) * 100

        if m.get("total_equity") and m["total_equity"] != 0 and m.get("total_debt"):
            m["debt_to_equity"] = m["total_debt"] / m["total_equity"]

        if m.get("total_assets") and m["total_assets"] != 0 and m.get("total_debt"):
            m["debt_to_assets"] = (m["total_debt"] / m["total_assets"]) * 100

        metrics_by_period[period] = m

    # =========================================================================
    # DISPLAY CREDIT METRICS TABLE
    # =========================================================================
    display_metrics = [
        ("Revenue ($M)", "revenue"),
        ("EBITDA ($M)", "ebitda"),
        ("EBITDA Margin (%)", "ebitda_margin"),
        ("Gross Leverage (Debt/EBITDA)", "gross_leverage"),
        ("Net Leverage", "net_leverage"),
        ("Interest Coverage (x)", "interest_coverage"),
        ("Total Debt ($M)", "total_debt"),
        ("Net Debt ($M)", "net_debt"),
        ("Cash ($M)", "cash"),
        ("Free Cash Flow ($M)", "fcf"),
        ("FCF / Debt (%)", "fcf_to_debt"),
        ("Debt / Equity (x)", "debt_to_equity"),
        ("Debt / Assets (%)", "debt_to_assets"),
        ("Net Income ($M)", "net_income"),
        ("Net Margin (%)", "net_margin"),
    ]

    rows = []
    for display_name, key in display_metrics:
        row = {"Metric": display_name}
        for period in periods:
            val = metrics_by_period[period].get(key)
            row[period] = round(val, 2) if val is not None else "N/A"
        rows.append(row)

    summary_df = pd.DataFrame(rows).set_index("Metric")
    st.dataframe(summary_df, use_container_width=True)

    # =========================================================================
    # TREND CHARTS
    # =========================================================================
    st.markdown("---")
    st.subheader("Trend Analysis")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        gross_lev = [metrics_by_period[p].get("gross_leverage") for p in periods]
        net_lev = [metrics_by_period[p].get("net_leverage") for p in periods]
        fig_lev = go.Figure()
        fig_lev.add_trace(go.Scatter(x=periods, y=gross_lev, mode="lines+markers", name="Gross Leverage", line=dict(color=CHART_COLORS["primary"])))
        fig_lev.add_trace(go.Scatter(x=periods, y=net_lev, mode="lines+markers", name="Net Leverage", line=dict(color=CHART_COLORS["accent"])))
        fig_lev.update_layout(title="Leverage Trend", yaxis_title="x EBITDA", height=350, **PLOTLY_LAYOUT)
        st.plotly_chart(fig_lev, use_container_width=True)

    with chart_col2:
        coverage = [metrics_by_period[p].get("interest_coverage") for p in periods]
        fig_cov = go.Figure()
        fig_cov.add_trace(go.Scatter(x=periods, y=coverage, mode="lines+markers",
                                      name="Interest Coverage", line=dict(color=CHART_COLORS["positive"])))
        fig_cov.update_layout(title="Interest Coverage Trend", yaxis_title="x", height=350, **PLOTLY_LAYOUT)
        st.plotly_chart(fig_cov, use_container_width=True)

    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        rev = [metrics_by_period[p].get("revenue") for p in periods]
        ebitda_vals = [metrics_by_period[p].get("ebitda") for p in periods]
        fig_rev = go.Figure()
        fig_rev.add_trace(go.Bar(x=periods, y=rev, name="Revenue", marker_color=CHART_COLORS["primary"]))
        fig_rev.add_trace(go.Bar(x=periods, y=ebitda_vals, name="EBITDA", marker_color=CHART_COLORS["accent"]))
        fig_rev.update_layout(title="Revenue & EBITDA", yaxis_title="$ Millions",
                               height=350, barmode="group", **PLOTLY_LAYOUT)
        st.plotly_chart(fig_rev, use_container_width=True)

    with chart_col4:
        fcf_vals = [metrics_by_period[p].get("fcf") for p in periods]
        fcf_clean = [v if v is not None else 0 for v in fcf_vals]
        colors = [CHART_COLORS["positive"] if v >= 0 else CHART_COLORS["negative"] for v in fcf_clean]
        fig_fcf = go.Figure()
        fig_fcf.add_trace(go.Bar(x=periods, y=fcf_clean, name="FCF", marker_color=colors))
        fig_fcf.update_layout(title="Free Cash Flow Trend", yaxis_title="$ Millions",
                               height=350, **PLOTLY_LAYOUT)
        st.plotly_chart(fig_fcf, use_container_width=True)

    # Margin trend
    fig_margins = go.Figure()
    fig_margins.add_trace(go.Scatter(
        x=periods, y=[metrics_by_period[p].get("ebitda_margin") for p in periods],
        mode="lines+markers", name="EBITDA Margin (%)", line=dict(color=CHART_COLORS["primary"])))
    fig_margins.add_trace(go.Scatter(
        x=periods, y=[metrics_by_period[p].get("net_margin") for p in periods],
        mode="lines+markers", name="Net Margin (%)", line=dict(color=CHART_COLORS["highlight"])))
    fig_margins.update_layout(title="Margin Trends", yaxis_title="%", height=350, **PLOTLY_LAYOUT)
    st.plotly_chart(fig_margins, use_container_width=True)

    # =========================================================================
    # CREDIT ASSESSMENT
    # =========================================================================
    st.markdown("---")
    st.subheader("Credit Assessment")

    latest = metrics_by_period[periods[-1]]

    def assess(value, threshold_good, threshold_ok, invert=False):
        if value is None:
            return "N/A", "gray"
        if invert:
            if value <= threshold_good:
                return "Strong", "green"
            elif value <= threshold_ok:
                return "Adequate", "orange"
            else:
                return "Weak", "red"
        else:
            if value >= threshold_good:
                return "Strong", "green"
            elif value >= threshold_ok:
                return "Adequate", "orange"
            else:
                return "Weak", "red"

    assessments = [
        ("Gross Leverage", latest.get("gross_leverage"),
         *assess(latest.get("gross_leverage"), 2.0, 3.5, invert=True)),
        ("Net Leverage", latest.get("net_leverage"),
         *assess(latest.get("net_leverage"), 1.5, 3.0, invert=True)),
        ("Interest Coverage", latest.get("interest_coverage"),
         *assess(latest.get("interest_coverage"), 6.0, 3.0)),
        ("EBITDA Margin", latest.get("ebitda_margin"),
         *assess(latest.get("ebitda_margin"), 25, 15)),
        ("FCF / Debt", latest.get("fcf_to_debt"),
         *assess(latest.get("fcf_to_debt"), 20, 10)),
    ]

    acols = st.columns(5)
    for col, (name, value, rating, color) in zip(acols, assessments):
        with col:
            val_str = f"{value:.1f}" if value is not None else "N/A"
            st.metric(name, val_str)
            if color == "green":
                st.success(rating)
            elif color == "orange":
                st.warning(rating)
            else:
                st.error(rating)

    # =========================================================================
    # AI COMMENTARY
    # =========================================================================
    st.markdown("---")
    st.subheader("AI Credit Commentary")

    # Initialize session state for saving commentary
    if "model_commentary" not in st.session_state:
        st.session_state.model_commentary = {}

    if st.session_state.get("anthropic_api_key"):
        if st.button("Generate AI Credit Summary", type="primary"):
            with st.spinner("Generating credit analysis with Claude..."):
                client = get_client()
                if client:
                    model_text = f"Company: {issuer_name}\n\n"
                    model_text += "KEY CREDIT METRICS BY PERIOD:\n"
                    model_text += summary_df.to_string()

                    try:
                        message = client.messages.create(
                            model="claude-sonnet-4-20250514",
                            max_tokens=2000,
                            system=(
                                "You are a senior fixed income credit analyst. Based on the 3-statement "
                                "model data provided, write a credit-focused summary that covers:\n"
                                "1. CREDIT PROFILE: Overall assessment of creditworthiness\n"
                                "2. LEVERAGE TRAJECTORY: Is leverage improving, stable, or deteriorating?\n"
                                "3. CASH FLOW ADEQUACY: Can the company service its debt comfortably?\n"
                                "4. KEY STRENGTHS: What supports the credit?\n"
                                "5. KEY RISKS: What could impair creditworthiness?\n"
                                "6. RATING ESTIMATE: Based on the metrics, what credit rating range "
                                "would you estimate? (e.g., BBB/BBB+)\n"
                                "7. OUTLOOK: What to watch going forward\n\n"
                                "Be specific, use the actual numbers, and write as if briefing a PM."
                            ),
                            messages=[
                                {"role": "user", "content": f"Analyze this credit model:\n\n{model_text}"}
                            ],
                        )
                        st.session_state.model_commentary[issuer_name] = message.content[0].text
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    else:
        st.info("Add your Anthropic API key in the sidebar to enable AI-generated credit commentary.")

    # Display saved commentary and PDF download
    saved_commentary = st.session_state.model_commentary.get(issuer_name)
    if saved_commentary:
        st.markdown(saved_commentary)
        pdf_bytes = create_analysis_pdf(
            title=f"Credit Summary: {issuer_name}",
            issuer=issuer_name,
            analysis_type="3-Statement Model Credit Analysis",
            content=saved_commentary,
        )
        st.download_button(
            "Download Credit Summary as PDF",
            data=pdf_bytes,
            file_name=f"{issuer_name}_credit_summary.pdf",
            mime="application/pdf",
            key="pdf_model_summary",
        )

    # Export
    st.markdown("---")
    csv = summary_df.reset_index().to_csv(index=False)
    st.download_button("Export Credit Summary as CSV", data=csv,
                        file_name=f"{issuer_name}_credit_summary.csv", mime="text/csv")

except Exception as e:
    st.error(f"Error processing file: {str(e)}")
    st.markdown(
        "**Troubleshooting:**\n"
        "- Make sure your Excel has sheets named 'Income Statement', 'Balance Sheet', and 'Cash Flow Statement'\n"
        "- The first column of each sheet should contain row labels (Revenue, EBITDA, etc.)\n"
        "- Remaining columns should be periods (FY 2022, FY 2023, etc.)\n"
        "- Download the template above for the expected format"
    )
