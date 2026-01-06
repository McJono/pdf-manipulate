"""
Tooltip widget for Tkinter applications.

Provides simple hover tooltips for UI elements.
"""

import tkinter as tk
from typing import Optional


class ToolTip:
    """
    Create a tooltip for a given widget.
    
    Usage:
        button = ttk.Button(root, text="Click me")
        ToolTip(button, "This is a helpful tooltip")
    """
    
    def __init__(self, widget: tk.Widget, text: str, delay: int = 500):
        """
        Initialize tooltip.
        
        Args:
            widget: The widget to attach tooltip to
            text: Tooltip text to display
            delay: Delay in milliseconds before showing tooltip
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip_window: Optional[tk.Toplevel] = None
        self.schedule_id: Optional[str] = None
        
        # Bind events
        self.widget.bind("<Enter>", self._on_enter)
        self.widget.bind("<Leave>", self._on_leave)
        self.widget.bind("<Button>", self._on_leave)  # Hide on click
    
    def _on_enter(self, event=None):
        """Handle mouse enter event."""
        self._cancel_schedule()
        self.schedule_id = self.widget.after(self.delay, self._show_tip)
    
    def _on_leave(self, event=None):
        """Handle mouse leave event."""
        self._cancel_schedule()
        self._hide_tip()
    
    def _cancel_schedule(self):
        """Cancel scheduled tooltip display."""
        if self.schedule_id:
            self.widget.after_cancel(self.schedule_id)
            self.schedule_id = None
    
    def _show_tip(self):
        """Display the tooltip."""
        if self.tip_window or not self.text:
            return
        
        # Get widget position
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        # Create tooltip window
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)  # Remove window decorations
        self.tip_window.wm_geometry(f"+{x}+{y}")
        
        # Create label with tooltip text
        label = tk.Label(
            self.tip_window,
            text=self.text,
            justify=tk.LEFT,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Arial", 9, "normal"),
            padx=5,
            pady=3
        )
        label.pack()
    
    def _hide_tip(self):
        """Hide the tooltip."""
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


def create_tooltip(widget: tk.Widget, text: str, delay: int = 500) -> ToolTip:
    """
    Helper function to create a tooltip.
    
    Args:
        widget: The widget to attach tooltip to
        text: Tooltip text to display
        delay: Delay in milliseconds before showing tooltip
        
    Returns:
        ToolTip instance
    """
    return ToolTip(widget, text, delay)
