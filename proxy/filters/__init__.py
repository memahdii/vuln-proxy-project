# This file makes the filters directory a Python package

# Import functions from submodules and give them shorter/more consistent names
from .sqli_filter import is_enabled as sqli_enabled, detect_attack as detect_sqli
from .xss_filter import is_enabled as xss_enabled, detect_attack as detect_xss

# Define what gets imported when using `from filters import *`
__all__ = ['sqli_enabled', 'detect_sqli', 'xss_enabled', 'detect_xss']

