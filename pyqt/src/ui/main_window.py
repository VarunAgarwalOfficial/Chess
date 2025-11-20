"""
PyQt6 Chess Main Window
Modern chess interface with QStackedWidget for multiple screens and dashboard
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QDockWidget, QLabel, QProgressBar,
    QListWidget, QFrame, QPushButton, QMenuBar, QMenu,
    QStatusBar, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QFont


class ChessMainWindow(QMainWindow):
    """
    Main window for PyQt6 Chess Application

    Features:
    - QStackedWidget for multiple screens (menu, game, tutorial, puzzles, help)
    - Right dock widget for game dashboard
    - Pink/black modern theme
    - Menu bar with File, Game, Help menus
    - Status bar for messages
    - Proper window sizing: 940x600 (560 board + 380 dashboard)
    """

    # Signals for screen navigation
    screen_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle("PyQt6 Chess - Modern Chess Interface")
        self.setMinimumSize(940, 600)
        self.resize(940, 600)

        # Initialize UI components
        self._init_ui()
        self._init_menu_bar()
        self._init_status_bar()
        self._apply_theme()

        # Show menu screen by default
        self.show_menu_screen()

    def _init_ui(self):
        """Initialize the main UI components"""
        # Create central widget with stacked widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        central_layout = QHBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # Create stacked widget for different screens
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setMinimumWidth(560)

        # Create placeholder screens
        self.menu_screen = self._create_menu_screen()
        self.game_screen = self._create_game_screen()
        self.tutorial_screen = self._create_tutorial_screen()
        self.puzzle_screen = self._create_puzzle_screen()
        self.help_screen = self._create_help_screen()

        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.menu_screen)
        self.stacked_widget.addWidget(self.game_screen)
        self.stacked_widget.addWidget(self.tutorial_screen)
        self.stacked_widget.addWidget(self.puzzle_screen)
        self.stacked_widget.addWidget(self.help_screen)

        central_layout.addWidget(self.stacked_widget)

        # Create right dock widget for dashboard
        self._create_dashboard_dock()

    def _create_menu_screen(self):
        """Create the main menu screen"""
        screen = QWidget()
        layout = QVBoxLayout(screen)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title = QLabel("PyQt6 Chess")
        title.setObjectName("menu_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Arial", 48, QFont.Weight.Bold)
        title.setFont(font)
        layout.addWidget(title)

        layout.addSpacing(40)

        # Menu buttons
        buttons = [
            ("Play vs AI", self.show_game_screen),
            ("Tutorials", self.show_tutorial_screen),
            ("Puzzles", self.show_puzzle_screen),
            ("Help", self.show_help_screen),
            ("Exit", self.close)
        ]

        for btn_text, btn_callback in buttons:
            btn = QPushButton(btn_text)
            btn.setObjectName("menu_button")
            btn.setFixedSize(300, 60)
            btn.clicked.connect(btn_callback)
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addSpacing(15)

        return screen

    def _create_game_screen(self):
        """Create the game screen (chess board will be added here)"""
        screen = QWidget()
        layout = QVBoxLayout(screen)
        layout.setContentsMargins(10, 10, 10, 10)

        # Placeholder for chess board
        placeholder = QLabel("Chess Board Widget\nWill be placed here")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setObjectName("board_placeholder")
        placeholder.setMinimumSize(540, 540)
        placeholder.setStyleSheet("""
            QLabel#board_placeholder {
                background-color: #2a2a2a;
                border: 2px solid #ff1493;
                border-radius: 8px;
                color: #ffffff;
                font-size: 24px;
            }
        """)

        layout.addWidget(placeholder, alignment=Qt.AlignmentFlag.AlignCenter)

        return screen

    def _create_tutorial_screen(self):
        """Create the tutorial screen"""
        screen = QWidget()
        layout = QVBoxLayout(screen)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Chess Tutorials")
        title.setObjectName("screen_title")
        title.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        layout.addWidget(title)

        layout.addSpacing(20)

        # Tutorial content placeholder
        content = QLabel("Tutorial content will be displayed here.\n\n"
                        "Topics:\n"
                        "- Basic Rules\n"
                        "- Piece Movement\n"
                        "- Special Moves\n"
                        "- Strategy Basics\n"
                        "- Opening Principles")
        content.setObjectName("screen_content")
        content.setWordWrap(True)
        layout.addWidget(content)

        layout.addStretch()

        # Back button
        back_btn = QPushButton("Back to Menu")
        back_btn.setObjectName("back_button")
        back_btn.clicked.connect(self.show_menu_screen)
        back_btn.setFixedSize(200, 40)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        return screen

    def _create_puzzle_screen(self):
        """Create the puzzle screen"""
        screen = QWidget()
        layout = QVBoxLayout(screen)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Chess Puzzles")
        title.setObjectName("screen_title")
        title.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        layout.addWidget(title)

        layout.addSpacing(20)

        # Puzzle content placeholder
        content = QLabel("Puzzle board will be displayed here.\n\n"
                        "Solve tactical puzzles to improve your skills!")
        content.setObjectName("screen_content")
        content.setWordWrap(True)
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(content)

        layout.addStretch()

        # Back button
        back_btn = QPushButton("Back to Menu")
        back_btn.setObjectName("back_button")
        back_btn.clicked.connect(self.show_menu_screen)
        back_btn.setFixedSize(200, 40)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        return screen

    def _create_help_screen(self):
        """Create the help screen"""
        screen = QWidget()
        layout = QVBoxLayout(screen)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Help & Instructions")
        title.setObjectName("screen_title")
        title.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        layout.addWidget(title)

        layout.addSpacing(20)

        # Help content
        help_text = """
        <h3>How to Play</h3>
        <p>Click on a piece to select it, then click on a valid square to move.</p>

        <h3>Game Modes</h3>
        <ul>
            <li><b>Play vs AI:</b> Play against the computer at various difficulty levels</li>
            <li><b>Tutorials:</b> Learn chess basics and strategies</li>
            <li><b>Puzzles:</b> Solve tactical puzzles to improve your skills</li>
        </ul>

        <h3>Controls</h3>
        <ul>
            <li><b>Click:</b> Select and move pieces</li>
            <li><b>Ctrl+Z:</b> Undo last move</li>
            <li><b>Ctrl+N:</b> New game</li>
        </ul>

        <h3>About</h3>
        <p>PyQt6 Chess - A modern chess application built with PyQt6</p>
        <p>Features AI opponent, tutorials, puzzles, and more!</p>
        """

        content = QLabel(help_text)
        content.setObjectName("screen_content")
        content.setWordWrap(True)
        content.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(content)

        layout.addStretch()

        # Back button
        back_btn = QPushButton("Back to Menu")
        back_btn.setObjectName("back_button")
        back_btn.clicked.connect(self.show_menu_screen)
        back_btn.setFixedSize(200, 40)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        return screen

    def _create_dashboard_dock(self):
        """Create the right dock widget for game dashboard"""
        # Create dock widget
        self.dashboard_dock = QDockWidget("Game Dashboard", self)
        self.dashboard_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.dashboard_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        # Dashboard container
        dashboard_widget = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_widget)
        dashboard_layout.setContentsMargins(10, 10, 10, 10)
        dashboard_layout.setSpacing(15)

        # Game Info Card
        self.game_info_card = self._create_game_info_card()
        dashboard_layout.addWidget(self.game_info_card)

        # Evaluation Bar
        self.eval_bar = self._create_evaluation_bar()
        dashboard_layout.addWidget(self.eval_bar)

        # Captured Pieces Display
        self.captured_pieces_widget = self._create_captured_pieces_widget()
        dashboard_layout.addWidget(self.captured_pieces_widget)

        # Move History List
        self.move_history_widget = self._create_move_history_widget()
        dashboard_layout.addWidget(self.move_history_widget)

        # AI Thinking Indicator
        self.ai_thinking_widget = self._create_ai_thinking_widget()
        dashboard_layout.addWidget(self.ai_thinking_widget)

        dashboard_layout.addStretch()

        self.dashboard_dock.setWidget(dashboard_widget)
        self.dashboard_dock.setFixedWidth(380)

        # Add dock to main window
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dashboard_dock)

    def _create_game_info_card(self):
        """Create game information card"""
        card = QFrame()
        card.setObjectName("info_card")
        card.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(card)
        layout.setSpacing(8)

        # Title
        title = QLabel("Game Information")
        title.setObjectName("card_title")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Info labels
        self.game_mode_label = QLabel("Mode: vs AI")
        self.difficulty_label = QLabel("Difficulty: Medium")
        self.turn_label = QLabel("Turn: White")
        self.opening_label = QLabel("Opening: Starting Position")

        for label in [self.game_mode_label, self.difficulty_label,
                     self.turn_label, self.opening_label]:
            label.setObjectName("info_label")
            layout.addWidget(label)

        return card

    def _create_evaluation_bar(self):
        """Create position evaluation bar"""
        widget = QFrame()
        widget.setObjectName("eval_card")
        widget.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(widget)
        layout.setSpacing(8)

        # Title
        title = QLabel("Position Evaluation")
        title.setObjectName("card_title")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Evaluation score
        self.eval_score_label = QLabel("0.0")
        self.eval_score_label.setObjectName("eval_score")
        self.eval_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.eval_score_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(self.eval_score_label)

        # Progress bar (visual representation)
        self.eval_progress = QProgressBar()
        self.eval_progress.setObjectName("eval_bar")
        self.eval_progress.setMinimum(-1000)
        self.eval_progress.setMaximum(1000)
        self.eval_progress.setValue(0)
        self.eval_progress.setTextVisible(False)
        self.eval_progress.setFixedHeight(30)
        layout.addWidget(self.eval_progress)

        return widget

    def _create_captured_pieces_widget(self):
        """Create captured pieces display"""
        widget = QFrame()
        widget.setObjectName("captured_card")
        widget.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(widget)
        layout.setSpacing(8)

        # Title
        title = QLabel("Captured Pieces")
        title.setObjectName("card_title")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # White captured
        white_label = QLabel("White:")
        white_label.setObjectName("captured_label")
        layout.addWidget(white_label)

        self.white_captured = QLabel("None")
        self.white_captured.setObjectName("captured_pieces")
        self.white_captured.setWordWrap(True)
        layout.addWidget(self.white_captured)

        # Black captured
        black_label = QLabel("Black:")
        black_label.setObjectName("captured_label")
        layout.addWidget(black_label)

        self.black_captured = QLabel("None")
        self.black_captured.setObjectName("captured_pieces")
        self.black_captured.setWordWrap(True)
        layout.addWidget(self.black_captured)

        return widget

    def _create_move_history_widget(self):
        """Create move history list widget"""
        widget = QFrame()
        widget.setObjectName("history_card")
        widget.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(widget)
        layout.setSpacing(8)

        # Title
        title = QLabel("Move History")
        title.setObjectName("card_title")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Move list
        self.move_history_list = QListWidget()
        self.move_history_list.setObjectName("move_list")
        self.move_history_list.setMinimumHeight(150)
        layout.addWidget(self.move_history_list)

        return widget

    def _create_ai_thinking_widget(self):
        """Create AI thinking indicator"""
        widget = QFrame()
        widget.setObjectName("ai_card")
        widget.setFrameShape(QFrame.Shape.StyledPanel)
        widget.setVisible(False)  # Hidden by default

        layout = QVBoxLayout(widget)
        layout.setSpacing(8)

        # Title
        title = QLabel("AI Status")
        title.setObjectName("card_title")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Status label
        self.ai_status_label = QLabel("AI is thinking...")
        self.ai_status_label.setObjectName("ai_status")
        self.ai_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.ai_status_label)

        # Progress indicator
        self.ai_progress = QProgressBar()
        self.ai_progress.setObjectName("ai_progress")
        self.ai_progress.setMinimum(0)
        self.ai_progress.setMaximum(0)  # Indeterminate
        layout.addWidget(self.ai_progress)

        return widget

    def _init_menu_bar(self):
        """Initialize the menu bar"""
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("&File")

        new_game_action = QAction("&New Game", self)
        new_game_action.setShortcut("Ctrl+N")
        new_game_action.triggered.connect(self._on_new_game)
        file_menu.addAction(new_game_action)

        file_menu.addSeparator()

        load_pgn_action = QAction("&Load PGN...", self)
        load_pgn_action.setShortcut("Ctrl+O")
        load_pgn_action.triggered.connect(self._on_load_pgn)
        file_menu.addAction(load_pgn_action)

        save_pgn_action = QAction("&Save PGN...", self)
        save_pgn_action.setShortcut("Ctrl+S")
        save_pgn_action.triggered.connect(self._on_save_pgn)
        file_menu.addAction(save_pgn_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Game Menu
        game_menu = menubar.addMenu("&Game")

        undo_action = QAction("&Undo Move", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self._on_undo_move)
        game_menu.addAction(undo_action)

        reset_action = QAction("&Reset Game", self)
        reset_action.setShortcut("Ctrl+R")
        reset_action.triggered.connect(self._on_reset_game)
        game_menu.addAction(reset_action)

        game_menu.addSeparator()

        menu_action = QAction("Return to &Menu", self)
        menu_action.setShortcut("Esc")
        menu_action.triggered.connect(self.show_menu_screen)
        game_menu.addAction(menu_action)

        game_menu.addSeparator()

        settings_action = QAction("&Settings...", self)
        settings_action.triggered.connect(self._on_settings)
        game_menu.addAction(settings_action)

        # Help Menu
        help_menu = menubar.addMenu("&Help")

        how_to_play_action = QAction("&How to Play", self)
        how_to_play_action.setShortcut("F1")
        how_to_play_action.triggered.connect(self.show_help_screen)
        help_menu.addAction(how_to_play_action)

        help_menu.addSeparator()

        about_action = QAction("&About", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

    def _init_status_bar(self):
        """Initialize the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.set_status_message("Welcome to PyQt6 Chess!")

    def _apply_theme(self):
        """Apply pink/black modern theme"""
        self.setStyleSheet("""
            /* Main Window */
            QMainWindow {
                background-color: #1a1a1a;
            }

            /* Central Widget */
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }

            /* Menu Screen */
            QLabel#menu_title {
                color: #ff1493;
                margin: 20px;
            }

            QPushButton#menu_button {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 2px solid #ff1493;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }

            QPushButton#menu_button:hover {
                background-color: #ff1493;
                color: #000000;
            }

            QPushButton#menu_button:pressed {
                background-color: #d11080;
            }

            /* Screen Titles and Content */
            QLabel#screen_title {
                color: #ff1493;
                margin-bottom: 10px;
            }

            QLabel#screen_content {
                color: #ffffff;
                font-size: 14px;
                line-height: 1.6;
            }

            QPushButton#back_button {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 2px solid #ff1493;
                border-radius: 6px;
                font-size: 14px;
                padding: 8px;
            }

            QPushButton#back_button:hover {
                background-color: #ff1493;
                color: #000000;
            }

            /* Dashboard Cards */
            QFrame#info_card, QFrame#eval_card, QFrame#captured_card,
            QFrame#history_card, QFrame#ai_card {
                background-color: #2a2a2a;
                border: 2px solid #ff1493;
                border-radius: 8px;
                padding: 10px;
            }

            QLabel#card_title {
                color: #ff1493;
                font-size: 14px;
                font-weight: bold;
            }

            QLabel#info_label, QLabel#captured_label {
                color: #ffffff;
                font-size: 12px;
                padding: 2px;
            }

            QLabel#eval_score {
                color: #ff1493;
                font-size: 24px;
                font-weight: bold;
            }

            QLabel#captured_pieces {
                color: #cccccc;
                font-size: 11px;
                padding: 4px;
            }

            /* Evaluation Bar */
            QProgressBar#eval_bar {
                border: 2px solid #ff1493;
                border-radius: 4px;
                background-color: #1a1a1a;
                text-align: center;
            }

            QProgressBar#eval_bar::chunk {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #ff1493,
                    stop: 1 #ff69b4
                );
            }

            /* AI Progress Bar */
            QProgressBar#ai_progress {
                border: 2px solid #ff1493;
                border-radius: 4px;
                background-color: #1a1a1a;
            }

            QProgressBar#ai_progress::chunk {
                background-color: #ff1493;
            }

            QLabel#ai_status {
                color: #ff69b4;
                font-size: 12px;
            }

            /* Move History List */
            QListWidget#move_list {
                background-color: #1a1a1a;
                border: 1px solid #ff1493;
                border-radius: 4px;
                color: #ffffff;
                font-size: 12px;
                padding: 4px;
            }

            QListWidget#move_list::item {
                padding: 4px;
                border-bottom: 1px solid #3a3a3a;
            }

            QListWidget#move_list::item:selected {
                background-color: #ff1493;
                color: #000000;
            }

            QListWidget#move_list::item:hover {
                background-color: #3a3a3a;
            }

            /* Dock Widget */
            QDockWidget {
                background-color: #1a1a1a;
                color: #ffffff;
                titlebar-close-icon: none;
                titlebar-normal-icon: none;
            }

            QDockWidget::title {
                background-color: #2a2a2a;
                border: 2px solid #ff1493;
                border-radius: 4px;
                padding: 8px;
                text-align: center;
                font-weight: bold;
                color: #ff1493;
            }

            /* Menu Bar */
            QMenuBar {
                background-color: #2a2a2a;
                color: #ffffff;
                border-bottom: 2px solid #ff1493;
                padding: 4px;
            }

            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                border-radius: 4px;
            }

            QMenuBar::item:selected {
                background-color: #ff1493;
                color: #000000;
            }

            QMenu {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 2px solid #ff1493;
                border-radius: 4px;
                padding: 4px;
            }

            QMenu::item {
                padding: 8px 24px;
                border-radius: 4px;
            }

            QMenu::item:selected {
                background-color: #ff1493;
                color: #000000;
            }

            QMenu::separator {
                height: 2px;
                background-color: #ff1493;
                margin: 4px 8px;
            }

            /* Status Bar */
            QStatusBar {
                background-color: #2a2a2a;
                color: #ffffff;
                border-top: 2px solid #ff1493;
                padding: 4px;
            }
        """)

    # Screen navigation methods
    def show_menu_screen(self):
        """Show the main menu screen"""
        self.stacked_widget.setCurrentWidget(self.menu_screen)
        self.dashboard_dock.hide()
        self.set_status_message("Main Menu")
        self.screen_changed.emit("menu")

    def show_game_screen(self):
        """Show the game screen"""
        self.stacked_widget.setCurrentWidget(self.game_screen)
        self.dashboard_dock.show()
        self.set_status_message("Game in progress")
        self.screen_changed.emit("game")

    def show_tutorial_screen(self):
        """Show the tutorial screen"""
        self.stacked_widget.setCurrentWidget(self.tutorial_screen)
        self.dashboard_dock.hide()
        self.set_status_message("Tutorial Mode")
        self.screen_changed.emit("tutorial")

    def show_puzzle_screen(self):
        """Show the puzzle screen"""
        self.stacked_widget.setCurrentWidget(self.puzzle_screen)
        self.dashboard_dock.hide()
        self.set_status_message("Puzzle Mode")
        self.screen_changed.emit("puzzle")

    def show_help_screen(self):
        """Show the help screen"""
        self.stacked_widget.setCurrentWidget(self.help_screen)
        self.dashboard_dock.hide()
        self.set_status_message("Help & Instructions")
        self.screen_changed.emit("help")

    # Dashboard update methods
    def update_dashboard(self, board=None, eval_score=0.0, captured=None):
        """
        Update the dashboard with current game state

        Args:
            board: Chess board object (optional)
            eval_score: Position evaluation score (-∞ to +∞)
            captured: Dict with 'white' and 'black' lists of captured pieces
        """
        # Update evaluation
        self.eval_score_label.setText(f"{eval_score:+.1f}")

        # Update evaluation bar (clamp to -10 to +10 for display)
        clamped_score = max(-10, min(10, eval_score))
        bar_value = int(clamped_score * 100)
        self.eval_progress.setValue(bar_value)

        # Update captured pieces
        if captured:
            white_pieces = ", ".join(captured.get('white', [])) or "None"
            black_pieces = ", ".join(captured.get('black', [])) or "None"
            self.white_captured.setText(white_pieces)
            self.black_captured.setText(black_pieces)

    def update_game_info(self, mode=None, difficulty=None, turn=None, opening=None):
        """Update game information card"""
        if mode:
            self.game_mode_label.setText(f"Mode: {mode}")
        if difficulty:
            self.difficulty_label.setText(f"Difficulty: {difficulty}")
        if turn:
            self.turn_label.setText(f"Turn: {turn}")
        if opening:
            self.opening_label.setText(f"Opening: {opening}")

    def add_move_to_history(self, move_number, white_move, black_move=None):
        """
        Add a move to the history list

        Args:
            move_number: The move number
            white_move: White's move in algebraic notation
            black_move: Black's move in algebraic notation (optional)
        """
        if black_move:
            move_text = f"{move_number}. {white_move} {black_move}"
        else:
            move_text = f"{move_number}. {white_move}"

        self.move_history_list.addItem(move_text)
        self.move_history_list.scrollToBottom()

    def clear_move_history(self):
        """Clear the move history list"""
        self.move_history_list.clear()

    def show_ai_thinking(self, status_text="AI is thinking..."):
        """Show AI thinking indicator"""
        self.ai_thinking_widget.setVisible(True)
        self.ai_status_label.setText(status_text)

    def hide_ai_thinking(self):
        """Hide AI thinking indicator"""
        self.ai_thinking_widget.setVisible(False)

    def set_status_message(self, message, timeout=0):
        """
        Show a message in the status bar

        Args:
            message: Status message to display
            timeout: Time in milliseconds to show message (0 = permanent)
        """
        if timeout > 0:
            self.status_bar.showMessage(message, timeout)
        else:
            self.status_bar.showMessage(message)

    # Menu action handlers
    def _on_new_game(self):
        """Handle new game action"""
        self.show_game_screen()
        self.clear_move_history()
        self.update_dashboard(eval_score=0.0, captured={'white': [], 'black': []})
        self.set_status_message("New game started")

    def _on_load_pgn(self):
        """Handle load PGN action"""
        self.set_status_message("Load PGN not implemented yet")

    def _on_save_pgn(self):
        """Handle save PGN action"""
        self.set_status_message("Save PGN not implemented yet")

    def _on_undo_move(self):
        """Handle undo move action"""
        self.set_status_message("Undo move not implemented yet")

    def _on_reset_game(self):
        """Handle reset game action"""
        self.clear_move_history()
        self.update_dashboard(eval_score=0.0, captured={'white': [], 'black': []})
        self.set_status_message("Game reset")

    def _on_settings(self):
        """Handle settings action"""
        self.set_status_message("Settings dialog not implemented yet")

    def _on_about(self):
        """Handle about action"""
        self.set_status_message("PyQt6 Chess - A modern chess application")
