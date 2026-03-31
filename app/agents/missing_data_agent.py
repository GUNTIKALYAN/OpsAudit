from typing import Dict, Any
from app.utils.constants import CRITICAL_COLUMNS, IMPORTANT_COLUMNS


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    df = state["data"]

    issues = []
    total_rows = len(df)

    for col in df.columns:
        missing_count = df[col].isnull().sum()

        if missing_count == 0:
            continue

        percentage = (missing_count / total_rows) * 100

        if percentage < 5:
            continue

        issue = {
            "type": "missing",
            "column": col,
            "missing_count": int(missing_count),
            "missing_percentage": round(percentage, 2)
        }

        if col in CRITICAL_COLUMNS:
            issue["priority"] = "critical"

        elif col in IMPORTANT_COLUMNS:
            issue["priority"] = "important"

        else:
            issue["priority"] = "normal"

        issues.append(issue)

    return {"issues": issues}