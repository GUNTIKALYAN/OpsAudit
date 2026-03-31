from typing import Dict, Any

from app.services.rule_engine import validate_rules


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    df = state["data"]

    issues = validate_rules(df)

    return {"issues": issues}