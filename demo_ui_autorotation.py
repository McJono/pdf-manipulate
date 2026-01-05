#!/usr/bin/env python3
"""
Demo script for the auto-rotation UI.

Launches the auto-rotation screen GUI.
"""

import sys

try:
    from src.ui.auto_rotation_screen import show_auto_rotation_screen
except ImportError as e:
    print(f"Error: {e}")
    print("Make sure all dependencies are installed:")
    print("  pip install -r requirements.txt")
    sys.exit(1)


def main():
    """Main function"""
    print("Launching Auto-Rotation UI...")
    print("Note: This is a demo interface. Some features are placeholders.")
    print()
    
    show_auto_rotation_screen()


if __name__ == "__main__":
    main()
