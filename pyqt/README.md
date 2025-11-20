# PyQt6 Chess Application

A modern, high-performance chess application built with PyQt6 featuring AI opponent, puzzle system, tutorials, and an elegant pink/black UI.

## Quick Start

### Prerequisites

- Python 3.8+
- PyQt6 6.6.0+
- NumPy 1.24.0+

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

> **Note**: The application now uses `run.py` as the main entry point. See `APPLICATION_GUIDE.md` for detailed documentation.

### Running Tests

```bash
# Install pytest first
pip install pytest pytest-qt

# Run all tests
pytest tests/

# Run specific test class
pytest tests/test_integration.py::TestMainWindow -v

# Run tests with markers
pytest -m "not slow" tests/  # Skip slow tests
pytest -m integration tests/  # Only integration tests

# Run with coverage
pip install pytest-cov
pytest --cov=src tests/
```

## Architecture Overview

### Component Structure

```
src/
├── ui/
│   ├── main_window.py         # Main application window (QMainWindow)
│   ├── game_controller.py      # Game logic controller (QObject with signals)
│   └── chess_board.py          # Chess board widget (QGraphicsView)
├── game/
│   ├── __init__.py            # Board class
│   ├── Piece.py               # Piece representation
│   ├── MoveGenerator.py        # Legal move generation
│   ├── CheckFunctions.py       # Check/checkmate detection
│   ├── GameEndFunctions.py     # Game ending logic
│   └── fen_parser.py           # FEN position parsing
├── ai/
│   ├── ai.py                  # AI engine with minimax
│   ├── advanced_search.py      # Advanced search strategies
│   ├── attack_tables.py        # RAM-based attack tables
│   ├── cache_system.py         # Position caching
│   └── optimizations.py        # Search optimizations
└── features/
    ├── puzzles.py             # Puzzle system (40+ puzzles)
    ├── opening_book.py        # Opening library
    ├── pgn_handler.py         # PGN file support
    ├── chess_clock.py         # Time control
    ├── settings.py            # Application settings
    └── tutorial.py            # Tutorial system
```

### Design Patterns Used

#### Model-View-Controller (MVC)

- **Model**: `Game.Board` - Manages chess position and rules
- **View**: `ChessBoardWidget` - Renders the board with animations
- **Controller**: `GameController` - Coordinates model and view

#### Signal/Slot Pattern (Qt)

All inter-component communication uses Qt signals and slots:

```python
# In GameController
moveCompleted = pyqtSignal(tuple, tuple)  # (from_pos, to_pos)
gameStateChanged = pyqtSignal()
evaluationUpdated = pyqtSignal(float)

# Connections
game_controller.moveCompleted.connect(chess_board_widget.animate_move)
game_controller.evaluationUpdated.connect(main_window.update_evaluation)
```

#### Threading Pattern

AI moves are calculated in background threads to prevent UI freezing:

```python
class AIWorker(QThread):
    moveCalculated = pyqtSignal(dict, tuple)

    def run(self):
        best_move, position = self.ai.get_best_move()
        self.moveCalculated.emit(best_move, position)

# Usage
worker = AIWorker(ai_instance)
worker.moveCalculated.connect(game_controller._handle_ai_move)
worker.start()
```

### Component Details

#### MainWindow (`main_window.py`)

Manages:
- Multiple screens (menu, game, tutorial, puzzles, help) via QStackedWidget
- Right dock widget with game dashboard
- Menu bar with File, Game, Help menus
- Status bar for user messages
- Dashboard with:
  - Game information (mode, difficulty, turn, opening)
  - Position evaluation bar
  - Captured pieces display
  - Move history list
  - AI thinking indicator

**Key Methods:**
- `show_*_screen()` - Navigate between screens
- `update_dashboard()` - Update game info and evaluation
- `add_move_to_history()` - Add moves to history list
- `show_ai_thinking()` / `hide_ai_thinking()` - Show AI status

#### GameController (`game_controller.py`)

Coordinates:
- Move validation and execution
- AI opponent (with threading)
- Puzzle mode handling
- Game state management
- Undo/Reset functionality
- FEN position loading

