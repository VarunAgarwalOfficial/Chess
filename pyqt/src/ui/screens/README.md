# PyQt Chess Menu Screens

Complete set of menu screens for PyQt Chess application with pink/black theme.

## Files Created

1. **`__init__.py`** - Module exports for all screens
2. **`menu_screen.py`** - Main menu with game mode selection
3. **`tutorial_screen.py`** - Interactive tutorial interface
4. **`puzzle_screen.py`** - Tactical puzzle solver interface
5. **`help_screen.py`** - Help, controls, and about screen

## Quick Start

```python
from ui.screens import MenuScreen, TutorialScreen, PuzzleScreen, HelpScreen

# Create screens
menu = MenuScreen()
tutorial = TutorialScreen()
puzzle = PuzzleScreen()
help_screen = HelpScreen()

# Connect signals
menu.startPvP.connect(lambda: print("Starting PvP"))
menu.startPvAI.connect(lambda diff: print(f"Starting vs AI: {diff}"))
menu.showTutorial.connect(lambda: stack.setCurrentWidget(tutorial))
menu.showPuzzles.connect(lambda: stack.setCurrentWidget(puzzle))
menu.showHelp.connect(lambda: stack.setCurrentWidget(help_screen))
menu.exitApp.connect(app.quit)

tutorial.backToMenu.connect(lambda: stack.setCurrentWidget(menu))
puzzle.backToMenu.connect(lambda: stack.setCurrentWidget(menu))
help_screen.backToMenu.connect(lambda: stack.setCurrentWidget(menu))
```

## MenuScreen

Main menu with game mode selection.

### Signals
- `startPvP()` - Start player vs player game
- `startPvAI(str)` - Start vs AI with difficulty: "easy", "medium", "hard", "expert"
- `showTutorial()` - Navigate to tutorial screen
- `showPuzzles()` - Navigate to puzzle screen
- `showHelp()` - Navigate to help screen
- `exitApp()` - Exit application

### Features
- Clean, centered layout with large buttons
- AI difficulty selection grid (Easy/Medium/Hard/Expert)
- Hover effects and smooth transitions
- Keyboard navigation support

## TutorialScreen

Interactive chess tutorial with lesson selector and content display.

### Signals
- `backToMenu()` - Return to main menu
- `loadLesson(int)` - Emitted when lesson is loaded
- `lessonCompleted(int)` - Emitted when lesson marked complete

### Features
- Integrates with `features.tutorial.ChessTutorial` backend
- 20+ lessons organized by category
- Progress tracking (completed lessons marked with ✓)
- Lesson categories: basics, special_moves, strategy, tactics, endgame
- Navigation: Previous/Next buttons
- Display: Title, content, key points, FEN position
- Mark lessons as complete

### Backend Integration
```python
# Automatically initializes ChessTutorial
tutorial_screen = TutorialScreen()

# Access tutorial backend
tutorial_screen.tutorial.get_lesson(5)  # Get specific lesson
tutorial_screen.tutorial.mark_completed(5)  # Mark complete
tutorial_screen.tutorial.get_progress()  # Get progress stats
```

## PuzzleScreen

Tactical puzzle solver with hints and solution checking.

### Signals
- `backToMenu()` - Return to main menu
- `loadPuzzle(int)` - Emitted when puzzle is loaded
- `puzzleSolved(int)` - Emitted when puzzle is solved correctly
- `requestHint()` - Emitted when user requests hint

### Features
- Integrates with `features.puzzles.ChessPuzzles` backend
- 40+ tactical puzzles
- Themes: forks, pins, mates, skewers, etc.
- Difficulty levels: easy, medium, hard
- Hint system (progressive hints)
- Show solution button
- Reset puzzle functionality
- Navigation: Previous/Next puzzle
- Track moves made and hints used

### Backend Integration
```python
# Automatically initializes ChessPuzzles
puzzle_screen = PuzzleScreen()

# Check user moves (called by chess board)
is_correct, is_complete, msg = puzzle_screen.check_move("Nf7")

# Access puzzle backend
puzzle_screen.puzzles.get_puzzle(10)  # Get specific puzzle
puzzle_screen.puzzles.get_hint()  # Get hint
```

## HelpScreen

Comprehensive help and about screen with tabbed interface.

### Signals
- `backToMenu()` - Return to main menu

### Features
- 4 tabs: Controls, Features, Chess Rules, About
- **Controls Tab**: Keyboard shortcuts and mouse controls
- **Features Tab**: Complete list of application features
- **Rules Tab**: Chess rules quick reference with HTML formatting
- **About Tab**: Application info, version, credits

### Tabs Content

#### Controls Tab
- Game controls (click, drag, shortcuts)
- File operations (Ctrl+O, Ctrl+S)
- Navigation shortcuts
- Mouse controls

#### Features Tab
- Game modes overview
- Tutorial system details
- Puzzle mode features
- Visual features list
- Analysis tools
- File support

#### Chess Rules Tab
- Objective and win conditions
- Piece movement rules
- Special moves (castling, en passant, promotion)
- Game end conditions
- Basic strategy tips
- Piece values

