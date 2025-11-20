"""
Example tests showing common testing patterns for PyQt6 Chess

These tests demonstrate:
- How to use fixtures
- How to mock components
- How to test signals
- How to test error conditions
- Best practices for test organization
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock, patch
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, pyqtSignal, QObject
from PyQt6.QtTest import QSignalSpy

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


# ============================================================================
# EXAMPLE 1: Basic Fixture Usage
# ============================================================================

class TestFixtureUsage:
    """Examples of using fixtures"""

    def test_using_qapp_fixture(self, qapp):
        """Example: Access QApplication instance"""
        assert qapp is not None
        assert isinstance(qapp, QApplication)

    def test_using_game_controller_fixture(self, game_controller):
        """Example: Use game controller fixture"""
        assert game_controller is not None
        assert game_controller.game_mode == 'pvp'

    def test_fixture_isolation(self, game_controller):
        """Example: Each test gets fresh fixture"""
        # This game_controller is independent of other tests
        game_controller.move_history = []
        assert len(game_controller.move_history) == 0


# ============================================================================
# EXAMPLE 2: Mocking Dependencies
# ============================================================================

class TestMockingPatterns:
    """Examples of mocking components"""

    def test_mock_ai_for_speed(self, game_controller, mock_ai):
        """
        Example: Use mocked AI to keep tests fast

        Instead of waiting for real AI calculation (could be seconds),
        mock returns immediately.
        """
        game_controller.ai = mock_ai

        # This returns instantly instead of thinking
        move, pos = game_controller.ai.get_best_move()
        assert move == {'to': (4, 4)}
        assert pos == (6, 4)

    def test_mock_board_method(self, game_controller):
        """Example: Mock specific board method"""
        # Replace real method with mock
        game_controller.board.get_legal_moves = MagicMock(
            return_value=[{'to': (4, 4)}, {'to': (5, 4)}]
        )

        # Test code using mocked method
        moves = game_controller.get_legal_moves((6, 4))
        assert len(moves) == 2

        # Verify mock was called correctly
        game_controller.board.get_legal_moves.assert_called_once_with((6, 4))

    def test_mock_with_side_effect(self, game_controller):
        """Example: Mock that raises exception"""
        game_controller.board.move = MagicMock(
            side_effect=Exception("Invalid move")
        )

        # Code handles exception gracefully
        with pytest.raises(Exception):
            game_controller.board.move((6, 4), {'to': (4, 4)})

    def test_patch_decorator(self):
        """Example: Using @patch to replace modules"""
        with patch('sys.exit') as mock_exit:
            # sys.exit is now mocked
            mock_exit.return_value = None

            # Can verify it was called
            mock_exit(0)
            mock_exit.assert_called_with(0)


# ============================================================================
# EXAMPLE 3: Testing Signals
# ============================================================================

class TestSignalExamples:
    """Examples of testing Qt signals"""

    def test_simple_signal_spy(self, game_controller):
        """Example: Verify signal is emitted"""
        spy = QSignalSpy(game_controller.gameStateChanged)

        # Action should emit signal
        game_controller.reset_game()

        # Verify signal was emitted at least once
        assert len(spy) >= 1

    def test_signal_with_arguments(self, main_window):
        """Example: Test signal with arguments"""
        spy = QSignalSpy(main_window.screen_changed)

        main_window.show_game_screen()

        # Signal emitted with 'game' argument
        assert len(spy) > 0
        assert spy[-1][0] == "game"

    def test_multiple_signal_emissions(self, main_window):
        """Example: Track multiple signal emissions"""
        spy = QSignalSpy(main_window.screen_changed)

        main_window.show_game_screen()  # Emits "game"
        main_window.show_menu_screen()  # Emits "menu"
        main_window.show_puzzle_screen()  # Emits "puzzle"

        assert len(spy) >= 3
        signals = [call[0] for call in spy]
        assert "game" in signals
        assert "menu" in signals
        assert "puzzle" in signals


# ============================================================================
# EXAMPLE 4: Testing Error Conditions
# ============================================================================

class TestErrorHandlingExamples:
    """Examples of testing error conditions"""

    def test_handling_invalid_move(self, game_controller):
        """Example: Test handling of illegal move"""
        game_controller.board.get_legal_moves = MagicMock(return_value=[])

        # Should handle gracefully without crashing
        game_controller.handle_move_attempt((6, 4), (5, 5))

    def test_handling_missing_data(self, game_controller):
        """Example: Test handling of missing puzzle"""
        puzzle = game_controller.puzzle_system.get_puzzle(9999)

        # Should return None instead of crashing
        assert puzzle is None

    def test_exception_handling(self, game_controller):
        """Example: Test exception handling"""
        game_controller.board.move = MagicMock(
            side_effect=Exception("Test error")
        )

        # Should emit error signal instead of crashing
        spy = QSignalSpy(game_controller.errorOccurred)
        try:
            game_controller.board.move(None, None)
        except:
            pass  # Expected


# ============================================================================
# EXAMPLE 5: Testing Game Logic
# ============================================================================

class TestGameLogicExamples:
    """Examples of testing game logic"""

    def test_game_mode_switching(self, game_controller):
        """Example: Test changing game modes"""
        # Start in PvP
        assert game_controller.game_mode == 'pvp'
        assert game_controller.ai is None

        # Switch to PvAI
        with patch('ui.game_controller.AI'):
            game_controller.set_game_mode('pvai', 'black', 'medium')
            assert game_controller.game_mode == 'pvai'
            assert game_controller.ai_color == 'black'
            assert game_controller.ai_difficulty == 'medium'

    def test_move_sequence(self, game_controller):
        """Example: Test sequence of moves"""
        game_controller.board.get_legal_moves = MagicMock(
            return_value=[{'to': (4, 4)}]
        )
        game_controller.board.move = MagicMock()
        game_controller.board.game_over = False
        game_controller.board.to_move = "white"

        # Make first move
        game_controller.handle_move_attempt((6, 4), (4, 4))
        assert len(game_controller.move_history) == 1

        # Make second move
        game_controller.handle_move_attempt((1, 4), (3, 4))
        assert len(game_controller.move_history) == 2

    def test_undo_functionality(self, game_controller):
        """Example: Test undo operation"""
        game_controller.move_history = [((6, 4), (4, 4), {})]
        game_controller.board.move_log = [{"from": (6, 4)}]
        game_controller.board.undo = MagicMock()

        game_controller.undo_move()

        # Verify board undo was called
        game_controller.board.undo.assert_called()
        assert len(game_controller.move_history) == 0


# ============================================================================
# EXAMPLE 6: Testing UI Components
# ============================================================================

class TestUIComponentExamples:
    """Examples of testing UI components"""

    def test_window_state(self, main_window):
        """Example: Test window properties"""
        assert main_window.windowTitle() == "PyQt6 Chess - Modern Chess Interface"
        assert main_window.width() == 940
        assert main_window.height() == 600

    def test_screen_switching(self, main_window):
        """Example: Test navigation between screens"""
        main_window.show()

        # Test each screen
        main_window.show_game_screen()
        assert main_window.stacked_widget.currentWidget() == main_window.game_screen

        main_window.show_menu_screen()
        assert main_window.stacked_widget.currentWidget() == main_window.menu_screen

    def test_dashboard_updates(self, main_window):
        """Example: Test dashboard update methods"""
        main_window.show_game_screen()

        # Update evaluation
        main_window.update_dashboard(eval_score=2.5)
        assert "+2.5" in main_window.eval_score_label.text()

        # Add moves to history
        main_window.add_move_to_history(1, "e4")
        main_window.add_move_to_history(1, "c5", "e5")

        assert main_window.move_history_list.count() == 2


# ============================================================================
# EXAMPLE 7: Testing Puzzle System
# ============================================================================

class TestPuzzleSystemExamples:
    """Examples of testing puzzle system"""

    def test_puzzle_loading(self, puzzle_system):
        """Example: Load puzzle and verify structure"""
        puzzle = puzzle_system.get_puzzle(1)

        assert puzzle is not None
        assert puzzle["id"] == 1
        assert "fen" in puzzle
        assert "solution" in puzzle
        assert len(puzzle["solution"]) > 0

    def test_puzzle_filtering(self, puzzle_system):
        """Example: Filter puzzles by difficulty"""
        easy_puzzles = puzzle_system.get_puzzles_by_difficulty("easy")

        assert len(easy_puzzles) > 0
        for puzzle in easy_puzzles:
            assert puzzle["difficulty"] == "easy"

    def test_puzzle_solving(self, puzzle_system):
        """Example: Test puzzle solving process"""
        puzzle_system.current_puzzle_index = 0
        puzzle = puzzle_system.get_puzzle()

        # Check first move
        first_move = puzzle["solution"][0]
        is_correct, is_complete, message = puzzle_system.check_move(first_move)

        assert is_correct
        assert len(puzzle_system.user_moves) == 1

    def test_puzzle_hints(self, puzzle_system):
        """Example: Test hint system"""
        puzzle_system.current_puzzle_index = 0
        puzzle_system.user_moves = []

        hint = puzzle_system.get_hint()

        assert hint is not None
        assert isinstance(hint, str)
        assert puzzle_system.hints_used > 0


# ============================================================================
# EXAMPLE 8: Parametrized Tests
# ============================================================================

class TestParametrizedExamples:
    """Examples of parametrized tests"""

    @pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
    def test_game_mode_with_difficulties(self, game_controller, difficulty):
        """Example: Test with multiple parameter values"""
        with patch('ui.game_controller.AI'):
            game_controller.set_game_mode('pvai', 'black', difficulty)
            assert game_controller.ai_difficulty == difficulty

    @pytest.mark.parametrize("screen,expected", [
        ("game", True),
        ("menu", False),
        ("tutorial", False),
        ("puzzle", False),
    ])
    def test_dashboard_visibility_on_screens(self, main_window, screen, expected):
        """Example: Test multiple scenarios with one test"""
        main_window.show()

        if screen == "game":
            main_window.show_game_screen()
        elif screen == "menu":
            main_window.show_menu_screen()
        elif screen == "tutorial":
            main_window.show_tutorial_screen()
        elif screen == "puzzle":
            main_window.show_puzzle_screen()

        assert main_window.dashboard_dock.isVisible() == expected


# ============================================================================
# EXAMPLE 9: Fixture Composition
# ============================================================================

@pytest.fixture
def game_with_ai(game_controller, mock_ai):
    """Example: Fixture that composes other fixtures"""
    game_controller.set_game_mode('pvai')
    game_controller.ai = mock_ai
    return game_controller


class TestFixtureComposition:
    """Examples of using composite fixtures"""

    def test_pvai_game_with_mock_ai(self, game_with_ai):
        """Example: Using a composite fixture"""
        assert game_with_ai.game_mode == 'pvai'
        assert game_with_ai.ai is not None

        # AI operations are fast with mock
        move, pos = game_with_ai.ai.get_best_move()
        assert move is not None


# ============================================================================
# EXAMPLE 10: Custom Test Decorators
# ============================================================================

def slow_test(func):
    """Example: Custom decorator to mark slow tests"""
    return pytest.mark.slow(func)


class TestCustomDecorators:
    """Examples of custom decorators"""

    @slow_test
    def test_slow_operation(self):
        """Example: Test marked as slow"""
        # This test will be marked with pytest.mark.slow
        # Can skip with: pytest -m "not slow"
        pass

    @pytest.mark.xfail(reason="Feature not implemented yet")
    def test_not_yet_implemented(self):
        """Example: Test for unimplemented feature"""
        # This test will be marked as expected to fail
        # Won't cause test suite to fail
        pass

    @pytest.mark.skip(reason="Requires display server")
    def test_requires_display(self):
        """Example: Skip test that requires display"""
        # This test will be skipped
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
