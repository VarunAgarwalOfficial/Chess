# PyQt6 Chess - Quick Start Guide

## Installation & Running

```bash
# Navigate to project directory
cd /home/user/Chess/pyqt

# Install dependencies (first time only)
pip install PyQt6

# Run the application
python run.py
```

## File Overview

| File | Purpose |
|------|---------|
| `run.py` | Main entry point - run this file |
| `src/ui/app.py` | Application wrapper - manages all components |
| `src/ui/main_window.py` | Main window with screens and dashboard |
| `src/ui/game_controller.py` | Game logic coordinator |
| `src/ui/chess_board.py` | Interactive chess board widget |
| `styles/chess_theme.qss` | Pink/black color theme |

## Quick Commands

```bash
# Run application
python run.py

# Verify integration
python verify_integration.py

# Run with verbose output
python run.py --verbose  # (if implemented)
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New Game |
| `Ctrl+Z` | Undo Move |
| `Ctrl+R` | Reset Game |
| `Esc` | Return to Menu |
| `F1` | Help |

## Game Controls

### Playing
1. Click on a piece to select it
2. Legal moves are highlighted in green
3. Click destination square or drag piece
4. AI automatically responds (if in AI mode)

### Features
- **Dashboard**: Shows evaluation, captured pieces, move history
- **AI Thinking**: Indicator shows when AI is calculating
- **Move History**: Displays all moves in algebraic notation
- **Evaluation Bar**: Visual representation of position advantage

## Application Structure

```
ChessApplication
├── Main Window (screens + dashboard)
├── Game Controller (game logic)
└── Chess Board Widget (interactive board)
```

## Screens

| Screen | Access | Purpose |
|--------|--------|---------|
| Main Menu | Startup / Esc | Main navigation |
| Game | "Play vs AI" button | Play against computer |
| Tutorial | "Tutorials" button | Learn chess |
| Puzzles | "Puzzles" button | Solve tactical puzzles |
| Help | "Help" button / F1 | Instructions |

## Common Tasks

### Start a New Game
1. Press `Ctrl+N` or click "New Game" in File menu
2. Game screen opens with fresh board
3. Make your move (white starts)

### Change AI Difficulty
1. Click "Game" → "Settings"
2. Select difficulty level
3. Start new game for changes to take effect

### Undo Moves
- Press `Ctrl+Z` to undo last move(s)
- In AI mode, undoes both your move and AI's move

### Save/Load Games
- `Ctrl+S` to save (PGN format) - *coming soon*
- `Ctrl+O` to load (PGN format) - *coming soon*

## Troubleshooting

### Application won't start
```bash
# Check PyQt6 is installed
pip install PyQt6

# Run from correct directory
cd /home/user/Chess/pyqt
python run.py
```

### Pieces don't display
- Ensure `assets/images/` directory contains piece images
- Check console for image loading errors

### AI doesn't move
- Wait for AI thinking indicator
- Check that you're in "vs AI" mode
- Verify it's AI's turn (check turn indicator)

### Window appears off-screen
- Delete config file (if it exists)
- Window will center on next startup

## Documentation Files

| File | Contents |
|------|----------|
| `APPLICATION_GUIDE.md` | Complete usage guide |
| `SIGNAL_FLOW_REFERENCE.md` | Signal connection details |
| `INTEGRATION_COMPLETE.md` | Requirements checklist |
| `QUICK_START.md` | This file |

## Component API (for testing)

```python
from PyQt6.QtWidgets import QApplication
from src.ui.app import ChessApplication

app = QApplication([])
chess = ChessApplication()

# Access components
controller = chess.get_controller()
window = chess.get_main_window()
board = chess.get_board_widget()

# Set game mode
chess.set_game_mode('pvai', ai_color='black', ai_difficulty='hard')

# Show and run
chess.show()
app.exec()
```

## Game Modes

| Mode | Code | Description |
|------|------|-------------|
| Player vs AI | `'pvai'` | Play against computer |
| Player vs Player | `'pvp'` | Two-player mode |
| Puzzle | `'puzzle'` | Solve chess puzzles |

## Signal Flow (Simplified)

```
User Move → Board Widget → Controller → Validates → Updates Board
                                      ↓
                               Triggers AI Move (if PvAI mode)
                                      ↓
                               AI Calculates → Makes Move
                                      ↓
                               Updates Dashboard
```

## Dashboard Components

1. **Game Info** - Mode, difficulty, turn, opening
2. **Evaluation Bar** - Position advantage indicator
3. **Captured Pieces** - Pieces taken by each side
4. **Move History** - Scrollable move list
5. **AI Status** - Shows when AI is thinking

## Tips

- Use keyboard shortcuts for faster navigation
- Watch the evaluation bar to see position advantage
- Review move history to analyze your game
- Try different AI difficulty levels
- Use Esc to quickly return to menu

## Support

For issues or questions:
1. Check `APPLICATION_GUIDE.md` for detailed help
2. Run `verify_integration.py` to check setup
3. Review console output for error messages

## Quick Reference

### File Locations
- Entry point: `/home/user/Chess/pyqt/run.py`
- App wrapper: `/home/user/Chess/pyqt/src/ui/app.py`
- Stylesheet: `/home/user/Chess/pyqt/styles/chess_theme.qss`

### Important Classes
- `ChessApplication` - Main app wrapper
- `ChessMainWindow` - Window with screens
- `GameController` - Game logic
- `ChessBoardWidget` - Interactive board

### Key Methods
- `chess_app.show()` - Show window
- `chess_app.exec()` - Run main loop
- `chess_app.cleanup()` - Clean shutdown
- `controller.reset_game()` - Reset board
- `controller.undo_move()` - Undo last move

---

**Ready to play?** Run: `python run.py`
