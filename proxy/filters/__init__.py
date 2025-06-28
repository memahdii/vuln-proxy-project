# This file makes the filters directory a Python package

from .sqli_filter import is_enabled as sqli_enabled, detect_attack as detect_sqli
from .xss_filter import is_enabled as xss_enabled, detect_attack as detect_xss

__all__ = ['sqli_enabled', 'detect_sqli', 'xss_enabled', 'detect_xss']

# Dynamic Filter System
import os
import importlib.util
import glob
from typing import Dict, Any

class FilterManager:
    def __init__(self, filters_dir: str = "filters"):
        self.filters_dir = filters_dir
        self.filters = {}
        self.discover_filters()
    
    def discover_filters(self):
        """Automatically discover all filter modules"""
        # Find all Python files in filters directory
        filter_files = glob.glob(os.path.join(self.filters_dir, "*.py"))
        
        for filter_file in filter_files:
            if filter_file.endswith("__init__.py"):
                continue
                
            module_name = os.path.basename(filter_file)[:-3]  # Remove .py
            try:
                # Import the filter module
                spec = importlib.util.spec_from_file_location(module_name, filter_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check if module has required attributes
                if hasattr(module, 'is_enabled') and hasattr(module, 'detect_attack'):
                    self.filters[module_name] = module
                    print(f"✓ Discovered filter: {module_name}")
                else:
                    print(f"⚠ Skipping {module_name}: missing required attributes")
                    
            except Exception as e:
                print(f"✗ Error loading {module_name}: {e}")
    
    def check_all_filters(self, request_data: Dict[str, Any]) -> bool:
        """Check all enabled filters"""
        for filter_name, filter_module in self.filters.items():
            if filter_module.is_enabled():
                if filter_module.detect_attack(request_data):
                    print(f"Attack blocked by {filter_name} filter")
                    return True
        return False

# Initialize filter manager
filter_manager = FilterManager()
