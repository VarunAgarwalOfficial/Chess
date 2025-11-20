# Chess Application Signal Flow Reference

## Complete Signal Connection Map

### Legend
- `→` Signal emission
- `▶` Slot/handler
- `[Component]` Component name

---

## 1. User Interaction Signals

### Piece Selection
```
[User] Clicks piece on board
    ↓
[ChessBoardWidget] pieceSelected(position)
    ↓
[ChessApplication] ▶ _on_piece_selected(position)
    ↓
[GameController] get_legal_moves(position)
    ↓
[ChessBoardWidget] set_legal_moves(moves) - highlights legal moves
```

### Move Attempt
```
[User] Drags/drops piece
    ↓
[ChessBoardWidget] moveAttempted(from_pos, to_pos)
    ↓
[GameController] ▶ handle_move_attempt(from_pos, to_pos)
    ↓
[GameController] validates move
    ↓
If valid:
    [GameController] → moveCompleted(from_pos, to_pos)
    [GameController] → gameStateChanged()
    [GameController] → moveValidated(True)
If invalid:
    [GameController] → errorOccurred(message)
    [GameController] → moveValidated(False)
```

---

## 2. Game State Signals

### State Update Flow
```
[GameController] gameStateChanged()
    ↓
[ChessApplication] ▶ _on_game_state_changed()
    ↓
[ChessBoardWidget] set_board_state(board)
    [ChessBoardWidget] clear_highlights()
    [MainWindow] update_game_info(turn=current_player)
```

### Move Completion Flow
```
[GameController] moveCompleted(from_pos, to_pos)
    ↓
[ChessApplication] ▶ _on_move_completed(from_pos, to_pos)
    ↓
[ChessBoardWidget] animate_move(from_pos, to_pos, 250ms)
    [ChessBoardWidget] set_last_move(from_pos, to_pos)
    [ChessBoardWidget] clear_highlights()
```

### Move History Update
```
[GameController] moveCompleted(from_pos, to_pos)
    ↓
[ChessApplication] ▶ _on_move_for_history(from_pos, to_pos)
    ↓
[ChessApplication] converts to algebraic notation
    ↓
[MainWindow] add_move_to_history(move_number, move_text)
```

---

## 3. AI Signals

### AI Move Calculation
```
[GameController] Player move completed
    ↓
[GameController] start_ai_move()
    ↓
[GameController] → aiThinking(True)
    ↓
[ChessApplication] ▶ _on_ai_thinking(True)
    ↓
[MainWindow] show_ai_thinking("AI is thinking...")
    [MainWindow] set_status_message("AI is calculating best move...")

[AIWorker] Calculates in background thread
    ↓
[AIWorker] → moveCalculated(move, position)
    ↓
[GameController] ▶ _handle_ai_move(move, position)
    ↓
[GameController] executes AI move
    ↓
[GameController] → moveCompleted(from_pos, to_pos)
    [GameController] → gameStateChanged()
    [GameController] → aiThinking(False)
    ↓
[ChessApplication] ▶ _on_ai_thinking(False)
    ↓
[MainWindow] hide_ai_thinking()
    [MainWindow] set_status_message("Your turn")
```

---

## 4. Evaluation Signals

### Evaluation Update
```
[GameController] move completed or state changed
    ↓
[GameController] → evaluationUpdated(eval_score)
    ↓
[ChessApplication] ▶ _on_evaluation_updated(eval_score)
    ↓
[ChessApplication] converts centipawns to pawns
    [ChessApplication] gets captured pieces
    ↓
[MainWindow] update_dashboard(eval_score=pawns, captured=pieces)
    ↓
[MainWindow] updates:
    - eval_score_label.setText("+2.5")
    - eval_progress.setValue(250)
    - white_captured.setText("Pawn, Knight")
    - black_captured.setText("Pawn")
```

---

## 5. Game Over Signals

