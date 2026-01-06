#!/usr/bin/env python3
"""
Demo script for testing the naming dialog UI
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.naming_dialog import show_naming_dialog


def main():
    """Run naming dialog demo"""
    root = tk.Tk()
    root.title("Naming Dialog Demo")
    root.geometry("400x200")
    
    # Center label
    label = tk.Label(
        root,
        text="Click the button to test the naming dialog",
        pady=20
    )
    label.pack()
    
    def show_dialog():
        """Show the naming dialog"""
        def on_save(filename):
            messagebox.showinfo(
                "Result",
                f"You chose the filename:\n\n{filename}\n\n"
                "In a real scenario, this would save the file."
            )
            return True  # Return True to close dialog
        
        result = show_naming_dialog(
            root,
            title="Test Naming Dialog",
            default_filename="merged_document",
            on_save=on_save
        )
        
        if result:
            print(f"Dialog returned: {result}")
        else:
            print("Dialog cancelled")
    
    # Button to open dialog
    button = tk.Button(
        root,
        text="Open Naming Dialog",
        command=show_dialog,
        width=20,
        height=2
    )
    button.pack(pady=20)
    
    # Close button
    close_button = tk.Button(
        root,
        text="Close Demo",
        command=root.quit,
        width=20
    )
    close_button.pack(pady=10)
    
    root.mainloop()


if __name__ == "__main__":
    main()
