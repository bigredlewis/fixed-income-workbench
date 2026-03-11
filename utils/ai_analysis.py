"""
AI-powered analysis using Claude API.
Falls back to manual mode if no API key is configured.
"""

import streamlit as st

def get_client():
    """Get an Anthropic client if API key is available."""
    api_key = st.session_state.get("anthropic_api_key", "")
    if not api_key:
        return None
    try:
        from anthropic import Anthropic
        return Anthropic(api_key=api_key)
    except Exception:
        return None


def analyze_document(text: str, analysis_type: str = "general") -> str | None:
    """Analyze document text using Claude.

    Args:
        text: The document text to analyze
        analysis_type: One of 'general', 'credit', 'earnings', 'qualitative'

    Returns:
        Analysis string, or None if no API key
    """
    client = get_client()
    if client is None:
        return None

    prompts = {
        "general": (
            "You are a fixed income credit analyst. Analyze this document and provide:\n"
            "1. KEY FINANCIAL DATA: Extract any financial metrics, ratios, or projections mentioned\n"
            "2. CREDIT IMPLICATIONS: What does this mean for the issuer's creditworthiness?\n"
            "3. KEY RISKS: What risks are highlighted or implied?\n"
            "4. ACTIONABLE TAKEAWAYS: What should an analyst focus on?\n\n"
            "Be concise and use bullet points."
        ),
        "credit": (
            "You are a fixed income credit analyst. Extract and analyze credit-relevant information:\n"
            "1. LEVERAGE METRICS: Any debt/EBITDA, net leverage, or debt figures mentioned\n"
            "2. COVERAGE: Interest coverage, fixed charge coverage mentioned or calculable\n"
            "3. CASH FLOW: FCF, operating cash flow, capex figures\n"
            "4. CREDIT OPINION: Based on the data, assess credit trajectory (improving/stable/deteriorating)\n"
            "5. RATING IMPLICATIONS: How might this affect credit ratings?\n\n"
            "Be specific with numbers where available."
        ),
        "earnings": (
            "You are a fixed income credit analyst reviewing earnings materials. Provide:\n"
            "1. REVENUE & GROWTH: Revenue figures and growth rates\n"
            "2. PROFITABILITY: EBITDA, margins, and trends\n"
            "3. BALANCE SHEET: Debt levels, cash, leverage changes\n"
            "4. GUIDANCE: Any forward-looking statements or guidance\n"
            "5. MANAGEMENT TONE: Assess management's confidence and key messages\n"
            "6. MODEL IMPLICATIONS: Suggest how this should affect financial model assumptions\n\n"
            "Be specific with numbers."
        ),
        "qualitative": (
            "You are a fixed income credit analyst. Focus on qualitative factors:\n"
            "1. BUSINESS QUALITY: Competitive position, market share, barriers to entry\n"
            "2. MANAGEMENT: Quality signals, strategic direction, capital allocation philosophy\n"
            "3. INDUSTRY TRENDS: Sector headwinds or tailwinds mentioned\n"
            "4. ESG FACTORS: Any environmental, social, or governance considerations\n"
            "5. MODEL TRANSLATION: For each qualitative insight, suggest a specific\n"
            "   quantitative assumption it implies (e.g., 'strong pricing power' -> '2-3% annual price increases')\n\n"
            "Be specific about how qualitative factors translate to numbers."
        ),
    }

    system_prompt = prompts.get(analysis_type, prompts["general"])

    # Truncate very long documents to stay within limits
    max_chars = 80000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[Document truncated for analysis]"

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": f"Analyze this document:\n\n{text}"}
            ],
        )
        return message.content[0].text
    except Exception as e:
        return f"Error calling Claude API: {str(e)}"


def generate_variance_commentary(your_estimates: dict, consensus: dict) -> str | None:
    """Generate commentary on estimate variances using Claude.

    Args:
        your_estimates: dict of metric_name -> value
        consensus: dict of metric_name -> value

    Returns:
        Commentary string, or None if no API key
    """
    client = get_client()
    if client is None:
        return None

    # Build comparison text
    comparison_lines = []
    for metric in your_estimates:
        yours = your_estimates[metric]
        cons = consensus.get(metric)
        if yours is not None and cons is not None and cons != 0:
            variance_pct = ((yours - cons) / abs(cons)) * 100
            comparison_lines.append(
                f"- {metric}: Your estimate = {yours:.2f}, Consensus = {cons:.2f}, "
                f"Variance = {variance_pct:+.1f}%"
            )

    if not comparison_lines:
        return "No comparable metrics to analyze."

    comparison_text = "\n".join(comparison_lines)

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=(
                "You are a fixed income analyst. Analyze the variance between the analyst's "
                "estimates and Street consensus. For each significant variance:\n"
                "1. Flag whether the analyst is ABOVE or BELOW consensus\n"
                "2. Assess whether the variance is meaningful (>5% is notable, >10% is significant)\n"
                "3. Suggest what fundamental view might explain the difference\n"
                "4. Note any metrics where the analyst should double-check assumptions\n\n"
                "Be concise and actionable."
            ),
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze these estimate variances:\n\n{comparison_text}",
                }
            ],
        )
        return message.content[0].text
    except Exception as e:
        return f"Error calling Claude API: {str(e)}"
