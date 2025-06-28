#!/usr/bin/env python3
"""
Template for creating new attack modules
Copy this file and modify it to create your own attack
"""

import requests

# Attack metadata - REQUIRED
name = "Your Attack Name"
description = "Description of what this attack does"
category = "Category (e.g., Injection, Authentication, etc.)"

def run_attack(target_url: str = "http://proxy:8000/endpoint", **kwargs):
    """
    Main attack function - REQUIRED
    
    Args:
        target_url: The target URL to attack
        **kwargs: Additional parameters
    
    Returns:
        dict: Attack results with the following structure:
        {
            "attack_type": "Attack Type Name",
            "total_tests": number_of_tests,
            "blocked": number_blocked,
            "successful": number_successful,
            "results": list_of_test_results
        }
    """
    results = []
    
    # Define your test cases here
    test_cases = [
        {
            "name": "Test Case 1",
            "payload": "your_payload_here",
            "method": "GET",  # or "POST"
            "data": {"param": "value"},  # for POST requests
            "expected": "success"  # or "blocked"
        },
        # Add more test cases...
    ]
    
    print(f"Testing {len(test_cases)} scenarios...")
    
    for test_case in test_cases:
        try:
            if test_case.get("method", "GET") == "GET":
                response = requests.get(
                    target_url, 
                    params=test_case.get("data", {}),
                    timeout=5
                )
            else:
                response = requests.post(
                    target_url,
                    data=test_case.get("data", {}),
                    timeout=5
                )
            
            result = {
                "test": test_case['name'],
                "status_code": response.status_code,
                "response": response.text.strip()[:100] + "..." if len(response.text) > 100 else response.text.strip(),
                "blocked": response.status_code == 403,
                "success": response.status_code == 200
            }
            
            results.append(result)
            
            # Print result
            status = "BLOCKED" if result["blocked"] else "ALLOWED"
            print(f"  {test_case['name']}: {status} ({response.status_code})")
            
        except Exception as e:
            result = {
                "test": test_case['name'],
                "error": str(e),
                "blocked": False,
                "success": False
            }
            results.append(result)
            print(f"  {test_case['name']}: ERROR - {e}")
    
    return {
        "attack_type": name,
        "total_tests": len(test_cases),
        "blocked": sum(1 for r in results if r.get("blocked")),
        "successful": sum(1 for r in results if r.get("success")),
        "results": results
    }

# Example: How to add a new attack
"""
Example: Command Injection Attack

1. Copy this template:
   cp template_attack.py command_injection_attack.py

2. Modify the metadata:
   name = "Command Injection Attack"
   description = "Tests command injection vulnerabilities"
   category = "Injection"

3. Add your test cases:
   test_cases = [
       {
           "name": "Basic Command Injection",
           "payload": "; ls -la",
           "method": "POST",
           "data": {"command": "; ls -la"},
           "expected": "blocked"
       }
   ]

4. The attack will be automatically discovered and run!
""" 