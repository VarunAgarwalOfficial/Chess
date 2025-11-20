"""
Chess Application - Main Application Wrapper
Manages all components and connects signals between UI and game logic.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt, pyqtSlot, QEvent
from PyQt6.QtGui import QShortcut, QKeySequence

from src.ui.main_window import ChessMainWindow
from src.ui.game_controller import GameController
from src.ui.chess_board import ChessBoardWidget


class ChessApplication:
    """
    Main Chess Application Wrapper

    Manages all components and their interactions:
    - ChessMainWindow: UI window with screens and dashboard
    - GameController: Game logic coordinator
    - ChessBoardWidget: Interactive chess board

    Responsibilities:
    - Initialize all components
    - Connect signals between components
    - Set up keyboard shortcuts
    - Manage application lifecycle
    - Provide public API for testing
    """

    def __init__(self):
        """Initialize the chess application"""
        # Get QApplication instance (create if needed)
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(sys.argv)

        # Load stylesheet
        self._load_stylesheet()

        # Create main components
        self.main_window = ChessMainWindow()
        self.controller = GameController()
        self.board_widget = None  # Created when game screen is shown

        # Set up components
        self._setup_board_widget()
        self._connect_signals()
        self._setup_keyboard_shortcuts()
        self._setup_event_filter()

        # Center window on screen
        self._center_window()

        # Set window icon if available
        self._set_window_icon()

    def _load_stylesheet(self):
        """Load QSS stylesheet from file"""
        try:
            # Get path to stylesheet
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            qss_path = os.path.join(base_path, 'styles', 'chess_theme.qss')

            if os.path.exists(qss_path):
                with open(qss_path, 'r') as f:
                    stylesheet = f.read()
                    self.app.setStyleSheet(stylesheet)
                print(f"Loaded stylesheet from: {qss_path}")
            else:
                print(f"Warning: Stylesheet not found at {qss_path}")
                print("Using default Qt styling")
        except Exception as e:
            print(f"Error loading stylesheet: {e}")
            print("Using default Qt styling")

    def _setup_board_widget(self):
        """Create and integrate chess board widget into game screen"""
        # Create board widget
        self.board_widget = ChessBoardWidget()

        # Replace placeholder in game screen
        game_screen = self.main_window.game_screen
        layout = game_screen.layout()

        # Remove placeholder
        placeholder = layout.itemAt(0).widget()
        layout.removeWidget(placeholder)
        placeholder.deleteLater()

        # Add chess board
        layout.addWidget(self.board_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # Initialize board with starting position
        self.board_widget.set_board_state(self.controller.board)

    def _connect_signals(self):
        """Connect all signals between components"""
        # ===== Board Widget → Controller =====
        self.board_widget.moveAttempted.connect(self.controller.handle_move_attempt)
        self.board_widget.pieceSelected.connect(self._on_piece_selected)

        # ===== Controller → Board Widget =====
        self.controller.gameStateChanged.connect(self._on_game_state_changed)
        self.controller.moveCompleted.connect(self._on_move_completed)

        # ===== Controller → Main Window (Dashboard Updates) =====
        self.controller.gameStateChanged.connect(self._update_dashboard)
        self.controller.evaluationUpdated.connect(self._on_evaluation_updated)
        self.controller.gameOver.connect(self._on_game_over)
        self.controller.aiThinking.connect(self._on_ai_thinking)
        self.controller.errorOccurred.connect(self._on_error)
        self.controller.moveCompleted.connect(self._on_move_for_history)

        # ===== Puzzle-specific signals =====
        self.controller.puzzleLoaded.connect(self._on_puzzle_loaded)
        self.controller.puzzleProgress.connect(self._on_puzzle_progress)

        # ===== Main Window → Controller (Menu Actions) =====
        # These are connected via menu action handlers
        # We'll override the menu action handlers to call controller methods
        self._connect_menu_actions()

        # ===== Main Window Screen Changes =====
        self.main_window.screen_changed.connect(self._on_screen_changed)

    def _connect_menu_actions(self):
        """Connect menu actions to controller methods"""
        # Override main window's menu action handlers
        original_new_game = self.main_window._on_new_game
        original_undo = self.main_window._on_undo_move
        original_reset = self.main_window._on_reset_game

        def new_game():
            original_new_game()
            self.controller.reset_game()

        def undo_move():
            self.controller.undo_move()

        def reset_game():
            self.controller.reset_game()

        # Replace handlers
        self.main_window._on_new_game = new_game
        self.main_window._on_undo_move = undo_move
        self.main_window._on_reset_game = reset_game

    def _setup_keyboard_shortcuts(self):
        """Set up keyboard shortcuts"""
        # Undo move: Ctrl+Z
        self.undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self.main_window)
        self.undo_shortcut.activated.connect(self.controller.undo_move)

        # Reset game: Ctrl+R
        self.reset_shortcut = QShortcut(QKeySequence("Ctrl+R"), self.main_window)
        self.reset_shortcut.activated.connect(self.controller.reset_game)

        # Return to menu: Esc
        self.menu_shortcut = QShortcut(QKeySequence("Esc"), self.main_window)
        self.menu_shortcut.activated.connect(self.main_window.show_menu_screen)

        # New game: Ctrl+N
        self.new_game_shortcut = QShortcut(QKeySequence("Ctrl+N"), self.main_window)
        self.new_game_shortcut.activated.connect(self._on_new_game_shortcut)

    def _setup_event_filter(self):
        """Set up event filter for additional event handling"""
        self.main_window.installEventFilter(self)

    def _center_window(self):
        """Center the main window on screen"""
        screen_geometry = self.app.primaryScreen().geometry()
        window_geometry = self.main_window.frameGeometry()

        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.main_window.move(window_geometry.topLeft())

    def _set_window_icon(self):
        """Set window icon if available"""
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            icon_path = os.path.join(base_path, 'assets', 'images', 'icon.png')

            if os.path.exists(icon_path):
                from PyQt6.QtGui import QIcon
                self.main_window.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            print(f"Could not load window icon: {e}")

    # ===== Signal Handlers =====

    @pyqtSlot(tuple)
    def _on_piece_selected(self, position):
        """Handle piece selection - show legal moves"""
        legal_moves = self.controller.get_legal_moves(position)
        if legal_moves:
            # Extract destination positions
            move_positions = [move["to"] for move in legal_moves]
            self.board_widget.set_legal_moves(move_positions)

    @pyqtSlot()
    def _on_game_state_changed(self):
        """Handle game state change - update board display"""
        self.board_widget.set_board_state(self.controller.board)
        self.board_widget.clear_highlights()

        # Update turn indicator
        current_player = self.controller.get_current_player()
        self.main_window.update_game_info(turn=current_player.capitalize())

    @pyqtSlot(tuple, tuple)
    def _on_move_completed(self, from_pos, to_pos):
        """Handle move completion - animate and highlight"""
        # Animate the move
        self.board_widget.animate_move(from_pos, to_pos, duration_ms=250)

        # Highlight last move
        self.board_widget.set_last_move(from_pos, to_pos)

        # Clear legal moves
        self.board_widget.clear_highlights()

    @pyqtSlot()
    def _update_dashboard(self):
        """Update dashboard with current game state"""
        # Get captured pieces
        captured = self._get_captured_pieces()

        # Get evaluation (if AI exists)
        eval_score = 0.0
        if self.controller.ai:
            try:
                eval_score = self.controller.ai.evaluate_board() / 100.0  # Convert centipawns to pawns
            except:
                eval_score = 0.0

        # Update dashboard
        self.main_window.update_dashboard(
            board=self.controller.board,
            eval_score=eval_score,
            captured=captured
        )

    @pyqtSlot(float)
    def _on_evaluation_updated(self, eval_score):
        """Handle evaluation update"""
        # Convert centipawns to pawns for display
        eval_pawns = eval_score / 100.0

        captured = self._get_captured_pieces()
        self.main_window.update_dashboard(
            eval_score=eval_pawns,
            captured=captured
        )

    @pyqtSlot(str)
    def _on_game_over(self, result):
        """Handle game over"""
        self.main_window.hide_ai_thinking()

        # Format result message
        result_messages = {
            "checkmate_white": "Checkmate! White wins!",
            "checkmate_black": "Checkmate! Black wins!",
            "stalemate": "Stalemate! It's a draw.",
            "insufficient_material": "Draw by insufficient material.",
            "threefold_repetition": "Draw by threefold repetition.",
            "fifty_move_rule": "Draw by fifty-move rule."
        }

        message = result_messages.get(result, f"Game Over: {result}")

        # Show message box
        QMessageBox.information(
            self.main_window,
            "Game Over",
            message,
            QMessageBox.StandardButton.Ok
        )

        self.main_window.set_status_message(message)

    @pyqtSlot(bool)
    def _on_ai_thinking(self, is_thinking):
        """Handle AI thinking state"""
        if is_thinking:
            self.main_window.show_ai_thinking("AI is thinking...")
            self.main_window.set_status_message("AI is calculating best move...")
        else:
            self.main_window.hide_ai_thinking()
            self.main_window.set_status_message("Your turn")

    @pyqtSlot(str)
    def _on_error(self, error_message):
        """Handle error message"""
        self.main_window.set_status_message(error_message, timeout=5000)

    @pyqtSlot(tuple, tuple)
    def _on_move_for_history(self, from_pos, to_pos):
        """Add move to history display"""
        # Get move number (half moves / 2 + 1)
        move_number = len(self.controller.board.move_log) // 2 + 1

        # Determine if this is white or black's move
        is_white_move = len(self.controller.board.move_log) % 2 == 1

        # Convert position to algebraic notation (simplified)
        from_square = self._pos_to_algebraic(from_pos)
        to_square = self._pos_to_algebraic(to_pos)
        move_text = f"{from_square}-{to_square}"

        if is_white_move:
            # White's move - add new entry
            self.main_window.add_move_to_history(move_number, move_text)
        else:
            # Black's move - update last entry
            # For now, just add as separate entry
            self.main_window.add_move_to_history(move_number, move_text)

    @pyqtSlot(dict)
    def _on_puzzle_loaded(self, puzzle):
        """Handle puzzle loaded"""
        self.main_window.set_status_message(f"Puzzle loaded: {puzzle.get('name', 'Unknown')}")
        self.board_widget.set_board_state(self.controller.board)

    @pyqtSlot(bool, bool, str)
    def _on_puzzle_progress(self, is_correct, is_complete, message):
        """Handle puzzle progress"""
        if is_complete:
            QMessageBox.information(
                self.main_window,
                "Puzzle Complete!",
                message,
                QMessageBox.StandardButton.Ok
            )
        else:
            self.main_window.set_status_message(message, timeout=3000)

    @pyqtSlot(str)
    def _on_screen_changed(self, screen_name):
        """Handle screen change"""
        # Update game mode based on screen
        if screen_name == "game":
            # Set to PvAI mode by default
            if self.controller.game_mode != 'pvai':
                self.controller.set_game_mode('pvai', ai_color='black', ai_difficulty='medium')
                self.board_widget.set_board_state(self.controller.board)
                self.main_window.update_game_info(mode="vs AI", difficulty="Medium")
        elif screen_name == "puzzle":
            # Load first puzzle
            self.controller.set_game_mode('puzzle')
            self.controller.load_puzzle()

    def _on_new_game_shortcut(self):
        """Handle new game shortcut"""
        self.main_window.show_game_screen()
        self.controller.reset_game()

    # ===== Helper Methods =====

    def _get_captured_pieces(self):
        """Get captured pieces from board state"""
        # Count initial pieces
        initial_pieces = {
            'white': {'pawn': 8, 'knight': 2, 'bishop': 2, 'rook': 2, 'queen': 1},
            'black': {'pawn': 8, 'knight': 2, 'bishop': 2, 'rook': 2, 'queen': 1}
        }

        # Count current pieces
        current_pieces = {
            'white': {'pawn': 0, 'knight': 0, 'bishop': 0, 'rook': 0, 'queen': 0},
            'black': {'pawn': 0, 'knight': 0, 'bishop': 0, 'rook': 0, 'queen': 0}
        }

        for row in self.controller.board.state:
            for piece in row:
                if piece and piece.type != 'king':
                    current_pieces[piece.color][piece.type] += 1

        # Calculate captured pieces
        captured = {'white': [], 'black': []}

        for color in ['white', 'black']:
            for piece_type in ['pawn', 'knight', 'bishop', 'rook', 'queen']:
                count = initial_pieces[color][piece_type] - current_pieces[color][piece_type]
                captured[color].extend([piece_type.capitalize()] * count)

        return captured

    def _pos_to_algebraic(self, pos):
        """Convert (row, col) to algebraic notation"""
        row, col = pos
        file = chr(ord('a') + col)
        rank = str(8 - row)
        return f"{file}{rank}"

    # ===== Public API =====

    def show(self):
        """Show the main window"""
        self.main_window.show()

    def exec(self):
        """Execute the application main loop"""
        return self.app.exec()

    def cleanup(self):
        """Clean up resources before exit"""
        try:
            # Stop AI worker if running
            self.controller.cleanup()

            # Close main window
            self.main_window.close()
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def eventFilter(self, obj, event):
        """Event filter for additional event handling"""
        # Handle close event
        if event.type() == QEvent.Type.Close and obj == self.main_window:
            self.cleanup()

        return False

    # ===== Testing API =====

    def get_controller(self):
        """Get game controller (for testing)"""
        return self.controller

    def get_main_window(self):
        """Get main window (for testing)"""
        return self.main_window

    def get_board_widget(self):
        """Get board widget (for testing)"""
        return self.board_widget

    def set_game_mode(self, mode, **kwargs):
        """Set game mode (for testing)"""
        self.controller.set_game_mode(mode, **kwargs)
        if mode == 'pvai':
            self.main_window.show_game_screen()
            self.main_window.update_game_info(
                mode="vs AI",
                difficulty=kwargs.get('ai_difficulty', 'medium').capitalize()
            )
