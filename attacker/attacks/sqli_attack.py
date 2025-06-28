#!/usr/bin/env python3
"""
SQL Injection Attack Module
"""

import requests

# Attack metadata
name = "SQL Injection Attack"
description = "Tests various SQL injection techniques against login endpoint"
category = "Injection"

def run_attack(target_url: str = "http://proxy:8000/login", **kwargs):
    """Run SQL injection attacks"""
    results = []
    
    # Test cases
    test_cases = [
        {
            "name": "Normal Login",
            "username": "admin",
            "password": "adminpass",
            "expected": "success"
        },
        {
            "name": "OR Injection",
            "username": "admin' OR '1'='1",
            "password": "anything",
            "expected": "blocked"
        },
        {
            "name": "Comment Injection",
            "username": "admin' --",
            "password": "anything", 
            "expected": "blocked"
        },
        {
            "name": "UNION Injection",
            "username": "admin' UNION SELECT * FROM users --",
            "password": "anything",
            "expected": "blocked"
        }
    ]
    
    print(f"Testing {len(test_cases)} SQL injection scenarios...")
    
    for test_case in test_cases:
        try:
            params = {
                'username': test_case['username'],
                'password': test_case['password']
            }
            
            response = requests.get(target_url, params=params, timeout=5)
            
            result = {
                "test": test_case['name'],
                "status_code": response.status_code,
                "response": response.text.strip(),
                "blocked": response.status_code == 403,
                "success": response.status_code == 200 and "successful" in response.text.lower()
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
        "attack_type": "SQL Injection",
        "total_tests": len(test_cases),
        "blocked": sum(1 for r in results if r.get("blocked")),
        "successful": sum(1 for r in results if r.get("success")),
        "results": results
    } 