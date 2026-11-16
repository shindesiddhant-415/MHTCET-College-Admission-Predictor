"""
Input validation utilities for the Streamlit application.
"""

def validate_percentile(val):
    try:
        f = float(val)
        if 0.0 <= f <= 100.0:
            return True, f
        return False, "Percentile must be between 0.00 and 100.00"
    except (ValueError, TypeError):
        return False, "Invalid numeric percentile input."

def validate_preferences(branches, category):
    if not branches or len(branches) == 0:
        return False, "Please select at least one engineering branch."
    if not category:
        return False, "Please select an eligible seat category."
    return True, "Valid"

