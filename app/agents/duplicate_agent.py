from typing import Dict, Any


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    df = state["data"]

    issues = []

    total_rows = len(df)

    # FULL ROW DUPLICATES
    duplicate_rows = df[df.duplicated()]

    if not duplicate_rows.empty:
        issues.append({
            "type": "duplicate",
            "level": "row",
            "count": int(len(duplicate_rows))
        })

    # COLUMN-LEVEL DUPLICATES
    for col in df.columns:
        dup_count = df[col].duplicated().sum()

        if dup_count > 0:
            issues.append({
                "type": "duplicate",
                "column": col,
                "count": int(dup_count)
            })

    # -------------------------
    # 3. PRIMARY KEY DETECTION (SMART)
    # -------------------------
    possible_keys = ["id", "user_id", "email"]

    for key in possible_keys:
        if key in df.columns:
            dup_count = df[key].duplicated().sum()

            if dup_count > 0:
                issues.append({
                    "type": "duplicate",
                    "column": key,
                    "count": int(dup_count),
                    "note": "Potential primary key duplication"
                })

    return {"issues": issues}