import os
import re  # Regular expressions used to detect XSS patterns

# Function to check whether the XSS filter is enabled
def is_enabled():
    # Returns True if the environment variable ENABLE_XSS_FILTER is set to "1"
    return os.environ.get("ENABLE_XSS_FILTER", "0") == "1"

# Function to detect potential XSS attack patterns in input strings
def detect_attack(value):
    if not isinstance(value, str):  # Only check string input
        return False
        
    # List of regular expressions to match common XSS payloads
    xss_patterns = [
        r'<script.*?>.*?</script.*?>',   # Full <script> tags
        r'on\w+=',                       # Inline event handlers (e.g. onclick, onload)
        r'javascript:',                  # javascript: protocol
        r'<img.*?onerror=',              # <img> tag with onerror
        r'<svg.*?onload=',               # <svg> tag with onload
        r'<iframe.*?>',                  # <iframe> tag
        r'<object.*?>',                  # <object> tag
        r'<embed.*?>',                   # <embed> tag
        r'<form.*?>',                    # <form> tag
        r'<input.*?on\w+=',              # <input> with event handler
        r'<a.*?on\w+=',                  # <a> tag with event handler
        r'<div.*?on\w+=',                # <div> with inline JS
        r'<style.*?>.*?</style.*?>',     # <style> tags
        r'<link.*?on\w+=',               # <link> tag with event handler
        r'<meta.*?on\w+=',               # <meta> tag with event handler
    ]
    
    # Compile regex patterns for performance and case-insensitive matching
    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in xss_patterns]
    
    # Scan input for any matching XSS pattern
    for pattern in compiled_patterns:
        if pattern.search(value):
            return True  # XSS pattern detected

    return False  # No suspicious patterns found

