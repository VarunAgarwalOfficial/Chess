"""
Help and About Screen for PyQt Chess
Displays controls, features, and credits information
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QScrollArea, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class HelpScreen(QWidget):
    """
    Help and about screen with controls, features, and credits

    Signals:
        backToMenu() - Return to main menu
    """

    # Navigation signals
    backToMenu = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._apply_styles()

    def _init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = self._create_header()
        main_layout.addWidget(header)

        # Tab widget for different help sections
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("help_tabs")

        # Add tabs
        self.tab_widget.addTab(self._create_controls_tab(), "Controls")
        self.tab_widget.addTab(self._create_features_tab(), "Features")
        self.tab_widget.addTab(self._create_rules_tab(), "Chess Rules")
        self.tab_widget.addTab(self._create_about_tab(), "About")

        main_layout.addWidget(self.tab_widget)

        # Footer
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
        title = QLabel("Help & Instructions")
        title.setObjectName("screen_title")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        layout.addWidget(title)

        layout.addStretch()

        # Back button
        back_btn = QPushButton("Back to Menu")
        back_btn.setObjectName("back_button")
        back_btn.setFixedSize(150, 40)
        back_btn.clicked.connect(self.backToMenu.emit)
        layout.addWidget(back_btn)

        return header

    def _create_controls_tab(self):
        """Create the controls/keyboard shortcuts tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("Keyboard Shortcuts & Controls")
        title.setObjectName("tab_title")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)

        # Controls sections
        controls = [
            ("Game Controls", [
                ("Click", "Select and move pieces"),
                ("Drag & Drop", "Click and drag pieces to move"),
                ("Right Click", "Deselect piece"),
                ("Ctrl+N", "Start new game"),
                ("Ctrl+Z", "Undo last move"),
                ("Ctrl+R", "Reset game"),
                ("Esc", "Return to menu"),
            ]),
            ("File Operations", [
                ("Ctrl+O", "Load PGN file"),
                ("Ctrl+S", "Save game as PGN"),
                ("Ctrl+Q", "Quit application"),
            ]),
            ("Navigation", [
                ("Tab", "Switch between UI elements"),
                ("Arrow Keys", "Navigate menu options"),
                ("Enter", "Confirm selection"),
                ("F1", "Show help screen"),
            ]),
            ("Mouse Controls", [
                ("Left Click", "Select/move piece"),
                ("Right Click", "Cancel selection"),
                ("Hover", "Preview legal moves"),
                ("Double Click", "Quick move (if only one legal move)"),
            ]),
        ]

        for section_title, shortcuts in controls:
            section_frame = self._create_control_section(section_title, shortcuts)
            scroll_layout.addWidget(section_frame)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        return widget

    def _create_control_section(self, title, shortcuts):
        """Create a control section with shortcuts"""
        frame = QFrame()
        frame.setObjectName("control_section")

        layout = QVBoxLayout(frame)
        layout.setSpacing(8)

        # Section title
        title_label = QLabel(title)
        title_label.setObjectName("section_title")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title_label)

        # Shortcuts
        for key, description in shortcuts:
            shortcut_layout = QHBoxLayout()

            key_label = QLabel(key)
            key_label.setObjectName("key_label")
            key_label.setFont(QFont("Courier", 11, QFont.Weight.Bold))
            key_label.setFixedWidth(150)
            shortcut_layout.addWidget(key_label)

            desc_label = QLabel(description)
            desc_label.setObjectName("desc_label")
            desc_label.setFont(QFont("Arial", 11))
            desc_label.setWordWrap(True)
            shortcut_layout.addWidget(desc_label)

            layout.addLayout(shortcut_layout)

        return frame

    def _create_features_tab(self):
        """Create the features overview tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("Features")
        title.setObjectName("tab_title")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)

        # Features list
        features = [
            ("Game Modes", [
                "Player vs Player - Play against a friend locally",
                "Player vs AI - Challenge the computer at 4 difficulty levels",
                "Easy: Perfect for beginners learning the game",
                "Medium: Good challenge for casual players",
                "Hard: Tests experienced players",
                "Expert: Maximum challenge with deep analysis",
            ]),
            ("Tutorial System", [
                "20+ interactive chess lessons",
                "Learn piece movements and special moves",
                "Master tactical patterns and strategies",
                "Track your progress through lessons",
                "Organized by category and difficulty",
            ]),
            ("Puzzle Mode", [
                "40+ tactical puzzles to solve",
                "Various themes: forks, pins, mates, and more",
                "Multiple difficulty levels",
                "Hint system to help when stuck",
                "Track moves and solution attempts",
            ]),
            ("Visual Features", [
                "Modern pink/black color theme",
                "Smooth piece animations",
                "Legal move highlighting",
                "Last move indication",
                "Captured pieces display",
                "Hardware-accelerated graphics",
            ]),
            ("Game Analysis", [
                "Position evaluation display",
                "Complete move history",
                "Opening book detection",
                "AI thinking indicator",
                "Material count tracking",
            ]),
            ("File Support", [
                "Load games from PGN files",
                "Save games in PGN format",
                "FEN position import/export",
                "Game notation display",
            ]),
        ]

        for section_title, feature_list in features:
            section_frame = self._create_feature_section(section_title, feature_list)
            scroll_layout.addWidget(section_frame)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        return widget

    def _create_feature_section(self, title, features):
        """Create a feature section"""
        frame = QFrame()
        frame.setObjectName("feature_section")

        layout = QVBoxLayout(frame)
        layout.setSpacing(8)

        # Section title
        title_label = QLabel(title)
        title_label.setObjectName("section_title")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title_label)

        # Feature list
        for feature in features:
            feature_label = QLabel(f"• {feature}")
            feature_label.setObjectName("feature_label")
            feature_label.setFont(QFont("Arial", 11))
            feature_label.setWordWrap(True)
            layout.addWidget(feature_label)

        return frame

    def _create_rules_tab(self):
        """Create the chess rules quick reference tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("Chess Rules Quick Reference")
        title.setObjectName("tab_title")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)

        # Rules content
        rules_html = """
        <h3 style='color: #ff1493;'>Objective</h3>
        <p>Checkmate your opponent's king. The king is in checkmate when it's under attack
        and cannot escape.</p>

        <h3 style='color: #ff1493;'>Piece Movement</h3>
        <ul>
            <li><b>Pawn:</b> Moves forward one square (two on first move). Captures diagonally.</li>
            <li><b>Knight:</b> Moves in an L-shape (2+1 squares). Can jump over pieces.</li>
            <li><b>Bishop:</b> Moves diagonally any number of squares.</li>
            <li><b>Rook:</b> Moves horizontally or vertically any number of squares.</li>
            <li><b>Queen:</b> Combines rook and bishop movement.</li>
            <li><b>King:</b> Moves one square in any direction.</li>
        </ul>

        <h3 style='color: #ff1493;'>Special Moves</h3>
        <ul>
            <li><b>Castling:</b> King moves two squares toward rook, rook jumps over.
            Requirements: neither piece has moved, no pieces between them, king not in check.</li>
            <li><b>En Passant:</b> Special pawn capture when enemy pawn moves two squares forward
            and lands beside your pawn.</li>
            <li><b>Promotion:</b> When a pawn reaches the opposite end, it promotes to queen,
            rook, bishop, or knight.</li>
        </ul>

        <h3 style='color: #ff1493;'>Game End Conditions</h3>
        <ul>
            <li><b>Checkmate:</b> King in check with no legal moves - you win!</li>
            <li><b>Stalemate:</b> No legal moves but not in check - draw.</li>
            <li><b>Draw by Agreement:</b> Both players agree to a draw.</li>
            <li><b>Insufficient Material:</b> Neither player can checkmate.</li>
            <li><b>Threefold Repetition:</b> Same position occurs three times.</li>
            <li><b>50-Move Rule:</b> 50 moves without capture or pawn move.</li>
        </ul>

        <h3 style='color: #ff1493;'>Basic Strategy Tips</h3>
        <ul>
            <li>Control the center of the board</li>
            <li>Develop your pieces early (knights and bishops first)</li>
            <li>Castle early to protect your king</li>
            <li>Don't move the same piece twice in the opening</li>
            <li>Protect your pieces and look for undefended enemy pieces</li>
            <li>Think about your opponent's threats before making your move</li>
        </ul>

        <h3 style='color: #ff1493;'>Piece Values</h3>
        <ul>
            <li>Pawn = 1 point</li>
            <li>Knight = 3 points</li>
            <li>Bishop = 3 points</li>
            <li>Rook = 5 points</li>
            <li>Queen = 9 points</li>
            <li>King = invaluable (game ends if captured)</li>
        </ul>
        """

        rules_label = QLabel(rules_html)
        rules_label.setObjectName("rules_content")
        rules_label.setWordWrap(True)
        rules_label.setTextFormat(Qt.TextFormat.RichText)
        rules_label.setFont(QFont("Arial", 11))
        scroll_layout.addWidget(rules_label)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        return widget

    def _create_about_tab(self):
        """Create the about/credits tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        # App title
        app_title = QLabel("PyQt Chess")
        app_title.setObjectName("about_title")
        app_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_title.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        layout.addWidget(app_title)

        # Version
        version = QLabel("Version 1.0.0")
        version.setObjectName("version_label")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version.setFont(QFont("Arial", 14))
        layout.addWidget(version)

        layout.addSpacing(20)

        # Description
        description = QLabel(
            "A modern, feature-rich chess application built with PyQt6.\n\n"
            "Featuring AI opponents, interactive tutorials, tactical puzzles,\n"
            "and a beautiful pink/black color scheme."
        )
        description.setObjectName("about_description")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        description.setFont(QFont("Arial", 12))
        layout.addWidget(description)

        layout.addSpacing(30)

        # Features highlight
        features_frame = QFrame()
        features_frame.setObjectName("about_features")
        features_layout = QVBoxLayout(features_frame)
        features_layout.setSpacing(10)

        highlights = [
            "Hardware-Accelerated Graphics",
            "Multiple AI Difficulty Levels",
            "20+ Interactive Tutorial Lessons",
            "40+ Tactical Puzzles",
            "PGN File Support",
            "Position Evaluation",
            "Opening Book Integration",
        ]

        for highlight in highlights:
            label = QLabel(f"✓ {highlight}")
            label.setObjectName("feature_highlight")
            label.setFont(QFont("Arial", 11))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            features_layout.addWidget(label)

        layout.addWidget(features_frame)

        layout.addSpacing(30)

        # Credits
        credits_frame = QFrame()
        credits_frame.setObjectName("credits_frame")
        credits_layout = QVBoxLayout(credits_frame)
        credits_layout.setSpacing(8)

        credits_title = QLabel("Credits")
        credits_title.setObjectName("credits_title")
        credits_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credits_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        credits_layout.addWidget(credits_title)

        credits_text = QLabel(
            "Built with PyQt6\n"
            "Chess engine and game logic: Custom implementation\n"
            "UI/UX Design: Modern minimalist approach\n"
            "Testing and development: Community contributors"
        )
        credits_text.setObjectName("credits_text")
        credits_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credits_text.setFont(QFont("Arial", 10))
        credits_layout.addWidget(credits_text)

        layout.addWidget(credits_frame)

        layout.addSpacing(30)

        # License
        license_label = QLabel("© 2024 PyQt Chess. All rights reserved.")
        license_label.setObjectName("license_label")
        license_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        license_label.setFont(QFont("Arial", 9))
        layout.addWidget(license_label)

        layout.addStretch()

        return widget

    def _create_footer(self):
        """Create footer with additional info"""
        footer = QFrame()
        footer.setObjectName("footer")
        footer.setFixedHeight(60)

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(20, 10, 20, 10)

        # Info text
        info = QLabel("For more information, visit the Tutorial or Puzzle sections")
        info.setObjectName("footer_text")
        info.setFont(QFont("Arial", 10))
        layout.addWidget(info)

        layout.addStretch()

        return footer

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

            /* Tab Widget */
            QTabWidget#help_tabs {
                background-color: #1a1a1a;
            }

            QTabWidget::pane {
                border: 2px solid #ff1493;
                border-radius: 4px;
                background-color: #1a1a1a;
            }

            QTabBar::tab {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 2px solid #ff1493;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                padding: 10px 20px;
                margin-right: 2px;
                font-size: 13px;
                font-weight: bold;
            }

            QTabBar::tab:selected {
                background-color: #ff1493;
                color: #000000;
            }

            QTabBar::tab:hover:!selected {
                background-color: #3a3a3a;
            }

            /* Tab content */
            QLabel#tab_title {
                color: #ff1493;
                margin-bottom: 10px;
            }

            /* Control sections */
            QFrame#control_section {
                background-color: #2a2a2a;
                border: 2px solid #ff1493;
                border-radius: 6px;
                padding: 15px;
            }

            QLabel#section_title {
                color: #ff69b4;
            }

            QLabel#key_label {
                color: #ff1493;
                background-color: #1a1a1a;
                border: 1px solid #ff1493;
                border-radius: 4px;
                padding: 4px 8px;
            }

            QLabel#desc_label {
                color: #cccccc;
            }

            /* Feature sections */
            QFrame#feature_section {
                background-color: #2a2a2a;
                border: 2px solid #ff1493;
                border-radius: 6px;
                padding: 15px;
            }

            QLabel#feature_label {
                color: #cccccc;
                padding: 2px;
            }

            /* Rules content */
            QLabel#rules_content {
                color: #ffffff;
                padding: 10px;
            }

            /* About tab */
            QLabel#about_title {
                color: #ff1493;
            }

            QLabel#version_label {
                color: #ff69b4;
            }

            QLabel#about_description {
                color: #cccccc;
            }

            QFrame#about_features {
                background-color: #2a2a2a;
                border: 2px solid #ff1493;
                border-radius: 8px;
                padding: 20px;
            }

            QLabel#feature_highlight {
                color: #50c878;
            }

            QFrame#credits_frame {
                background-color: #2a2a2a;
                border: 2px solid #ff1493;
                border-radius: 8px;
                padding: 20px;
            }

            QLabel#credits_title {
                color: #ff69b4;
            }

            QLabel#credits_text {
                color: #cccccc;
            }

            QLabel#license_label {
                color: #666666;
            }

            /* Footer */
            QFrame#footer {
                background-color: #2a2a2a;
                border-top: 3px solid #ff1493;
            }

            QLabel#footer_text {
                color: #cccccc;
            }

            /* Scroll areas */
            QScrollArea {
                background-color: transparent;
                border: none;
            }

            QScrollBar:vertical {
                background-color: #1a1a1a;
                width: 12px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background-color: #ff1493;
                border-radius: 6px;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #ff69b4;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
