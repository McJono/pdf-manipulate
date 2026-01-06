#!/usr/bin/env python3
"""
Demo script to showcase tooltip functionality.

This demonstrates the ToolTip widget with various UI elements.
"""

import tkinter as tk
from tkinter import ttk
from src.ui.tooltip import create_tooltip


def main():
    """Main demo function."""
    root = tk.Tk()
    root.title("Tooltip Demo - PDF Manipulate")
    root.geometry("500x400")
    
    # Main frame
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title = ttk.Label(
        frame,
        text="Tooltip Demo",
        font=("Arial", 16, "bold")
    )
    title.pack(pady=(0, 20))
    
    # Description
    desc = ttk.Label(
        frame,
        text="Hover over the buttons below to see tooltips:",
        font=("Arial", 10)
    )
    desc.pack(pady=(0, 20))
    
    # Buttons with tooltips
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=10)
    
    # Button 1
    btn1 = ttk.Button(button_frame, text="Open Folder")
    btn1.pack(pady=5)
    create_tooltip(btn1, "Open a folder and display all PDF files")
    
    # Button 2
    btn2 = ttk.Button(button_frame, text="Merge PDFs")
    btn2.pack(pady=5)
    create_tooltip(
        btn2, 
        "Merge all files in the queue into a single PDF\n(Select at least 2 files to enable)"
    )
    
    # Button 3
    btn3 = ttk.Button(button_frame, text="Zoom In")
    btn3.pack(pady=5)
    create_tooltip(btn3, "Zoom in to see more detail")
    
    # Button 4
    btn4 = ttk.Button(button_frame, text="Zoom Out")
    btn4.pack(pady=5)
    create_tooltip(btn4, "Zoom out to see more of the page")
    
    # Entry with tooltip
    entry_frame = ttk.Frame(frame)
    entry_frame.pack(pady=20)
    
    ttk.Label(entry_frame, text="Name:").pack(side=tk.LEFT, padx=5)
    entry = ttk.Entry(entry_frame, width=30)
    entry.pack(side=tk.LEFT)
    create_tooltip(entry, "Enter a name for the merged PDF file")
    
    # Info
    info = ttk.Label(
        frame,
        text="Tooltips appear after hovering for 500ms",
        font=("Arial", 9),
        foreground="gray"
    )
    info.pack(side=tk.BOTTOM, pady=10)
    
    root.mainloop()


if __name__ == "__main__":
    main()
