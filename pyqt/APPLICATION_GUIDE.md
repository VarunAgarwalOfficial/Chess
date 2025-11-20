# PyQt6 Chess Application - Complete Integration Guide

## Overview

The PyQt6 Chess application is now fully integrated with two main entry files:

1. **`run.py`** - Simple, production-ready entry point
2. **`src/ui/app.py`** - Comprehensive application wrapper that manages all components

## File Structure

```
/home/user/Chess/pyqt/
├── run.py                          # Main entry point (NEW)
├── src/
│   ├── ui/
│   │   ├── app.py                  # Application wrapper (NEW)
│   │   ├── main_window.py          # Main window with screens
│   │   ├── game_controller.py      # Game logic controller
│   │   └── chess_board.py          # Interactive chess board widget
│   ├── game/                       # Game logic (Board, Piece, etc.)
│   ├── ai/                         # AI implementation
│   └── features/                   # Puzzles, tutorials, etc.
├── styles/
│   └── chess_theme.qss             # QSS stylesheet
└── assets/
    └── images/                     # Piece images
```

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

### Alternative: Direct Python Execution

```bash
cd /home/user/Chess/pyqt
python3 run.py
```

## Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     ChessApplication                         │
│  (Manages lifecycle, connects all components)               │
└────────────┬────────────────────────────────────────────────┘
             │
    ┌────────┴────────┬─────────────────┬──────────────────┐
    │                 │                 │                  │
┌───▼──────┐  ┌───────▼────────┐  ┌────▼─────────┐  ┌────▼──────┐
│ Main     │  │ Game           │  │ Chess Board  │  │ QSS Theme │
│ Window   │  │ Controller     │  │ Widget       │  │ Styles    │
└──────────┘  └────────────────┘  └──────────────┘  └───────────┘
```

### Signal Flow

#### Move Flow
```
User clicks piece
    ↓
ChessBoardWidget.pieceSelected → App._on_piece_selected
    ↓
GameController.get_legal_moves() → App highlights legal moves
    ↓
User drops piece
    ↓
ChessBoardWidget.moveAttempted → GameController.handle_move_attempt
    ↓
GameController.moveCompleted → App._on_move_completed
    ↓
Board updates + Animation + Dashboard refresh
```

#### AI Move Flow
```
Player move completed
    ↓
GameController.start_ai_move()
    ↓
GameController.aiThinking(True) → App._on_ai_thinking → Dashboard shows "AI thinking"
    ↓
AIWorker calculates in background
    ↓
AIWorker.moveCalculated → GameController._handle_ai_move
    ↓
GameController.moveCompleted → App._on_move_completed
    ↓
GameController.aiThinking(False) → Dashboard hides "AI thinking"
```

## Key Features

### 1. ChessApplication (src/ui/app.py)

**Purpose**: Central coordinator that manages all components and their interactions.

**Key Responsibilities**:
- Initialize QApplication and load stylesheet
- Create and configure all UI components
- Connect signals between components
- Set up keyboard shortcuts
- Manage application lifecycle

**Public API**:
```python
app = ChessApplication()
app.show()                           # Show the main window
app.exec()                           # Run the main loop
app.cleanup()                        # Clean up resources

# Testing API
controller = app.get_controller()
window = app.get_main_window()
board = app.get_board_widget()
app.set_game_mode('pvai', ai_color='black', ai_difficulty='hard')
```

**Signal Connections**:
- Board → Controller: moveAttempted, pieceSelected
- Controller → Board: gameStateChanged, moveCompleted
- Controller → Dashboard: evaluationUpdated, aiThinking, gameOver
- Menu → Controller: New game, Undo, Reset
- Keyboard shortcuts: Ctrl+Z (undo), Ctrl+R (reset), Esc (menu)

### 2. Main Entry Point (run.py)

**Purpose**: Simple, clean entry point with proper error handling.

**Features**:
- High DPI scaling support
- Application metadata setup
- Exception handling
- Keyboard interrupt handling
- Proper cleanup on exit

**Usage**:
```bash
python run.py
```

### 3. Component Integration

#### Chess Board Integration
The chess board widget is dynamically integrated into the game screen:

```python
# In app.py
def _setup_board_widget(self):
    self.board_widget = ChessBoardWidget()

    # Replace placeholder in game screen
    game_screen = self.main_window.game_screen
    layout = game_screen.layout()

    # Remove placeholder
    placeholder = layout.itemAt(0).widget()
    layout.removeWidget(placeholder)
    placeholder.deleteLater()

    # Add chess board
    layout.addWidget(self.board_widget, alignment=Qt.AlignmentFlag.AlignCenter)
```

#### Controller Integration
The game controller manages all game logic and AI:

```python
# Signal connections
self.board_widget.moveAttempted.connect(self.controller.handle_move_attempt)
self.controller.gameStateChanged.connect(self._on_game_state_changed)
self.controller.moveCompleted.connect(self._on_move_completed)
```

#### Dashboard Integration
Real-time updates to the dashboard:

```python
# Evaluation updates
self.controller.evaluationUpdated.connect(self._on_evaluation_updated)

# Game state updates
self.controller.gameStateChanged.connect(self._update_dashboard)

# Captured pieces tracking
captured = self._get_captured_pieces()
self.main_window.update_dashboard(eval_score=eval_score, captured=captured)
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New Game |
| `Ctrl+Z` | Undo Move |
| `Ctrl+R` | Reset Game |
| `Esc` | Return to Menu |
| `Ctrl+S` | Save PGN (placeholder) |
| `Ctrl+O` | Load PGN (placeholder) |
| `Ctrl+Q` | Quit Application |
| `F1` | Help Screen |

