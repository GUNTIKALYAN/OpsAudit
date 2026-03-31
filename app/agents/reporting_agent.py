from typing import Dict, Any, List


SEVERITY_ORDER = {
    "high": 3,
    "medium": 2,
    "low": 1
}


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    report: List[Dict[str, Any]] = state.get("report", [])

    
    # EDGE CASE: EMPTY REPORT
    if not report:
        summary = {
            "total_issues": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "health_score": 100
        }

        return {
            "report": {
                "summary": summary,
                "grouped": {"high": [], "medium": [], "low": []},
                "details": []
            }
        }

    
    # 1. SORT ISSUES BY SEVERITY
    sorted_report = sorted(
        report,
        key=lambda x: SEVERITY_ORDER.get(x.get("severity", "low"), 0),
        reverse=True
    )

    # 2. GROUP BY SEVERITY
    grouped = {
        "high": [],
        "medium": [],
        "low": []
    }

    for item in sorted_report:
        severity = item.get("severity", "low")
        if severity in grouped:
            grouped[severity].append(item)

    # 3. GENERATE SUMMARY
    summary = {
        "total_issues": len(sorted_report),
        "high": len(grouped["high"]),
        "medium": len(grouped["medium"]),
        "low": len(grouped["low"])
    }

    summary["health_score"] = calculate_health_score(summary)

    # 4. FINAL STRUCTURE
    final_report = {
        "summary": summary,
        "grouped": grouped,
        "details": sorted_report
    }

    return {"report": final_report}


def calculate_health_score(summary: Dict[str, int]) -> int:
    score = 100

    score -= summary["high"] * 20
    score -= summary["medium"] * 10
    score -= summary["low"] * 5

    return max(score, 0)