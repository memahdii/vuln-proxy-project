#!/usr/bin/env python3
"""
Template for creating new filter modules
Copy this file and modify it to create your own filter
"""

import os
import re

def is_enabled():
    """
    Check if this filter is enabled - REQUIRED
    
    Returns:
        bool: True if filter should be active
    """
    # You can use environment variables to control the filter
    return os.environ.get("ENABLE_YOUR_FILTER", "1") == "1"

def detect_attack(request_data):
    """
    Detect attacks in the request data - REQUIRED
    
    Args:
        request_data: dict containing:
            - 'args': GET parameters
            - 'form': POST form data
            - 'method': HTTP method
            - 'path': request path
    
    Returns:
        bool: True if attack detected, False otherwise
    """
    # Check GET parameters
    if 'args' in request_data:
        for key, value in request_data['args'].items():
            if not isinstance(value, str):
                continue
            
            # Add your detection patterns here
            patterns = [
                # Example patterns for your attack type
                r'your_pattern_here',
                r'another_pattern',
            ]
            
            for pattern in patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    return True
    
    # Check POST form data
    if 'form' in request_data and request_data['method'] == 'POST':
        for key, value in request_data['form'].items():
            if not isinstance(value, str):
                continue
            
            # Add your detection patterns here
            patterns = [
                # Example patterns for your attack type
                r'your_pattern_here',
                r'another_pattern',
            ]
            
            for pattern in patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    return True
    
    return False

# Example: How to add a new filter
"""
Example: Command Injection Filter

1. Copy this template:
   cp template_filter.py command_injection_filter.py

2. Modify the is_enabled function:
   def is_enabled():
       return os.environ.get("ENABLE_COMMAND_INJECTION_FILTER", "1") == "1"

3. Add your detection patterns:
   patterns = [
       r'[;&|`]',  # Command separators
       r'\b(cat|ls|pwd|whoami|id)\b',  # Common commands
       r'\$\{.*\}',  # Variable substitution
   ]

4. The filter will be automatically discovered and used!

5. Control it with environment variables:
   ENABLE_COMMAND_INJECTION_FILTER=1  # Enable
   ENABLE_COMMAND_INJECTION_FILTER=0  # Disable
""" 