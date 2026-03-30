from typing import Dict, Any
import pandas as pd


def profile_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generates basic statistics about dataset
    """

    profile = {
        "columns": list(df.columns),
        "dtypes": {},
        "null_percentage": {},
        "unique_counts": {}
    }

    total_rows = len(df)

    for col in df.columns:
        profile["dtypes"][col] = str(df[col].dtype)

        null_count = df[col].isnull().sum()
        profile["null_percentage"][col] = round((null_count / total_rows) * 100, 2)

        profile["unique_counts"][col] = int(df[col].nunique())

    return profile