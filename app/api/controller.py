from typing import Dict, Any
import os

from app.core.runner import OpsAuditRunner
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AuditController:
    def __init__(self):
        self.runner = OpsAuditRunner()

    def run_audit(self, file_path: str) -> Dict[str, Any]:
        
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError("File does not exist")

            result = self.runner.run(file_path)

            if result.get("status") != "success":
                return {
                    "success": False,
                    "error": result.get("message", "Unknown error")
                }

            return {
                "success": True,
                "data": result.get("report", {})
            }

        except Exception as e:
            logger.error(f"Controller error: {str(e)}")

            return {
                "success": False,
                "error": str(e)
            }