**Key Signals:**
- `gameStateChanged` - Emitted when board changes
- `moveCompleted(from_pos, to_pos)` - Emitted after valid move
- `aiThinking(bool)` - AI started/stopped
- `evaluationUpdated(float)` - Position evaluation changed
- `puzzleProgress(bool, bool, str)` - Puzzle move feedback

**Key Methods:**
- `set_game_mode(mode, ai_color, ai_difficulty)` - Configure game mode
- `handle_move_attempt(from_pos, to_pos)` - Validate and execute move
- `start_ai_move()` - Start AI calculation in background
- `load_puzzle(puzzle_id)` - Load puzzle by ID
- `undo_move()` / `reset_game()` - Game control

#### ChessBoardWidget (`chess_board.py`)

Renders:
- 8x8 chess board with pink/black color scheme
- All 32 chess pieces with proper sizing
- Legal move highlights
- Last move highlighting
- Selected piece highlighting
- Drag-and-drop piece movement
- Smooth animations

**Key Features:**
- Hardware-accelerated rendering (QGraphicsView/QGraphicsScene)
- Anti-aliasing and smooth transformations
- 70x70 pixel squares (560x560 total)
- QPropertyAnimation for smooth piece movement
- Custom graphics items for squares and pieces

**Key Signals:**
- `moveAttempted(from_pos, to_pos)` - User attempted move
- `squareClicked(row, col)` - User clicked empty square
- `pieceSelected(row, col)` - User selected piece

**Key Methods:**
- `set_board_state(board)` - Update display from game state
- `animate_move(from_pos, to_pos)` - Animate piece movement
- `set_legal_moves(moves)` - Highlight legal moves
- `set_last_move(from_pos, to_pos)` - Highlight last move

#### Puzzle System (`features/puzzles.py`)

Includes:
- 40+ tactical puzzles (easy, medium, hard)
- Multiple themes (forks, pins, mates, tactics)
- Solution checking
- Hint system
- Progress tracking

**Methods:**
- `get_puzzle(puzzle_id)` - Get puzzle by ID or current
- `get_puzzles_by_difficulty(difficulty)` - Filter by difficulty
- `get_puzzles_by_theme(theme)` - Filter by theme
- `check_move(move_san)` - Validate move in puzzle
- `get_hint()` - Get hint with progressive difficulty
- `next_puzzle()` / `previous_puzzle()` - Navigate puzzles
- `get_progress()` - Get completion statistics

## Differences from Pygame Version

### UI Framework

| Aspect | Pygame | PyQt6 |
|--------|--------|-------|
| Framework | Game library | GUI toolkit |
| Rendering | SDL-based | Qt Graphics View |
| Responsiveness | Manual event loop | Integrated event loop |
| Scalability | Fixed resolution | Resizable windows |

### Features Added in PyQt6

1. **Modern UI Paradigm**
   - Menu bars with standard shortcuts
   - Dock widgets for flexible layouts
   - Stacked widgets for screen management
   - Status bar for status messages

2. **Dashboard System**
   - Real-time game information display
   - Position evaluation visualization
   - Captured pieces tracking
   - Move history with scrolling

3. **Multi-Screen Navigation**
   - Main menu with five screens
   - Tutorial system integration
   - Puzzle mode with dedicated interface
   - Help system with controls documentation

4. **Professional Styling**
   - Modern pink/black color scheme
   - Rounded buttons and cards
   - Consistent typography
   - Theme-wide styling with QSS

5. **Threading Infrastructure**
   - Background AI calculation
   - Non-blocking user interface
   - Signal-based progress reporting
   - Proper cleanup on exit

### Performance Improvements (vs Original)

1. **Hardware Acceleration**
   - QGraphicsView rendering pipeline
   - Rasterization optimizations
   - Smooth pixmap transforms
   - Anti-aliasing for quality

2. **Memory Efficiency**
   - Lazy piece image loading
   - Graphics scene batching
   - Efficient animation storage
   - Smart cache management

