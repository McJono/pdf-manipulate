"""
Undo/Redo functionality for PDF rotation operations.

Maintains a history of rotation operations and allows undoing/redoing them.
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
from ..utils.logger import logger


@dataclass
class RotationAction:
    """Represents a single rotation action that can be undone/redone."""
    
    pdf_path: Path
    page_num: int
    old_rotation: int  # 0, 90, 180, 270
    new_rotation: int  # 0, 90, 180, 270
    
    def __str__(self) -> str:
        """String representation."""
        return (f"Rotate page {self.page_num} of {self.pdf_path.name} "
                f"from {self.old_rotation}° to {self.new_rotation}°")


class UndoRedoManager:
    """
    Manages undo/redo history for rotation operations.
    
    Supports:
    - Adding rotation actions
    - Undoing last action
    - Redoing undone action
    - Clearing history
    - Getting history info
    """
    
    def __init__(self, max_history: int = 50):
        """
        Initialize undo/redo manager.
        
        Args:
            max_history: Maximum number of actions to keep in history
        """
        self.max_history = max_history
        self.undo_stack: List[RotationAction] = []
        self.redo_stack: List[RotationAction] = []
    
    def add_action(self, action: RotationAction) -> None:
        """
        Add a rotation action to the history.
        
        Args:
            action: The rotation action to add
        """
        self.undo_stack.append(action)
        
        # Trim history if needed
        if len(self.undo_stack) > self.max_history:
            self.undo_stack.pop(0)
        
        # Clear redo stack when new action is added
        self.redo_stack.clear()
        
        logger.debug(f"Added action to undo stack: {action}")
    
    def can_undo(self) -> bool:
        """
        Check if undo is available.
        
        Returns:
            True if there are actions to undo
        """
        return len(self.undo_stack) > 0
    
    def can_redo(self) -> bool:
        """
        Check if redo is available.
        
        Returns:
            True if there are actions to redo
        """
        return len(self.redo_stack) > 0
    
    def undo(self) -> Optional[RotationAction]:
        """
        Undo the last rotation action.
        
        Returns:
            The action that was undone, or None if nothing to undo
        """
        if not self.can_undo():
            logger.debug("Nothing to undo")
            return None
        
        action = self.undo_stack.pop()
        self.redo_stack.append(action)
        
        logger.info(f"Undoing: {action}")
        return action
    
    def redo(self) -> Optional[RotationAction]:
        """
        Redo the last undone action.
        
        Returns:
            The action that was redone, or None if nothing to redo
        """
        if not self.can_redo():
            logger.debug("Nothing to redo")
            return None
        
        action = self.redo_stack.pop()
        self.undo_stack.append(action)
        
        logger.info(f"Redoing: {action}")
        return action
    
    def clear(self) -> None:
        """Clear all undo/redo history."""
        self.undo_stack.clear()
        self.redo_stack.clear()
        logger.debug("Cleared undo/redo history")
    
    def get_undo_description(self) -> Optional[str]:
        """
        Get description of the action that would be undone.
        
        Returns:
            Description string, or None if nothing to undo
        """
        if not self.can_undo():
            return None
        return str(self.undo_stack[-1])
    
    def get_redo_description(self) -> Optional[str]:
        """
        Get description of the action that would be redone.
        
        Returns:
            Description string, or None if nothing to redo
        """
        if not self.can_redo():
            return None
        return str(self.redo_stack[-1])
    
    def get_history_size(self) -> Tuple[int, int]:
        """
        Get size of undo and redo stacks.
        
        Returns:
            Tuple of (undo_count, redo_count)
        """
        return (len(self.undo_stack), len(self.redo_stack))
    
    def get_all_actions(self) -> List[RotationAction]:
        """
        Get all actions in undo stack (most recent last).
        
        Returns:
            List of RotationAction objects
        """
        return self.undo_stack.copy()
