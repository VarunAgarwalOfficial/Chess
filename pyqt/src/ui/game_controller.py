'''
Game Controller - MVC Pattern Implementation
This module acts as the glue between the UI and game logic.
Manages game state, coordinates AI moves, and updates the UI.
'''

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from game import Board
from ai.ai import AI
from game.fen_parser import parse_fen
from features.puzzles import ChessPuzzles


class AIWorker(QThread):
    '''
    Background worker thread for AI move calculation
    Prevents UI freezing during AI thinking
    '''
    # Signals
    moveCalculated = pyqtSignal(dict, tuple)  # (move, position)
    thinkingProgress = pyqtSignal(int, int)  # (depth, nodes_searched)
    error = pyqtSignal(str)  # Error message

    def __init__(self, ai_instance):
        super().__init__()
        self.ai = ai_instance
        self.is_calculating = False

    def run(self):
        '''Execute AI move calculation in background thread'''
        try:
            self.is_calculating = True

            # Get best move from AI
            best_move, best_pos = self.ai.get_best_move()

            # Emit progress updates (depth and nodes searched)
            self.thinkingProgress.emit(self.ai.max_depth, self.ai.nodes_searched)

            # Emit the calculated move
            if best_move and best_pos:
                self.moveCalculated.emit(best_move, best_pos)
            else:
                self.error.emit("AI could not find a valid move")

        except Exception as e:
            self.error.emit(f"AI calculation error: {str(e)}")
        finally:
            self.is_calculating = False

    def stop(self):
        '''Stop the AI calculation (if possible)'''
        self.is_calculating = False
        self.quit()
        self.wait()


