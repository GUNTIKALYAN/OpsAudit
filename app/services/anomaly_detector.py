from typing import List, Dict, Any
import pandas as pd
import numpy as np


def detect_anomalies(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Detects anomalies using Z-score method
    """

    issues = []

    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        series = df[col].dropna()

        if len(series) < 10:
            continue

        mean = series.mean()
        std = series.std()

        if std == 0:
            continue

        z_scores = (series - mean) / std
        outliers = series[abs(z_scores) > 3]

        if not outliers.empty:
            issues.append({
                "type": "anomaly",
                "column": col,
                "outliers": int(len(outliers))
            })

    return issues