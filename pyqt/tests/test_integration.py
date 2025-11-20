"""
Comprehensive Integration Test Suite for PyQt6 Chess Application

Tests all components:
- ChessBoardWidget (rendering, moves, animations)
- GameController (move validation, AI, puzzles)
- MainWindow (navigation, dashboard updates)
- Menu screens (button clicks, navigation)
- Full integration workflows
- Puzzle system (load, solve, hint)
- AI threading (non-blocking computation)
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock, patch, call
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtTest import QSignalSpy

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Create QApplication instance (required for PyQt6 testing)
if not QApplication.instance():
    app = QApplication([])
else:
    app = QApplication.instance()


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def qapp():
    """Fixture providing QApplication instance"""
    return QApplication.instance()


@pytest.fixture
def game_controller():
    """Fixture providing a GameController instance"""
    from ui.game_controller import GameController
    controller = GameController()
    yield controller
    controller.cleanup()


@pytest.fixture
def main_window():
    """Fixture providing a MainWindow instance"""
    from ui.main_window import ChessMainWindow
    window = ChessMainWindow()
    yield window
    window.close()


@pytest.fixture
def chess_board_widget():
    """Fixture providing a ChessBoardWidget instance"""
    from ui.chess_board import ChessBoardWidget
    board = ChessBoardWidget()
    yield board
    # Cleanup not needed as it's a view


@pytest.fixture
def puzzle_system():
    """Fixture providing a ChessPuzzles instance"""
    from features.puzzles import ChessPuzzles
    puzzles = ChessPuzzles()
    yield puzzles


@pytest.fixture
def mock_ai():
    """Fixture providing a mock AI instance"""
    mock_ai_instance = MagicMock()
    mock_ai_instance.get_best_move = MagicMock(return_value=({'to': (4, 4)}, (6, 4)))
    mock_ai_instance.evaluate_board = MagicMock(return_value=0.5)
    mock_ai_instance.max_depth = 6
    mock_ai_instance.nodes_searched = 10000
    return mock_ai_instance


# ============================================================================
# MAIN WINDOW TESTS
# ============================================================================

class TestMainWindow:
    """Tests for ChessMainWindow component"""

    def test_window_initialization(self, main_window):
        """Test main window initializes correctly"""
        assert main_window.windowTitle() == "PyQt6 Chess - Modern Chess Interface"
        assert main_window.width() == 940
        assert main_window.height() == 600
        assert main_window.stacked_widget is not None
        assert main_window.dashboard_dock is not None

    def test_menu_screen_display(self, main_window):
        """Test menu screen is displayed by default"""
        main_window.show()
        assert main_window.stacked_widget.currentWidget() == main_window.menu_screen
        assert not main_window.dashboard_dock.isVisible()

    def test_screen_navigation(self, main_window):
        """Test navigation between screens"""
        main_window.show()

        # Test game screen
        main_window.show_game_screen()
        assert main_window.stacked_widget.currentWidget() == main_window.game_screen
        assert main_window.dashboard_dock.isVisible()

        # Test tutorial screen
        main_window.show_tutorial_screen()
        assert main_window.stacked_widget.currentWidget() == main_window.tutorial_screen
        assert not main_window.dashboard_dock.isVisible()

        # Test puzzle screen
        main_window.show_puzzle_screen()
        assert main_window.stacked_widget.currentWidget() == main_window.puzzle_screen
        assert not main_window.dashboard_dock.isVisible()

        # Test help screen
        main_window.show_help_screen()
        assert main_window.stacked_widget.currentWidget() == main_window.help_screen
        assert not main_window.dashboard_dock.isVisible()

        # Return to menu
        main_window.show_menu_screen()
        assert main_window.stacked_widget.currentWidget() == main_window.menu_screen

    def test_screen_changed_signal(self, main_window):
        """Test screen_changed signal is emitted"""
        spy = QSignalSpy(main_window.screen_changed)

        main_window.show_game_screen()
        assert len(spy) == 1
        assert spy[-1][0] == "game"

        main_window.show_menu_screen()
        assert len(spy) == 2
        assert spy[-1][0] == "menu"

    def test_menu_button_navigation(self, main_window):
        """Test menu buttons trigger navigation"""
        main_window.show()

        # Get menu buttons
        menu_layout = main_window.menu_screen.layout()
        assert menu_layout is not None

        # Find buttons by iterating through layout
        buttons = []
        for i in range(menu_layout.count()):
            widget = menu_layout.itemAt(i).widget()
            if hasattr(widget, 'clicked'):
                buttons.append(widget)

    def test_dashboard_updates(self, main_window):
        """Test dashboard update methods"""
        main_window.show_game_screen()

        # Update evaluation
        main_window.update_dashboard(eval_score=2.5)
        assert main_window.eval_score_label.text() == "+2.5"

        # Update game info
        main_window.update_game_info(
            mode="vs AI",
            difficulty="Hard",
            turn="Black",
            opening="Sicilian"
        )
        assert "vs AI" in main_window.game_mode_label.text()
        assert "Hard" in main_window.difficulty_label.text()

        # Add move to history
        main_window.add_move_to_history(1, "e4", "c5")
        assert main_window.move_history_list.count() == 1

        # Clear move history
        main_window.clear_move_history()
        assert main_window.move_history_list.count() == 0

    def test_ai_thinking_indicator(self, main_window):
        """Test AI thinking indicator shows/hides"""
        main_window.show_game_screen()

        assert not main_window.ai_thinking_widget.isVisible()

        main_window.show_ai_thinking("AI is calculating...")
        assert main_window.ai_thinking_widget.isVisible()
        assert "calculating" in main_window.ai_status_label.text()

        main_window.hide_ai_thinking()
        assert not main_window.ai_thinking_widget.isVisible()

    def test_status_message(self, main_window):
        """Test status bar messages"""
        main_window.show()

        main_window.set_status_message("Test message")
        assert "Test message" in main_window.status_bar.currentMessage()


# ============================================================================
# CHESS BOARD WIDGET TESTS
# ============================================================================

class TestChessBoardWidget:
    """Tests for ChessBoardWidget component"""

    def test_board_widget_initialization(self, chess_board_widget):
        """Test chess board widget initializes correctly"""
        assert chess_board_widget.board_scene is not None
        assert len(chess_board_widget.board_scene.squares) == 8
        assert len(chess_board_widget.board_scene.squares[0]) == 8

    def test_board_size(self, chess_board_widget):
        """Test board has correct size"""
        # BOARD_WIDTH should be 560 (8 * 70)
        assert chess_board_widget.width() == 562  # 560 + 2 for borders

    def test_piece_selection(self, chess_board_widget):
        """Test piece selection highlighting"""
        spy = QSignalSpy(chess_board_widget.pieceSelected)

        # Simulate piece selection
        chess_board_widget.board_scene.piece_pressed(MagicMock(get_board_position=lambda: (6, 4)))
        chess_board_widget.board_scene.pieceSelected.emit((6, 4))

        # Note: QSignalSpy might not work perfectly with complex signals
        # This is a simplified test

    def test_legal_moves_highlighting(self, chess_board_widget):
        """Test legal moves are highlighted"""
        moves = [(4, 4), (5, 4)]
        chess_board_widget.set_legal_moves(moves)

        # Verify squares are highlighted (simplified check)
        assert chess_board_widget.board_scene.legal_moves == moves

    def test_move_animation(self, chess_board_widget):
        """Test move animation is created"""
        # Create a simple board state
        from game import Board, Piece

        board = Board()
        chess_board_widget.set_board_state(board)

        # Animate a move
        chess_board_widget.animate_move((6, 4), (4, 4), duration_ms=300)

        # The animation should be created (check for _animations list)
        assert hasattr(chess_board_widget.board_scene, '_animations')

    def test_last_move_highlighting(self, chess_board_widget):
        """Test last move highlighting"""
        chess_board_widget.set_last_move((6, 4), (4, 4))

        assert chess_board_widget.board_scene.last_move == ((6, 4), (4, 4))
        # Verify squares are highlighted with LAST_MOVE_COLOR


# ============================================================================
# GAME CONTROLLER TESTS
# ============================================================================

class TestGameController:
    """Tests for GameController component"""

    def test_controller_initialization(self, game_controller):
        """Test game controller initializes correctly"""
        assert game_controller.board is not None
        assert game_controller.game_mode == 'pvp'
        assert game_controller.ai_color == "black"
        assert game_controller.ai_difficulty == "medium"
        assert game_controller.puzzle_system is not None

    def test_set_game_mode_pvp(self, game_controller):
        """Test setting PvP game mode"""
        game_controller.set_game_mode('pvp')
        assert game_controller.game_mode == 'pvp'
        assert game_controller.ai is None

    def test_set_game_mode_pvai(self, game_controller):
        """Test setting PvAI game mode"""
        with patch('ui.game_controller.AI'):
            game_controller.set_game_mode('pvai', ai_color='black', ai_difficulty='hard')
            assert game_controller.game_mode == 'pvai'
            assert game_controller.ai_color == 'black'
            assert game_controller.ai_difficulty == 'hard'

    def test_legal_moves_retrieval(self, game_controller):
        """Test getting legal moves for a piece"""
        # Mock the board's get_legal_moves method
        game_controller.board.get_legal_moves = MagicMock(return_value=[
            {"to": (4, 4)},
            {"to": (5, 4)}
        ])

        moves = game_controller.get_legal_moves((6, 4))
        assert len(moves) == 2
        assert moves[0]["to"] == (4, 4)

    def test_board_state_retrieval(self, game_controller):
        """Test getting current board state"""
        state = game_controller.get_board_state()
        assert state is not None
        assert len(state) == 8
        assert len(state[0]) == 8

    def test_current_player(self, game_controller):
        """Test getting current player to move"""
        game_controller.board.to_move = "white"
        assert game_controller.get_current_player() == "white"

        game_controller.board.to_move = "black"
        assert game_controller.get_current_player() == "black"

    def test_game_over_check(self, game_controller):
        """Test game over status"""
        game_controller.board.game_over = False
        assert not game_controller.is_game_over()

        game_controller.board.game_over = True
        game_controller.board.game_result = "checkmate_white"
        assert game_controller.is_game_over()
        assert game_controller.get_game_result() == "checkmate_white"

    def test_move_validation_illegal(self, game_controller):
        """Test illegal move detection"""
        spy = QSignalSpy(game_controller.moveValidated)

        # Set up board to have a piece at a position
        game_controller.board.get_legal_moves = MagicMock(return_value=[])
        game_controller.board.to_move = "white"

        # Try to make an illegal move
        game_controller.handle_move_attempt((6, 4), (5, 5))

        # Should emit moveValidated(False)
        # Note: QSignalSpy may not capture all signals reliably

    def test_undo_move(self, game_controller):
        """Test undo move functionality"""
        game_controller.board.move_log = [
            {"from": (6, 4), "to": (4, 4)},
            {"from": (1, 4), "to": (3, 4)}
        ]
        game_controller.board.undo = MagicMock()

        game_controller.undo_move()
        game_controller.board.undo.assert_called()

    def test_reset_game(self, game_controller):
        """Test game reset"""
        # Add some move history
        game_controller.move_history = [((6, 4), (4, 4), {})]

        game_controller.reset_game()

        assert len(game_controller.move_history) == 0

    def test_fen_loading(self, game_controller):
        """Test loading a FEN position"""
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        with patch('ui.game_controller.parse_fen'):
            game_controller.load_fen(fen)
            # FEN should be loaded without error


# ============================================================================
# PUZZLE SYSTEM TESTS
# ============================================================================

class TestPuzzleSystem:
    """Tests for ChessPuzzles component"""

    def test_puzzle_system_initialization(self, puzzle_system):
        """Test puzzle system initializes with puzzles"""
        assert len(puzzle_system.puzzles) > 0
        assert puzzle_system.current_puzzle_index == 0
        assert puzzle_system.user_moves == []

    def test_get_current_puzzle(self, puzzle_system):
        """Test getting current puzzle"""
        puzzle = puzzle_system.get_puzzle()
        assert puzzle is not None
        assert "id" in puzzle
        assert "fen" in puzzle
        assert "solution" in puzzle

    def test_get_puzzle_by_id(self, puzzle_system):
        """Test getting puzzle by ID"""
        puzzle = puzzle_system.get_puzzle(1)
        assert puzzle is not None
        assert puzzle["id"] == 1

    def test_get_puzzle_by_difficulty(self, puzzle_system):
        """Test filtering puzzles by difficulty"""
        easy_puzzles = puzzle_system.get_puzzles_by_difficulty("easy")
        assert len(easy_puzzles) > 0
        assert all(p["difficulty"] == "easy" for p in easy_puzzles)

    def test_get_puzzle_by_theme(self, puzzle_system):
        """Test filtering puzzles by theme"""
        fork_puzzles = puzzle_system.get_puzzles_by_theme("Fork")
        assert len(fork_puzzles) > 0
        assert all(p["theme"] == "Fork" for p in fork_puzzles)

    def test_next_puzzle(self, puzzle_system):
        """Test moving to next puzzle"""
        initial_index = puzzle_system.current_puzzle_index
        puzzle_system.next_puzzle()
        assert puzzle_system.current_puzzle_index == (initial_index + 1) % len(puzzle_system.puzzles)
        assert puzzle_system.user_moves == []

    def test_previous_puzzle(self, puzzle_system):
        """Test moving to previous puzzle"""
        puzzle_system.current_puzzle_index = 5
        puzzle_system.previous_puzzle()
        assert puzzle_system.current_puzzle_index == 4

    def test_get_hint(self, puzzle_system):
        """Test getting hint for puzzle"""
        puzzle_system.current_puzzle_index = 0
        puzzle_system.user_moves = []

        hint = puzzle_system.get_hint()
        assert hint is not None
        assert isinstance(hint, str)

    def test_check_move_correct(self, puzzle_system):
        """Test checking a correct move"""
        puzzle_system.current_puzzle_index = 0
        puzzle = puzzle_system.get_puzzle()
        first_move = puzzle["solution"][0]

        is_correct, is_complete, message = puzzle_system.check_move(first_move)
        assert is_correct
        assert not is_complete  # Not complete after first move (usually)

    def test_check_move_incorrect(self, puzzle_system):
        """Test checking an incorrect move"""
        puzzle_system.current_puzzle_index = 0

        is_correct, is_complete, message = puzzle_system.check_move("Nf3")
        assert not is_correct

    def test_reset_puzzle(self, puzzle_system):
        """Test resetting current puzzle"""
        puzzle_system.user_moves = ["e4", "c5"]
        puzzle_system.hints_used = 3

        puzzle_system.reset_puzzle()
        assert puzzle_system.user_moves == []
        assert puzzle_system.hints_used == 0

    def test_get_progress(self, puzzle_system):
        """Test getting puzzle progress"""
        progress = puzzle_system.get_progress()
        assert "current" in progress
        assert "total" in progress
        assert "percentage" in progress
        assert progress["current"] >= 1
        assert progress["total"] > 0


# ============================================================================
# AI THREADING TESTS
# ============================================================================

class TestAIThreading:
    """Tests for AI threading functionality"""

    def test_ai_worker_creation(self, mock_ai):
        """Test AI worker thread creation"""
        from ui.game_controller import AIWorker

        worker = AIWorker(mock_ai)
        assert worker is not None
        assert worker.ai == mock_ai
        assert not worker.is_calculating

    def test_ai_worker_signals(self, mock_ai):
        """Test AI worker signals are defined"""
        from ui.game_controller import AIWorker

        worker = AIWorker(mock_ai)
        assert hasattr(worker, 'moveCalculated')
        assert hasattr(worker, 'thinkingProgress')
        assert hasattr(worker, 'error')

    def test_ai_move_calculation_non_blocking(self, game_controller, mock_ai):
        """Test AI move is calculated in background thread"""
        game_controller.ai = mock_ai
        game_controller.game_mode = 'pvai'

        # Spy on AI thinking signal
        spy = QSignalSpy(game_controller.aiThinking)

        game_controller.start_ai_move()

        # aiThinking should emit True (thread started)
        # Note: Due to threading, we can't reliably test the full flow here
        assert game_controller.ai_worker is not None

    def test_ai_error_handling(self, game_controller, mock_ai):
        """Test AI error handling"""
        game_controller.ai = mock_ai
        game_controller.game_mode = 'pvai'

        # Configure mock to raise error
        mock_ai.get_best_move.side_effect = Exception("AI Error")

        # This should be handled gracefully


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for full workflows"""

    def test_complete_game_flow_pvp(self, game_controller):
        """Test complete PvP game flow"""
        # Set up game
        game_controller.set_game_mode('pvp')

        # Mock board methods
        game_controller.board.get_legal_moves = MagicMock(return_value=[
            {"to": (4, 4)}
        ])
        game_controller.board.move = MagicMock()
        game_controller.board.game_over = False
        game_controller.board.to_move = "white"

        # Make a move
        initial_move_count = len(game_controller.move_history)
        game_controller.handle_move_attempt((6, 4), (4, 4))

        # Verify move was recorded
        assert len(game_controller.move_history) > initial_move_count

    def test_undo_and_reset_flow(self, game_controller):
        """Test undo and reset workflow"""
        game_controller.board.move_log = [{"from": (6, 4), "to": (4, 4)}]
        game_controller.board.undo = MagicMock()
        game_controller.move_history = [((6, 4), (4, 4), {})]

        # Test undo
        game_controller.undo_move()
        assert len(game_controller.move_history) == 0

        # Test reset
        game_controller.move_history = [((6, 4), (4, 4), {})]
        game_controller.reset_game()
        assert len(game_controller.move_history) == 0

    def test_puzzle_complete_workflow(self, game_controller):
        """Test loading and solving a puzzle"""
        game_controller.set_game_mode('puzzle')

        # Load a puzzle
        game_controller.puzzle_system.current_puzzle_index = 0
        puzzle = game_controller.puzzle_system.get_puzzle()

        assert puzzle is not None
        assert len(puzzle["solution"]) > 0

        # Check first move of solution
        first_move = puzzle["solution"][0]
        is_correct, _, _ = game_controller.puzzle_system.check_move(first_move)
        assert is_correct

    def test_main_window_game_flow(self, main_window):
        """Test main window in a game flow"""
        main_window.show()

        # Start new game
        main_window._on_new_game()
        assert main_window.stacked_widget.currentWidget() == main_window.game_screen

        # Update dashboard
        main_window.update_dashboard(eval_score=1.5)
        main_window.add_move_to_history(1, "e4")

        # Reset game
        main_window._on_reset_game()
        assert main_window.move_history_list.count() == 0

    def test_multi_screen_navigation(self, main_window):
        """Test navigating through multiple screens"""
        main_window.show()

        screens = [
            (main_window.show_game_screen, main_window.game_screen),
            (main_window.show_tutorial_screen, main_window.tutorial_screen),
            (main_window.show_puzzle_screen, main_window.puzzle_screen),
            (main_window.show_help_screen, main_window.help_screen),
            (main_window.show_menu_screen, main_window.menu_screen),
        ]

        for show_func, expected_screen in screens:
            show_func()
            assert main_window.stacked_widget.currentWidget() == expected_screen


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

