#!/usr/bin/env python3
"""
Linting and code quality checking script for PDF Manipulate

This script runs various code quality tools on the project.
"""

import sys
import subprocess
from pathlib import Path


def run_command(cmd: list, description: str) -> bool:
    """
    Run a command and return success status.
    
    Args:
        cmd: Command to run as list
        description: Description of what's being checked
    
    Returns:
        True if command succeeded, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, check=False, capture_output=False)
        if result.returncode == 0:
            print(f"✅ {description} passed")
            return True
        else:
            print(f"❌ {description} failed")
            return False
    except FileNotFoundError:
        print(f"⚠️  Tool not found. Install with: pip install {cmd[0]}")
        return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False


def main():
    """Run all linting and quality checks"""
    print("PDF Manipulate - Code Quality Checks")
    print("=" * 60)
    
    # Change to project root
    project_root = Path(__file__).parent
    
    results = []
    
    # 1. Black - Code formatting
    results.append(run_command(
        ["black", "--check", "src/", "tests/"],
        "Black code formatting check"
    ))
    
    # 2. Pylint - Code quality
    results.append(run_command(
        ["pylint", "src/"],
        "Pylint code quality check"
    ))
    
    # 3. MyPy - Type checking
    results.append(run_command(
        ["mypy", "src/", "--ignore-missing-imports"],
        "MyPy type checking"
    ))
    
    # 4. Flake8 - Style guide enforcement
    results.append(run_command(
        ["flake8", "src/", "tests/", "--max-line-length=100"],
        "Flake8 style check"
    ))
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All checks passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} check(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
