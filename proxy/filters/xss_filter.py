import os
import re

def is_enabled():
    # Returns True if XSS filter enabled via env var
    return os.environ.get("ENABLE_XSS_FILTER", "0") == "1"

def detect_attack(value):
    if not isinstance(value, str):
        return False
        
    # Check for common XSS patterns
    xss_patterns = [
        r'<script.*?>.*?</script.*?>',  # Script tags
        r'on\w+=',                      # Event handlers
        r'javascript:',                 # JavaScript protocol
        r'<img.*?onerror=',            # Image with onerror
        r'<svg.*?onload=',             # SVG with onload
        r'<iframe.*?>',                # iframe tags
        r'<object.*?>',                # object tags
        r'<embed.*?>',                 # embed tags
        r'<form.*?>',                  # form tags
        r'<input.*?on\w+=',           # input with event handlers
        r'<a.*?on\w+=',               # anchor with event handlers
        r'<div.*?on\w+=',             # div with event handlers
        r'<style.*?>.*?</style.*?>',  # style tags
        r'<link.*?on\w+=',            # link with event handlers
        r'<meta.*?on\w+=',            # meta with event handlers
    ]
    
    # Compile patterns for better performance
    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in xss_patterns]
    
    # Check for XSS patterns
    for pattern in compiled_patterns:
        if pattern.search(value):
            return True
    return False