#### About Tab
- Application title and version
- Description and highlights
- Feature checklist
- Credits and license

## Styling

All screens use consistent pink/black theme:

### Colors
- **Primary Pink**: `#ff1493` (borders, highlights, titles)
- **Light Pink**: `#ff69b4` (hover states, secondary text)
- **Dark Background**: `#1a1a1a` (main background)
- **Panel Background**: `#2a2a2a` (cards, panels)
- **Success Green**: `#50c878` (completed items)
- **Warning Orange**: `#ffa500` (hints)
- **Error Red**: `#ff6b6b` (incorrect moves, exit button)

### Components
- Buttons: Rounded corners, 2-3px borders, hover effects
- Cards/Frames: Rounded corners, pink borders, dark background
- Lists: Pink borders, selection highlighting
- Progress indicators: Pink themed

## Integration Example

```python
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from ui.screens import MenuScreen, TutorialScreen, PuzzleScreen, HelpScreen

class ChessApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create stacked widget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Create screens
        self.menu = MenuScreen()
        self.tutorial = TutorialScreen()
        self.puzzle = PuzzleScreen()
        self.help = HelpScreen()

        # Add to stack
        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.tutorial)
        self.stack.addWidget(self.puzzle)
        self.stack.addWidget(self.help)

        # Connect navigation signals
        self.menu.showTutorial.connect(lambda: self.stack.setCurrentWidget(self.tutorial))
        self.menu.showPuzzles.connect(lambda: self.stack.setCurrentWidget(self.puzzle))
        self.menu.showHelp.connect(lambda: self.stack.setCurrentWidget(self.help))
        self.menu.exitApp.connect(self.close)

        self.tutorial.backToMenu.connect(lambda: self.stack.setCurrentWidget(self.menu))
        self.puzzle.backToMenu.connect(lambda: self.stack.setCurrentWidget(self.menu))
        self.help.backToMenu.connect(lambda: self.stack.setCurrentWidget(self.menu))

        # Connect game start signals
        self.menu.startPvP.connect(self.start_pvp_game)
        self.menu.startPvAI.connect(self.start_ai_game)

    def start_pvp_game(self):
        print("Starting PvP game")
        # Switch to game screen, initialize board, etc.

    def start_ai_game(self, difficulty):
        print(f"Starting AI game with difficulty: {difficulty}")
        # Switch to game screen, initialize AI, etc.

if __name__ == '__main__':
    app = QApplication([])
    window = ChessApp()
    window.show()
    app.exec()
```

## Features Summary

### MenuScreen
- ✓ PvP button
- ✓ AI difficulty grid (4 buttons)
- ✓ Tutorial button
- ✓ Puzzles button
- ✓ Help button
- ✓ Exit button
- ✓ All signals properly defined

### TutorialScreen
- ✓ Lesson list with categories
- ✓ Lesson content display
- ✓ Progress tracking
- ✓ Navigation (prev/next)
- ✓ Mark complete functionality
- ✓ Backend integration (ChessTutorial)
- ✓ FEN position display

### PuzzleScreen
- ✓ Puzzle selector (spinner)
- ✓ Difficulty filter (combo box)
- ✓ Puzzle board placeholder
- ✓ Info panel with metadata
- ✓ Solution progress tracking
- ✓ Hint system
- ✓ Reset functionality
- ✓ Show solution button
- ✓ Navigation (prev/next)
- ✓ Backend integration (ChessPuzzles)

### HelpScreen
- ✓ Tabbed interface
- ✓ Controls tab with shortcuts
- ✓ Features tab with complete list
- ✓ Chess rules tab
- ✓ About tab with credits
- ✓ Scrollable content
- ✓ Rich text formatting

## Notes

1. **Chess Board Integration**: The puzzle and tutorial screens have placeholder areas for the chess board. To integrate a chess board widget:
   ```python
   from ui.chess_board import ChessBoardWidget

   # In puzzle screen
   board = ChessBoardWidget()
   puzzle_screen.board_container.layout().replaceWidget(
       puzzle_screen.board_placeholder, board
   )
   ```

2. **Backend Dependencies**: Tutorial and puzzle screens automatically initialize their backend classes (`ChessTutorial` and `ChessPuzzles`). Make sure these modules are available in `features/` directory.

3. **Signal Connections**: All navigation signals are defined. Connect them to your main window's screen switching logic.

4. **Theming**: All screens use consistent styling. The theme is defined in each screen's `_apply_styles()` method using Qt stylesheets.

5. **Responsive Design**: Screens use proper layouts (QVBoxLayout, QHBoxLayout, QGridLayout) for responsive sizing.

## Testing

Each screen can be tested individually:

```python
from PyQt6.QtWidgets import QApplication
from ui.screens import MenuScreen

app = QApplication([])
menu = MenuScreen()
menu.show()
app.exec()
```

Replace `MenuScreen` with `TutorialScreen`, `PuzzleScreen`, or `HelpScreen` to test other screens.
