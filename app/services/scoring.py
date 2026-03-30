from typing import Dict, Any


def calculate_severity(issue: Dict[str, Any], total_rows: int = 1) -> str:
    """
    Improved severity scoring using ratios instead of absolute numbers
    """

    issue_type = issue.get("type")

    # DUPLICATES
    if issue_type == "duplicate":
        count = issue.get("count", 0)
        ratio = count / max(total_rows, 1)

        if ratio > 0.3:
            return "high"
        elif ratio > 0.1:
            return "medium"
        return "low"

    # MISSING DATA
    elif issue_type == "missing":
        pct = issue.get("missing_percentage", 0)
        priority = issue.get("priority", "normal")

        if priority == "critical":
            return "high"

        if priority == "important":
            if pct > 20:
                return "high"
            elif pct > 10:
                return "medium"
            return "low"

        # normal columns
        if pct > 40:
            return "high"
        elif pct > 15:
            return "medium"
        return "low"

    # LOGIC ERRORS
    elif issue_type == "logic_error":
        violations = issue.get("violations", 0)
        ratio = violations / max(total_rows, 1)

        if ratio > 0.3:
            return "high"
        elif ratio > 0.1:
            return "medium"
        return "low"

    # ANOMALIES
    elif issue_type == "anomaly":
        outliers = issue.get("outliers", 0)
        ratio = outliers / max(total_rows, 1)

        if ratio > 0.2:
            return "high"
        elif ratio > 0.05:
            return "medium"
        return "low"

    return "low"