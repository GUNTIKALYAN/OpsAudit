from typing import TypedDict, Dict, List, Any


class MetaSchema(TypedDict, total=False):
    rows: int
    columns: List[str]


class StateSchema(TypedDict, total=False):
    """
    Global state shared across all agents
    """

    # Core data
    data: Any

    # Data understanding
    profile: Dict[str, Any]

    # Detected issues
    issues: List[Dict[str, Any]]

    # Final report
    report: Any

    # Metadata
    meta: MetaSchema

    # Error tracking
    errors: List[str]