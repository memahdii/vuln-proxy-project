import os
import re

def is_enabled():
    # Returns True if SQLi filter enabled via env var
    return os.environ.get("ENABLE_SQLI_FILTER", "0") == "1"

def detect_attack(request_data):
    """
    Detect SQL injection attacks in request data
    Args:
        request_data: dict containing 'args', 'form', 'method', 'path'
    """
    # Check GET parameters
    if 'args' in request_data:
        for key, value in request_data['args'].items():
            if not isinstance(value, str):
                continue
            
            # Better regex patterns that won't block legitimate usernames like "Igor"
            sql_patterns = [
                r"'\s*(OR|AND)\s+",             # ' OR, ' AND
                r"'\s*--\s*$",                  # ' --
                r"'\s*#\s*$",                   # ' #
                r"'\s*/\*",                     # ' /*
                r'\b(OR|AND)\s+\d+\s*=\s*\d+',  # OR 1=1, AND 1=1
                r'\bUNION\s+SELECT\b',          # UNION SELECT
                r'\bSELECT\s+\*',               # SELECT *
                r'\bDROP\s+TABLE\b',            # DROP TABLE
                r'\bDELETE\s+FROM\b',           # DELETE FROM
                r'\bINSERT\s+INTO\b',           # INSERT INTO
                r'\bUPDATE\s+SET\b',            # UPDATE SET
                r';\s*(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE)',  # ; SELECT
            ]
            
            # Check each pattern
            for pattern in sql_patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    print(f"SQLi pattern detected: {pattern} in {key}={value}")
                    return True
    
    # Check POST form data
    if 'form' in request_data and request_data['method'] == 'POST':
        for key, value in request_data['form'].items():
            if not isinstance(value, str):
                continue
            
            # Same patterns for POST data
            sql_patterns = [
                r"'\s*(OR|AND)\s+",             # ' OR, ' AND
                r"'\s*--\s*$",                  # ' --
                r"'\s*#\s*$",                   # ' #
                r"'\s*/\*",                     # ' /*
                r'\b(OR|AND)\s+\d+\s*=\s*\d+',  # OR 1=1, AND 1=1
                r'\bUNION\s+SELECT\b',          # UNION SELECT
                r'\bSELECT\s+\*',               # SELECT *
                r'\bDROP\s+TABLE\b',            # DROP TABLE
                r'\bDELETE\s+FROM\b',           # DELETE FROM
                r'\bINSERT\s+INTO\b',           # INSERT INTO
                r'\bUPDATE\s+SET\b',            # UPDATE SET
                r';\s*(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE)',  # ; SELECT
            ]
            
            # Check each pattern
            for pattern in sql_patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    print(f"SQLi pattern detected: {pattern} in {key}={value}")
                    return True
                    
    return False

def is_sqli_pattern(value):
    """
    Check if a value contains SQLi patterns without blocking legitimate usernames.
    This is used for logging and monitoring purposes.
    """
    if not isinstance(value, str):
        return False
    
    # More lenient patterns for detection (not blocking)
    detection_patterns = [
        r'\b(OR|AND)\s+\d+\s*=\s*\d+',  # OR 1=1, AND 1=1
        r'\bUNION\s+SELECT\b',          # UNION SELECT
        r'\bSELECT\s+\*',               # SELECT *
        r'\bDROP\s+TABLE\b',            # DROP TABLE
        r'\bDELETE\s+FROM\b',           # DELETE FROM
        r'\bINSERT\s+INTO\b',           # INSERT INTO
        r'\bUPDATE\s+SET\b',            # UPDATE SET
        r"'\s*(OR|AND)\s+",             # ' OR, ' AND
        r"'\s*--\s*$",                  # ' --
        r"'\s*#\s*$",                   # ' #
        r"'\s*/\*",                     # ' /*
        r';\s*(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE)',  # ; SELECT
    ]
    
    for pattern in detection_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            return True
            
    return False
