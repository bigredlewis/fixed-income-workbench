# Fixed Income Analyst Workbench

A Streamlit-based tool designed to streamline common workflows for fundamental fixed income analysts. Built using Claude Code as the primary AI-powered development tool.

## Features

### 1. Credit Analysis Model
- Upload quarterly financial data via Excel or enter manually
- Download Excel templates for easy data formatting
- Auto-calculates key credit metrics: leverage, interest coverage, EBITDA margin, free cash flow
- Color-coded assessments (Strong / Adequate / Weak / Critical)
- Trend charts across quarters
- Export to CSV

### 2. Consensus Comparison
- Upload your estimates vs. Street consensus via Excel or enter manually
- Automatic variance calculation with visual flags (In-Line / Slight / Notable / Significant)
- Side-by-side bar charts and variance waterfall
- AI-powered commentary on where and why you diverge (requires API key)
- PDF export of AI-generated insights
- Export comparison to CSV

### 3. Document Analysis
- Upload multiple sell-side reports or earnings transcripts (PDF or TXT)
- AI-powered analysis with 4 modes: General, Credit Metrics, Earnings Review, Qualitative-to-Quantitative (requires API key)
- Persistent results across page navigation
- PDF export per analysis or combined "Download All"
- Structured manual analysis framework (works without API key)

### 4. Portfolio Fit Analysis
- Upload full portfolio holdings via Excel with flexible column matching
- Auto-calculates portfolio stats: weighted avg duration, yield, rating, spread, sector weights
- Portfolio overview with sector pie chart and rating distribution bar chart
- Model how a candidate bond impacts duration, yield, and credit quality
- Automated risk flags for concentration, duration drift, and quality dilution

### 5. 3-Statement Model Summary
- Upload a 3-statement Excel model (Income Statement, Balance Sheet, Cash Flow)
- Auto-detects sheets and key financial line items via keyword matching
- Calculates 15+ derived credit metrics including EBITDA, leverage, and coverage ratios
- Color-coded credit assessment cards
- AI-powered credit commentary with PDF export (requires API key)

### 6. Key Terms & Concepts
- Static reference page with 90+ fixed income terms and definitions
- Organized across 10 sections: Bond Basics, Yield Concepts, Spread Concepts, Duration & Risk, Credit Analysis, Bond Structures, Fixed Income Markets, Treasury Concepts, Portfolio Management, Special Topics
- Searchable via Ctrl+F (Cmd+F on Mac)

## Getting Started

### Option A: Use the Live App (Recommended)
The app is deployed on Streamlit Community Cloud — just open the link provided and start using it. No installation required.

### Option B: Run Locally

**Prerequisites:** Python 3.10 or higher

1. **Clone the repository:**
   ```
   git clone https://github.com/bigredlewis/fixed-income-workbench.git
   cd fixed-income-workbench
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```
   streamlit run app.py
   ```

4. **Open your browser** to `http://localhost:8501` (it should open automatically)

### Enabling AI Features

Several pages offer AI-powered analysis using the Claude API. To enable them:

1. Go to [console.anthropic.com](https://console.anthropic.com) and create an account
2. Generate an API key
3. In the app, click "AI Settings" in the sidebar and paste your key

The app works fully without an API key — AI features simply show a manual mode instead.

## Tech Stack

| Component | Technology |
|---|---|
| Frontend/App | Streamlit |
| Data Processing | Pandas, NumPy |
| Charts | Plotly |
| PDF Parsing | pdfplumber |
| PDF Export | fpdf2 |
| AI Analysis | Anthropic Claude API |
| Language | Python 3.13 |

## Project Structure

```
fixed-income-workbench/
├── app.py                          # Main app with home page
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── pages/
│   ├── 1_Credit_Analysis.py        # Credit metrics model
│   ├── 2_Consensus_Comparison.py   # Estimate vs consensus
│   ├── 3_Document_Analysis.py      # Report analysis
│   ├── 4_Portfolio_Fit.py          # Portfolio impact tool
│   ├── 5_Model_Summary.py          # 3-statement model analysis
│   └── 6_Key_Terms.py              # FI terms reference
└── utils/
    ├── __init__.py
    ├── calculations.py             # Financial calculations
    ├── ai_analysis.py              # Claude API integration
    ├── templates.py                # Excel template generators
    └── pdf_export.py               # PDF report generation
```

## Usage Tips

- **Start with Credit Analysis**: Upload or input a few quarters of data for a company you're covering to see trend charts and metric assessments
- **Use Consensus Comparison** after building your model to see where your estimates diverge from the Street
- **Upload sell-side reports** in Document Analysis to quickly extract key data points from multiple files at once
- **Run Portfolio Fit** before recommending a bond to your PM to check for concentration or duration issues
- **Upload your 3-statement model** in Model Summary to get an automated credit assessment
- **Reference Key Terms** when you encounter unfamiliar fixed income concepts

## Built With

This application was built using **Claude Code** as the primary AI-powered development tool, demonstrating how AI can accelerate software development for domain-specific financial tools.
