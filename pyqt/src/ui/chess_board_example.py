"""
Example usage of the ChessBoardWidget

This demonstrates how to use the professional chess board widget with
the game.Board class, including handling moves, legal move highlighting,
and animations.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from chess_board import ChessBoardWidget
import sys
import os

# Add parent directory to path to import game module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from game import Board


class ChessGameWindow(QMainWindow):
    """Example chess game window using ChessBoardWidget"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Chess Board Example")

        # Create game board
        self.board = Board()

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create chess board widget
        self.chess_board = ChessBoardWidget()
        layout.addWidget(self.chess_board, alignment=Qt.AlignmentFlag.AlignCenter)

        # Connect signals
        self.chess_board.moveAttempted.connect(self.on_move_attempted)
        self.chess_board.pieceSelected.connect(self.on_piece_selected)
        self.chess_board.squareClicked.connect(self.on_square_clicked)

        # Add control buttons
        button_layout = QHBoxLayout()

        reset_button = QPushButton("Reset Board")
        reset_button.clicked.connect(self.reset_game)
        button_layout.addWidget(reset_button)

        undo_button = QPushButton("Undo Move")
        undo_button.clicked.connect(self.undo_move)
        button_layout.addWidget(undo_button)

        layout.addLayout(button_layout)

        # Initialize board display
        self.chess_board.set_board_state(self.board)

        # Track selected piece for legal moves
        self.selected_position = None

    def on_piece_selected(self, pos):
        """Handle piece selection - show legal moves"""
        row, col = pos
        piece = self.board.state[row][col]

        if piece and piece.color == self.board.to_move:
            self.selected_position = pos

            # Get legal moves for this piece
            legal_moves = self.board.get_legal_moves(pos)

            # Extract destination positions
            move_positions = [move["to"] for move in legal_moves]

            # Highlight legal moves
            self.chess_board.set_legal_moves(move_positions)

            print(f"Selected {piece.color} {piece.type} at {pos}")
            print(f"Legal moves: {move_positions}")
        else:
            self.selected_position = None
            self.chess_board.clear_highlights()

    def on_square_clicked(self, pos):
        """Handle square click"""
        print(f"Square clicked: {pos}")

    def on_move_attempted(self, from_pos, to_pos):
        """Handle move attempt"""
        print(f"Move attempted: {from_pos} -> {to_pos}")

        # Get piece at from position
        piece = self.board.state[from_pos[0]][from_pos[1]]
        if not piece or piece.color != self.board.to_move:
            print("Not your piece!")
            self.chess_board.set_board_state(self.board)
            return

        # Get legal moves for this piece
        legal_moves = self.board.get_legal_moves(from_pos)

        # Check if this move is legal
        matching_move = None
        for move in legal_moves:
            if move["to"] == to_pos:
                matching_move = move
                break

        if matching_move:
            # Make the move
            self.board.move(from_pos, matching_move)

            # Animate the move
            self.chess_board.animate_move(from_pos, to_pos, duration_ms=250)

            # Update board state after animation
            # (In production, you'd wait for animation to finish)
            import time
            QApplication.processEvents()
            time.sleep(0.3)

            self.chess_board.set_board_state(self.board)
            self.chess_board.set_last_move(from_pos, to_pos)

            print(f"Move made: {piece.color} {piece.type} from {from_pos} to {to_pos}")
            print(f"Next to move: {self.board.to_move}")

            if self.board.check:
                print("CHECK!")
            if self.board.game_over:
                print(f"GAME OVER: {self.board.game_result}")
        else:
            print("Illegal move!")
            # Reset board display
            self.chess_board.set_board_state(self.board)

        # Clear highlights
        self.chess_board.clear_highlights()
        self.selected_position = None

    def reset_game(self):
        """Reset the game to starting position"""
        self.board = Board()
        self.chess_board.set_board_state(self.board)
        self.chess_board.clear_highlights()
        self.selected_position = None
        print("Game reset!")

    def undo_move(self):
        """Undo the last move"""
        if self.board.move_log:
            self.board.undo()
            self.chess_board.set_board_state(self.board)
            self.chess_board.clear_highlights()
            self.selected_position = None
            print("Move undone!")
        else:
            print("No moves to undo!")


def main():
    """Run the example application"""
    app = QApplication(sys.argv)
    window = ChessGameWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
