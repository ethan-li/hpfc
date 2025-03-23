"""
Path setup helper for tests

This module adds the project root directory to the Python path,
allowing test modules to import the package without E402 warnings.
"""

import os
import sys

# Add parent directory to path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
