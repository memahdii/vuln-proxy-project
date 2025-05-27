import os

def is_enabled():
    # Returns True if SQLi filter enabled via env var
    return os.environ.get("ENABLE_SQLI_FILTER", "0") == "1"

def detect_attack(query_params):
    username = query_params.get("username", "")
    # Simple check for common SQL injection patterns
    if "'" in username or "1=1" in username or "--" in username:
        return True
    return False
