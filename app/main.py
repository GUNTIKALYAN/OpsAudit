import sys
from fastapi import FastAPI

from app.api.routes import router as api_router
from app.core.runner import OpsAuditRunner


# FASTAPI APP
app = FastAPI(
    title="OpsAudit AI",
    description="AI-powered system to detect and analyze data inefficiencies",
    version="1.0.0"
)

app.include_router(api_router)



# CLI MODE
def run_cli(file_path: str):
    runner = OpsAuditRunner()
    result = runner.run(file_path)

    if result["status"] == "success":
        report = result["report"]

        print("\nAudit Completed Successfully\n")

        print("Summary:")
        print(report.get("summary", {}))

        print("\nHigh Priority Issues:")
        for item in report.get("grouped", {}).get("high", []):
            print(item)

        print("\nSample Issues:")
        for item in report.get("details", [])[:3]:
            print(item)

    else:
        print("\nError:")
        print(result["message"])


# CLI ENTRY (optional)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python app/main.py <file_path>")
        sys.exit(1)

    run_cli(sys.argv[1])