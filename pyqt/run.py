#!/usr/bin/env python3
"""
PyQt6 Chess Application - Main Entry Point

A modern, full-featured chess application with:
- Play against AI with multiple difficulty levels
- Chess puzzles
- Tutorials
- Move history and analysis
- Modern pink/black UI theme

Usage:
    python run.py
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Import the chess application
from src.ui.app import ChessApplication


def main():
    """Main entry point for the chess application"""
    try:
        # Enable high DPI scaling
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )

        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("PyQt6 Chess")
        app.setOrganizationName("Chess")
        app.setApplicationVersion("1.0.0")

        # Create and show chess application
        chess_app = ChessApplication()
        chess_app.show()

        # Execute application loop
        exit_code = app.exec()

        # Cleanup
        chess_app.cleanup()

        # Exit with proper code
        sys.exit(exit_code)

    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)

    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
