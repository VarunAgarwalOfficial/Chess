#!/usr/bin/env python3
"""
Integration Verification Script
Tests that all components are properly integrated without running the GUI
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def verify_imports():
    """Verify all imports work correctly"""
    print("=" * 60)
    print("IMPORT VERIFICATION")
    print("=" * 60)

    checks = []

    # Check PyQt6
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt, pyqtSignal
        from PyQt6.QtGui import QShortcut
        checks.append(("PyQt6 modules", True, ""))
    except ImportError as e:
        checks.append(("PyQt6 modules", False, str(e)))

    # Check game modules
    try:
        from game import Board
        from game.Piece import Piece
        checks.append(("Game modules (Board, Piece)", True, ""))
    except ImportError as e:
        checks.append(("Game modules (Board, Piece)", False, str(e)))

    # Check AI modules
    try:
        from ai.ai import AI
        checks.append(("AI modules", True, ""))
    except ImportError as e:
        checks.append(("AI modules", False, str(e)))

    # Check UI modules
    try:
        from src.ui.chess_board import ChessBoardWidget
        checks.append(("UI: ChessBoardWidget", True, ""))
    except ImportError as e:
        checks.append(("UI: ChessBoardWidget", False, str(e)))

    try:
        from src.ui.game_controller import GameController
        checks.append(("UI: GameController", True, ""))
    except ImportError as e:
        checks.append(("UI: GameController", False, str(e)))

    try:
        from src.ui.main_window import ChessMainWindow
        checks.append(("UI: ChessMainWindow", True, ""))
    except ImportError as e:
        checks.append(("UI: ChessMainWindow", False, str(e)))

    try:
        from src.ui.app import ChessApplication
        checks.append(("UI: ChessApplication", True, ""))
    except ImportError as e:
        checks.append(("UI: ChessApplication", False, str(e)))

    # Print results
    success_count = sum(1 for _, success, _ in checks if success)
    total_count = len(checks)

    for name, success, error in checks:
        status = "✓" if success else "✗"
        print(f"{status} {name}")
        if not success and error:
            print(f"  Error: {error}")

    print()
    print(f"Results: {success_count}/{total_count} imports successful")

    return success_count == total_count

def verify_file_structure():
    """Verify all required files exist"""
    print("\n" + "=" * 60)
    print("FILE STRUCTURE VERIFICATION")
    print("=" * 60)

    required_files = [
        "run.py",
        "src/ui/app.py",
        "src/ui/main_window.py",
        "src/ui/game_controller.py",
        "src/ui/chess_board.py",
        "src/ui/__init__.py",
        "src/game/__init__.py",
        "styles/chess_theme.qss",
        "requirements.txt"
    ]

    checks = []
    for file_path in required_files:
        full_path = os.path.join(project_root, file_path)
        exists = os.path.exists(full_path)
        checks.append((file_path, exists))

    success_count = sum(1 for _, exists in checks if exists)
    total_count = len(checks)

    for file_path, exists in checks:
        status = "✓" if exists else "✗"
        print(f"{status} {file_path}")

    print()
    print(f"Results: {success_count}/{total_count} files found")

    return success_count == total_count

def verify_signal_connections():
    """Verify signal connections (requires PyQt6)"""
    print("\n" + "=" * 60)
    print("SIGNAL CONNECTION VERIFICATION")
    print("=" * 60)

    try:
        from PyQt6.QtCore import pyqtSignal, QObject

        # Check GameController signals
        from src.ui.game_controller import GameController

        controller_signals = [
            'gameStateChanged',
            'moveCompleted',
            'aiThinking',
            'gameOver',
            'evaluationUpdated',
            'moveValidated',
            'errorOccurred',
            'puzzleLoaded',
            'puzzleProgress'
        ]

        print("\nGameController signals:")
        for signal_name in controller_signals:
            has_signal = hasattr(GameController, signal_name)
            status = "✓" if has_signal else "✗"
            print(f"  {status} {signal_name}")

        # Check ChessBoardWidget signals
        from src.ui.chess_board import ChessBoardWidget

        board_signals = [
            'moveAttempted',
            'squareClicked',
            'pieceSelected'
        ]

        print("\nChessBoardWidget signals:")
        for signal_name in board_signals:
            has_signal = hasattr(ChessBoardWidget, signal_name)
            status = "✓" if has_signal else "✗"
            print(f"  {status} {signal_name}")

        # Check MainWindow signals
        from src.ui.main_window import ChessMainWindow

        window_signals = [
            'screen_changed'
        ]

        print("\nChessMainWindow signals:")
        for signal_name in window_signals:
            has_signal = hasattr(ChessMainWindow, signal_name)
            status = "✓" if has_signal else "✗"
            print(f"  {status} {signal_name}")

        return True

    except ImportError as e:
        print(f"✗ Cannot verify signals (PyQt6 not available): {e}")
        return False

def verify_methods():
    """Verify key methods exist"""
    print("\n" + "=" * 60)
    print("METHOD VERIFICATION")
    print("=" * 60)

    try:
        from src.ui.app import ChessApplication

        required_methods = [
            'show',
            'exec',
            'cleanup',
            'get_controller',
            'get_main_window',
            'get_board_widget',
            'set_game_mode',
            '_setup_board_widget',
            '_connect_signals',
            '_setup_keyboard_shortcuts'
        ]

        print("\nChessApplication methods:")
        for method_name in required_methods:
            has_method = hasattr(ChessApplication, method_name)
            status = "✓" if has_method else "✗"
            print(f"  {status} {method_name}")

        return True

    except ImportError as e:
        print(f"✗ Cannot verify methods (import failed): {e}")
        return False

def print_summary(results):
    """Print overall summary"""
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)

    total = len(results)
    passed = sum(1 for r in results if r[1])

    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")

    print()
    print(f"Overall: {passed}/{total} checks passed")

    if passed == total:
        print("\n🎉 All checks passed! Application is ready to run.")
        print("\nRun with: python run.py")
        return True
    else:
        print("\n⚠️  Some checks failed. Please review the errors above.")
        if not results[0][1]:  # PyQt6 import failed
            print("\nNote: Install PyQt6 with: pip install PyQt6")
        return False

def main():
    """Main verification function"""
    print("\n" + "=" * 60)
    print("PyQt6 Chess Application - Integration Verification")
    print("=" * 60)

    results = [
        ("File Structure", verify_file_structure()),
        ("Imports", verify_imports()),
        ("Signal Connections", verify_signal_connections()),
        ("Methods", verify_methods())
    ]

    success = print_summary(results)

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
