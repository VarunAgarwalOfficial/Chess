# Chess Game - Python Edition

A fully-featured chess game implementation in Python with an advanced computer opponent, comprehensive game rules, and a modern user interface.

![Chess Game](screenshots/chess_screenshot.png)

## Features

### Complete Chess Rules
- [x] All standard piece movements (pawns, rooks, knights, bishops, queens, kings)
- [x] Special moves:
  - **Castling** (king-side and queen-side)
  - **En Passant** capture
  - **Pawn Promotion** to queen
- [x] Check and checkmate detection
- [x] Stalemate detection
- [x] Draw conditions:
  - Insufficient material
  - Fifty-move rule
  - Threefold repetition

### Advanced Computer Opponent
- Multiple difficulty levels: Easy, Medium, Hard
- **Minimax algorithm with Alpha-Beta pruning** for efficient move search
- **Piece-square tables** for positional evaluation
- **Move ordering (MVV-LVA)** for optimal pruning
- **Quiescence search** to avoid horizon effect
- **Iterative deepening** for better time management
- **Transposition table** for position caching
- **Real-time evaluation** showing position advantage

### Modern User Interface
- Clean, intuitive chessboard design
- **Dashboard** displaying:
  - Current turn indicator
  - Position evaluation bar
  - Move history in algebraic notation
  - Captured pieces
  - Current opening name
- Legal move highlighting
- Smooth piece selection and movement
- Multiple game modes:
  - Player vs Player
  - Player vs Computer (multiple difficulties)

### Opening Book
- Recognition of common chess openings:
  - Italian Game
  - Ruy Lopez
  - Sicilian Defense
  - French Defense
  - Caro-Kann Defense
  - Queen's Gambit
  - King's Indian Defense
  - English Opening

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Install Dependencies

```bash
pip install pygame numpy
```

## Running the Game

```bash
python3 __init__.py
```

Or:

```bash
python -m Chess
```

## How to Play

### Starting a Game
1. Run the game executable
2. Select your preferred game mode:
   - **Player vs Player**: Play against another human
   - **Player vs Computer**: Challenge the computer opponent (select difficulty)

### Making Moves
1. **Click** on a piece to select it (must be your turn)
2. **Legal moves** will be highlighted:
   - Blue = normal move
   - Green = capture
3. **Click** on a highlighted square to move
4. **Click** the selected piece again to deselect

### Keyboard Controls
- **Z**: Undo last move
- **R**: Return to main menu / Restart game
- **ESC**: Quit game

## Game Modes

### Player vs Player
Classic chess where two players take turns on the same computer.

### Player vs Computer
Challenge the computer opponent with three difficulty levels:
- **Easy** (Depth 2): Suitable for beginners
- **Medium** (Depth 3): Balanced challenge
- **Hard** (Depth 4): Strong opponent for experienced players

## Technical Details

### Architecture
```
Chess/
├── __init__.py           # Main game loop and UI
├── Game/
│   ├── __init__.py       # Board class and game state
│   ├── Piece.py          # Piece data structure
│   ├── MoveGenerator.py  # Move generation for all pieces
│   ├── CheckFunctions.py # Check and pin detection
│   └── GameEndFunctions.py # Checkmate/stalemate detection
├── ai.py                 # Computer opponent engine
├── opening_book.py       # Opening recognition
├── tests.py              # Comprehensive test suite
└── images/               # Piece graphics
```

### Computer Opponent Implementation

The computer opponent uses several advanced algorithms:

#### 1. **Minimax with Alpha-Beta Pruning**
Searches the game tree to find the best move, using alpha-beta pruning to eliminate unnecessary branches and dramatically improve performance.

#### 2. **Evaluation Function**
Evaluates positions based on:
- **Material**: Piece values (pawn=100, knight=320, bishop=330, rook=500, queen=900)
- **Position**: Piece-square tables reward good piece placement
- **King Safety**: Encourages castling and keeping king safe in middlegame

#### 3. **Move Ordering**
Prioritizes moves for better pruning:
- Captures (sorted by MVV-LVA)
- Promotions
- Special moves (castling)

#### 4. **Quiescence Search**
Extends search in tactical positions to avoid the horizon effect, ensuring the engine doesn't miss obvious captures.

#### 5. **Transposition Table**
Caches previously evaluated positions to avoid redundant calculations.

## Testing

Run the comprehensive test suite:

```bash
python3 tests.py
```

Tests include:
- Checkmate detection (Fool's Mate)
- Stalemate detection
- Draw by insufficient material
- Computer opponent move generation
- Special moves (en passant, castling)
- Move undo functionality
- Evaluation function

## Performance

The computer opponent can search:
- **Easy**: ~1,000 positions in <0.1s
- **Medium**: ~10,000 positions in ~0.5s
- **Hard**: ~50,000 positions in ~2-3s

Performance varies based on position complexity.

## Future Enhancements

Potential improvements:
- [ ] Pawn promotion piece selection UI
- [ ] Time controls
- [ ] Save/load games (PGN format)
- [ ] Move highlighting (show last move)
- [ ] Sound effects
- [ ] Online multiplayer
- [ ] Chess engine UCI protocol support
- [ ] Opening book moves from database

## Credits

### Chess Piece Images
Chess piece graphics are used in accordance with standard chess piece designs.

### Algorithms
Implementation based on standard chess programming techniques:
- Minimax algorithm
- Alpha-beta pruning
- Piece-square tables
- Move ordering heuristics

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Development Setup

```bash
git clone https://github.com/yourusername/chess.git
cd chess
pip install -r requirements.txt
python3 tests.py  # Run tests
python3 __init__.py  # Run game
```

## Changelog

### Version 2.0 (Current)
- Added advanced computer opponent with multiple difficulty levels
- Implemented comprehensive dashboard with evaluation bar
- Added move history in algebraic notation
- Added captured pieces display
- Added opening book recognition
- Implemented all draw conditions
- Added comprehensive test suite
- Fixed castling rights bug
- Improved UI with better color scheme

### Version 1.0 (Initial)
- Basic chess rules implementation
- Check detection
- Special moves (castling, en passant, promotion)
- Simple GUI

---

**Enjoy playing chess!**
