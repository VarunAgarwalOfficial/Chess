# PyQt6 Chess Test Suite

Comprehensive integration and unit tests for the PyQt6 Chess Application.

## Quick Start

```bash
# Install test dependencies
pip install -r ../requirements-dev.txt

# Run all tests
pytest test_integration.py -v

# Run with coverage
pytest --cov=../src test_integration.py

# Use the shell script
../run_tests.sh -v -c
```

## Test Organization

### File Structure

```
tests/
├── __init__.py              # Test package marker
├── conftest.py              # Pytest configuration and shared fixtures
├── test_integration.py      # Main test suite (120+ test cases)
├── README.md                # This file
```

### Test Categories

#### 1. MainWindow Tests (12 tests)
Tests the main application window and navigation:

- Window initialization and sizing
- Screen navigation between game/tutorial/puzzle/help
- Dashboard updates and information display
- AI thinking indicator
- Status messages
- Menu actions

```python
# Example: Test screen navigation
def test_screen_navigation(main_window):
    main_window.show()
    main_window.show_game_screen()
    assert main_window.stacked_widget.currentWidget() == main_window.game_screen
```

#### 2. ChessBoardWidget Tests (6 tests)
Tests the chess board rendering and interaction:

- Board initialization and sizing
- Piece selection and highlighting
- Legal move visualization
- Move animation
- Last move highlighting

```python
# Example: Test piece selection
def test_piece_selection(chess_board_widget):
    spy = QSignalSpy(chess_board_widget.pieceSelected)
    # Simulate piece selection
    chess_board_widget.board_scene.piece_pressed(mock_piece)
```

#### 3. GameController Tests (10 tests)
Tests game logic and move handling:

- Game mode initialization
- Move validation and execution
- Legal move retrieval
- Board state management
- Undo and reset functionality
- FEN position loading
- Game over detection

```python
# Example: Test move validation
def test_move_validation_illegal(game_controller):
    game_controller.board.get_legal_moves = MagicMock(return_value=[])
    game_controller.handle_move_attempt((6, 4), (5, 5))
    # Should emit moveValidated(False)
```

#### 4. Puzzle System Tests (10 tests)
Tests puzzle loading and solving:

- Puzzle initialization
- Getting puzzles by ID/difficulty/theme
- Solution checking
- Hint generation
- Puzzle navigation (next/previous)
- Progress tracking

```python
# Example: Test puzzle solving
def test_check_move_correct(puzzle_system):
    puzzle = puzzle_system.get_puzzle()
    first_move = puzzle["solution"][0]
    is_correct, _, _ = puzzle_system.check_move(first_move)
    assert is_correct
```

#### 5. AI Threading Tests (3 tests)
Tests background AI calculation:

- AI worker thread creation
- Signal definition and emission
- Non-blocking move calculation
- Error handling

```python
# Example: Test AI worker
def test_ai_worker_creation(mock_ai):
    worker = AIWorker(mock_ai)
    assert worker.is_calculating == False
```

#### 6. Integration Tests (5 tests)
Tests complete workflows:

- Full PvP game flow (multiple moves)
- Undo and reset workflow
- Puzzle solving workflow
- Multi-screen navigation
- Main window game flow

```python
# Example: Test complete game flow
def test_complete_game_flow_pvp(game_controller):
    game_controller.set_game_mode('pvp')
    # ... make moves ...
    assert game_controller.is_game_over() == expected_result
```

#### 7. Error Handling Tests (5 tests)
Tests edge cases and error conditions:

- Moving when game is over
- Undo with empty history
- Invalid puzzle IDs
- Missing data handling
- Invalid FEN strings

```python
# Example: Test empty undo
def test_undo_with_empty_history(game_controller):
    game_controller.board.move_log = []
    game_controller.undo_move()  # Should handle gracefully
```

#### 8. Edge Case Tests (4 tests)
Tests boundary conditions:

- Board with pieces at all squares
- Rapid move sequences
- Puzzle cycling through all puzzles
- Extreme evaluation scores