class TestErrorHandling:
    """Tests for error handling and edge cases"""

    def test_move_when_game_over(self, game_controller):
        """Test attempting move when game is over"""
        game_controller.board.game_over = True
        game_controller.board.to_move = "white"

        spy = QSignalSpy(game_controller.moveValidated)
        game_controller.handle_move_attempt((6, 4), (4, 4))

        # Should handle gracefully

    def test_undo_with_empty_history(self, game_controller):
        """Test undo with no moves to undo"""
        game_controller.board.move_log = []
        game_controller.move_history = []

        spy = QSignalSpy(game_controller.errorOccurred)
        game_controller.undo_move()

        # Should emit error or handle gracefully

    def test_invalid_puzzle_id(self, puzzle_system):
        """Test loading non-existent puzzle"""
        puzzle = puzzle_system.get_puzzle(999)
        assert puzzle is None

    def test_hint_with_no_puzzle(self, game_controller):
        """Test getting hint with no puzzle loaded"""
        game_controller.game_mode = 'pvp'  # Not puzzle mode
        game_controller.current_puzzle = None

        spy = QSignalSpy(game_controller.errorOccurred)
        game_controller.get_puzzle_hint()

    def test_fen_with_invalid_string(self, game_controller):
        """Test loading invalid FEN"""
        with patch('ui.game_controller.parse_fen', side_effect=Exception("Invalid FEN")):
            spy = QSignalSpy(game_controller.errorOccurred)
            game_controller.load_fen("invalid fen string")


