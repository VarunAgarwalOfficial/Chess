# ChessBoardWidget - Quick Reference Card

## Import

```python
from ui.chess_board import ChessBoardWidget
from game import Board
```

## Basic Setup

```python
# Create widget
chess_widget = ChessBoardWidget()

# Create game
board = Board()

# Initialize display
chess_widget.set_board_state(board)
```

## Handle Moves

```python
def on_move(from_pos, to_pos):
    # Validate and execute
    legal_moves = board.get_legal_moves(from_pos)
    for move in legal_moves:
        if move["to"] == to_pos:
            board.move(from_pos, move)
            chess_widget.animate_move(from_pos, to_pos)
            chess_widget.set_board_state(board)
            chess_widget.set_last_move(from_pos, to_pos)
            break

chess_widget.moveAttempted.connect(on_move)
```

## Show Legal Moves

```python
def on_select(pos):
    piece = board.state[pos[0]][pos[1]]
    if piece and piece.color == board.to_move:
        legal_moves = board.get_legal_moves(pos)
        destinations = [m["to"] for m in legal_moves]
        chess_widget.set_legal_moves(destinations)

chess_widget.pieceSelected.connect(on_select)
```

## Signals

| Signal | When Emitted | Parameters |
|--------|-------------|------------|
| `moveAttempted` | User drags or clicks to move | `(from_pos, to_pos)` |
| `pieceSelected` | User clicks/presses a piece | `(pos)` |
| `squareClicked` | User clicks empty square | `(pos)` |

Where `pos` and positions are `(row, col)` tuples (0-7).

## Methods

| Method | Description | Example |
|--------|-------------|---------|
| `set_board_state(board)` | Update display from Board | `chess_widget.set_board_state(board)` |
| `animate_move(from, to, ms)` | Animate piece movement | `chess_widget.animate_move((6,4), (4,4), 300)` |
| `set_last_move(from, to)` | Highlight last move | `chess_widget.set_last_move((7,4), (7,6))` |
| `set_legal_moves(list)` | Highlight legal moves | `chess_widget.set_legal_moves([(5,4), (4,4)])` |
| `highlight_squares(list, color)` | Custom highlighting | `chess_widget.highlight_squares([(3,3)], red)` |
| `clear_highlights()` | Remove highlights | `chess_widget.clear_highlights()` |

## Color Constants

```python
from chess_board import (
    LIGHT_SQUARE,      # QColor(255, 182, 193) - Light pink
    DARK_SQUARE,       # QColor(219, 112, 147) - Pale violet red
    LEGAL_MOVE_COLOR,  # QColor(50, 205, 50, 100) - Green
    LAST_MOVE_COLOR,   # QColor(255, 165, 0, 100) - Orange
    SELECTED_COLOR,    # QColor(255, 215, 0, 150) - Gold
)
```

## Board Coordinates

```
   0   1   2   3   4   5   6   7  (cols)
0  ♜  ♞  ♝  ♛  ♚  ♝  ♞  ♜
1  ♟  ♟  ♟  ♟  ♟  ♟  ♟  ♟
2  ·  ·  ·  ·  ·  ·  ·  ·
3  ·  ·  ·  ·  ·  ·  ·  ·
4  ·  ·  ·  ·  ·  ·  ·  ·
5  ·  ·  ·  ·  ·  ·  ·  ·
6  ♙  ♙  ♙  ♙  ♙  ♙  ♙  ♙
7  ♖  ♘  ♗  ♕  ♔  ♗  ♘  ♖
(rows)

Top-left = (0,0) = Black rook
Bottom-right = (7,7) = White rook
```

## Complete Example

```python
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.chess_board import ChessBoardWidget
from game import Board

app = QApplication([])
window = QMainWindow()
board = Board()
chess = ChessBoardWidget()

def handle_move(from_pos, to_pos):
    piece = board.state[from_pos[0]][from_pos[1]]
    if piece and piece.color == board.to_move:
        moves = board.get_legal_moves(from_pos)
        for m in moves:
            if m["to"] == to_pos:
                board.move(from_pos, m)
                chess.animate_move(from_pos, to_pos)
                chess.set_board_state(board)
                chess.set_last_move(from_pos, to_pos)
                return

def show_moves(pos):
    piece = board.state[pos[0]][pos[1]]
    if piece and piece.color == board.to_move:
        moves = board.get_legal_moves(pos)
        chess.set_legal_moves([m["to"] for m in moves])

chess.moveAttempted.connect(handle_move)
chess.pieceSelected.connect(show_moves)
chess.set_board_state(board)

window.setCentralWidget(chess)
window.show()
app.exec()
```

## Asset Paths

```
pyqt/assets/images/
  white/  [king, queen, rook, bishop, knight, pawn].png
  black/  [king, queen, rook, bishop, knight, pawn].png
```

## Piece Properties

```python
piece = board.state[row][col]  # or None
piece.color  # "white" or "black"
piece.type   # "king", "queen", "rook", "bishop", "knight", "pawn"
```

## Common Patterns

### Undo Move
```python
if board.move_log:
    board.undo()
    chess.set_board_state(board)
    chess.clear_highlights()
```

### Reset Game
```python
board = Board()
chess.set_board_state(board)
chess.clear_highlights()
```

### Check Game State
```python
if board.check:
    print("Check!")
if board.game_over:
    print(f"Game over: {board.game_result}")
```

### Disable Interaction
```python
for piece in chess.board_scene.pieces.values():
    piece.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable, False)
```

## Dimensions

- **Square Size**: 70 pixels
- **Board Size**: 560x560 pixels (8×8 squares)
- **Piece Size**: ~60 pixels (85% of square size)
- **Fixed Size**: Widget is 562x562 (board + 2px border)

## Animation Timing

```python
chess.animate_move(from_pos, to_pos, 150)   # Fast
chess.animate_move(from_pos, to_pos, 300)   # Normal (default)
chess.animate_move(from_pos, to_pos, 600)   # Slow
```

## Tips

1. Always call `set_board_state()` after moves to sync display
2. Use `animate_move()` BEFORE `set_board_state()` for smooth animation
3. Connect `pieceSelected` signal to show legal moves for better UX
4. Use `set_last_move()` to help users track the game flow
5. Check `piece.color == board.to_move` before allowing moves

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Pieces not showing | Check asset paths, verify PNG files exist |
| Can't drag pieces | Ensure `ItemIsMovable` flag is set |
| No highlights | Call with alpha channel: `QColor(r,g,b,alpha)` |
| Moves not working | Validate with `board.get_legal_moves()` |

## Running Example

```bash
cd /home/user/Chess/pyqt
python3 src/ui/chess_board_example.py
```

---

**Documentation**: See `CHESS_BOARD_USAGE.md` for full API reference

**Implementation**: See `IMPLEMENTATION_SUMMARY.md` for architecture details
