from typing import Dict, Any, List
import json
import uuid

from app.services.scoring import calculate_severity
from app.services.llm_client import call_llm
from app.utils.logger import get_logger

logger = get_logger(__name__)


# MAIN AGENT
def calculate_confidence(issue: Dict[str, Any]) -> float:
    """
    Confidence based on type of detection
    """

    issue_type = issue.get("type")

    if issue_type in ["duplicate", "missing"]:
        return 0.95  

    if issue_type == "logic_error":
        return 0.9

    if issue_type == "anomaly":
        return 0.75

    return 0.6


def calculate_impact(issue: Dict[str, Any], total_rows: int) -> float:
    """
    Impact score (0–1 scale)
    """

    if issue["type"] == "missing":
        return issue.get("missing_percentage", 0) / 100

    if issue["type"] == "duplicate":
        return issue.get("count", 0) / max(total_rows, 1)

    if issue["type"] == "logic_error":
        return issue.get("violations", 0) / max(total_rows, 1)

    if issue["type"] == "anomaly":
        return issue.get("outliers", 0) / max(total_rows, 1)

    return 0.1

def run(state: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = state.get("issues", [])
    report: List[Dict[str, Any]] = []

    total_rows = state.get("meta", {}).get("rows", 1)

    if not issues:
        return {"report": []}

    for issue in issues:
        try:
            enriched = enrich_issue(issue, total_rows)  # ✅ pass here
            report.append(enriched)
        except Exception as e:
            logger.error(f"Error processing issue: {e}")

    return {"report": report}


# ENRICHMENT LOGIC
def enrich_issue(issue: Dict[str, Any], total_rows: int) -> Dict[str, Any]:
    """
    Hybrid approach:
    1. Rule-based (always works)
    2. LLM enhancement (optional)
    """

    #  Rule-based baseline 
    severity = calculate_severity(issue, total_rows)
    impact, suggestion = generate_rule_based_insight(issue)
    confidence = calculate_confidence(issue)
    impact_score = calculate_impact(issue, total_rows)
    fallback = {
        "id": str(uuid.uuid4()),
        "type": issue.get("type"),
        "column": issue.get("column"),
        "impact": impact,
        "severity": severity,
        "suggestion": suggestion,
        "confidence": round(confidence, 2),
        "impact_score": round(impact_score, 2)
    }

    #  LLM Enhancement 
    try:
        llm_response = call_llm(
            system_prompt="You are a strict data quality expert. Return ONLY valid JSON.",
            user_prompt=json.dumps(issue)
        )

        if not llm_response:
            return fallback

        parsed = safe_parse_json(llm_response)

        if validate_llm_output(parsed):
            return parsed

    except Exception as e:
        logger.error(f"LLM enrichment failed: {e}")

    return fallback


# VALIDATION
def validate_llm_output(output: Dict[str, Any]) -> bool:
    if not isinstance(output, dict):
        return False

    required_keys = {"type", "impact", "severity", "suggestion"}

    if not required_keys.issubset(output.keys()):
        return False

    if output.get("severity") not in {"low", "medium", "high"}:
        return False

    return True


def safe_parse_json(text: str):
    try:
        return json.loads(text)
    except Exception:
        logger.warning("Failed to parse LLM response")
        return None



# RULE-BASED INSIGHTS
def generate_rule_based_insight(issue: Dict[str, Any]):
    issue_type = issue.get("type")

    if issue_type == "duplicate":
        return (
            "Duplicate records lead to inconsistent analytics and incorrect aggregations",
            "Remove duplicates and enforce unique constraints"
        )

    elif issue_type == "missing":
        return (
            "Missing values reduce data reliability and may break downstream systems",
            "Impute missing values or enforce validation at ingestion"
        )

    elif issue_type == "logic_error":
        return (
            "Logical inconsistencies indicate violations of business rules",
            "Add strict validation rules and constraints in pipeline"
        )

    elif issue_type == "anomaly":
        return (
            "Outliers may indicate abnormal behavior or data entry issues",
            "Investigate anomalies and apply normalization or filtering"
        )

    return (
        "Unknown issue detected",
        "Further investigation required"
    )