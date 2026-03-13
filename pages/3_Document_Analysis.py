"""
Document Analysis page - Upload and analyze sell-side reports and earnings materials.
Supports multiple file uploads and persists results in session state.
"""

import streamlit as st
import pdfplumber
from utils.ai_analysis import analyze_document
from utils.pdf_export import create_analysis_pdf, create_multi_analysis_pdf
from utils.styles import inject_custom_css

st.set_page_config(page_title="Document Analysis", page_icon="📄", layout="wide")
inject_custom_css()
st.title("Document Analysis")
st.markdown("""
<p style="color: #64748B; font-size: 1.05rem; margin-top: -0.5em; margin-bottom: 1em;">
    Upload sell-side reports, earnings transcripts, or other research documents.
    Extract key insights and translate qualitative views into model assumptions.
    <strong>Results are saved in your session</strong> so you can navigate away and come back.
</p>
""", unsafe_allow_html=True)

# --- Initialize session state for persistent results ---
if "doc_analysis_results" not in st.session_state:
    st.session_state.doc_analysis_results = []  # list of {file, type, result, text_preview}
if "doc_manual_notes" not in st.session_state:
    st.session_state.doc_manual_notes = {}

# --- File upload (multiple files) ---
uploaded_files = st.file_uploader(
    "Upload documents (PDF or TXT) — you can select multiple files",
    type=["pdf", "txt"],
    accept_multiple_files=True,
    help="Upload sell-side research, earnings transcripts, 10-K/10-Q excerpts, or credit reports",
)

# --- Process uploaded files ---
documents = {}  # {filename: text}

if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.name in documents:
            continue

        if uploaded_file.type == "application/pdf":
            try:
                uploaded_file.seek(0)
                with pdfplumber.open(uploaded_file) as pdf:
                    pages_text = []
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            pages_text.append(text)
                    documents[uploaded_file.name] = "\n\n".join(pages_text)
            except Exception as e:
                st.error(f"Error reading {uploaded_file.name}: {str(e)}")
        else:
            try:
                uploaded_file.seek(0)
                documents[uploaded_file.name] = uploaded_file.read().decode("utf-8", errors="ignore")
            except Exception as e:
                st.error(f"Error reading {uploaded_file.name}: {str(e)}")

    if documents:
        st.success(f"Loaded {len(documents)} document(s): {', '.join(documents.keys())}")

# Also allow pasting text directly
with st.expander("Or paste text directly"):
    pasted_text = st.text_area(
        "Paste document text here",
        height=200,
        placeholder="Paste earnings call transcript, research note, or any text...",
    )
    if pasted_text:
        documents["Pasted Text"] = pasted_text

if not documents and not st.session_state.doc_analysis_results:
    st.info("Upload PDF/TXT files or paste text to get started. Previous analysis results will appear here.")
    st.stop()

# --- Analysis section (only show if we have documents) ---
if documents:
    st.markdown("---")
    st.subheader("Analyze Documents")

    # If multiple documents, let user select which to analyze
    if len(documents) > 1:
        selected_doc = st.selectbox("Select document to analyze", list(documents.keys()))
        document_text = documents[selected_doc]
        analyze_all = st.checkbox("Analyze all documents at once", value=False)
    else:
        selected_doc = list(documents.keys())[0]
        document_text = documents[selected_doc]
        analyze_all = False

    # Show preview
    with st.expander(f"Preview: {selected_doc}", expanded=False):
        st.text(document_text[:3000] + ("..." if len(document_text) > 3000 else ""))
        st.caption(f"Total characters: {len(document_text):,}")

    # Analysis type
    analysis_options = [
        ("General Credit Analysis", "general"),
        ("Credit Metrics Extraction", "credit"),
        ("Earnings Review", "earnings"),
        ("Qualitative-to-Quantitative Translation", "qualitative"),
    ]
    analysis_type = st.selectbox(
        "Analysis Type",
        analysis_options,
        format_func=lambda x: x[0],
    )

    has_api_key = bool(st.session_state.get("anthropic_api_key"))

    if has_api_key:
        if st.button("Analyze with AI", type="primary"):
            docs_to_analyze = documents if analyze_all else {selected_doc: document_text}

            for doc_name, doc_text in docs_to_analyze.items():
                with st.spinner(f"Claude is analyzing: {doc_name}..."):
                    result = analyze_document(doc_text, analysis_type[1])
                    if result:
                        # Save to session state
                        st.session_state.doc_analysis_results.append({
                            "file": doc_name,
                            "type": analysis_type[0],
                            "result": result,
                            "text_preview": doc_text[:500],
                        })

            st.success("Analysis complete! Results saved below.")
            st.rerun()
    else:
        st.warning(
            "**AI analysis requires an Anthropic API key.** Add it in the sidebar under 'AI Settings'. "
            "In the meantime, use the manual analysis framework below."
        )

# --- Manual analysis framework (always available) ---
st.markdown("---")
st.subheader("Manual Analysis Framework")
st.markdown("Use this structured framework to organize your analysis notes. These notes are saved in your session.")

tab1, tab2, tab3, tab4 = st.tabs([
    "Key Financial Data",
    "Qualitative Insights",
    "Model Implications",
    "Risk Factors",
])

