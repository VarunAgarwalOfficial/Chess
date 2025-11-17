'''
Chess AI Engine with Advanced Optimizations:
- Minimax algorithm with Alpha-Beta pruning
- Enhanced transposition table with replacement strategy
- Zobrist hashing for fast position comparison
- Advanced move ordering (PV, hash moves, MVV-LVA, killer moves, history heuristic)
- Late Move Reduction (LMR)
- Null Move Pruning
- Aspiration windows
- Quiescence search for tactical positions
- Iterative deepening
- Search extensions (check, passed pawn, recapture)
- Endgame knowledge
- Piece-square tables for positional evaluation
'''

import time
from copy import deepcopy
from .cache_system import TranspositionTable, CacheManager
from .optimizations import MoveOrderingOptimizer, LateMovePruning, NullMovePruning, AspirationWindow
from .advanced_search import EndgameKnowledge, SearchExtensions, SearchOptimizer


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

        # Enhanced transposition table with replacement strategy
        self.transposition_table = TranspositionTable(size_mb=128)

        # Cache manager for all caching systems
        self.cache_manager = CacheManager()

        # Advanced move ordering with killer moves, history, and PV
        self.move_ordering = MoveOrderingOptimizer()

        # Endgame knowledge
        self.endgame_knowledge = EndgameKnowledge()

        # Search optimizer (extensions, etc.)
        self.search_optimizer = SearchOptimizer()

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

        # Check for known endgame positions
        if self.endgame_knowledge.is_simple_endgame(self.board):
            endgame_score = self.endgame_knowledge.evaluate_known_endgame(self.board)
            if endgame_score is not None:
                return endgame_score

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

    def order_moves(self, moves_with_positions, depth):
        '''
        Order moves for better alpha-beta pruning using advanced heuristics
        Priority: PV > Hash > Captures (MVV-LVA) > Killers > History > Other
        '''
        return self.move_ordering.order_moves(moves_with_positions, depth, self.board)

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

        # Order captures by MVV-LVA (depth 0 for quiescence)
        for move, pos in self.order_moves(capture_moves, 0):
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

    def alpha_beta(self, depth, alpha, beta, maximizing_player, null_move_allowed=True, last_move=None, pv_node=True):
        '''
        Alpha-Beta pruning search algorithm with advanced optimizations:
        - Principal Variation Search (PVS) for ~10% speed improvement
        - Enhanced transposition table
        - Null move pruning
        - Late move reduction (LMR)
        - Futility pruning
        - Search extensions
        '''
        self.nodes_searched += 1
        original_alpha = alpha
        in_check = self.board.check

        # Check transposition table
        position_hash = self._hash_position()
        tt_entry = self.transposition_table.probe(position_hash, depth, alpha, beta)
        if tt_entry[2]:  # Hit
            self.transposition_hits += 1
            return tt_entry[0]

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

        # Null Move Pruning
        if null_move_allowed and NullMovePruning.can_use_null_move(self.board, depth, in_check):
            # Make null move (skip turn)
            initial_state = self._save_state()
            self.board.to_move = self.opponent if self.board.to_move == self.color else self.color

            reduction = NullMovePruning.get_null_move_reduction(depth)
            score = -self.alpha_beta(depth - 1 - reduction, -beta, -beta + 1, not maximizing_player, False, None)

            self._restore_state(initial_state)

            if score >= beta:
                return beta

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

        # Futility Pruning: Skip moves at low depths if position is hopeless
        # Only apply at depth 1-3, not in check, and not in PV nodes
        if not pv_node and not in_check and 1 <= depth <= 3:
            futility_margin = [0, 200, 350, 500]  # Margins in centipawns for depth 1-3
            static_eval = self.evaluate_board()

            # Forward futility pruning (for maximizing player)
            if maximizing_player and static_eval + futility_margin[depth] <= alpha:
                # Position is so bad that even with margin, can't improve alpha
                return alpha

            # Reverse futility pruning (for minimizing player)
            if not maximizing_player and static_eval - futility_margin[depth] >= beta:
                # Position is so good that even opponent can't make it worse
                return beta

        # Order moves for better pruning
        ordered_moves = self.order_moves(all_moves, depth)

        best_move = None
        move_count = 0

        if maximizing_player:
            max_eval = float('-inf')
            for move, pos in ordered_moves:
                move_count += 1

                # Save state before move
                initial_state = self._save_state()

                # Make move
                self.board.move(pos, move)

                # Calculate search extension
                extension = self.search_optimizer.should_extend(
                    self.board, move, pos, depth, self.board.check, last_move
                )

                # Late Move Reduction
                reduction = 0
                if LateMovePruning.should_reduce(move, pos, move_count, depth, in_check):
                    reduction = LateMovePruning.get_reduction(move_count, depth)

                # Principal Variation Search (PVS) - ~10% faster than plain alpha-beta
                # Search first move with full window, rest with null window then re-search
                if move_count == 1:
                    # First move: full window search (this is the PV move)
                    new_depth = depth - 1 + extension - reduction
                    eval_score = self.alpha_beta(new_depth, alpha, beta, False, True, move, True)
                else:
                    # Other moves: try null window search first
                    new_depth = depth - 1 + extension - reduction
                    eval_score = self.alpha_beta(new_depth, alpha, alpha + 1, False, True, move, False)

                    # If null window search failed high, re-search with full window
                    if eval_score > alpha and eval_score < beta:
                        eval_score = self.alpha_beta(new_depth, alpha, beta, False, True, move, True)

                # If LMR was used and failed high, re-search at full depth
                if reduction > 0 and eval_score > alpha:
                    eval_score = self.alpha_beta(depth - 1 + extension, alpha, beta, False, True, move, pv_node)

                # Undo move
                self._restore_state(initial_state)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (move, pos)

                alpha = max(alpha, eval_score)

                if beta <= alpha:
                    self.cutoffs += 1
                    # Update killer moves and history
                    self.move_ordering.update_killer(move, pos, depth)
                    self.move_ordering.update_history(move, pos, depth)
                    break  # Beta cutoff

            # Store in transposition table
            if max_eval <= original_alpha:
                flag = TranspositionTable.UPPER_BOUND
            elif max_eval >= beta:
                flag = TranspositionTable.LOWER_BOUND
            else:
                flag = TranspositionTable.EXACT

            self.transposition_table.store(position_hash, depth, max_eval, flag, best_move)

            # Store PV move
            if best_move:
                self.move_ordering.store_pv_move(best_move[0], best_move[1], depth)

            return max_eval
        else:
            min_eval = float('inf')
            for move, pos in ordered_moves:
                move_count += 1

                # Save state before move
                initial_state = self._save_state()

                # Make move
                self.board.move(pos, move)

                # Calculate search extension
                extension = self.search_optimizer.should_extend(
                    self.board, move, pos, depth, self.board.check, last_move
                )

                # Late Move Reduction
                reduction = 0
                if LateMovePruning.should_reduce(move, pos, move_count, depth, in_check):
                    reduction = LateMovePruning.get_reduction(move_count, depth)

                # Principal Variation Search (PVS) for minimizing player
                if move_count == 1:
                    # First move: full window search
                    new_depth = depth - 1 + extension - reduction
                    eval_score = self.alpha_beta(new_depth, alpha, beta, True, True, move, True)
                else:
                    # Other moves: null window search then re-search if needed
                    new_depth = depth - 1 + extension - reduction
                    eval_score = self.alpha_beta(new_depth, beta - 1, beta, True, True, move, False)

                    # If null window search failed low, re-search with full window
                    if eval_score > alpha and eval_score < beta:
                        eval_score = self.alpha_beta(new_depth, alpha, beta, True, True, move, True)

                # If LMR was used and failed low, re-search at full depth
                if reduction > 0 and eval_score < beta:
                    eval_score = self.alpha_beta(depth - 1 + extension, alpha, beta, True, True, move, pv_node)

                # Undo move
                self._restore_state(initial_state)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (move, pos)

                beta = min(beta, eval_score)

                if beta <= alpha:
                    self.cutoffs += 1
                    # Update killer moves and history
                    self.move_ordering.update_killer(move, pos, depth)
                    self.move_ordering.update_history(move, pos, depth)
                    break  # Alpha cutoff

            # Store in transposition table
            if min_eval <= original_alpha:
                flag = TranspositionTable.UPPER_BOUND
            elif min_eval >= beta:
                flag = TranspositionTable.LOWER_BOUND
            else:
                flag = TranspositionTable.EXACT

            self.transposition_table.store(position_hash, depth, min_eval, flag, best_move)

            # Store PV move
            if best_move:
                self.move_ordering.store_pv_move(best_move[0], best_move[1], depth)

            return min_eval

    def get_best_move(self):
        '''
        Find the best move using iterative deepening with aspiration windows
        '''
        print(f"AI ({self.color}) is thinking...")
        start_time = time.time()

        # Reset statistics
        self.nodes_searched = 0
        self.cutoffs = 0
        self.transposition_hits = 0

        # Increment generation for new search
        self.transposition_table.new_search()

        best_move = None
        best_pos = None
        prev_score = 0

        # Determine if we're maximizing (white) or minimizing (black)
        maximizing = (self.color == "white")

        # Iterative deepening with aspiration windows
        for current_depth in range(1, self.max_depth + 1):
            best_score = float('-inf') if maximizing else float('inf')
            current_best_move = None
            current_best_pos = None

            # Get aspiration window based on previous iteration
            alpha, beta = AspirationWindow.get_initial_window(prev_score, current_depth)

            # Re-search with wider window if needed
            search_iterations = 0
            while True:
                search_iterations += 1

                all_moves = self.get_all_moves()
                ordered_moves = self.order_moves(all_moves, current_depth)

                for move, pos in ordered_moves:
                    # Save state
                    initial_state = self._save_state()

                    # Make move
                    self.board.move(pos, move)

                    # Evaluate
                    if maximizing:
                        score = self.alpha_beta(current_depth - 1, alpha, beta, False, True, None)
                        if score > best_score:
                            best_score = score
                            current_best_move = move
                            current_best_pos = pos
                    else:
                        score = self.alpha_beta(current_depth - 1, alpha, beta, True, True, None)
                        if score < best_score:
                            best_score = score
                            current_best_move = move
                            current_best_pos = pos

                    # Restore state
                    self._restore_state(initial_state)

                # Check if we need to re-search with wider window
                if best_score <= alpha:
                    # Fail low - widen alpha
                    alpha, beta = AspirationWindow.widen_window(alpha, beta, "low")
                    continue
                elif best_score >= beta:
                    # Fail high - widen beta
                    alpha, beta = AspirationWindow.widen_window(alpha, beta, "high")
                    continue
                else:
                    # Score within window - done
                    break

            # Update best move for this iteration (silently, no output per depth)
            if current_best_move:
                best_move = current_best_move
                best_pos = current_best_pos
                prev_score = best_score

        elapsed_time = time.time() - start_time

        # Only show final result - concise output
        print(f"AI move: {best_pos} -> {best_move['to']} ({elapsed_time:.2f}s)\n")

        return best_move, best_pos

    def _hash_position(self):
        '''Create a hash of the current position for transposition table using Zobrist hashing'''
        # Use fast Zobrist hash from board
        return self.board.position_hash

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
            'move_log_len': len(self.board.move_log),
            'position_hash': self.board.position_hash
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
        self.board.position_hash = state['position_hash']

        # Remove any moves added during the search
        while len(self.board.move_log) > state['move_log_len']:
            self.board.move_log.pop()
