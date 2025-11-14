'''
Chess AI Engine with:
- Minimax algorithm with Alpha-Beta pruning
- Piece-square tables for positional evaluation
- Move ordering (MVV-LVA - Most Valuable Victim, Least Valuable Attacker)
- Quiescence search for tactical positions
- Iterative deepening
- Transposition table for caching positions
'''

import time
from copy import deepcopy


class AI:
    def __init__(self, board, color="black", difficulty="medium"):
        self.board = board
        self.color = color
        self.opponent = "white" if color == "black" else "black"
        self.difficulty = difficulty

        # Set search depth based on difficulty
        self.max_depth = {
            "easy": 2,
            "medium": 3,
            "hard": 4,
            "expert": 5
        }.get(difficulty, 3)

        # Transposition table for caching evaluated positions
        self.transposition_table = {}

        # Killer moves heuristic (moves that caused cutoffs)
        self.killer_moves = [[None, None] for _ in range(10)]

        # Material values (centipawns)
        self.piece_values = {
            "pawn": 100,
            "knight": 320,
            "bishop": 330,
            "rook": 500,
            "queen": 900,
            "king": 20000
        }

        # Piece-Square Tables (PST) - values for piece positioning
        # White's perspective (flip for black)

        self.pawn_table = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ]

        self.knight_table = [
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ]

        self.bishop_table = [
            [-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0, 10, 10, 10, 10,  0,-10],
            [-10, 10, 10, 10, 10, 10, 10,-10],
            [-10,  5,  0,  0,  0,  0,  5,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]
        ]

        self.rook_table = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [5, 10, 10, 10, 10, 10, 10,  5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [0,  0,  0,  5,  5,  0,  0,  0]
        ]

        self.queen_table = [
            [-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [-5,  0,  5,  5,  5,  5,  0, -5],
            [0,  0,  5,  5,  5,  5,  0, -5],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]
        ]

        self.king_middlegame_table = [
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [20, 20,  0,  0,  0,  0, 20, 20],
            [20, 30, 10,  0,  0, 10, 30, 20]
        ]

        self.king_endgame_table = [
            [-50,-40,-30,-20,-20,-30,-40,-50],
            [-30,-20,-10,  0,  0,-10,-20,-30],
            [-30,-10, 20, 30, 30, 20,-10,-30],
            [-30,-10, 30, 40, 40, 30,-10,-30],
            [-30,-10, 30, 40, 40, 30,-10,-30],
            [-30,-10, 20, 30, 30, 20,-10,-30],
            [-30,-30,  0,  0,  0,  0,-30,-30],
            [-50,-30,-30,-30,-30,-30,-30,-50]
        ]

        self.piece_square_tables = {
            "pawn": self.pawn_table,
            "knight": self.knight_table,
            "bishop": self.bishop_table,
            "rook": self.rook_table,
            "queen": self.queen_table,
            "king": self.king_middlegame_table
        }

        # Statistics
        self.nodes_searched = 0
        self.cutoffs = 0
        self.transposition_hits = 0

    def get_piece_value(self, piece, row, col):
        '''Get the value of a piece including its positional bonus'''
        if not piece:
            return 0

        value = self.piece_values[piece.type]

        # Get positional bonus from piece-square table
        table = self.piece_square_tables[piece.type]

        # Flip the table for black pieces
        if piece.color == "white":
            positional_value = table[row][col]
        else:
            positional_value = table[7 - row][col]

        return value + positional_value

    def evaluate_board(self):
        '''
        Evaluate the current board position
        Positive scores favor white, negative favor black
        '''
        if self.board.game_over:
            if self.board.game_result == "checkmate_white":
                return 100000
            elif self.board.game_result == "checkmate_black":
                return -100000
            else:
                return 0  # Draw

        score = 0

        # Material and positional evaluation
        for row in range(8):
            for col in range(8):
                piece = self.board.state[row][col]
                if piece:
                    piece_score = self.get_piece_value(piece, row, col)
                    if piece.color == "white":
                        score += piece_score
                    else:
                        score -= piece_score

        # Mobility bonus (number of legal moves)
        # Commented out for performance - can be enabled for stronger play
        # white_mobility = sum(len(self.board.get_legal_moves((r, c)))
        #                     for r in range(8) for c in range(8)
        #                     if self.board.state[r][c] and self.board.state[r][c].color == "white")
        # black_mobility = sum(len(self.board.get_legal_moves((r, c)))
        #                     for r in range(8) for c in range(8)
        #                     if self.board.state[r][c] and self.board.state[r][c].color == "black")
        # score += (white_mobility - black_mobility) * 10

        return score

    def order_moves(self, moves_with_positions):
        '''
        Order moves for better alpha-beta pruning
        Priority: Captures (MVV-LVA) > Killer moves > Other moves
        '''
        def move_score(move_data):
            move, pos = move_data
            score = 0

            # Check if move is a capture
            target_square = self.board.state[move["to"][0]][move["to"][1]]
            if target_square:
                # MVV-LVA: Most Valuable Victim - Least Valuable Attacker
                moving_piece = self.board.state[pos[0]][pos[1]]
                victim_value = self.piece_values[target_square.type]
                attacker_value = self.piece_values[moving_piece.type]
                score += (victim_value - attacker_value / 10) * 10000

            # Check for special moves
            if move["special"] in ["promotion", "KSC", "QSC"]:
                score += 8000

            # Check if it's a killer move
            # (Simplified - full implementation would check against killer_moves table)

            return score

        return sorted(moves_with_positions, key=move_score, reverse=True)

    def get_all_moves(self):
        '''Get all legal moves for the current player'''
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.state[row][col]
                if piece and piece.color == self.board.to_move:
                    piece_moves = self.board.get_legal_moves((row, col))
                    for move in piece_moves:
                        moves.append((move, (row, col)))
        return moves

    def quiescence_search(self, alpha, beta, depth=0):
        '''
        Quiescence search to avoid horizon effect
        Only searches captures and checks
        '''
        self.nodes_searched += 1

        # Stand pat score
        stand_pat = self.evaluate_board()

        if depth >= 5:  # Limit quiescence depth
            return stand_pat

        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        # Only consider captures
        all_moves = self.get_all_moves()
        capture_moves = [(move, pos) for move, pos in all_moves
                        if self.board.state[move["to"][0]][move["to"][1]] is not None]

        for move, pos in self.order_moves(capture_moves):
            # Make move
            initial_state = self._save_state()
            self.board.move(pos, move)

            score = -self.quiescence_search(-beta, -alpha, depth + 1)

            # Undo move
            self._restore_state(initial_state)

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

        return alpha

    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        '''
        Alpha-Beta pruning search algorithm
        Returns the best evaluation score for the current position
        '''
        self.nodes_searched += 1

        # Check transposition table
        position_hash = self._hash_position()
        if position_hash in self.transposition_table:
            cached_depth, cached_score = self.transposition_table[position_hash]
            if cached_depth >= depth:
                self.transposition_hits += 1
                return cached_score

        # Terminal node (depth 0 or game over)
        if depth == 0:
            # Use quiescence search at leaf nodes
            return self.quiescence_search(alpha, beta)

        # Check for game over
        result = self.board.get_game_result()
        if result:
            if result == "checkmate_white":
                return 100000
            elif result == "checkmate_black":
                return -100000
            else:
                return 0  # Draw

        # Get all legal moves
        all_moves = self.get_all_moves()

        # Checkmate or stalemate
        if not all_moves:
            if self.board.check:
                # Checkmate
                return -100000 if maximizing_player else 100000
            else:
                # Stalemate
                return 0

        # Order moves for better pruning
        ordered_moves = self.order_moves(all_moves)

        if maximizing_player:
            max_eval = float('-inf')
            for move, pos in ordered_moves:
                # Save state before move
                initial_state = self._save_state()

                # Make move
                self.board.move(pos, move)

                # Recursive call
                eval_score = self.alpha_beta(depth - 1, alpha, beta, False)

                # Undo move
                self._restore_state(initial_state)

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                if beta <= alpha:
                    self.cutoffs += 1
                    break  # Beta cutoff

            # Store in transposition table
            self.transposition_table[position_hash] = (depth, max_eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move, pos in ordered_moves:
                # Save state before move
                initial_state = self._save_state()

                # Make move
                self.board.move(pos, move)

                # Recursive call
                eval_score = self.alpha_beta(depth - 1, alpha, beta, True)

                # Undo move
                self._restore_state(initial_state)

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                if beta <= alpha:
                    self.cutoffs += 1
                    break  # Alpha cutoff

            # Store in transposition table
            self.transposition_table[position_hash] = (depth, min_eval)
            return min_eval

    def get_best_move(self):
        '''
        Find the best move using iterative deepening and alpha-beta pruning
        '''
        print(f"\n=== AI ({self.color}) thinking (Difficulty: {self.difficulty}, Depth: {self.max_depth}) ===")
        start_time = time.time()

        # Reset statistics
        self.nodes_searched = 0
        self.cutoffs = 0
        self.transposition_hits = 0

        best_move = None
        best_pos = None

        # Determine if we're maximizing (white) or minimizing (black)
        maximizing = (self.color == "white")

        # Iterative deepening
        for current_depth in range(1, self.max_depth + 1):
            best_score = float('-inf') if maximizing else float('inf')
            current_best_move = None
            current_best_pos = None

            all_moves = self.get_all_moves()
            ordered_moves = self.order_moves(all_moves)

            for move, pos in ordered_moves:
                # Save state
                initial_state = self._save_state()

                # Make move
                self.board.move(pos, move)

                # Evaluate
                if maximizing:
                    score = self.alpha_beta(current_depth - 1, float('-inf'), float('inf'), False)
                    if score > best_score:
                        best_score = score
                        current_best_move = move
                        current_best_pos = pos
                else:
                    score = self.alpha_beta(current_depth - 1, float('-inf'), float('inf'), True)
                    if score < best_score:
                        best_score = score
                        current_best_move = move
                        current_best_pos = pos

                # Restore state
                self._restore_state(initial_state)

            # Update best move for this iteration
            if current_best_move:
                best_move = current_best_move
                best_pos = current_best_pos
                print(f"Depth {current_depth}: Score = {best_score}, Move = {best_pos} -> {best_move['to']}")

        elapsed_time = time.time() - start_time
        print(f"Search completed in {elapsed_time:.2f}s")
        print(f"Nodes searched: {self.nodes_searched}")
        print(f"Cutoffs: {self.cutoffs}")
        print(f"Transposition hits: {self.transposition_hits}")
        print(f"Best move: {best_pos} -> {best_move['to']}\n")

        return best_move, best_pos

    def _hash_position(self):
        '''Create a hash of the current position for transposition table'''
        position = []
        for row in range(8):
            for col in range(8):
                piece = self.board.state[row][col]
                if piece:
                    position.append((row, col, piece.color, piece.type))
        position.append(self.board.to_move)
        return tuple(position)

    def _save_state(self):
        '''Save the current board state'''
        return {
            'state': [[piece for piece in row] for row in self.board.state],
            'to_move': self.board.to_move,
            'castling': deepcopy(self.board.castling),
            'king_positions': self.board.king_positions.copy(),
            'check': self.board.check,
            'checks': self.board.checks.copy(),
            'double_check': self.board.double_check,
            'game_over': self.board.game_over,
            'game_result': self.board.game_result,
            'move_log_len': len(self.board.move_log)
        }

    def _restore_state(self, state):
        '''Restore a saved board state'''
        self.board.state = state['state']
        self.board.to_move = state['to_move']
        self.board.castling = state['castling']
        self.board.king_positions = state['king_positions']
        self.board.check = state['check']
        self.board.checks = state['checks']
        self.board.double_check = state['double_check']
        self.board.game_over = state['game_over']
        self.board.game_result = state['game_result']

        # Remove any moves added during the search
        while len(self.board.move_log) > state['move_log_len']:
            self.board.move_log.pop()