with tab1:
    st.markdown("**Extract key financial data points from the document:**")
    col1, col2 = st.columns(2)
    with col1:
        val = st.text_area("Revenue / Growth Metrics", height=100, key="manual_revenue",
                            value=st.session_state.doc_manual_notes.get("revenue", ""),
                            placeholder="e.g., Revenue of $5.2B, up 8% YoY...")
        st.session_state.doc_manual_notes["revenue"] = val

        val2 = st.text_area("Profitability Metrics", height=100, key="manual_profit",
                             value=st.session_state.doc_manual_notes.get("profit", ""),
                             placeholder="e.g., EBITDA margin expanded 150bps to 22%...")
        st.session_state.doc_manual_notes["profit"] = val2
    with col2:
        val3 = st.text_area("Leverage / Balance Sheet", height=100, key="manual_leverage",
                             value=st.session_state.doc_manual_notes.get("leverage", ""),
                             placeholder="e.g., Net leverage declined to 3.2x from 3.8x...")
        st.session_state.doc_manual_notes["leverage"] = val3

        val4 = st.text_area("Cash Flow Metrics", height=100, key="manual_cashflow",
                             value=st.session_state.doc_manual_notes.get("cashflow", ""),
                             placeholder="e.g., FCF of $450M, up from $380M...")
        st.session_state.doc_manual_notes["cashflow"] = val4

with tab2:
    st.markdown("**Capture qualitative insights:**")
    val5 = st.text_area("Management Tone & Commentary", height=100, key="manual_mgmt",
                         value=st.session_state.doc_manual_notes.get("mgmt", ""),
                         placeholder="e.g., Management expressed confidence in pricing power...")
    st.session_state.doc_manual_notes["mgmt"] = val5

    val6 = st.text_area("Competitive Position & Industry Trends", height=100, key="manual_competitive",
                         value=st.session_state.doc_manual_notes.get("competitive", ""),
                         placeholder="e.g., Gaining market share in key segments...")
    st.session_state.doc_manual_notes["competitive"] = val6

    val7 = st.text_area("Strategic Initiatives", height=100, key="manual_strategy",
                         value=st.session_state.doc_manual_notes.get("strategy", ""),
                         placeholder="e.g., Announced $500M cost reduction program...")
    st.session_state.doc_manual_notes["strategy"] = val7

with tab3:
    st.markdown("**Translate insights into model assumptions:**")
    st.markdown(
        "For each qualitative insight, suggest a specific quantitative assumption "
        "it implies for your financial model."
    )
    for i in range(5):
        col_q, col_a = st.columns(2)
        with col_q:
            qi = st.text_input(f"Qualitative Insight #{i+1}", key=f"qual_insight_{i}",
                               value=st.session_state.doc_manual_notes.get(f"qi_{i}", ""),
                               placeholder="e.g., Strong pricing power")
            st.session_state.doc_manual_notes[f"qi_{i}"] = qi
        with col_a:
            qa = st.text_input(f"Model Assumption #{i+1}", key=f"quant_assumption_{i}",
                               value=st.session_state.doc_manual_notes.get(f"qa_{i}", ""),
                               placeholder="e.g., 2-3% annual price increases")
            st.session_state.doc_manual_notes[f"qa_{i}"] = qa

with tab4:
    st.markdown("**Identify key risks:**")
    val8 = st.text_area("Credit Risks", height=100, key="manual_credit_risks",
                         value=st.session_state.doc_manual_notes.get("credit_risks", ""),
                         placeholder="e.g., Leverage remains elevated above target...")
    st.session_state.doc_manual_notes["credit_risks"] = val8

    val9 = st.text_area("Business Risks", height=100, key="manual_business_risks",
                         value=st.session_state.doc_manual_notes.get("business_risks", ""),
                         placeholder="e.g., Customer concentration with top 3 at 40% of revenue...")
    st.session_state.doc_manual_notes["business_risks"] = val9

    val10 = st.text_area("Macro / Industry Risks", height=100, key="manual_macro_risks",
                          value=st.session_state.doc_manual_notes.get("macro_risks", ""),
                          placeholder="e.g., Rising input costs could pressure margins...")
    st.session_state.doc_manual_notes["macro_risks"] = val10

# --- Previous analyses (persistent) ---
if st.session_state.doc_analysis_results:
    st.markdown("---")
    st.subheader("Saved Analysis Results")
    st.caption("These results persist while the app is running, even if you navigate to other pages.")

    for i, analysis in enumerate(reversed(st.session_state.doc_analysis_results)):
        idx = len(st.session_state.doc_analysis_results) - 1 - i
        with st.expander(f"{analysis['file']} — {analysis['type']}", expanded=(i == 0)):
            st.markdown(analysis["result"])
            col_pdf, col_del, col_spacer = st.columns([1, 1, 3])
            with col_pdf:
                pdf_bytes = create_analysis_pdf(
                    title=f"Document Analysis: {analysis['file']}",
                    issuer="",
                    analysis_type=analysis["type"],
                    content=analysis["result"],
                    source_file=analysis["file"],
                )
                st.download_button(
                    "Download PDF",
                    data=pdf_bytes,
                    file_name=f"{analysis['file'].replace('.', '_')}_analysis.pdf",
                    mime="application/pdf",
                    key=f"pdf_analysis_{idx}",
                )
            with col_del:
                if st.button("Remove", key=f"del_analysis_{idx}"):
                    st.session_state.doc_analysis_results.pop(idx)
                    st.rerun()

    # Download all as single PDF
    if len(st.session_state.doc_analysis_results) > 1:
        all_pdf_bytes = create_multi_analysis_pdf(
            title="Document Analysis - All Results",
            analyses=st.session_state.doc_analysis_results,
        )
        st.download_button(
            "Download All Analyses as PDF",
            data=all_pdf_bytes,
            file_name="all_document_analyses.pdf",
            mime="application/pdf",
            key="pdf_all_analyses",
        )

    if st.button("Clear All Results"):
        st.session_state.doc_analysis_results = []
        st.rerun()