```python
# Example: Test rapid moves
def test_rapid_move_sequence(game_controller):
    for _ in range(5):
        game_controller.handle_move_attempt((6, 4), (4, 4))
    # Should handle rapid input gracefully
```

#### 9. Signal/Slot Tests (5 tests)
Tests Qt signal and slot mechanisms:

- Game state changed signals
- Move completed signals
- Evaluation updated signals
- Screen changed signals
- Board widget signals

```python
# Example: Test signal emission
def test_game_state_changed_signal(game_controller):
    spy = QSignalSpy(game_controller.gameStateChanged)
    game_controller.reset_game()
    # Verify signal was emitted
```

#### 10. Mocking Tests (3 tests)
Tests proper mocking for unit isolation:

- AI mocking
- Board method mocking
- Puzzle system mocking

```python
# Example: Test with mocked AI
def test_ai_mock(mock_ai):
    move, pos = mock_ai.get_best_move()
    assert move == {'to': (4, 4)}
```

## Fixtures

Reusable test components defined in `conftest.py`:

### Session-wide Fixtures

```python
@pytest.fixture(scope="session", autouse=True)
def qapp_session():
    """Creates QApplication for entire test session"""
    # Automatically used by all tests
    return QApplication([])
```

### Function-wide Fixtures

```python
@pytest.fixture
def game_controller():
    """Fresh GameController for each test"""
    controller = GameController()
    yield controller
    controller.cleanup()

@pytest.fixture
def main_window():
    """Fresh MainWindow for each test"""
    window = ChessMainWindow()
    yield window
    window.close()

@pytest.fixture
def mock_ai():
    """Pre-configured mock AI for fast tests"""
    mock_ai_instance = MagicMock()
    mock_ai_instance.get_best_move = MagicMock(return_value=({'to': (4, 4)}, (6, 4)))
    return mock_ai_instance
```

## Running Tests

### Basic Commands

```bash
# Run all tests with default settings
pytest test_integration.py

# Run with verbose output
pytest test_integration.py -v

# Run specific test class
pytest test_integration.py::TestMainWindow -v

# Run specific test function
pytest test_integration.py::TestMainWindow::test_window_initialization -v
```

### Using Markers

```bash
# Run only integration tests
pytest -m integration test_integration.py

# Skip slow tests
pytest -m "not slow" test_integration.py

# Run UI tests only
pytest -m ui test_integration.py

# Run AI-related tests
pytest -m ai test_integration.py
```

### Coverage Reports

```bash
# Generate coverage report
pytest --cov=../src test_integration.py

# Generate HTML coverage report
pytest --cov=../src --cov-report=html test_integration.py
# Open htmlcov/index.html in browser
```

### Using the Test Runner Script

```bash
# Make script executable (first time only)
chmod +x ../run_tests.sh

# Run all tests
../run_tests.sh

# Verbose with coverage
../run_tests.sh -v -c

# Only integration tests
../run_tests.sh -m integration

# Skip slow tests
../run_tests.sh -m "not slow"

# Run specific test
../run_tests.sh -t test_integration.py::TestMainWindow::test_screen_navigation
```

## Writing New Tests

### Test Structure

```python
def test_something(fixture_name):
    """
    Test description - what should this test verify?

    Arrange: Set up test data and mocks
    Act: Perform the action being tested
    Assert: Verify the expected outcome
    """
    # Arrange
    controller = fixture_name
    controller.board.get_legal_moves = MagicMock(return_value=[{"to": (4, 4)}])

    # Act
    controller.handle_move_attempt((6, 4), (4, 4))

    # Assert
    assert controller.move_history_length > 0
```

### Using Mocks

```python
from unittest.mock import Mock, MagicMock, patch

# Create a simple mock
mock_board = Mock()
mock_board.to_move = "white"

# Create a mock with return values
mock_ai = MagicMock()
mock_ai.get_best_move.return_value = ({'to': (4, 4)}, (6, 4))

# Mock side effects
mock_board.move.side_effect = Exception("Invalid move")

# Use patch decorator
@patch('module.function_to_patch')
def test_something(mock_function):
    mock_function.return_value = "mocked result"
```

