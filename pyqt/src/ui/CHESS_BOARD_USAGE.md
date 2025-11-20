# ChessBoardWidget Usage Guide

## Overview

The `ChessBoardWidget` is a professional, hardware-accelerated chess board component for PyQt6 applications. It features drag & drop piece movement, smooth animations, legal move highlighting, and a modern pink/black color scheme.

## Architecture

### Class Hierarchy

```
ChessBoardWidget (QGraphicsView)
  └── ChessBoardScene (QGraphicsScene)
       ├── ChessSquareItem (QGraphicsRectItem) × 64
       └── ChessPieceItem (QGraphicsPixmapItem) × pieces
```

### Key Features

- **Hardware-Accelerated Rendering**: Uses `QGraphicsView` with anti-aliasing
- **Drag & Drop**: Full support for dragging pieces with mouse
- **Click-to-Move**: Click a piece to select, click destination to move
- **Legal Move Highlighting**: Visual feedback for valid moves
- **Smooth Animations**: `QPropertyAnimation` for piece movement
- **Last Move Highlighting**: Shows the previous move
- **Modern Design**: Pink/black color scheme with smooth rendering

## Basic Usage

### 1. Simple Integration

```python
from PyQt6.QtWidgets import QApplication, QMainWindow
from chess_board import ChessBoardWidget
from game import Board

app = QApplication([])
window = QMainWindow()

# Create board and widget
board = Board()
chess_widget = ChessBoardWidget()

# Set initial board state
chess_widget.set_board_state(board)

# Add to window
window.setCentralWidget(chess_widget)
window.show()
app.exec()
```

### 2. Handling Moves

```python
def on_move_attempted(from_pos, to_pos):
    """Handle when user attempts a move"""
    # Get piece at from_pos
    piece = board.state[from_pos[0]][from_pos[1]]

    # Verify it's the right player's turn
    if piece and piece.color == board.to_move:
        # Get legal moves
        legal_moves = board.get_legal_moves(from_pos)

        # Find matching move
        for move in legal_moves:
            if move["to"] == to_pos:
                # Make the move
                board.move(from_pos, move)

                # Animate it
                chess_widget.animate_move(from_pos, to_pos, duration_ms=300)

                # Update display
                chess_widget.set_board_state(board)
                chess_widget.set_last_move(from_pos, to_pos)
                break

# Connect signal
chess_widget.moveAttempted.connect(on_move_attempted)
```

### 3. Highlighting Legal Moves

```python
def on_piece_selected(pos):
    """Show legal moves when piece is selected"""
    row, col = pos
    piece = board.state[row][col]

    if piece and piece.color == board.to_move:
        # Get legal moves
        legal_moves = board.get_legal_moves(pos)

        # Extract destination positions
        destinations = [move["to"] for move in legal_moves]

        # Highlight them
        chess_widget.set_legal_moves(destinations)

# Connect signal
chess_widget.pieceSelected.connect(on_piece_selected)
```

## API Reference

### ChessBoardWidget

Main widget class - subclass of `QGraphicsView`.

#### Methods

**`set_board_state(board: Board)`**
- Updates the visual display from a `game.Board` object
- Removes old pieces and adds new ones based on board state
- Call this after making moves on the board

**`highlight_squares(positions: List[Tuple[int, int]], color: QColor)`**
- Highlights specified squares with a given color
- `positions`: List of (row, col) tuples
- `color`: QColor for the highlight

**`clear_highlights()`**
- Removes all highlighting except last move
- Called automatically when new piece is selected

**`animate_move(from_pos: Tuple[int, int], to_pos: Tuple[int, int], duration_ms: int = 300)`**
- Smoothly animates piece movement
- `from_pos`: Starting (row, col)
- `to_pos`: Ending (row, col)
- `duration_ms`: Animation duration in milliseconds

**`set_last_move(from_pos: Tuple[int, int], to_pos: Tuple[int, int])`**
- Highlights the squares of the last move with orange color
- Persists across other highlighting operations

**`set_legal_moves(moves: List[Tuple[int, int]])`**
- Convenience method to highlight legal moves in green
- Equivalent to `highlight_squares(moves, LEGAL_MOVE_COLOR)`

#### Signals

**`moveAttempted(from_pos: tuple, to_pos: tuple)`**
- Emitted when user attempts to move a piece (either drag or click)
- `from_pos`: (row, col) starting position
- `to_pos`: (row, col) ending position
- You must validate and execute the move in your handler

**`pieceSelected(pos: tuple)`**
- Emitted when user clicks/presses a piece
- `pos`: (row, col) of the selected piece
- Use this to show legal moves

**`squareClicked(pos: tuple)`**
- Emitted when user clicks an empty square
- `pos`: (row, col) of the clicked square

### Color Constants

You can customize colors by modifying these constants in `chess_board.py`:

```python
LIGHT_SQUARE = QColor(255, 182, 193)      # Light pink
DARK_SQUARE = QColor(219, 112, 147)       # Pale violet red
HIGHLIGHT_COLOR = QColor(255, 255, 0, 120)  # Yellow highlight
LEGAL_MOVE_COLOR = QColor(50, 205, 50, 100)  # Green for legal moves
LAST_MOVE_COLOR = QColor(255, 165, 0, 100)  # Orange for last move
SELECTED_COLOR = QColor(255, 215, 0, 150)   # Gold for selected piece
```