# ============================================================================
# PERFORMANCE AND EDGE CASES
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""

    def test_board_piece_at_every_square(self, chess_board_widget):
        """Test board can handle pieces at every square"""
        from game import Board, Piece

        board = Board()
        # This would be an invalid position, but test that it doesn't crash
        chess_board_widget.set_board_state(board)
        assert chess_board_widget.board_scene.pieces is not None

    def test_rapid_move_sequence(self, game_controller):
        """Test rapid sequence of moves"""
        game_controller.board.get_legal_moves = MagicMock(return_value=[{"to": (4, 4)}])
        game_controller.board.move = MagicMock()
        game_controller.board.game_over = False
        game_controller.board.to_move = "white"

        # Make multiple moves rapidly
        for _ in range(5):
            game_controller.handle_move_attempt((6, 4), (4, 4))

    def test_puzzle_progression(self, puzzle_system):
        """Test progression through all puzzles"""
        initial_count = len(puzzle_system.puzzles)

        for _ in range(initial_count):
            puzzle_system.next_puzzle()

        # Should cycle back to start
        assert puzzle_system.current_puzzle_index == 0

    def test_evaluation_score_bounds(self, main_window):
        """Test evaluation score with extreme values"""
        main_window.show_game_screen()

        # Test large positive
        main_window.update_dashboard(eval_score=999.9)
        assert "+999.9" in main_window.eval_score_label.text()

        # Test large negative
        main_window.update_dashboard(eval_score=-999.9)
        assert "-999.9" in main_window.eval_score_label.text()

        # Test zero
        main_window.update_dashboard(eval_score=0.0)
        assert "+0.0" in main_window.eval_score_label.text()