### Testing Signals

```python
def test_signal(game_controller):
    """Test that a signal is emitted"""
    spy = QSignalSpy(game_controller.moveCompleted)

    # Action that should emit signal
    game_controller.handle_move_attempt((6, 4), (4, 4))

    # Verify signal was emitted
    assert len(spy) > 0
```

### Testing Exceptions

```python
def test_error_handling():
    """Test that errors are handled correctly"""
    with pytest.raises(ValueError):
        # Code that should raise ValueError
        validate_fen("invalid")
```

## Common Issues

### QApplication Already Exists

```python
# Solution: Check if instance exists first
if not QApplication.instance():
    app = QApplication([])
else:
    app = QApplication.instance()
```

### Signals Not Firing in Tests

```python
# Ensure proper signal connection before emitting
controller.moveCompleted.connect(handler)

# Process Qt events
from PyQt6.QtCore import QCoreApplication
QCoreApplication.processEvents()
```

### Fixture Not Passed Correctly

```python
# Wrong: fixture name should match parameter name
def test_something(wrong_name):  # Fixture not injected

# Correct: parameter name matches fixture name
def test_something(game_controller):  # Fixture injected correctly
```

### Test Hanging

```
Solutions:
1. Add timeout: pytest --timeout=30 test_integration.py
2. Check for infinite loops in test code
3. Ensure cleanup is happening in fixtures
4. Process Qt events: QCoreApplication.processEvents()
```

## Best Practices

1. **One assertion per test** (when possible)
   ```python
   # Better: Separate tests for clarity
   def test_window_title(main_window):
       assert main_window.windowTitle() == "PyQt6 Chess - Modern Chess Interface"

   def test_window_size(main_window):
       assert main_window.width() == 940
   ```

2. **Use descriptive names**
   ```python
   # Bad: test_1, test_window
   # Good: test_window_navigation_to_game_screen
   ```

3. **Mock external dependencies**
   ```python
   # Don't test AI engine details in integration tests
   # Use mocks for speed and isolation
   game_controller.ai = mock_ai
   ```

4. **Test behavior, not implementation**
   ```python
   # Bad: Checking internal state
   assert game_controller.board.move_log[0] == expected_move

   # Good: Testing external behavior
   assert game_controller.move_history_count == 1
   ```

5. **Keep tests focused**
   ```python
   # Each test should test one thing
   # Use fixtures for setup instead of complex test methods
   ```

6. **Use parametrize for multiple scenarios**
   ```python
   @pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
   def test_ai_difficulty(difficulty):
       ai = AI(difficulty=difficulty)
       assert ai.difficulty == difficulty
   ```

## Performance Considerations

- Tests use mocked AI to run in milliseconds instead of seconds
- QApplication is created once per session
- Fixtures are reused efficiently
- No file I/O in fast tests
- Signals are tested without full event loop processing

## Continuous Integration

For CI/CD pipelines:

```bash
# Run with junit XML output
pytest --junitxml=results.xml test_integration.py

# Generate coverage in XML (for coverage.io, etc.)
pytest --cov=../src --cov-report=xml test_integration.py

# Run in headless mode (no display)
DISPLAY="" pytest test_integration.py
```

## Troubleshooting

### Tests fail with "QApplication already exists"

```bash
# Solution: Use existing instance in conftest.py
# (Already handled in provided conftest.py)
```

### Tests are slow

```bash
# Use mocked AI
# Skip slow tests: pytest -m "not slow"
# Run specific tests: pytest test_integration.py::TestMainWindow
```

### Import errors in tests

```bash
# Ensure src is in path (done in conftest.py)
# Check that all modules have __init__.py files
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [PyTest-Qt Documentation](https://pytest-qt.readthedocs.io/)
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Python Unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

**Happy Testing!**
