from typing import List, Dict, Any
import pandas as pd


def validate_rules(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Central rule engine for all business validations
    """

    issues = []

    total_rows = len(df)

    # RULE 1: status vs progress
    if "status" in df.columns and "progress" in df.columns:
        invalid = df[
            (df["status"] == "completed") & (df["progress"] < 100)
        ]

        if not invalid.empty:
            issues.append({
                "type": "logic_error",
                "rule": "status-progress mismatch",
                "violations": int(len(invalid)),
                "affected_percentage": round(len(invalid) / total_rows * 100, 2)
            })

    # RULE 2: start_date < end_date
    if "start_date" in df.columns and "end_date" in df.columns:
        try:
            temp_df = df.copy()

            temp_df["start_date"] = pd.to_datetime(temp_df["start_date"], errors="coerce")
            temp_df["end_date"] = pd.to_datetime(temp_df["end_date"], errors="coerce")

            invalid = temp_df[temp_df["start_date"] > temp_df["end_date"]]

            if not invalid.empty:
                issues.append({
                    "type": "logic_error",
                    "rule": "invalid date range",
                    "violations": int(len(invalid)),
                    "affected_percentage": round(len(invalid) / total_rows * 100, 2)
                })

        except Exception:
            pass

    return issues