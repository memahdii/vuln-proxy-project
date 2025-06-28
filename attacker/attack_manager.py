#!/usr/bin/env python3
"""
Dynamic Attack Manager
Automatically discovers and runs all attack modules
"""

import os
import importlib.util
import glob
from typing import List, Dict, Any

class AttackManager:
    def __init__(self, attacks_dir: str = "attacks"):
        self.attacks_dir = attacks_dir
        self.attacks = {}
        self.discover_attacks()
    
    def discover_attacks(self):
        """Automatically discover all attack modules"""
        if not os.path.exists(self.attacks_dir):
            print(f"Attacks directory '{self.attacks_dir}' not found. Creating it...")
            os.makedirs(self.attacks_dir)
            return
        
        # Find all Python files in attacks directory
        attack_files = glob.glob(os.path.join(self.attacks_dir, "*.py"))
        
        for attack_file in attack_files:
            if attack_file.endswith("__init__.py"):
                continue
                
            module_name = os.path.basename(attack_file)[:-3]  # Remove .py
            try:
                # Import the attack module
                spec = importlib.util.spec_from_file_location(module_name, attack_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check if module has required attributes
                if hasattr(module, 'name') and hasattr(module, 'run_attack'):
                    self.attacks[module_name] = module
                    print(f"✓ Discovered attack: {module.name}")
                else:
                    print(f"⚠ Skipping {module_name}: missing required attributes")
                    
            except Exception as e:
                print(f"✗ Error loading {module_name}: {e}")
    
    def list_attacks(self) -> List[str]:
        """List all available attacks"""
        return list(self.attacks.keys())
    
    def run_attack(self, attack_name: str, **kwargs) -> Dict[str, Any]:
        """Run a specific attack"""
        if attack_name not in self.attacks:
            return {"error": f"Attack '{attack_name}' not found"}
        
        try:
            result = self.attacks[attack_name].run_attack(**kwargs)
            return {"success": True, "attack": attack_name, "result": result}
        except Exception as e:
            return {"success": False, "attack": attack_name, "error": str(e)}
    
    def run_all_attacks(self, **kwargs) -> List[Dict[str, Any]]:
        """Run all discovered attacks"""
        results = []
        print(f"\n{'='*60}")
        print(f"Running {len(self.attacks)} discovered attacks...")
        print(f"{'='*60}")
        
        for attack_name in self.attacks:
            print(f"\n--- Running {attack_name} ---")
            result = self.run_attack(attack_name, **kwargs)
            results.append(result)
            
            if result.get("success"):
                print(f"✓ {attack_name}: Success")
            else:
                print(f"✗ {attack_name}: {result.get('error', 'Unknown error')}")
        
        return results

def main():
    """Main function to run all attacks"""
    manager = AttackManager()
    
    if not manager.attacks:
        print("No attacks found! Create attack modules in the 'attacks' directory.")
        return
    
    print(f"Found {len(manager.attacks)} attacks: {', '.join(manager.list_attacks())}")
    
    # Run all attacks
    results = manager.run_all_attacks()
    
    # Summary
    successful = sum(1 for r in results if r.get("success"))
    print(f"\n{'='*60}")
    print(f"SUMMARY: {successful}/{len(results)} attacks completed successfully")
    print(f"{'='*60}")

if __name__ == "__main__":
    main() 