### Board Dimensions

```python
SQUARE_SIZE = 70      # Size of each square in pixels
BOARD_SIZE = 8        # 8x8 board
BOARD_WIDTH = 560     # Total board width (70 * 8)
```

## Advanced Usage

### Custom Animation Timing

```python
# Fast moves
chess_widget.animate_move(from_pos, to_pos, duration_ms=150)

# Slow, dramatic moves
chess_widget.animate_move(from_pos, to_pos, duration_ms=800)
```

### Multiple Highlight Types

```python
# Highlight selected square in gold
chess_widget.highlight_squares([selected_pos], SELECTED_COLOR)

# Highlight legal moves in green
chess_widget.highlight_squares(legal_moves, LEGAL_MOVE_COLOR)

# Highlight attacked squares in red
chess_widget.highlight_squares(attacked, QColor(255, 0, 0, 100))
```

### Handling Promotions

```python
def on_move_attempted(from_pos, to_pos):
    # ... validate move ...

    # Check if pawn promotion
    piece = board.state[from_pos[0]][from_pos[1]]
    if piece.type == "pawn":
        if (piece.color == "white" and to_pos[0] == 0) or \
           (piece.color == "black" and to_pos[0] == 7):
            # Show promotion dialog
            promotion_piece = show_promotion_dialog()
            # Handle promotion...

    # Make move and animate
    board.move(from_pos, move)
    chess_widget.animate_move(from_pos, to_pos)
    chess_widget.set_board_state(board)
```

### Disabling Interaction

```python
# Disable all piece movement (for AI thinking or game over)
for piece in chess_widget.board_scene.pieces.values():
    piece.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable, False)

# Re-enable
for piece in chess_widget.board_scene.pieces.values():
    piece.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable, True)
```

## Integration with Game Logic

### Complete Game Loop

```python
class ChessGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.board = Board()
        self.chess_widget = ChessBoardWidget()

        # Connect signals
        self.chess_widget.moveAttempted.connect(self.handle_move)
        self.chess_widget.pieceSelected.connect(self.show_legal_moves)

        # Initialize
        self.chess_widget.set_board_state(self.board)
        self.setCentralWidget(self.chess_widget)

    def handle_move(self, from_pos, to_pos):
        """Process and validate moves"""
        piece = self.board.state[from_pos[0]][from_pos[1]]

        # Validate turn
        if not piece or piece.color != self.board.to_move:
            return

        # Get and validate legal moves
        legal_moves = self.board.get_legal_moves(from_pos)
        move = next((m for m in legal_moves if m["to"] == to_pos), None)

        if move:
            # Execute move
            self.board.move(from_pos, move)

            # Animate
            self.chess_widget.animate_move(from_pos, to_pos)

            # Update display
            self.chess_widget.set_board_state(self.board)
            self.chess_widget.set_last_move(from_pos, to_pos)

            # Check game state
            if self.board.game_over:
                self.show_game_over_dialog(self.board.game_result)

    def show_legal_moves(self, pos):
        """Highlight legal moves for selected piece"""
        piece = self.board.state[pos[0]][pos[1]]

        if piece and piece.color == self.board.to_move:
            legal_moves = self.board.get_legal_moves(pos)
            destinations = [m["to"] for m in legal_moves]
            self.chess_widget.set_legal_moves(destinations)
```

## File Structure

```
pyqt/
├── src/
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── chess_board.py           # Main widget
│   │   ├── chess_board_example.py   # Usage example
│   │   └── CHESS_BOARD_USAGE.md     # This file
│   └── game/
│       └── __init__.py               # Board class
└── assets/
    └── images/
        ├── white/
        │   ├── king.png
        │   ├── queen.png
        │   ├── rook.png
        │   ├── bishop.png
        │   ├── knight.png
        │   └── pawn.png
        └── black/
            ├── king.png
            ├── queen.png
            ├── rook.png
            ├── bishop.png
            ├── knight.png
            └── pawn.png
```

## Running the Example

```bash
cd /home/user/Chess/pyqt
python3 src/ui/chess_board_example.py
```

## Troubleshooting

### Pieces Not Showing

- Verify image paths: `../../assets/images/white/king.png` etc.
- Check that PNG files exist in assets directory
- Ensure file permissions allow reading

### Drag Not Working

- Verify `ItemIsMovable` flag is set on pieces
- Check that scene reference is set: `piece.scene_ref = self`
- Ensure view is not read-only

### Animations Not Smooth

- Enable anti-aliasing: `setRenderHint(QPainter.RenderHint.Antialiasing)`
- Use `SmoothTransformation` mode for pixmaps
- Reduce animation duration if system is slow

### Highlights Not Showing

- Check Z-order: squares should be behind pieces
- Verify alpha channel in color: `QColor(r, g, b, alpha)`
- Call `clear_highlights()` before new highlights

## Performance Tips

1. **Reuse Animations**: Store animation objects to prevent recreation
2. **Batch Updates**: Call `set_board_state()` once after multiple changes
3. **Optimize Images**: Use pre-scaled PNG files at 60x60 pixels
4. **Scene Rect**: Keep scene rect fixed to prevent recalculation
5. **View Updates**: Use `setViewportUpdateMode()` for better performance

## License

This chess board widget is part of the Chess project.
