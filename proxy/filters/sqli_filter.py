import os

def is_enabled():
    # Returns True if SQLi filter enabled via env var
    return os.environ.get("ENABLE_SQLI_FILTER", "0") == "1"

def detect_attack(args):
    # Check each argument for SQL injection patterns
    for key, value in args.items():
        if not isinstance(value, str):
            continue
        # Simple check for common SQL injection patterns
        if "'" in value or "1=1" in value or "--" in value or "OR" in value.upper() or "AND" in value.upper():
            return True
    return False
