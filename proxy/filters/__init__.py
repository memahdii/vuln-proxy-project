# This file makes the filters directory a Python package

from .sqli_filter import is_enabled as sqli_enabled, detect_attack as detect_sqli
from .xss_filter import is_enabled as xss_enabled, detect_attack as detect_xss

__all__ = ['sqli_enabled', 'detect_sqli', 'xss_enabled', 'detect_xss']
