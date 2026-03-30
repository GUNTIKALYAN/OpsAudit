from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil

from app.api.controller import AuditController
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()
controller = AuditController()


# Health Check
@router.get("/health")
def health_check():
    return {"status": "ok", "service": "OpsAudit AI"}


# Upload + Audit Endpoint
@router.post("/audit")
async def audit_file(file: UploadFile = File(...)):
    """
    Upload file and run audit
    """

    try:
        # Validate file type
        if not any(file.filename.endswith(ext) for ext in settings.ALLOWED_FILE_TYPES):
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Save file temporarily
        os.makedirs("temp", exist_ok=True)
        temp_path = os.path.join("temp", file.filename)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run audit
        result = controller.run_audit(temp_path)

        # Cleanup
        try:
            os.remove(temp_path)
        except Exception:
            pass

        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])

        return {
            "status": "success",
            "report": result["data"]
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")