### Game End Flow
```
[GameController] detects game over condition
    ↓
[GameController] → gameOver(result)
    ↓
[ChessApplication] ▶ _on_game_over(result)
    ↓
[MainWindow] hide_ai_thinking()
    [QMessageBox] shows game result dialog
    [MainWindow] set_status_message(result_message)
```

**Game Over Results:**
- `"checkmate_white"` - White wins
- `"checkmate_black"` - Black wins
- `"stalemate"` - Draw
- `"insufficient_material"` - Draw
- `"threefold_repetition"` - Draw
- `"fifty_move_rule"` - Draw

---

## 6. Error Signals

### Error Handling
```
[GameController] encounters error
    ↓
[GameController] → errorOccurred(error_message)
    ↓
[ChessApplication] ▶ _on_error(error_message)
    ↓
[MainWindow] set_status_message(error_message, timeout=5000)
```

**Common Errors:**
- "Illegal move!"
- "Wait for AI to move!"
- "No moves to undo!"
- "AI calculation error: ..."
- "Move error: ..."

---

## 7. Puzzle Signals

### Puzzle Loading
```
[GameController] load_puzzle(puzzle_id)
    ↓
[GameController] loads puzzle from puzzle system
    [GameController] loads FEN position
    ↓
[GameController] → puzzleLoaded(puzzle)
    ↓
[ChessApplication] ▶ _on_puzzle_loaded(puzzle)
    ↓
[MainWindow] set_status_message(f"Puzzle loaded: {name}")
    [ChessBoardWidget] set_board_state(controller.board)
```

### Puzzle Progress
```
[GameController] handles puzzle move
    ↓
[GameController] checks move correctness
    ↓
[GameController] → puzzleProgress(is_correct, is_complete, message)
    ↓
[ChessApplication] ▶ _on_puzzle_progress(is_correct, is_complete, message)
    ↓
If complete:
    [QMessageBox] shows "Puzzle Complete!" dialog
Else:
    [MainWindow] set_status_message(message, timeout=3000)
```

---

## 8. Menu Action Signals

### New Game
```
[User] clicks "New Game" or presses Ctrl+N
    ↓
[MainWindow] menu action triggered
    ↓
[ChessApplication] ▶ _on_new_game_shortcut()
    ↓
[MainWindow] show_game_screen()
    [GameController] reset_game()
```

### Undo Move
```
[User] clicks "Undo" or presses Ctrl+Z
    ↓
[QShortcut] activated
    ↓
[GameController] ▶ undo_move()
    ↓
[GameController] undoes move(s)
    ↓
[GameController] → gameStateChanged()
    [GameController] → evaluationUpdated(new_eval)
```

### Reset Game
```
[User] clicks "Reset" or presses Ctrl+R
    ↓
[QShortcut] activated
    ↓
[GameController] ▶ reset_game()
    ↓
[GameController] creates new board
    [GameController] resets AI
    [GameController] clears history
    ↓
[GameController] → gameStateChanged()
    [GameController] → evaluationUpdated(0.0)
```

### Return to Menu
```
[User] presses Esc
    ↓
[QShortcut] activated
    ↓
[MainWindow] ▶ show_menu_screen()
    ↓
[MainWindow] switches to menu screen
    [MainWindow] hides dashboard
    [MainWindow] set_status_message("Main Menu")
    ↓
[MainWindow] → screen_changed("menu")
```

---

## 9. Screen Change Signals

### Screen Navigation
```
[MainWindow] show_*_screen() called
    ↓
[MainWindow] → screen_changed(screen_name)
    ↓
[ChessApplication] ▶ _on_screen_changed(screen_name)
    ↓
If "game":
    [GameController] set_game_mode('pvai')
    [ChessBoardWidget] set_board_state(board)
    [MainWindow] update_game_info(mode="vs AI", difficulty="Medium")
If "puzzle":
    [GameController] set_game_mode('puzzle')
    [GameController] load_puzzle()
```

---

## 10. Keyboard Shortcuts

All keyboard shortcuts are set up in `ChessApplication._setup_keyboard_shortcuts()`:

