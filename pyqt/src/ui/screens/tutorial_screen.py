"""
Tutorial Screen for PyQt Chess
Interactive chess tutorial interface with lesson selector and content display
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QFrame,
    QScrollArea, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from features.tutorial import ChessTutorial


class TutorialScreen(QWidget):
    """
    Tutorial screen with lesson selector and content display

    Signals:
        backToMenu() - Return to main menu
        loadLesson(int) - Load a specific lesson by ID
        lessonCompleted(int) - Mark lesson as completed
    """

    # Navigation signals
    backToMenu = pyqtSignal()
    loadLesson = pyqtSignal(int)
    lessonCompleted = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize tutorial backend
        self.tutorial = ChessTutorial()
        self.current_lesson = None

        self._init_ui()
        self._apply_styles()
        self._load_lessons()

        # Load first lesson by default
        if self.tutorial.lessons:
            self._display_lesson(self.tutorial.lessons[0])

    def _init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = self._create_header()
        main_layout.addWidget(header)

        # Content area with splitter (lesson list + content)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel - Lesson selector
        self.lesson_list = self._create_lesson_list()
        splitter.addWidget(self.lesson_list)

        # Right panel - Lesson content
        self.content_area = self._create_content_area()
        splitter.addWidget(self.content_area)

        # Set splitter proportions (30% list, 70% content)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 7)

        main_layout.addWidget(splitter)

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
        title = QLabel("Chess Tutorial")
        title.setObjectName("screen_title")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        layout.addWidget(title)

        layout.addStretch()

        # Progress label
        self.progress_label = QLabel("0/0 Completed")
        self.progress_label.setObjectName("progress_label")
        self.progress_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.progress_label)

        layout.addSpacing(20)

        # Back button
        back_btn = QPushButton("Back to Menu")
        back_btn.setObjectName("back_button")
        back_btn.setFixedSize(150, 40)
        back_btn.clicked.connect(self.backToMenu.emit)
        layout.addWidget(back_btn)

        return header

    def _create_lesson_list(self):
        """Create the lesson list widget"""
        container = QFrame()
        container.setObjectName("lesson_list_container")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # Category filter label
        filter_label = QLabel("Lessons by Category")
        filter_label.setObjectName("section_label")
        filter_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(filter_label)

        # Lesson list
        self.lesson_list_widget = QListWidget()
        self.lesson_list_widget.setObjectName("lesson_list")
        self.lesson_list_widget.itemClicked.connect(self._on_lesson_selected)
        layout.addWidget(self.lesson_list_widget)

        return container

    def _create_content_area(self):
        """Create the lesson content display area"""
        container = QFrame()
        container.setObjectName("content_container")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Lesson title
        self.lesson_title = QLabel("Select a lesson")
        self.lesson_title.setObjectName("lesson_title")
        self.lesson_title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.lesson_title.setWordWrap(True)
        layout.addWidget(self.lesson_title)

        # Lesson metadata (category, difficulty)
        metadata_layout = QHBoxLayout()

        self.category_label = QLabel("")
        self.category_label.setObjectName("metadata_label")
        self.category_label.setFont(QFont("Arial", 11))
        metadata_layout.addWidget(self.category_label)

        metadata_layout.addSpacing(20)

        self.difficulty_label = QLabel("")
        self.difficulty_label.setObjectName("metadata_label")
        self.difficulty_label.setFont(QFont("Arial", 11))
        metadata_layout.addWidget(self.difficulty_label)

        metadata_layout.addStretch()
        layout.addLayout(metadata_layout)

        # Content scroll area
        scroll = QScrollArea()
        scroll.setObjectName("content_scroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        # Content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(10)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(self.content_widget)
        layout.addWidget(scroll)

        # Key points section
        key_points_label = QLabel("Key Points")
        key_points_label.setObjectName("section_label")
        key_points_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(key_points_label)

        self.key_points_layout = QVBoxLayout()
        self.key_points_layout.setSpacing(5)
        layout.addLayout(self.key_points_layout)

        # FEN position display
        fen_label = QLabel("Position (FEN):")
        fen_label.setObjectName("section_label")
        fen_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(fen_label)

        self.fen_display = QLabel("")
        self.fen_display.setObjectName("fen_display")
        self.fen_display.setFont(QFont("Courier", 9))
        self.fen_display.setWordWrap(True)
        self.fen_display.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.fen_display)

        return container

    def _create_footer(self):
        """Create navigation footer"""
        footer = QFrame()
        footer.setObjectName("footer")
        footer.setFixedHeight(70)

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(15)

        # Previous button
        self.prev_btn = QPushButton("← Previous")
        self.prev_btn.setObjectName("nav_button")
        self.prev_btn.setFixedSize(150, 45)
        self.prev_btn.clicked.connect(self._previous_lesson)
        layout.addWidget(self.prev_btn)

        layout.addStretch()

        # Mark complete button
        self.complete_btn = QPushButton("Mark Complete")
        self.complete_btn.setObjectName("complete_button")
        self.complete_btn.setFixedSize(180, 45)
        self.complete_btn.clicked.connect(self._mark_complete)
        layout.addWidget(self.complete_btn)

        layout.addStretch()

        # Next button
        self.next_btn = QPushButton("Next →")
        self.next_btn.setObjectName("nav_button")
        self.next_btn.setFixedSize(150, 45)
        self.next_btn.clicked.connect(self._next_lesson)
        layout.addWidget(self.next_btn)

        return footer

    def _load_lessons(self):
        """Load all lessons into the list widget"""
        self.lesson_list_widget.clear()

        # Group lessons by category
        categories = {}
        for lesson in self.tutorial.lessons:
            cat = lesson["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(lesson)

        # Add lessons grouped by category
        for category, lessons in categories.items():
            # Category header
            header_item = QListWidgetItem(f"── {category.replace('_', ' ').title()} ──")
            header_item.setFlags(Qt.ItemFlag.NoItemFlags)
            header_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            self.lesson_list_widget.addItem(header_item)

            # Lessons in category
            for lesson in lessons:
                item = QListWidgetItem(f"{lesson['id']}. {lesson['title']}")
                item.setData(Qt.ItemDataRole.UserRole, lesson["id"])

                # Mark completed lessons
                if lesson["id"] in self.tutorial.completed_lessons:
                    item.setText(f"✓ {lesson['id']}. {lesson['title']}")
                    item.setForeground(Qt.GlobalColor.green)

                self.lesson_list_widget.addItem(item)

        # Update progress
        self._update_progress()

    def _display_lesson(self, lesson):
        """Display a lesson's content"""
        self.current_lesson = lesson

        # Update title and metadata
        self.lesson_title.setText(f"Lesson {lesson['id']}: {lesson['title']}")
        self.category_label.setText(f"Category: {lesson['category'].replace('_', ' ').title()}")
        self.difficulty_label.setText(f"Difficulty: {lesson['difficulty'].title()}")

        # Clear previous content
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add content paragraphs
        for line in lesson["content"]:
            content_label = QLabel(line)
            content_label.setObjectName("content_text")
            content_label.setFont(QFont("Arial", 12))
            content_label.setWordWrap(True)
            self.content_layout.addWidget(content_label)

        # Clear previous key points
        while self.key_points_layout.count():
            child = self.key_points_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add key points
        for point in lesson["key_points"]:
            point_label = QLabel(f"• {point}")
            point_label.setObjectName("key_point")
            point_label.setFont(QFont("Arial", 11))
            self.key_points_layout.addWidget(point_label)

        # Display FEN
        self.fen_display.setText(lesson["fen"])

        # Update complete button state
        if lesson["id"] in self.tutorial.completed_lessons:
            self.complete_btn.setText("✓ Completed")
            self.complete_btn.setEnabled(False)
        else:
            self.complete_btn.setText("Mark Complete")
            self.complete_btn.setEnabled(True)

        # Update navigation buttons
        self._update_navigation_buttons()

    def _on_lesson_selected(self, item):
        """Handle lesson selection from list"""
        lesson_id = item.data(Qt.ItemDataRole.UserRole)
        if lesson_id is not None:
            lesson = self.tutorial.get_lesson(lesson_id)
            if lesson:
                self.tutorial.jump_to_lesson(lesson_id)
                self._display_lesson(lesson)
                self.loadLesson.emit(lesson_id)

    def _previous_lesson(self):
        """Navigate to previous lesson"""
        lesson = self.tutorial.previous_lesson()
        if lesson:
            self._display_lesson(lesson)
            self._highlight_current_lesson()

    def _next_lesson(self):
        """Navigate to next lesson"""
        lesson = self.tutorial.next_lesson()
        if lesson:
            self._display_lesson(lesson)
            self._highlight_current_lesson()

    def _mark_complete(self):
        """Mark current lesson as completed"""
        if self.current_lesson:
            lesson_id = self.current_lesson["id"]
            self.tutorial.mark_completed(lesson_id)
            self.lessonCompleted.emit(lesson_id)

            # Update UI
            self.complete_btn.setText("✓ Completed")
            self.complete_btn.setEnabled(False)
            self._load_lessons()
            self._highlight_current_lesson()

    def _update_progress(self):
        """Update progress label"""
        progress = self.tutorial.get_progress()
        self.progress_label.setText(
            f"{progress['completed']}/{progress['total']} Completed "
            f"({progress['percentage']:.0f}%)"
        )

    def _update_navigation_buttons(self):
        """Update navigation button states"""
        self.prev_btn.setEnabled(self.tutorial.current_lesson_index > 0)
        self.next_btn.setEnabled(
            self.tutorial.current_lesson_index < len(self.tutorial.lessons) - 1
        )

    def _highlight_current_lesson(self):
        """Highlight current lesson in the list"""
        if not self.current_lesson:
            return

        for i in range(self.lesson_list_widget.count()):
            item = self.lesson_list_widget.item(i)
            lesson_id = item.data(Qt.ItemDataRole.UserRole)
            if lesson_id == self.current_lesson["id"]:
                self.lesson_list_widget.setCurrentItem(item)
                break

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

            QLabel#progress_label {
                color: #ff69b4;
            }

            /* Lesson list container */
            QFrame#lesson_list_container {
                background-color: #2a2a2a;
                border-right: 2px solid #ff1493;
            }

            QListWidget#lesson_list {
                background-color: #1a1a1a;
                border: 1px solid #ff1493;
                border-radius: 4px;
                color: #ffffff;
                font-size: 12px;
                padding: 5px;
            }

            QListWidget#lesson_list::item {
                padding: 8px;
                border-bottom: 1px solid #3a3a3a;
                border-radius: 3px;
            }

            QListWidget#lesson_list::item:selected {
                background-color: #ff1493;
                color: #000000;
            }

            QListWidget#lesson_list::item:hover {
                background-color: #3a3a3a;
            }

            /* Content area */
            QFrame#content_container {
                background-color: #1a1a1a;
            }

            QLabel#lesson_title {
                color: #ff1493;
            }

            QLabel#metadata_label {
                color: #ff69b4;
            }

            QLabel#section_label {
                color: #ff69b4;
                margin-top: 10px;
            }

            QScrollArea#content_scroll {
                background-color: transparent;
                border: none;
            }

            QLabel#content_text {
                color: #ffffff;
                padding: 5px;
                line-height: 1.6;
            }

            QLabel#key_point {
                color: #cccccc;
                padding: 3px;
            }

            QLabel#fen_display {
                background-color: #2a2a2a;
                color: #ff69b4;
                border: 1px solid #ff1493;
                border-radius: 4px;
                padding: 10px;
            }

            /* Footer */
            QFrame#footer {
                background-color: #2a2a2a;
                border-top: 3px solid #ff1493;
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

            QPushButton#nav_button:disabled {
                background-color: #1a1a1a;
                color: #666666;
                border-color: #666666;
            }

            QPushButton#complete_button {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 2px solid #50c878;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#complete_button:hover {
                background-color: #50c878;
                color: #000000;
            }

            QPushButton#complete_button:disabled {
                background-color: #1a1a1a;
                color: #50c878;
                border-color: #50c878;
            }
        """)
