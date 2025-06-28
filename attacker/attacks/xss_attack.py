#!/usr/bin/env python3
"""
Cross-Site Scripting (XSS) Attack Module
"""

import requests

# Attack metadata
name = "Cross-Site Scripting Attack"
description = "Tests various XSS techniques against comment endpoint"
category = "Injection"

def run_attack(target_url: str = "http://proxy:8000/comment", **kwargs):
    """Run XSS attacks"""
    results = []
    
    # Test cases
    test_cases = [
        {
            "name": "Normal Comment",
            "payload": "Hello, this is a normal comment.",
            "expected": "success"
        },
        {
            "name": "Basic Script Tag",
            "payload": "<script>alert('XSS')</script>",
            "expected": "blocked"
        },
        {
            "name": "Event Handler",
            "payload": "<img src=x onerror=alert('XSS')>",
            "expected": "blocked"
        },
        {
            "name": "JavaScript Protocol",
            "payload": "<a href=\"javascript:alert('XSS')\">Click me</a>",
            "expected": "blocked"
        },
        {
            "name": "Encoded Script",
            "payload": "&#60;script&#62;alert('XSS')&#60;/script&#62;",
            "expected": "blocked"
        }
    ]
    
    print(f"Testing {len(test_cases)} XSS scenarios...")
    
    for test_case in test_cases:
        try:
            data = {'text': test_case['payload']}
            
            response = requests.post(target_url, data=data, timeout=5)
            
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
        "attack_type": "Cross-Site Scripting",
        "total_tests": len(test_cases),
        "blocked": sum(1 for r in results if r.get("blocked")),
        "successful": sum(1 for r in results if r.get("success")),
        "results": results
    } 