class GameController(QObject):
    '''
    Game Controller - Coordinates between UI and game logic
    Implements MVC pattern as the controller component
    '''

    # Signals
    gameStateChanged = pyqtSignal()  # Emitted when board state changes
    moveCompleted = pyqtSignal(tuple, tuple)  # (from_pos, to_pos)
    aiThinking = pyqtSignal(bool)  # True when AI starts thinking, False when done
    gameOver = pyqtSignal(str)  # Game result (checkmate_white, checkmate_black, draw, etc.)
    evaluationUpdated = pyqtSignal(float)  # Position evaluation score
    moveValidated = pyqtSignal(bool)  # True if move is valid, False otherwise
    errorOccurred = pyqtSignal(str)  # Error message
    puzzleLoaded = pyqtSignal(dict)  # Puzzle information
    puzzleProgress = pyqtSignal(bool, bool, str)  # (is_correct, is_complete, message)

    def __init__(self):
        super().__init__()

        # Initialize game board
        self.board = Board()

        # AI instance (initially None)
        self.ai = None
        self.ai_worker = None

        # Game mode: 'pvp', 'pvai', 'puzzle'
        self.game_mode = 'pvp'

        # AI settings
        self.ai_color = "black"
        self.ai_difficulty = "medium"

        # Puzzle system
        self.puzzle_system = ChessPuzzles()
        self.current_puzzle = None
        self.puzzle_moves = []

        # Move history for undo
        self.move_history = []

    def set_game_mode(self, mode, ai_color="black", ai_difficulty="medium"):
        '''
        Set the game mode

        Args:
            mode: 'pvp', 'pvai', or 'puzzle'
            ai_color: 'white' or 'black' (for pvai mode)
            ai_difficulty: 'easy', 'medium', 'hard', or 'expert'
        '''
        self.game_mode = mode
        self.ai_color = ai_color
        self.ai_difficulty = ai_difficulty

        # Initialize AI if needed
        if mode == 'pvai':
            self.ai = AI(self.board, color=ai_color, difficulty=ai_difficulty)

            # If AI plays white, start AI move immediately
            if ai_color == "white" and self.board.to_move == "white":
                self.start_ai_move()
        else:
            self.ai = None

    @pyqtSlot(tuple, tuple)
    def handle_move_attempt(self, from_pos, to_pos):
        '''
        Handle a move attempt from the UI
        Validates and executes the move if legal

        Args:
            from_pos: (row, col) tuple of starting position
            to_pos: (row, col) tuple of destination position
        '''
        try:
            # Check if it's the correct player's turn in PvAI mode
            if self.game_mode == 'pvai':
                if self.board.to_move == self.ai_color:
                    self.errorOccurred.emit("Wait for AI to move!")
                    self.moveValidated.emit(False)
                    return

            # Get legal moves for the piece at from_pos
            legal_moves = self.board.get_legal_moves(from_pos)

            # Find if the desired move is in legal moves
            target_move = None
            for move in legal_moves:
                if move["to"] == to_pos:
                    target_move = move
                    break

            if target_move is None:
                self.errorOccurred.emit("Illegal move!")
                self.moveValidated.emit(False)
                return

            # Execute the move
            self.board.move(from_pos, target_move)

            # Track move history
            self.move_history.append((from_pos, to_pos, target_move))

            # Emit signals
            self.moveCompleted.emit(from_pos, to_pos)
            self.gameStateChanged.emit()
            self.moveValidated.emit(True)

            # Update evaluation (if AI exists)
            if self.ai:
                evaluation = self.ai.evaluate_board()
                self.evaluationUpdated.emit(evaluation)

            # Check for game over
            if self.board.game_over:
                self.gameOver.emit(self.board.game_result)
                return

            # Handle puzzle mode
            if self.game_mode == 'puzzle' and self.current_puzzle:
                self._handle_puzzle_move(target_move, from_pos, to_pos)

            # Start AI move if it's AI's turn in PvAI mode
            if self.game_mode == 'pvai' and self.board.to_move == self.ai_color:
                self.start_ai_move()

        except Exception as e:
            self.errorOccurred.emit(f"Move error: {str(e)}")
            self.moveValidated.emit(False)

    def _handle_puzzle_move(self, move, from_pos, to_pos):
        '''Handle move in puzzle mode'''
        # Convert move to algebraic notation (simplified version)
        # In a real implementation, this would properly convert to SAN
        move_san = self._move_to_san(move, from_pos, to_pos)

        # Check if move matches puzzle solution
        is_correct, is_complete, message = self.puzzle_system.check_move(move_san)

        self.puzzleProgress.emit(is_correct, is_complete, message)

        if not is_correct:
            # Undo incorrect move after a delay
            pass  # UI should handle visual feedback

    def _move_to_san(self, move, from_pos, to_pos):
        '''
        Convert internal move representation to Standard Algebraic Notation (SAN)
        Simplified version - real implementation would be more complex
        '''
        piece = self.board.state[to_pos[0]][to_pos[1]]
        if not piece:
            return ""

        # Handle special moves
        if move.get("special") == "KSC":
            return "O-O"
        elif move.get("special") == "QSC":
            return "O-O-O"

        # Build SAN string
        san = ""

        # Piece letter (pawn moves don't include piece letter)
        if piece.type != "pawn":
            san += piece.type[0].upper()

        # File/rank of origin (simplified - would need disambiguation in real implementation)
        from_file = chr(ord('a') + from_pos[1])
        from_rank = str(8 - from_pos[0])

        # Capture notation
        if move.get("special") == "capture" or self.board.state[to_pos[0]][to_pos[1]]:
            if piece.type == "pawn":
                san += from_file
            san += "x"

        # Destination
        to_file = chr(ord('a') + to_pos[1])
        to_rank = str(8 - to_pos[0])
        san += to_file + to_rank

        # Check/checkmate
        if self.board.check:
            if self.board.game_over and "checkmate" in self.board.game_result:
                san += "#"
            else:
                san += "+"

        return san

    @pyqtSlot()
    def start_ai_move(self):
        '''Start AI move calculation in background thread'''
        if not self.ai or self.game_mode != 'pvai':
            return

        if self.board.game_over:
            return

        # Emit thinking signal
        self.aiThinking.emit(True)

        # Create and start AI worker thread
        self.ai_worker = AIWorker(self.ai)
        self.ai_worker.moveCalculated.connect(self._handle_ai_move)
        self.ai_worker.error.connect(self._handle_ai_error)
        self.ai_worker.finished.connect(lambda: self.aiThinking.emit(False))
        self.ai_worker.start()

    @pyqtSlot(dict, tuple)
    def _handle_ai_move(self, move, pos):
        '''Handle AI move once calculated'''
        try:
            # Execute AI move
            self.board.move(pos, move)

            # Track move history
            self.move_history.append((pos, move["to"], move))

            # Emit signals
            self.moveCompleted.emit(pos, move["to"])
            self.gameStateChanged.emit()

            # Update evaluation
            evaluation = self.ai.evaluate_board()
            self.evaluationUpdated.emit(evaluation)

            # Check for game over
            if self.board.game_over:
                self.gameOver.emit(self.board.game_result)

        except Exception as e:
            self.errorOccurred.emit(f"AI move error: {str(e)}")

    @pyqtSlot(str)
    def _handle_ai_error(self, error_msg):
        '''Handle AI calculation error'''
        self.errorOccurred.emit(error_msg)
        self.aiThinking.emit(False)

    @pyqtSlot()
    def undo_move(self):
        '''Undo the last move'''
        try:
            if len(self.board.move_log) == 0:
                self.errorOccurred.emit("No moves to undo!")
                return

            # In PvAI mode, undo both player and AI moves
            if self.game_mode == 'pvai':
                # Undo AI move
                if len(self.board.move_log) > 0:
                    self.board.undo()
                    if self.move_history:
                        self.move_history.pop()

                # Undo player move
                if len(self.board.move_log) > 0:
                    self.board.undo()
                    if self.move_history:
                        self.move_history.pop()
            else:
                # In PvP mode, undo one move
                self.board.undo()
                if self.move_history:
                    self.move_history.pop()

            # Emit signals
            self.gameStateChanged.emit()

            # Update evaluation
            if self.ai:
                evaluation = self.ai.evaluate_board()
                self.evaluationUpdated.emit(evaluation)

        except Exception as e:
            self.errorOccurred.emit(f"Undo error: {str(e)}")

    @pyqtSlot()
    def reset_game(self):
        '''Reset the game to initial position'''
        try:
            # Create new board
            self.board = Board()

            # Reset AI if in PvAI mode
            if self.game_mode == 'pvai':
                self.ai = AI(self.board, color=self.ai_color, difficulty=self.ai_difficulty)

                # If AI plays white, start AI move
                if self.ai_color == "white":
                    self.start_ai_move()

            # Reset puzzle if in puzzle mode
            if self.game_mode == 'puzzle':
                self.puzzle_system.reset_puzzle()
                self.puzzle_moves = []

            # Clear move history
            self.move_history = []

            # Emit signals
            self.gameStateChanged.emit()

            # Update evaluation
            if self.ai:
                evaluation = self.ai.evaluate_board()
                self.evaluationUpdated.emit(evaluation)

        except Exception as e:
            self.errorOccurred.emit(f"Reset error: {str(e)}")

    @pyqtSlot(str)
    def load_fen(self, fen_string):
        '''
        Load a position from FEN notation
        Used for puzzle mode and custom positions

        Args:
            fen_string: FEN notation string
        '''
        try:
            # Parse FEN and update board
            parse_fen(self.board, fen_string)

            # Reinitialize AI if needed
            if self.game_mode == 'pvai' and self.ai:
                self.ai = AI(self.board, color=self.ai_color, difficulty=self.ai_difficulty)

            # Clear move history
            self.move_history = []

            # Emit signals
            self.gameStateChanged.emit()

            # Update evaluation
            if self.ai:
                evaluation = self.ai.evaluate_board()
                self.evaluationUpdated.emit(evaluation)

        except Exception as e:
            self.errorOccurred.emit(f"FEN load error: {str(e)}")

    @pyqtSlot(int)
    def load_puzzle(self, puzzle_id=None):
        '''
        Load a chess puzzle

        Args:
            puzzle_id: ID of puzzle to load, or None for current puzzle
        '''
        try:
            # Get puzzle
            if puzzle_id is not None:
                puzzle = self.puzzle_system.get_puzzle(puzzle_id)
            else:
                puzzle = self.puzzle_system.get_puzzle()

            if not puzzle:
                self.errorOccurred.emit("Puzzle not found!")
                return

            # Store current puzzle
            self.current_puzzle = puzzle

            # Load puzzle position
            self.load_fen(puzzle["fen"])

            # Reset puzzle tracking
            self.puzzle_moves = []
            self.puzzle_system.reset_puzzle()

            # Emit puzzle loaded signal
            self.puzzleLoaded.emit(puzzle)

        except Exception as e:
            self.errorOccurred.emit(f"Puzzle load error: {str(e)}")

    @pyqtSlot()
    def next_puzzle(self):
        '''Load next puzzle'''
        self.puzzle_system.next_puzzle()
        self.load_puzzle()

    @pyqtSlot()
    def previous_puzzle(self):
        '''Load previous puzzle'''
        self.puzzle_system.previous_puzzle()
        self.load_puzzle()

    @pyqtSlot()
    def get_puzzle_hint(self):
        '''Get a hint for current puzzle'''
        if self.game_mode != 'puzzle' or not self.current_puzzle:
            self.errorOccurred.emit("No puzzle loaded!")
            return

        hint = self.puzzle_system.get_hint()
        if hint:
            self.errorOccurred.emit(f"Hint: {hint}")  # Use error signal for hint display

    def get_legal_moves(self, position):
        '''
        Get legal moves for a piece at given position

        Args:
            position: (row, col) tuple

        Returns:
            List of legal moves
        '''
        try:
            return self.board.get_legal_moves(position)
        except Exception as e:
            self.errorOccurred.emit(f"Legal moves error: {str(e)}")
            return []

    def get_board_state(self):
        '''
        Get current board state

        Returns:
            2D list representing the board
        '''
        return self.board.state

    def get_current_player(self):
        '''
        Get the color of the player to move

        Returns:
            'white' or 'black'
        '''
        return self.board.to_move

    def is_game_over(self):
        '''
        Check if game is over

        Returns:
            bool
        '''
        return self.board.game_over

    def get_game_result(self):
        '''
        Get game result

        Returns:
            Game result string or None
        '''
        return self.board.game_result

    def cleanup(self):
        '''Cleanup resources (call when closing application)'''
        if self.ai_worker:
            self.ai_worker.stop()
            self.ai_worker.wait()