## Screen Flow

```
Main Menu
    ├── Play vs AI → Game Screen (PvAI mode)
    ├── Tutorials → Tutorial Screen
    ├── Puzzles → Puzzle Screen (Puzzle mode)
    ├── Help → Help Screen
    └── Exit → Close application
```

## Game Modes

### Player vs AI (PvAI)
```python
controller.set_game_mode('pvai', ai_color='black', ai_difficulty='medium')
```

**Difficulty Levels**:
- Easy: Limited search depth, basic evaluation
- Medium: Moderate search depth, good evaluation
- Hard: Deep search, advanced evaluation
- Expert: Maximum search depth, perfect evaluation

### Puzzle Mode
```python
controller.set_game_mode('puzzle')
controller.load_puzzle()
```

### Player vs Player (PvP)
```python
controller.set_game_mode('pvp')
```

## Dashboard Features

### Game Information Card
- Game mode
- Difficulty level
- Current turn
- Opening name

### Position Evaluation
- Numerical evaluation (-∞ to +∞)
- Visual evaluation bar
- Real-time updates

### Captured Pieces
- White's captured pieces
- Black's captured pieces
- Material advantage tracking

### Move History
- Algebraic notation
- Scrollable list
- Click to review positions (future feature)

### AI Status
- Shows when AI is thinking
- Indeterminate progress bar
- Auto-hides when idle

## Stylesheet Integration

The application automatically loads the QSS stylesheet from:
```
/home/user/Chess/pyqt/styles/chess_theme.qss
```

**Theme Colors**:
- Primary background: `#1a1a1a` (dark black)
- Secondary background: `#2a2a2a` (lighter black)
- Accent color: `#ff1493` (hot pink)
- Secondary accent: `#ff69b4` (lighter pink)
- Text: `#ffffff` (white)

## Error Handling

### Application Level
```python
try:
    chess_app = ChessApplication()
    chess_app.show()
    sys.exit(app.exec())
except KeyboardInterrupt:
    print("\nApplication interrupted by user")
    sys.exit(0)
except Exception as e:
    print(f"Fatal error: {e}")
    traceback.print_exc()
    sys.exit(1)
```

### Component Level
- Controller catches and emits errors via `errorOccurred` signal
- App displays errors in status bar
- Game over events show message dialogs
- Invalid moves show temporary status messages

## Testing

### Manual Testing
```bash
# Run the application
python run.py

# Test features:
1. Click "Play vs AI"
2. Make moves on the board
3. Watch AI respond
4. Test Ctrl+Z to undo
5. Test Ctrl+R to reset
6. Test Esc to return to menu
```

### Programmatic Testing
```python
from PyQt6.QtWidgets import QApplication
from src.ui.app import ChessApplication

app = QApplication([])
chess_app = ChessApplication()

# Get components
controller = chess_app.get_controller()
board = chess_app.get_board_widget()
window = chess_app.get_main_window()

# Test game mode changes
chess_app.set_game_mode('pvai', ai_color='black', ai_difficulty='hard')

# Test moves programmatically
controller.handle_move_attempt((6, 4), (4, 4))  # e2-e4
```

## Extending the Application

### Adding New Screens
1. Create screen widget in `main_window.py`
2. Add to stacked widget
3. Create navigation method
4. Connect menu action

### Adding New Features
1. Add functionality to controller
2. Create signal in controller
3. Connect signal in app.py
4. Update UI in signal handler

### Customizing Appearance
Edit `styles/chess_theme.qss` to change:
- Colors
- Fonts
- Spacing
- Border styles
- Hover effects

## Troubleshooting

### Import Errors
```bash
# Ensure PyQt6 is installed
pip install PyQt6

# Ensure you're running from the correct directory
cd /home/user/Chess/pyqt
python run.py
```

### Missing Stylesheet
```
Warning: Stylesheet not found at /home/user/Chess/pyqt/styles/chess_theme.qss
Using default Qt styling
```
Solution: Stylesheet will be loaded if available, otherwise defaults to Qt styling.

### Missing Piece Images
```
Warning: Could not load image at /home/user/Chess/pyqt/assets/images/white/pawn.png
```
Solution: Ensure piece images are in the correct directory structure.

### AI Not Responding
- Check that game mode is set to 'pvai'
- Verify AI color matches the side to move
- Check console for error messages

## Performance Considerations

### AI Calculation
- Runs in background thread (doesn't freeze UI)
- Progress updates via signals
- Can be stopped/cancelled

### Board Rendering
- Hardware-accelerated QGraphicsView
- Smooth animations with QPropertyAnimation
- Efficient piece caching

### Memory Management
- Proper cleanup in `cleanup()` method
- AI worker threads properly terminated
- Widgets properly deleted

## Production Deployment

### Building Standalone Executable
```bash
# Using PyInstaller
pip install pyinstaller

pyinstaller --onefile \
    --windowed \
    --name "PyQt6Chess" \
    --add-data "styles:styles" \
    --add-data "assets:assets" \
    run.py
```

### Distribution
1. Include `styles/` directory
2. Include `assets/` directory
3. Include piece images
4. Test on target platform

## Conclusion

The PyQt6 Chess application is now fully integrated with:
- ✅ Clean entry point (`run.py`)
- ✅ Comprehensive application wrapper (`app.py`)
- ✅ All signals properly connected
- ✅ Keyboard shortcuts configured
- ✅ Dashboard fully integrated
- ✅ AI moves working
- ✅ Error handling in place
- ✅ Production-ready code

Run with: `python run.py`

Enjoy playing chess!
