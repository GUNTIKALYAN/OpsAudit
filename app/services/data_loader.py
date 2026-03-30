import pandas as pd
from typing import Union


def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads data from CSV or JSON safely.
    """

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)

    elif file_path.endswith(".json"):
        df = pd.read_json(file_path)

    else:
        raise ValueError("Unsupported file format")

    # Basic cleanup
    df = df.copy()

    # Strip column names
    df.columns = [col.strip() for col in df.columns]

    return df