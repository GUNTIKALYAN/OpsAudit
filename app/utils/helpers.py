import os
import pandas as pd
from typing import List
from app.utils.logger import get_logger

logger = get_logger(__name__)


# FILE VALIDATION
def validate_file(file_path: str, settings) -> None:
    """
    Validates file existence, type, and size
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError("File not found")

    # Check extension
    if not any(file_path.endswith(ext) for ext in settings.ALLOWED_FILE_TYPES):
        raise ValueError("Unsupported file type")

    # Check size
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

    if file_size_mb > settings.MAX_FILE_SIZE_MB:
        raise ValueError("File size exceeds limit")


# DATA MASKING
def mask_sensitive_data(df: pd.DataFrame, sensitive_columns: List[str]) -> pd.DataFrame:
    """
    Masks sensitive data like email, phone, etc.
    """

    df = df.copy()

    for col in df.columns:
        if col.lower() in sensitive_columns:
            df[col] = df[col].apply(mask_value)

    return df


def mask_value(value):
    """
    Generic masking function
    """

    if pd.isnull(value):
        return value

    value = str(value)

    if len(value) <= 4:
        return "*" * len(value)

    return value[:2] + "*" * (len(value) - 4) + value[-2:]


# SAFE APPEND (for agents)
def safe_append_issue(state: dict, issue: dict):
    """
    Ensures issues list exists and appends safely
    """

    if "issues" not in state:
        state["issues"] = []

    if isinstance(issue, dict):
        state["issues"].append(issue)


# CLEAN TEXT (for LLM safety)
def clean_text(text: str) -> str:
    """
    Basic sanitization for LLM input
    """

    if not isinstance(text, str):
        return ""

    return text.strip().replace("\n", " ")