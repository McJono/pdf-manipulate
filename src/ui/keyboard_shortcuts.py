"""
Keyboard shortcuts manager for the PDF Manipulate application.

Provides centralized keyboard shortcut handling for consistent
user experience across all screens.
"""

import tkinter as tk
from typing import Callable, Dict, Optional
from ..utils.logger import logger


class KeyboardShortcuts:
    """
    Manages keyboard shortcuts for the application.
    
    Provides methods to bind common shortcuts and handle them consistently.
    """
    
    # Standard shortcuts
    SHORTCUTS = {
        # File operations
        'open_file': '<Control-o>',
        'save': '<Control-s>',
        'quit': '<Control-q>',
        
        # Edit operations
        'undo': '<Control-z>',
        'redo': '<Control-y>',
        'settings': '<Control-comma>',
        
        # Navigation
        'next': '<Right>',
        'prev': '<Left>',
        'up': '<Up>',
        'down': '<Down>',
        'page_up': '<Prior>',
        'page_down': '<Next>',
        'home': '<Home>',
        'end': '<End>',
        
        # Actions
        'rotate_right': '<Control-r>',
        'rotate_left': '<Control-Shift-R>',
        'accept': '<Return>',
        'cancel': '<Escape>',
        'delete': '<Delete>',
        'select_all': '<Control-a>',
        
        # View
        'zoom_in': '<Control-plus>',
        'zoom_out': '<Control-minus>',
        'zoom_reset': '<Control-0>',
        'fullscreen': '<F11>',
        
        # Tools
        'auto_rotate': '<Control-Alt-r>',
        'merge': '<Control-m>',
        
        # Help
        'help': '<F1>',
    }
    
    # macOS uses Command instead of Control
    SHORTCUTS_MAC = {
        'open_file': '<Command-o>',
        'save': '<Command-s>',
        'quit': '<Command-q>',
        'undo': '<Command-z>',
        'redo': '<Command-Shift-Z>',
        'settings': '<Command-comma>',
        'rotate_right': '<Command-r>',
        'rotate_left': '<Command-Shift-R>',
        'select_all': '<Command-a>',
        'zoom_in': '<Command-plus>',
        'zoom_out': '<Command-minus>',
        'zoom_reset': '<Command-0>',
        'auto_rotate': '<Command-Option-r>',
        'merge': '<Command-m>',
    }
    
    def __init__(self, widget: tk.Widget, platform: str = 'linux'):
        """
        Initialize keyboard shortcuts manager.
        
        Args:
            widget: Root widget to bind shortcuts to
            platform: Platform identifier ('linux', 'darwin', 'win32')
        """
        self.widget = widget
        self.platform = platform
        self.bindings: Dict[str, str] = {}
        
        # Use macOS shortcuts on darwin
        if platform == 'darwin':
            self.shortcuts = {**self.SHORTCUTS, **self.SHORTCUTS_MAC}
        else:
            self.shortcuts = self.SHORTCUTS.copy()
    
    def bind(self, action: str, callback: Callable, add: bool = True) -> Optional[str]:
        """
        Bind a keyboard shortcut.
        
        Args:
            action: Action name (e.g., 'open_file', 'undo')
            callback: Function to call when shortcut is pressed
            add: If True, add to existing bindings; if False, replace
            
        Returns:
            The shortcut key sequence that was bound, or None if action not found
        """
        if action not in self.shortcuts:
            logger.warning(f"Unknown shortcut action: {action}")
            return None
        
        sequence = self.shortcuts[action]
        
        try:
            # Wrap callback to return "break" to prevent default handling
            def wrapper(event=None):
                callback(event)
                return "break"
            
            self.widget.bind(sequence, wrapper, add=add)
            self.bindings[action] = sequence
            logger.debug(f"Bound shortcut {sequence} to {action}")
            return sequence
        except Exception as e:
            logger.error(f"Error binding shortcut {action}: {e}")
            return None
    
    def unbind(self, action: str) -> None:
        """
        Unbind a keyboard shortcut.
        
        Args:
            action: Action name to unbind
        """
        if action in self.bindings:
            sequence = self.bindings[action]
            self.widget.unbind(sequence)
            del self.bindings[action]
            logger.debug(f"Unbound shortcut {sequence} for {action}")
    
    def get_shortcut(self, action: str) -> Optional[str]:
        """
        Get the keyboard shortcut for an action.
        
        Args:
            action: Action name
            
        Returns:
            Shortcut key sequence, or None if not found
        """
        return self.shortcuts.get(action)
    
    def get_display_text(self, action: str) -> str:
        """
        Get human-readable text for a shortcut.
        
        Args:
            action: Action name
            
        Returns:
            Display text for the shortcut (e.g., "Ctrl+O", "Cmd+S")
        """
        sequence = self.shortcuts.get(action)
        if not sequence:
            return ""
        
        # Convert Tkinter key notation to display text
        text = sequence.replace('<', '').replace('>', '')
        text = text.replace('Control-', 'Ctrl+')
        text = text.replace('Command-', 'Cmd+')
        text = text.replace('Shift-', 'Shift+')
        text = text.replace('Alt-', 'Alt+')
        text = text.replace('Option-', 'Opt+')
        text = text.replace('Return', 'Enter')
        text = text.replace('Prior', 'PgUp')
        text = text.replace('Next', 'PgDn')
        
        return text


def create_shortcuts_manager(widget: tk.Widget) -> KeyboardShortcuts:
    """
    Create a keyboard shortcuts manager for a widget.
    
    Args:
        widget: Widget to bind shortcuts to
        
    Returns:
        KeyboardShortcuts instance
    """
    import sys
    platform = sys.platform
    return KeyboardShortcuts(widget, platform)
