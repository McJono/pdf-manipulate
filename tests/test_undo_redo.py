"""
Tests for undo/redo manager.
"""

import pytest
from pathlib import Path
from src.ui.undo_redo import UndoRedoManager, RotationAction


class TestUndoRedoManager:
    """Test undo/redo functionality."""
    
    def test_init(self):
        """Test initialization."""
        manager = UndoRedoManager(max_history=10)
        assert manager.max_history == 10
        assert not manager.can_undo()
        assert not manager.can_redo()
    
    def test_add_action(self):
        """Test adding an action."""
        manager = UndoRedoManager()
        action = RotationAction(
            pdf_path=Path("test.pdf"),
            page_num=1,
            old_rotation=0,
            new_rotation=90
        )
        
        manager.add_action(action)
        assert manager.can_undo()
        assert not manager.can_redo()
    
    def test_undo(self):
        """Test undo functionality."""
        manager = UndoRedoManager()
        action = RotationAction(
            pdf_path=Path("test.pdf"),
            page_num=1,
            old_rotation=0,
            new_rotation=90
        )
        
        manager.add_action(action)
        undone = manager.undo()
        
        assert undone == action
        assert not manager.can_undo()
        assert manager.can_redo()
    
    def test_redo(self):
        """Test redo functionality."""
        manager = UndoRedoManager()
        action = RotationAction(
            pdf_path=Path("test.pdf"),
            page_num=1,
            old_rotation=0,
            new_rotation=90
        )
        
        manager.add_action(action)
        manager.undo()
        redone = manager.redo()
        
        assert redone == action
        assert manager.can_undo()
        assert not manager.can_redo()
    
    def test_undo_redo_sequence(self):
        """Test a sequence of undo/redo operations."""
        manager = UndoRedoManager()
        
        # Add multiple actions
        actions = []
        for i in range(3):
            action = RotationAction(
                pdf_path=Path(f"test{i}.pdf"),
                page_num=i,
                old_rotation=0,
                new_rotation=90
            )
            actions.append(action)
            manager.add_action(action)
        
        # Undo twice
        assert manager.undo() == actions[2]
        assert manager.undo() == actions[1]
        
        # Redo once
        assert manager.redo() == actions[1]
        
        # Should be able to redo once more
        assert manager.can_redo()
        assert manager.redo() == actions[2]
        
        # No more redos
        assert not manager.can_redo()
    
    def test_add_action_clears_redo(self):
        """Test that adding a new action clears redo stack."""
        manager = UndoRedoManager()
        
        action1 = RotationAction(Path("test1.pdf"), 1, 0, 90)
        action2 = RotationAction(Path("test2.pdf"), 1, 0, 90)
        
        manager.add_action(action1)
        manager.undo()
        
        assert manager.can_redo()
        
        # Add new action should clear redo
        manager.add_action(action2)
        assert not manager.can_redo()
    
    def test_max_history(self):
        """Test that history is limited to max_history."""
        manager = UndoRedoManager(max_history=5)
        
        # Add more actions than max_history
        for i in range(10):
            action = RotationAction(Path(f"test{i}.pdf"), i, 0, 90)
            manager.add_action(action)
        
        # Should only have 5 actions
        undo_count, _ = manager.get_history_size()
        assert undo_count == 5
    
    def test_clear(self):
        """Test clearing history."""
        manager = UndoRedoManager()
        
        action = RotationAction(Path("test.pdf"), 1, 0, 90)
        manager.add_action(action)
        manager.undo()
        
        manager.clear()
        
        assert not manager.can_undo()
        assert not manager.can_redo()
        assert manager.get_history_size() == (0, 0)
    
    def test_get_descriptions(self):
        """Test getting action descriptions."""
        manager = UndoRedoManager()
        
        action = RotationAction(
            pdf_path=Path("test.pdf"),
            page_num=1,
            old_rotation=0,
            new_rotation=90
        )
        
        assert manager.get_undo_description() is None
        assert manager.get_redo_description() is None
        
        manager.add_action(action)
        assert manager.get_undo_description() is not None
        assert "test.pdf" in manager.get_undo_description()
        
        manager.undo()
        assert manager.get_redo_description() is not None
    
    def test_get_all_actions(self):
        """Test getting all actions."""
        manager = UndoRedoManager()
        
        actions = []
        for i in range(3):
            action = RotationAction(Path(f"test{i}.pdf"), i, 0, 90)
            actions.append(action)
            manager.add_action(action)
        
        all_actions = manager.get_all_actions()
        assert len(all_actions) == 3
        assert all_actions == actions
    
    def test_rotation_action_str(self):
        """Test RotationAction string representation."""
        action = RotationAction(
            pdf_path=Path("/path/to/test.pdf"),
            page_num=5,
            old_rotation=0,
            new_rotation=90
        )
        
        str_repr = str(action)
        assert "page 5" in str_repr
        assert "test.pdf" in str_repr
        assert "0°" in str_repr
        assert "90°" in str_repr