| Shortcut | Signal/Slot |
|----------|-------------|
| `Ctrl+Z` | `QShortcut.activated` → `GameController.undo_move()` |
| `Ctrl+R` | `QShortcut.activated` → `GameController.reset_game()` |
| `Ctrl+N` | `QShortcut.activated` → `ChessApplication._on_new_game_shortcut()` |
| `Esc` | `QShortcut.activated` → `MainWindow.show_menu_screen()` |

---

## Signal Connection Summary Table

| Source | Signal | Destination | Handler |
|--------|--------|-------------|---------|
| ChessBoardWidget | moveAttempted | GameController | handle_move_attempt |
| ChessBoardWidget | pieceSelected | ChessApplication | _on_piece_selected |
| GameController | gameStateChanged | ChessApplication | _on_game_state_changed |
| GameController | moveCompleted | ChessApplication | _on_move_completed |
| GameController | moveCompleted | ChessApplication | _on_move_for_history |
| GameController | evaluationUpdated | ChessApplication | _on_evaluation_updated |
| GameController | aiThinking | ChessApplication | _on_ai_thinking |
| GameController | gameOver | ChessApplication | _on_game_over |
| GameController | errorOccurred | ChessApplication | _on_error |
| GameController | puzzleLoaded | ChessApplication | _on_puzzle_loaded |
| GameController | puzzleProgress | ChessApplication | _on_puzzle_progress |
| MainWindow | screen_changed | ChessApplication | _on_screen_changed |
| QShortcut (Ctrl+Z) | activated | GameController | undo_move |
| QShortcut (Ctrl+R) | activated | GameController | reset_game |
| QShortcut (Ctrl+N) | activated | ChessApplication | _on_new_game_shortcut |
| QShortcut (Esc) | activated | MainWindow | show_menu_screen |

---

## Dashboard Update Triggers

The dashboard is updated in these scenarios:

1. **Game State Changed**: Full dashboard refresh
2. **Evaluation Updated**: Updates eval bar and captured pieces
3. **Move Completed**: Adds to move history
4. **AI Thinking**: Shows/hides AI status widget
5. **Turn Changed**: Updates turn indicator

---

## Thread Safety

### Main Thread
- All UI updates
- Signal emissions
- Event handling

### Background Thread (AIWorker)
- AI move calculation
- Position evaluation
- Search tree exploration

**Communication**: Signals/slots are thread-safe in Qt

---

## Component Initialization Order

```
1. QApplication created
2. Stylesheet loaded
3. ChessMainWindow created
4. GameController created
5. ChessBoardWidget created
6. Board widget integrated into game screen
7. Signals connected
8. Keyboard shortcuts set up
9. Event filter installed
10. Window shown
```

---

## Cleanup Sequence

```
1. User closes window or exits
2. ChessApplication.cleanup() called
3. GameController.cleanup() stops AI worker
4. AI worker thread terminated
5. Main window closed
6. Application exits
```

---

## Best Practices

### Adding New Signals

1. **Define in source component**:
   ```python
   class GameController(QObject):
       newSignal = pyqtSignal(str, int)  # Define types
   ```

2. **Connect in ChessApplication**:
   ```python
   self.controller.newSignal.connect(self._on_new_signal)
   ```

3. **Create handler**:
   ```python
   @pyqtSlot(str, int)
   def _on_new_signal(self, text, value):
       # Handle signal
       pass
   ```

4. **Emit when needed**:
   ```python
   self.newSignal.emit("text", 42)
   ```

### Signal Naming Conventions

- **Signals**: `camelCase` (e.g., `gameStateChanged`)
- **Handlers**: `_on_signal_name` (e.g., `_on_game_state_changed`)
- **Public methods**: `snake_case` (e.g., `set_game_mode`)
- **Private methods**: `_snake_case` (e.g., `_update_dashboard`)

---

This reference provides a complete map of all signal flows in the PyQt6 Chess application. Use it to understand how components communicate and to add new features.
