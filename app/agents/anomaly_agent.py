from typing import Dict, Any
import numpy as np


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    df = state["data"]

    issues = []

    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        series = df[col].dropna()

        if len(series) < 3:
            continue 

        mean = series.mean()
        std = series.std()

        if std == 0:
            continue

        # Z-score method
        z_scores = (series - mean) / std
        outliers = series[abs(z_scores) > 2.5]   

        if len(outliers) > 0:
            issues.append({
                "type": "anomaly",
                "column": col,
                "outliers": int(len(outliers))
            })

        max_val = series.max()
        median_val = series.median()

        if median_val != 0 and max_val / median_val > 10:
            issues.append({
                "type": "anomaly",
                "column": col,
                "outliers": 1,
                "note": "Extreme spike detected"
            })

    return {"issues": issues}