from typing import TypedDict, Any, Dict, List, Annotated
from operator import add

class AuditState(TypedDict, total=False):
    # Core Data
    data: Any                     # Pandas DataFrame
    profile: Dict[str, Any]       # Schema profiling info

    # Issues detected by agents
    issues: Annotated[List[Dict[str, Any]], add]  

    # Final report
    report: List[Dict[str, Any]]

    # Metadata
    meta: Dict[str, Any]

    # Control flags (for future extension)
    errors: Annotated[List[str], add]