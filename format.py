#!/usr/bin/env python3
"""
Code formatting script for PDF Manipulate

Automatically formats code using Black.
"""

import sys
import subprocess


def main():
    """Format all Python code"""
    print("Formatting Python code with Black...")
    
    try:
        result = subprocess.run(
            ["black", "src/", "tests/", "*.py"],
            check=False
        )
        
        if result.returncode == 0:
            print("✅ Code formatting complete!")
            return 0
        else:
            print("❌ Formatting failed")
            return 1
            
    except FileNotFoundError:
        print("❌ Black not found. Install with: pip install black")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
