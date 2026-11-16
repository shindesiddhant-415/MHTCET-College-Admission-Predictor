"""
Display and styling helper functions for Streamlit.
"""

def get_badge_html(group):
    if group == "Safer":
        return '<span style="background-color: #27ae60; color: white; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 13px;">🛡️ SAFER</span>'
    elif group == "Moderate":
        return '<span style="background-color: #f39c12; color: white; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 13px;">⚖️ MODERATE</span>'
    else:
        return '<span style="background-color: #e74c3c; color: white; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 13px;">🚀 REACH</span>'

def format_gap(gap):
    if gap > 0:
        return f'<span style="color: #27ae60; font-weight: bold;">+{gap:.2f}%</span>'
    elif gap == 0:
        return f'<span style="color: #7f8c8d; font-weight: bold;">0.00%</span>'
    else:
        return f'<span style="color: #e74c3c; font-weight: bold;">{gap:.2f}%</span>'

