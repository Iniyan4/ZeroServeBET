from math import floor

def compute_trust_score(r: dict):
    """
    r = {
      completion_rate, cancellation_count, no_show_count,
      late_count, complaint_count
    }
    """
    score = 100.0

    # penalties
    score -= (100 - r.get('completion_rate', 100)) * 0.5
    score -= r.get('cancellation_count', 0) * 3
    score -= r.get('no_show_count', 0) * 7
    score -= r.get('late_count', 0) * 2
    score -= r.get('complaint_count', 0) * 4

    # clamp
    score = max(0.0, min(100.0, score))
    return round(score, 2)


def compute_risk_level(score: float):
    if score >= 80:
        return 'low'
    if score >= 60:
        return 'medium'
    if score >= 40:
        return 'high'
    return 'critical'


def decide_action(severity: str, current_warnings: int):
    """
    Simple policy:
    - low severity → warning
    - medium → temp_limit if >=2 warnings else warning
    - high → restricted or review
    """
    if severity == 'low':
        return 'warning'

    if severity == 'medium':
        return 'temp_limit' if current_warnings >= 2 else 'warning'

    # high severity
    if current_warnings >= 2:
        return 'restricted'
    return 'review'