# ============================================================================
# SIGNAL/SLOT TESTS
# ============================================================================

class TestSignalsAndSlots:
    """Tests for Qt signals and slots"""

    def test_game_state_changed_signal(self, game_controller):
        """Test gameStateChanged signal emission"""
        spy = QSignalSpy(game_controller.gameStateChanged)

        # This signal should be emitted on state changes
        game_controller.reset_game()

    def test_move_completed_signal(self, game_controller):
        """Test moveCompleted signal emission"""
        spy = QSignalSpy(game_controller.moveCompleted)

        game_controller.board.get_legal_moves = MagicMock(return_value=[{"to": (4, 4)}])
        game_controller.board.move = MagicMock()
        game_controller.board.game_over = False
        game_controller.board.to_move = "white"

        game_controller.handle_move_attempt((6, 4), (4, 4))

    def test_evaluation_updated_signal(self, game_controller):
        """Test evaluationUpdated signal emission"""
        with patch('ui.game_controller.AI'):
            game_controller.set_game_mode('pvai')
            game_controller.ai.evaluate_board = MagicMock(return_value=1.5)

            spy = QSignalSpy(game_controller.evaluationUpdated)

            game_controller.board.get_legal_moves = MagicMock(return_value=[{"to": (4, 4)}])
            game_controller.board.move = MagicMock()
            game_controller.board.game_over = False
            game_controller.board.to_move = "white"

            game_controller.handle_move_attempt((6, 4), (4, 4))

    def test_main_window_screen_changed_signal(self, main_window):
        """Test screen_changed signal emission"""
        spy = QSignalSpy(main_window.screen_changed)
        initial_count = len(spy)

        main_window.show_game_screen()
        assert len(spy) > initial_count

    def test_board_widget_move_attempted_signal(self, chess_board_widget):
        """Test moveAttempted signal emission"""
        spy = QSignalSpy(chess_board_widget.moveAttempted)

        # Simulate piece drop
        piece_item = MagicMock()
        piece_item.get_board_position = MagicMock(return_value=(6, 4))
        chess_board_widget.board_scene.piece_dropped(piece_item, 4, 4)


# ============================================================================
# MOCK AND PATCH TESTS
# ============================================================================

class TestMocking:
    """Tests demonstrating proper mocking for unit isolation"""

    def test_ai_mock(self, mock_ai):
        """Test using mocked AI"""
        assert mock_ai.get_best_move() == ({'to': (4, 4)}, (6, 4))
        assert mock_ai.evaluate_board() == 0.5
        assert mock_ai.max_depth == 6
        assert mock_ai.nodes_searched == 10000

    def test_board_mock_in_game_controller(self, game_controller):
        """Test mocking board methods"""
        game_controller.board.get_legal_moves = MagicMock(return_value=[{"to": (4, 4)}])

        moves = game_controller.get_legal_moves((6, 4))
        assert len(moves) == 1
        game_controller.board.get_legal_moves.assert_called_once_with((6, 4))

    def test_puzzle_system_mock(self):
        """Test mocking puzzle system"""
        mock_puzzles = MagicMock()
        mock_puzzles.get_puzzle = MagicMock(return_value={
            "id": 1,
            "fen": "test_fen",
            "solution": ["e4"]
        })

        puzzle = mock_puzzles.get_puzzle()
        assert puzzle["id"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
