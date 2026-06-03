#!/usr/bin/env python3
"""Helper script to run the tests and show results."""

import subprocess
import sys


def main():
    print("=" * 60)
    print("Running tests with unittest:")
    print("=" * 60)
    result = subprocess.run([sys.executable, "test_pal.py"], capture_output=False)
    
    print("\n" + "=" * 60)
    print("Running tests with pytest (if available):")
    print("=" * 60)
    result2 = subprocess.run([sys.executable, "-m", "pytest", "test_pal.py", "-v"], capture_output=False)
    
    return result.returncode or result2.returncode


if __name__ == "__main__":
    sys.exit(main())
