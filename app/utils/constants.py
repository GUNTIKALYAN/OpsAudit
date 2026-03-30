# Severity Levels
SEVERITY_HIGH = "high"
SEVERITY_MEDIUM = "medium"
SEVERITY_LOW = "low"

# Issue Types
ISSUE_DUPLICATE = "duplicate"
ISSUE_MISSING = "missing"
ISSUE_LOGIC = "logic_error"
ISSUE_ANOMALY = "anomaly"

# Default thresholds
MIN_ROWS_FOR_ANALYSIS = 10
MISSING_THRESHOLD_IGNORE = 5  # %
Z_SCORE_THRESHOLD = 3

# COLUMN IMPORTANCE
CRITICAL_COLUMNS = ["email", "user_id"]
IMPORTANT_COLUMNS = ["status", "start_date", "end_date"]