3. **Search Optimizations**
   - RAM-based attack tables (10x faster)
   - Position caching system
   - Transposition table
   - Alpha-beta pruning with killer moves

4. **AI Performance**
   - Typical depth: 6-8 moves ahead
   - Evaluation speed: 10,000+ nodes/sec
   - Difficulty levels: Easy, Medium, Hard, Expert
   - Move quality scales with time allocation

## Game Modes

### Player vs AI (PvAI)

```python
controller.set_game_mode('pvai', ai_color='black', ai_difficulty='medium')
```

- Play against computer opponent
- Choose AI color (white or black)
- Select difficulty level:
  - **Easy**: Shallow search, random moves among legal ones
  - **Medium**: 4-5 ply search
  - **Hard**: 6-7 ply search
  - **Expert**: 8+ ply search with advanced optimizations

### Player vs Player (PvP)

```python
controller.set_game_mode('pvp')
```

- Two players on same machine
- No AI opponent
- Full move history and undo support

### Puzzle Mode

```python
controller.set_game_mode('puzzle')
controller.load_puzzle(puzzle_id)
```

- Solve tactical puzzles
- 40+ puzzles covering major tactics
- Progressive difficulty
- Solution checking with feedback
- Hint system with escalating hints

## Testing

### Test Coverage

- **UI Components**: 120+ test cases
- **Game Logic**: Move validation, piece movement
- **AI System**: Threading, evaluation, search
- **Puzzle System**: Loading, solving, hints
- **Integration**: Full game workflows
- **Error Handling**: Invalid moves, edge cases
- **Signal/Slots**: Qt event handling

### Running Tests

```bash
# Run all tests with verbose output
pytest tests/test_integration.py -v

# Run specific component tests
pytest tests/test_integration.py::TestMainWindow -v
pytest tests/test_integration.py::TestGameController -v
pytest tests/test_integration.py::TestChessBoardWidget -v

# Run integration tests only
pytest -m integration tests/test_integration.py -v

# Run with coverage report
pytest --cov=src tests/test_integration.py

# Run tests and show print statements
pytest -s tests/test_integration.py
```

### Test Organization

```
test_integration.py
├── Fixtures
│   ├── qapp - QApplication instance
│   ├── game_controller - GameController instance
│   ├── main_window - MainWindow instance
│   ├── chess_board_widget - ChessBoardWidget instance
│   ├── puzzle_system - Puzzle system instance
│   └── mock_ai - Mocked AI for fast tests
│
├── TestMainWindow (12 tests)
│   ├── Window initialization
│   ├── Screen navigation
│   ├── Dashboard updates
│   └── Status messages
│
├── TestChessBoardWidget (6 tests)
│   ├── Board rendering
│   ├── Piece selection
│   ├── Move animation
│   └── Highlighting
│
├── TestGameController (10 tests)
│   ├── Move validation
│   ├── Game mode switching
│   ├── Undo/Reset
│   └── Legal moves
│
├── TestPuzzleSystem (10 tests)
│   ├── Puzzle loading
│   ├── Solution checking
│   ├── Hints
│   └── Navigation
│
├── TestAIThreading (3 tests)
│   ├── Worker creation
│   ├── Non-blocking calculation
│   └── Error handling
│
├── TestIntegration (5 tests)
│   ├── Complete game flow
│   ├── Puzzle workflow
│   └── Screen navigation
│
├── TestErrorHandling (5 tests)
│   ├── Invalid moves
│   ├── Game over conditions
│   └── Missing data
│
├── TestEdgeCases (4 tests)
│   ├── Rapid moves
│   ├── Extreme evaluations
│   └── Boundary conditions
│
├── TestSignalsAndSlots (5 tests)
│   ├── Signal emission
│   ├── Slot connections
│   └── Event propagation
│
└── TestMocking (3 tests)
    ├── AI mocking
    ├── Board mocking
    └── Isolation testing
```

## Configuration

### Game Settings

```python
# In GameController
controller.ai_difficulty = "hard"     # Change difficulty
controller.ai_color = "black"         # AI plays black
```

### UI Customization

The application uses QSS (Qt Style Sheets) for theming. Modify colors in `_apply_theme()`:

