# src/metrics.py
import math
import pandas as pd
import numpy as np

def safe_divide(a, b):
    """Safely divide two numbers, handling None and zero values."""
    try:
        a = 0 if a is None else a
        b = 0 if b is None else b
        if b == 0 or b is None:
            return 0.0
        return a / b
    except Exception:
        return 0.0

def calculate_cac(spend, new_customers):
    """Calculate Customer Acquisition Cost."""
    return safe_divide(spend, new_customers)

def calculate_ltv(total_revenue, new_customers):
    """Calculate Lifetime Value."""
    return safe_divide(total_revenue, new_customers)

def calculate_ltv_cac_ratio(ltv, cac):
    """Calculate LTV:CAC ratio."""
    return safe_divide(ltv, cac)

def calculate_roas(attributed_revenue, spend):
    """Calculate Return on Ad Spend."""
    return safe_divide(attributed_revenue, spend)

def calculate_ctr(clicks, impressions):
    """Calculate Click-Through Rate."""
    return safe_divide(clicks, impressions) * 100

def calculate_cpc(spend, clicks):
    """Calculate Cost Per Click."""
    return safe_divide(spend, clicks)

def calculate_cpm(spend, impressions):
    """Calculate Cost Per Mille (1000 impressions)."""
    return safe_divide(spend, impressions / 1000)

def calculate_conversion_rate(orders, clicks):
    """Calculate Conversion Rate."""
    return safe_divide(orders, clicks) * 100

def calculate_profit_margin(gross_profit, total_revenue):
    """Calculate Profit Margin."""
    return safe_divide(gross_profit, total_revenue) * 100

def calculate_revenue_per_order(total_revenue, orders):
    """Calculate Revenue Per Order."""
    return safe_divide(total_revenue, orders)

def calculate_attribution_rate(attributed_revenue, total_revenue):
    """Calculate what percentage of total revenue is attributed to marketing."""
    return safe_divide(attributed_revenue, total_revenue) * 100

def calculate_efficiency_score(roas, ctr, conversion_rate):
    """Calculate a composite efficiency score."""
    # Normalize metrics and create weighted score
    roas_score = min(roas / 3.0, 1.0) * 40  # ROAS weight: 40%
    ctr_score = min(ctr / 5.0, 1.0) * 30    # CTR weight: 30%
    conv_score = min(conversion_rate / 10.0, 1.0) * 30  # Conversion weight: 30%
    
    return roas_score + ctr_score + conv_score

def calculate_trend_direction(values):
    """Calculate trend direction (up, down, stable) based on recent values."""
    if len(values) < 2:
        return "stable"
    
    recent_avg = np.mean(values[-7:]) if len(values) >= 7 else np.mean(values[-3:])
    earlier_avg = np.mean(values[:-7]) if len(values) >= 14 else np.mean(values[:-3])
    
    if recent_avg > earlier_avg * 1.05:  # 5% increase threshold
        return "up"
    elif recent_avg < earlier_avg * 0.95:  # 5% decrease threshold
        return "down"
    else:
        return "stable"

def calculate_performance_grade(roas, ctr, conversion_rate):
    """Calculate performance grade (A, B, C, D, F) based on key metrics."""
    score = 0
    
    # ROAS scoring
    if roas >= 4.0:
        score += 40
    elif roas >= 3.0:
        score += 30
    elif roas >= 2.0:
        score += 20
    elif roas >= 1.0:
        score += 10
    
    # CTR scoring
    if ctr >= 3.0:
        score += 30
    elif ctr >= 2.0:
        score += 20
    elif ctr >= 1.0:
        score += 10
    
    # Conversion rate scoring
    if conversion_rate >= 5.0:
        score += 30
    elif conversion_rate >= 3.0:
        score += 20
    elif conversion_rate >= 1.0:
        score += 10
    
    # Grade assignment
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
