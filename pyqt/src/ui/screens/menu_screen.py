"""
Main Menu Screen for PyQt Chess
Displays main menu with game mode selection and navigation
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class MenuScreen(QWidget):
    """
    Main menu screen with game mode selection

    Signals:
        startPvP() - Start player vs player game
        startPvAI(str) - Start vs AI with difficulty (easy/medium/hard/expert)
        showTutorial() - Show tutorial screen
        showPuzzles() - Show puzzle screen
        showHelp() - Show help screen
        exitApp() - Exit application
    """

    # Navigation signals
    startPvP = pyqtSignal()
    startPvAI = pyqtSignal(str)  # difficulty: easy/medium/hard/expert
    showTutorial = pyqtSignal()
    showPuzzles = pyqtSignal()
    showHelp = pyqtSignal()
    exitApp = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._apply_styles()

    def _init_ui(self):
        """Initialize the UI components"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title = QLabel("PyQt Chess")
        title.setObjectName("menu_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 56, QFont.Weight.Bold))
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Choose your game mode")
        subtitle.setObjectName("menu_subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setFont(QFont("Arial", 16))
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        # Main menu buttons container
        buttons_container = QWidget()
        buttons_layout = QVBoxLayout(buttons_container)
        buttons_layout.setSpacing(15)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Player vs Player button
        self.pvp_button = self._create_menu_button(
            "Player vs Player",
            "Play against another human player"
        )
        self.pvp_button.clicked.connect(self.startPvP.emit)
        buttons_layout.addWidget(self.pvp_button)

        # VS AI section
        ai_label = QLabel("Play vs AI")
        ai_label.setObjectName("section_label")
        ai_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ai_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        buttons_layout.addWidget(ai_label)

        # AI difficulty buttons in a grid
        ai_buttons_widget = QWidget()
        ai_buttons_layout = QGridLayout(ai_buttons_widget)
        ai_buttons_layout.setSpacing(10)

        difficulties = [
            ("Easy", "easy"),
            ("Medium", "medium"),
            ("Hard", "hard"),
            ("Expert", "expert")
        ]

        for idx, (label, difficulty) in enumerate(difficulties):
            row = idx // 2
            col = idx % 2
            btn = self._create_ai_button(label, difficulty)
            btn.clicked.connect(lambda checked, d=difficulty: self.startPvAI.emit(d))
            ai_buttons_layout.addWidget(btn, row, col)

        buttons_layout.addWidget(ai_buttons_widget)

        buttons_layout.addSpacing(10)

        # Tutorial button
        self.tutorial_button = self._create_menu_button(
            "Tutorial",
            "Learn chess basics and strategies"
        )
        self.tutorial_button.clicked.connect(self.showTutorial.emit)
        buttons_layout.addWidget(self.tutorial_button)

        # Puzzles button
        self.puzzles_button = self._create_menu_button(
            "Puzzles",
            "Solve tactical puzzles"
        )
        self.puzzles_button.clicked.connect(self.showPuzzles.emit)
        buttons_layout.addWidget(self.puzzles_button)

        # Help button
        self.help_button = self._create_menu_button(
            "Help",
            "Instructions and about"
        )
        self.help_button.clicked.connect(self.showHelp.emit)
        buttons_layout.addWidget(self.help_button)

        buttons_layout.addSpacing(10)

        # Exit button
        self.exit_button = self._create_menu_button(
            "Exit",
            "Quit the application",
            is_exit=True
        )
        self.exit_button.clicked.connect(self.exitApp.emit)
        buttons_layout.addWidget(self.exit_button)

        layout.addWidget(buttons_container)

        # Footer
        footer = QLabel("Use arrow keys to navigate • Enter to select")
        footer.setObjectName("menu_footer")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setFont(QFont("Arial", 10))
        layout.addWidget(footer)

    def _create_menu_button(self, text, description, is_exit=False):
        """Create a styled menu button with text and description"""
        button = QPushButton()
        button.setObjectName("exit_button" if is_exit else "menu_button")
        button.setFixedSize(400, 70)
        button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Button layout
        btn_layout = QVBoxLayout(button)
        btn_layout.setContentsMargins(15, 10, 15, 10)
        btn_layout.setSpacing(2)

        # Main text
        main_label = QLabel(text)
        main_label.setObjectName("button_main_text")
        main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        btn_layout.addWidget(main_label)

        # Description text
        desc_label = QLabel(description)
        desc_label.setObjectName("button_desc_text")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setFont(QFont("Arial", 10))
        btn_layout.addWidget(desc_label)

        return button

    def _create_ai_button(self, text, difficulty):
        """Create a smaller AI difficulty button"""
        button = QPushButton(text)
        button.setObjectName(f"ai_button_{difficulty}")
        button.setFixedSize(190, 50)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        return button

    def _apply_styles(self):
        """Apply pink/black theme styling"""
        self.setStyleSheet("""
            /* Main container */
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }

            /* Title */
            QLabel#menu_title {
                color: #ff1493;
                margin-bottom: 10px;
            }

            /* Subtitle */
            QLabel#menu_subtitle {
                color: #cccccc;
                margin-bottom: 20px;
            }

            /* Section labels */
            QLabel#section_label {
                color: #ff69b4;
                margin-top: 10px;
                margin-bottom: 5px;
            }

            /* Menu buttons */
            QPushButton#menu_button {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 3px solid #ff1493;
                border-radius: 10px;
                padding: 10px;
            }

            QPushButton#menu_button:hover {
                background-color: #ff1493;
                color: #000000;
                border-color: #ff69b4;
            }

            QPushButton#menu_button:pressed {
                background-color: #d11080;
                border-color: #d11080;
            }

            /* AI difficulty buttons */
            QPushButton[objectName^="ai_button"] {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 2px solid #ff1493;
                border-radius: 8px;
                padding: 8px;
            }

            QPushButton[objectName^="ai_button"]:hover {
                background-color: #ff1493;
                color: #000000;
            }

            QPushButton[objectName^="ai_button"]:pressed {
                background-color: #d11080;
            }

            /* Exit button */
            QPushButton#exit_button {
                background-color: #2a2a2a;
                color: #ff6b6b;
                border: 3px solid #ff6b6b;
                border-radius: 10px;
                padding: 10px;
            }

            QPushButton#exit_button:hover {
                background-color: #ff6b6b;
                color: #000000;
            }

            QPushButton#exit_button:pressed {
                background-color: #d14545;
            }

            /* Button text labels */
            QLabel#button_main_text {
                background: transparent;
                color: inherit;
            }

            QLabel#button_desc_text {
                background: transparent;
                color: #aaaaaa;
            }

            QPushButton:hover QLabel#button_desc_text {
                color: #333333;
            }

            /* Footer */
            QLabel#menu_footer {
                color: #666666;
                margin-top: 20px;
            }
        """)
