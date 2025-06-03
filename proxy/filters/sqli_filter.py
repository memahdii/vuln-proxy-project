import os  # Used to access environment variables

# Function to check whether the SQL injection filter is enabled
def is_enabled():
    # Returns True if the environment variable ENABLE_SQLI_FILTER is set to "1"
    return os.environ.get("ENABLE_SQLI_FILTER", "0") == "1"

# Function to detect potential SQL injection patterns in query parameters
def detect_attack(args):
    # Iterate through each query parameter (key-value pair)
    for key, value in args.items():
        if not isinstance(value, str):  # Ensure the value is a string
            continue

        # Simple heuristic-based check for common SQL injection patterns
        if (
            "'" in value or              # Single quote used in SQL strings
            "1=1" in value or            # Always-true condition
            "--" in value or             # SQL comment to truncate query
            "OR" in value.upper() or     # Logical OR (case-insensitive)
            "AND" in value.upper()       # Logical AND (case-insensitive)
        ):
            return True  # Potential SQLi detected

    return False  # No suspicious patterns found

