#!/usr/bin/env python3
"""
Test script for ChessMainWindow
Demonstrates the main window functionality
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import ChessMainWindow


def main():
    """Test the main window"""
    app = QApplication(sys.argv)

    # Create and show main window
    window = ChessMainWindow()
    window.show()

    # Test dashboard updates
    window.update_dashboard(
        eval_score=1.5,
        captured={
            'white': ['pawn', 'knight'],
            'black': ['pawn', 'pawn', 'bishop']
        }
    )

    # Test game info updates
    window.update_game_info(
        mode="vs AI",
        difficulty="Hard",
        turn="White",
        opening="Sicilian Defense"
    )

    # Test move history
    window.add_move_to_history(1, "e4", "e5")
    window.add_move_to_history(2, "Nf3", "Nc6")
    window.add_move_to_history(3, "Bb5", "a6")

    # Test AI thinking indicator
    # window.show_ai_thinking("AI analyzing position...")

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
