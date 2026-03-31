from typing import Dict, Any
import pandas as pd


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    df = state.get("data")

    if df is None:
        raise ValueError("No data found in state")

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Data must be a pandas DataFrame")

    if df.empty:
        raise ValueError("Dataset is empty")

    # Normalize column names
    df.columns = [col.strip().lower() for col in df.columns]

    state["data"] = df
    return state