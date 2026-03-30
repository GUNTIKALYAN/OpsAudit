import os
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv

load_dotenv()  


@dataclass
class Settings:
    # App Config
    APP_NAME: str = "OpsAudit AI"
    DEBUG: bool = True

    # File Handling
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: List[str] = None

    # LLM Config (Groq)
    LLM_PROVIDER: str = "groq"
    LLM_MODEL: str = "llama-3.1-8b-instant"  
    LLM_TEMPERATURE: float = 0.2
    MAX_TOKENS: int = 1024

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "").strip()

    # Agent Controls
    MAX_AGENT_ITERATIONS: int = 10
    ENABLE_PARALLEL_AGENTS: bool = True

    # Data Safety
    MASK_SENSITIVE_DATA: bool = True
    SENSITIVE_COLUMNS: List[str] = None

    # Output Config
    OUTPUT_DIR: str = "outputs"
    SAVE_REPORT: bool = True

    # Logging
    LOG_LEVEL: str = "INFO"

    def __post_init__(self):
        if self.ALLOWED_FILE_TYPES is None:
            self.ALLOWED_FILE_TYPES = [".csv", ".json"]

        if self.SENSITIVE_COLUMNS is None:
            self.SENSITIVE_COLUMNS = [
                "email",
                "phone",
                "ssn",
                "password",
                "user_id"
            ]

        if not self.GROQ_API_KEY:
            print("⚠️ WARNING: GROQ_API_KEY not found. LLM features will be disabled.")


settings = Settings()

