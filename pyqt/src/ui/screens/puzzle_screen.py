"""
Puzzle Screen for PyQt Chess
Interactive chess puzzle interface with solution checking and hints
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QComboBox, QSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from features.puzzles import ChessPuzzles


class PuzzleScreen(QWidget):
    """
    Puzzle screen with puzzle board and solution checking

    Signals:
        backToMenu() - Return to main menu
        loadPuzzle(int) - Load a specific puzzle by ID
        puzzleSolved(int) - Puzzle successfully solved
        requestHint() - User requested a hint
    """

    # Navigation signals
    backToMenu = pyqtSignal()
    loadPuzzle = pyqtSignal(int)
    puzzleSolved = pyqtSignal(int)
    requestHint = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize puzzle backend
        self.puzzles = ChessPuzzles()
        self.current_puzzle = None
        self.user_moves = []

        self._init_ui()
        self._apply_styles()

        # Load first puzzle by default
        if self.puzzles.puzzles:
            self._load_puzzle(self.puzzles.get_puzzle())

    def _init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = self._create_header()
        main_layout.addWidget(header)

        # Content area
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Left side - Puzzle board placeholder
        self.board_container = self._create_board_container()
        content_layout.addWidget(self.board_container)

        # Right side - Puzzle info and controls
        self.info_panel = self._create_info_panel()
        content_layout.addWidget(self.info_panel)

        main_layout.addWidget(content)

        # Footer navigation
        footer = self._create_footer()
        main_layout.addWidget(footer)

    def _create_header(self):
        """Create the header with title and back button"""
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(80)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 10, 20, 10)

        # Title
        title = QLabel("Chess Puzzles")
        title.setObjectName("screen_title")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        layout.addWidget(title)

        layout.addStretch()

        # Puzzle selector
        selector_label = QLabel("Puzzle:")
        selector_label.setObjectName("selector_label")
        selector_label.setFont(QFont("Arial", 12))
        layout.addWidget(selector_label)

        self.puzzle_selector = QSpinBox()
        self.puzzle_selector.setObjectName("puzzle_selector")
        self.puzzle_selector.setMinimum(1)
        self.puzzle_selector.setMaximum(len(self.puzzles.puzzles))
        self.puzzle_selector.setValue(1)
        self.puzzle_selector.setFixedWidth(80)
        self.puzzle_selector.valueChanged.connect(self._on_puzzle_selected)
        layout.addWidget(self.puzzle_selector)

        layout.addSpacing(20)

        # Difficulty filter
        difficulty_label = QLabel("Difficulty:")
        difficulty_label.setObjectName("selector_label")
        difficulty_label.setFont(QFont("Arial", 12))
        layout.addWidget(difficulty_label)

        self.difficulty_combo = QComboBox()
        self.difficulty_combo.setObjectName("difficulty_combo")
        self.difficulty_combo.addItems(["All", "Easy", "Medium", "Hard"])
        self.difficulty_combo.setFixedWidth(120)
        self.difficulty_combo.currentTextChanged.connect(self._filter_by_difficulty)
        layout.addWidget(self.difficulty_combo)

        layout.addSpacing(20)

        # Back button
        back_btn = QPushButton("Back to Menu")
        back_btn.setObjectName("back_button")
        back_btn.setFixedSize(150, 40)
        back_btn.clicked.connect(self.backToMenu.emit)
        layout.addWidget(back_btn)

        return header

    def _create_board_container(self):
        """Create container for the chess board"""
        container = QFrame()
        container.setObjectName("board_container")
        container.setFixedSize(560, 560)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Placeholder for chess board (will be replaced with actual ChessBoard widget)
        self.board_placeholder = QLabel("Chess Board\nPuzzle Position")
        self.board_placeholder.setObjectName("board_placeholder")
        self.board_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.board_placeholder.setFont(QFont("Arial", 20))
        self.board_placeholder.setMinimumSize(540, 540)
        layout.addWidget(self.board_placeholder)

        return container

    def _create_info_panel(self):
        """Create puzzle information and controls panel"""
        panel = QFrame()
        panel.setObjectName("info_panel")
        panel.setFixedWidth(380)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Puzzle name
        self.puzzle_name = QLabel("Puzzle Name")
        self.puzzle_name.setObjectName("puzzle_name")
        self.puzzle_name.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.puzzle_name.setWordWrap(True)
        layout.addWidget(self.puzzle_name)

        # Puzzle metadata
        metadata_frame = QFrame()
        metadata_frame.setObjectName("metadata_frame")
        metadata_layout = QVBoxLayout(metadata_frame)
        metadata_layout.setSpacing(8)

        self.theme_label = QLabel("Theme: -")
        self.theme_label.setObjectName("metadata_label")
        self.theme_label.setFont(QFont("Arial", 12))
        metadata_layout.addWidget(self.theme_label)

        self.difficulty_label = QLabel("Difficulty: -")
        self.difficulty_label.setObjectName("metadata_label")
        self.difficulty_label.setFont(QFont("Arial", 12))
        metadata_layout.addWidget(self.difficulty_label)

        layout.addWidget(metadata_frame)

        # Description
        self.description_label = QLabel("")
        self.description_label.setObjectName("description_label")
        self.description_label.setFont(QFont("Arial", 13))
        self.description_label.setWordWrap(True)
        layout.addWidget(self.description_label)

        layout.addSpacing(10)

        # Solution progress
        progress_frame = QFrame()
        progress_frame.setObjectName("progress_frame")
        progress_layout = QVBoxLayout(progress_frame)
        progress_layout.setSpacing(8)

        progress_title = QLabel("Solution Progress")
        progress_title.setObjectName("section_label")
        progress_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        progress_layout.addWidget(progress_title)

        self.moves_made_label = QLabel("Moves: 0/0")
        self.moves_made_label.setObjectName("info_label")
        self.moves_made_label.setFont(QFont("Arial", 12))
        progress_layout.addWidget(self.moves_made_label)

        self.hints_used_label = QLabel("Hints used: 0")
        self.hints_used_label.setObjectName("info_label")
        self.hints_used_label.setFont(QFont("Arial", 12))
        progress_layout.addWidget(self.hints_used_label)

        layout.addWidget(progress_frame)

        # Status message
        self.status_label = QLabel("Make your move!")
        self.status_label.setObjectName("status_label")
        self.status_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Hint display
        self.hint_label = QLabel("")
        self.hint_label.setObjectName("hint_label")
        self.hint_label.setFont(QFont("Arial", 11))
        self.hint_label.setWordWrap(True)
        self.hint_label.setVisible(False)
        layout.addWidget(self.hint_label)

        layout.addSpacing(10)

        # FEN display
        fen_title = QLabel("Position (FEN):")
        fen_title.setObjectName("section_label")
        fen_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        layout.addWidget(fen_title)

        self.fen_display = QLabel("")
        self.fen_display.setObjectName("fen_display")
        self.fen_display.setFont(QFont("Courier", 8))
        self.fen_display.setWordWrap(True)
        self.fen_display.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.fen_display)

        layout.addStretch()

        # Action buttons
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(10)

        # Hint button
        self.hint_btn = QPushButton("Get Hint")
        self.hint_btn.setObjectName("hint_button")
        self.hint_btn.setFixedHeight(45)
        self.hint_btn.clicked.connect(self._show_hint)
        buttons_layout.addWidget(self.hint_btn)

        # Reset button
        self.reset_btn = QPushButton("Reset Puzzle")
        self.reset_btn.setObjectName("reset_button")
        self.reset_btn.setFixedHeight(45)
        self.reset_btn.clicked.connect(self._reset_puzzle)
        buttons_layout.addWidget(self.reset_btn)

        # Show solution button
        self.solution_btn = QPushButton("Show Solution")
        self.solution_btn.setObjectName("solution_button")
        self.solution_btn.setFixedHeight(45)
        self.solution_btn.clicked.connect(self._show_solution)
        buttons_layout.addWidget(self.solution_btn)

        layout.addLayout(buttons_layout)

        return panel

    def _create_footer(self):
        """Create navigation footer"""
        footer = QFrame()
        footer.setObjectName("footer")
        footer.setFixedHeight(70)

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(15)

        # Previous puzzle button
        self.prev_btn = QPushButton("← Previous Puzzle")
        self.prev_btn.setObjectName("nav_button")
        self.prev_btn.setFixedSize(180, 45)
        self.prev_btn.clicked.connect(self._previous_puzzle)
        layout.addWidget(self.prev_btn)

        layout.addStretch()

        # Progress indicator
        self.progress_label = QLabel("1/40")
        self.progress_label.setObjectName("progress_label")
        self.progress_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(self.progress_label)

        layout.addStretch()

        # Next puzzle button
        self.next_btn = QPushButton("Next Puzzle →")
        self.next_btn.setObjectName("nav_button")
        self.next_btn.setFixedSize(180, 45)
        self.next_btn.clicked.connect(self._next_puzzle)
        layout.addWidget(self.next_btn)

        return footer

    def _load_puzzle(self, puzzle):
        """Load and display a puzzle"""
        if not puzzle:
            return

        self.current_puzzle = puzzle
        self.user_moves = []
        self.puzzles.reset_puzzle()

        # Update UI
        self.puzzle_name.setText(puzzle["name"])
        self.theme_label.setText(f"Theme: {puzzle['theme']}")
        self.difficulty_label.setText(f"Difficulty: {puzzle['difficulty'].title()}")
        self.description_label.setText(puzzle["description"])
        self.fen_display.setText(puzzle["fen"])

        # Update progress
        solution_length = len(puzzle["solution"])
        self.moves_made_label.setText(f"Moves: 0/{solution_length}")
        self.hints_used_label.setText("Hints used: 0")

        # Update status
        self.status_label.setText("Make your move!")
        self.status_label.setStyleSheet("color: #ff69b4;")

        # Hide hint
        self.hint_label.setVisible(False)

        # Update selector
        self.puzzle_selector.setValue(puzzle["id"])

        # Update progress label
        progress = self.puzzles.get_progress()
        self.progress_label.setText(f"{progress['current']}/{progress['total']}")

        # Emit signal
        self.loadPuzzle.emit(puzzle["id"])

    def _on_puzzle_selected(self, puzzle_id):
        """Handle puzzle selection from spinner"""
        puzzle = self.puzzles.get_puzzle(puzzle_id)
        if puzzle:
            self.puzzles.current_puzzle_index = puzzle_id - 1
            self._load_puzzle(puzzle)

    def _filter_by_difficulty(self, difficulty):
        """Filter puzzles by difficulty"""
        if difficulty == "All":
            # Reset to show all puzzles
            self.puzzle_selector.setMaximum(len(self.puzzles.puzzles))
        else:
            # This is a simple implementation - in a full version,
            # you'd filter the puzzle list and update the selector accordingly
            pass

    def _previous_puzzle(self):
        """Navigate to previous puzzle"""
        self.puzzles.previous_puzzle()
        puzzle = self.puzzles.get_puzzle()
        self._load_puzzle(puzzle)

    def _next_puzzle(self):
        """Navigate to next puzzle"""
        self.puzzles.next_puzzle()
        puzzle = self.puzzles.get_puzzle()
        self._load_puzzle(puzzle)

    def _reset_puzzle(self):
        """Reset current puzzle"""
        if self.current_puzzle:
            self._load_puzzle(self.current_puzzle)

    def _show_hint(self):
        """Show a hint for the current puzzle"""
        if not self.current_puzzle:
            return

        hint = self.puzzles.get_hint()
        self.hint_label.setText(f"💡 Hint: {hint}")
        self.hint_label.setVisible(True)

        # Update hints counter
        self.hints_used_label.setText(f"Hints used: {self.puzzles.hints_used}")

        self.requestHint.emit()

    def _show_solution(self):
        """Show the complete solution"""
        if not self.current_puzzle:
            return

        solution = self.current_puzzle["solution"]
        solution_text = " → ".join(solution)

        msg = QMessageBox(self)
        msg.setWindowTitle("Puzzle Solution")
        msg.setText(f"Solution:\n\n{solution_text}")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2a2a2a;
                color: #ffffff;
            }
            QPushButton {
                background-color: #ff1493;
                color: #000000;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff69b4;
            }
        """)
        msg.exec()

    def check_move(self, move_san):
        """
        Check if a move is correct (called by chess board)

        Args:
            move_san: Move in Standard Algebraic Notation

        Returns:
            tuple: (is_correct, is_complete, message)
        """
        if not self.current_puzzle:
            return (False, False, "No puzzle loaded")

        is_correct, is_complete, message = self.puzzles.check_move(move_san)

        # Update UI
        solution_length = len(self.current_puzzle["solution"])
        self.moves_made_label.setText(f"Moves: {len(self.puzzles.user_moves)}/{solution_length}")

        if is_correct:
            if is_complete:
                self.status_label.setText("✓ Puzzle Solved! Well done!")
                self.status_label.setStyleSheet("color: #50c878;")
                self.puzzleSolved.emit(self.current_puzzle["id"])
            else:
                self.status_label.setText(f"✓ Correct! {message}")
                self.status_label.setStyleSheet("color: #50c878;")
        else:
            self.status_label.setText(f"✗ {message}")
            self.status_label.setStyleSheet("color: #ff6b6b;")

        return (is_correct, is_complete, message)

    def _apply_styles(self):
        """Apply pink/black theme styling"""
        self.setStyleSheet("""
            /* Main widget */
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }

            /* Header */
            QFrame#header {
                background-color: #2a2a2a;
                border-bottom: 3px solid #ff1493;
            }

            QLabel#screen_title {
                color: #ff1493;
            }

            QLabel#selector_label {
                color: #ffffff;
            }

            QSpinBox#puzzle_selector {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 2px solid #ff1493;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
            }

            QComboBox#difficulty_combo {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 2px solid #ff1493;
                border-radius: 4px;
                padding: 5px;
                font-size: 12px;
            }

            QComboBox::drop-down {
                border: none;
            }

            /* Board container */
            QFrame#board_container {
                background-color: #2a2a2a;
                border: 3px solid #ff1493;
                border-radius: 8px;
            }

            QLabel#board_placeholder {
                color: #666666;
            }

            /* Info panel */
            QFrame#info_panel {
                background-color: #2a2a2a;
                border: 2px solid #ff1493;
                border-radius: 8px;
            }

            QLabel#puzzle_name {
                color: #ff1493;
            }

            QFrame#metadata_frame {
                background-color: #1a1a1a;
                border: 1px solid #ff1493;
                border-radius: 4px;
                padding: 10px;
            }

            QLabel#metadata_label {
                color: #ff69b4;
            }

            QLabel#description_label {
                color: #cccccc;
            }

            QFrame#progress_frame {
                background-color: #1a1a1a;
                border: 1px solid #ff1493;
                border-radius: 4px;
                padding: 10px;
            }

            QLabel#section_label {
                color: #ff69b4;
            }

            QLabel#info_label {
                color: #ffffff;
            }

            QLabel#status_label {
                background-color: #1a1a1a;
                border: 2px solid #ff1493;
                border-radius: 6px;
                padding: 10px;
            }

            QLabel#hint_label {
                background-color: #2a2a2a;
                border: 2px solid #ffa500;
                border-radius: 6px;
                color: #ffa500;
                padding: 10px;
            }

            QLabel#fen_display {
                background-color: #1a1a1a;
                color: #ff69b4;
                border: 1px solid #ff1493;
                border-radius: 4px;
                padding: 8px;
            }

            /* Buttons */
            QPushButton#back_button {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 2px solid #ff1493;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton#back_button:hover {
                background-color: #ff1493;
                color: #000000;
            }

            QPushButton#hint_button {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 2px solid #ffa500;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#hint_button:hover {
                background-color: #ffa500;
                color: #000000;
            }

            QPushButton#reset_button {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 2px solid #ff69b4;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#reset_button:hover {
                background-color: #ff69b4;
                color: #000000;
            }

            QPushButton#solution_button {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 2px solid #6495ed;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#solution_button:hover {
                background-color: #6495ed;
                color: #000000;
            }

            /* Footer */
            QFrame#footer {
                background-color: #2a2a2a;
                border-top: 3px solid #ff1493;
            }

            QPushButton#nav_button {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 2px solid #ff1493;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#nav_button:hover {
                background-color: #ff1493;
                color: #000000;
            }

            QLabel#progress_label {
                color: #ff69b4;
            }
        """)