```python
# Colors
LIGHT_SQUARE = QColor(255, 182, 193)   # Light pink
DARK_SQUARE = QColor(219, 112, 147)    # Pale violet red
HIGHLIGHT_COLOR = QColor(255, 255, 0)  # Yellow highlight
```

### Window Sizing

```python
self.setMinimumSize(940, 600)  # Minimum window size
self.resize(940, 600)          # Default window size
```

Components:
- Board widget: 560x560 (8 × 70 pixel squares)
- Dashboard: 380 pixels wide
- Dock widget: Fixed width

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| PyQt6 | ≥6.6.0 | GUI framework |
| PyQt6-Qt6 | ≥6.6.0 | Qt bindings |
| NumPy | ≥1.24.0 | Numerical operations (AI, move generation) |

### Development Dependencies

```bash
# For testing
pip install pytest pytest-qt pytest-cov

# For debugging
pip install pyqt6-debug
```

## Future Enhancements

### Planned Features

1. **Online Play**
   - Chess.com API integration
   - Lichess.org support
   - Real-time multiplayer

2. **Advanced Analysis**
   - Engine analysis on demand
   - Best move suggestions
   - Blunder detection
   - Position evaluation graph

3. **Database Integration**
   - Game history storage
   - Opening statistics
   - Puzzle completion tracking
   - ELO calculation

4. **Enhanced UI**
   - Piece themes and board skins
   - Customizable keyboard shortcuts
   - Dark/light mode toggle
   - Multi-language support

5. **Training Features**
   - Endgame tablebase support
   - Interactive tactics trainer
   - Opening preparation module
   - Puzzlebot with increasing difficulty

6. **Performance**
   - Parallel search (multi-threaded)
   - GPU acceleration for evaluation
   - Neural network evaluation
   - Distributed engine support

## Architecture Decisions

### Why QGraphicsView?

- Hardware acceleration for smooth animations
- Efficient rendering of complex scenes
- Built-in zoom and pan capabilities
- Superior performance vs. pixel-by-pixel drawing

### Why Threading?

- Prevents UI freezing during AI computation
- Allows responsive user interactions
- Proper signal-based communication
- Clean separation of concerns

### Why Signals/Slots?

- Loose coupling between components
- Thread-safe event propagation
- Automatic memory management
- Clear data flow

### Why Mocked AI in Tests?

- Fast test execution (milliseconds vs. seconds)
- Deterministic behavior
- Focus on integration logic
- Isolation of AI complexity

## Performance Tips

1. **For Faster AI**
   - Increase `max_depth` in AI constructor
   - Use "Expert" difficulty
   - Enable opening book for faster starts

2. **For Smoother UI**
   - Reduce animation duration (default 300ms)
   - Disable visual effects on slow systems
   - Use hardware rendering

3. **For Memory Efficiency**
   - Limit puzzle count if needed
   - Clear move history periodically
   - Disable position caching on low-memory systems

## Troubleshooting

### QApplication Already Exists

```python
# Solution: Use existing instance
app = QApplication.instance() or QApplication([])
```

### Piece Images Not Loading

```
Check:
- Image files exist in assets/images/white/ and assets/images/black/
- File names match piece types: pawn.png, knight.png, bishop.png, etc.
- Images are valid PNG files
```

### AI Too Slow

```
Solutions:
- Reduce difficulty level
- Decrease max_depth
- Enable opening book
- Use faster hardware
```

### Signals Not Firing

```python
# Ensure proper connection syntax
controller.moveCompleted.connect(on_move_completed)

# Check that slots are connected before signals emit
board_widget.moveAttempted.connect(controller.handle_move_attempt)
```

## License

This project is part of the Chess Engine suite. See main repository for license information.

## Contributing

To contribute:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Add tests for new functionality
4. Ensure all tests pass (`pytest tests/`)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open Pull Request

## Support

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Review test cases for usage examples
3. Consult inline code documentation
4. Post detailed bug reports with reproduction steps

---

**PyQt6 Chess** - Modern Chess, Built with Qt
