"""
Financial calculations for credit analysis.
"""

import pandas as pd
import numpy as np


def calculate_credit_metrics(financials: dict) -> dict:
    """Calculate key credit metrics from raw financial inputs.

    Args:
        financials: dict with keys like 'revenue', 'ebitda', 'total_debt',
                    'interest_expense', 'capex', 'cash', 'depreciation',
                    'taxes', 'working_capital_change'

    Returns:
        dict of calculated credit metrics
    """
    metrics = {}

    revenue = financials.get("revenue", 0)
    ebitda = financials.get("ebitda", 0)
    total_debt = financials.get("total_debt", 0)
    interest_expense = financials.get("interest_expense", 0)
    capex = financials.get("capex", 0)
    cash = financials.get("cash", 0)
    depreciation = financials.get("depreciation", 0)
    taxes = financials.get("taxes", 0)
    wc_change = financials.get("working_capital_change", 0)

    # Leverage
    metrics["gross_leverage"] = total_debt / ebitda if ebitda else None
    net_debt = total_debt - cash
    metrics["net_debt"] = net_debt
    metrics["net_leverage"] = net_debt / ebitda if ebitda else None

    # Coverage
    metrics["interest_coverage"] = ebitda / interest_expense if interest_expense else None

    # Margins
    metrics["ebitda_margin"] = (ebitda / revenue * 100) if revenue else None

    # Free Cash Flow
    # FCF = EBITDA - Capex - Taxes - Working Capital Changes
    fcf = ebitda - capex - taxes - wc_change
    metrics["free_cash_flow"] = fcf
    metrics["fcf_to_debt"] = (fcf / total_debt * 100) if total_debt else None

    # Debt service
    metrics["debt_to_total_capital"] = None  # needs equity input
    metrics["cash_to_debt"] = (cash / total_debt * 100) if total_debt else None

    return metrics


def rate_metric(metric_name: str, value: float) -> str:
    """Return a qualitative assessment of a credit metric.

    Returns one of: 'Strong', 'Adequate', 'Weak', 'Critical'
    """
    if value is None:
        return "N/A"

    thresholds = {
        "gross_leverage": [(2.0, "Strong"), (3.5, "Adequate"), (5.0, "Weak")],
        "net_leverage": [(1.5, "Strong"), (3.0, "Adequate"), (4.5, "Weak")],
        "interest_coverage": [(6.0, "Strong"), (3.0, "Adequate"), (1.5, "Weak")],
        "ebitda_margin": [(25, "Strong"), (15, "Adequate"), (8, "Weak")],
        "fcf_to_debt": [(20, "Strong"), (10, "Adequate"), (5, "Weak")],
        "cash_to_debt": [(30, "Strong"), (15, "Adequate"), (5, "Weak")],
    }

    if metric_name not in thresholds:
        return "N/A"

    ranges = thresholds[metric_name]

    # For leverage metrics, lower is better (invert logic)
    if "leverage" in metric_name:
        if value <= ranges[0][0]:
            return "Strong"
        elif value <= ranges[1][0]:
            return "Adequate"
        elif value <= ranges[2][0]:
            return "Weak"
        else:
            return "Critical"
    else:
        # For coverage/margin/FCF metrics, higher is better
        if value >= ranges[0][0]:
            return "Strong"
        elif value >= ranges[1][0]:
            return "Adequate"
        elif value >= ranges[2][0]:
            return "Weak"
        else:
            return "Critical"


def rating_color(rating: str) -> str:
    """Return a color for a rating assessment."""
    colors = {
        "Strong": "green",
        "Adequate": "orange",
        "Weak": "red",
        "Critical": "red",
        "N/A": "gray",
    }
    return colors.get(rating, "gray")


def calculate_portfolio_impact(
    portfolio: dict, new_bond: dict, allocation_pct: float
) -> dict:
    """Calculate the impact of adding a bond to a portfolio.

    Args:
        portfolio: dict with 'duration', 'yield_pct', 'avg_rating_numeric',
                   'sector_weights' (dict), 'total_value'
        new_bond: dict with 'duration', 'yield_pct', 'rating_numeric',
                  'sector', 'spread_bps'
        allocation_pct: what % of portfolio to allocate to new bond (0-100)

    Returns:
        dict with before/after portfolio metrics
    """
    alloc = allocation_pct / 100.0
    remaining = 1.0 - alloc

    result = {}

    # Duration impact
    old_dur = portfolio.get("duration", 0)
    new_dur = new_bond.get("duration", 0)
    result["duration_before"] = old_dur
    result["duration_after"] = old_dur * remaining + new_dur * alloc
    result["duration_change"] = result["duration_after"] - result["duration_before"]

    # Yield impact
    old_yield = portfolio.get("yield_pct", 0)
    new_yield = new_bond.get("yield_pct", 0)
    result["yield_before"] = old_yield
    result["yield_after"] = old_yield * remaining + new_yield * alloc
    result["yield_change"] = result["yield_after"] - result["yield_before"]

    # Credit quality impact (using numeric scale: AAA=1, AA+=2, ... CCC=10)
    old_rating = portfolio.get("avg_rating_numeric", 5)
    new_rating = new_bond.get("rating_numeric", 5)
    result["rating_before"] = old_rating
    result["rating_after"] = old_rating * remaining + new_rating * alloc
    result["rating_change"] = result["rating_after"] - result["rating_before"]

    # Sector concentration
    sector_weights = dict(portfolio.get("sector_weights", {}))
    bond_sector = new_bond.get("sector", "Other")

    result["sector_weights_before"] = dict(sector_weights)

    # Adjust existing weights and add new bond
    new_weights = {}
    for sector, weight in sector_weights.items():
        new_weights[sector] = weight * remaining
    new_weights[bond_sector] = new_weights.get(bond_sector, 0) + alloc * 100
    result["sector_weights_after"] = new_weights

    return result


RATING_SCALE = {
    "AAA": 1, "AA+": 2, "AA": 3, "AA-": 4,
    "A+": 5, "A": 6, "A-": 7,
    "BBB+": 8, "BBB": 9, "BBB-": 10,
    "BB+": 11, "BB": 12, "BB-": 13,
    "B+": 14, "B": 15, "B-": 16,
    "CCC+": 17, "CCC": 18, "CCC-": 19,
    "CC": 20, "C": 21, "D": 22,
}

RATING_SCALE_REVERSE = {v: k for k, v in RATING_SCALE.items()}


def numeric_to_rating(value: float) -> str:
    """Convert numeric rating back to letter rating (rounds to nearest)."""
    rounded = int(round(value))
    rounded = max(1, min(22, rounded))
    return RATING_SCALE_REVERSE.get(rounded, "NR")
