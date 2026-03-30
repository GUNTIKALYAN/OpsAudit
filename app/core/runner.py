import os
import traceback
from typing import Any, Dict

from app.config import settings
from app.graph.builder import build_graph
from app.services.data_loader import load_data
from app.utils.logger import get_logger
from app.utils.helpers import validate_file, mask_sensitive_data
from app.schemas.report_schema import FinalReport

logger = get_logger(__name__)


class OpsAuditRunner:
    def __init__(self):
        self.graph = build_graph()

    def run(self, file_path: str) -> Dict[str, Any]:
        try:
            logger.info("Starting OpsAudit pipeline...")

            validate_file(file_path, settings)

            df = load_data(file_path)

            if df.empty:
                raise ValueError("Input dataset is empty")

            if settings.MASK_SENSITIVE_DATA:
                df = mask_sensitive_data(df, settings.SENSITIVE_COLUMNS)

            state = {
                "data": df,
                "profile": {},
                "issues": [],
                "report": [],
                "meta": {
                    "rows": len(df),
                    "columns": list(df.columns)
                }
            }

            final_state = self.graph.invoke(state)

            report = final_state.get("report")

            validated_report = FinalReport(**report)

            if settings.SAVE_REPORT:
                self._save_report(validated_report.model_dump())

            return {
                "status": "success",
                "report": validated_report.model_dump()
            }

        except Exception as e:
            logger.error(str(e))
            traceback.print_exc()

            return {
                "status": "error",
                "message": str(e)
            }

    def _save_report(self, report: Dict[str, Any]):
        os.makedirs(settings.OUTPUT_DIR, exist_ok=True)

        import json
        with open(os.path.join(settings.OUTPUT_DIR, "audit_report.json"), "w") as f:
            json.dump(report, f, indent=4)