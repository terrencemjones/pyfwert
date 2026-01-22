#!/usr/bin/env python3
"""Pyfwert - Pattern-based password generator.

This is a standalone script for development/testing.
After installation, use: python -m pyfwert
"""

import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pyfwert.cli import main

if __name__ == "__main__":
    main()
