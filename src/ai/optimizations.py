'''
Performance Optimizations for Chess Engine
Advanced techniques to improve speed and efficiency
'''

class BitboardOptimizer:
    '''
    Bitboard representation for faster move generation
    Each piece type represented as 64-bit integer
    '''

    def __init__(self):
        # Initialize bitboards for each piece type and color
        self.white_pawns = 0
        self.white_knights = 0
        self.white_bishops = 0
        self.white_rooks = 0
        self.white_queens = 0
        self.white_king = 0

        self.black_pawns = 0
        self.black_knights = 0
        self.black_bishops = 0
        self.black_rooks = 0
        self.black_queens = 0
        self.black_king = 0

        self.all_white = 0
        self.all_black = 0
        self.all_pieces = 0

    def set_bit(self, square):
        '''Set a bit at given square (0-63)'''
        return 1 << square

    def get_bit(self, bitboard, square):
        '''Get bit value at square'''
        return (bitboard >> square) & 1

    def clear_bit(self, bitboard, square):
        '''Clear bit at square'''
        return bitboard & ~(1 << square)

    def pop_count(self, bitboard):
        '''Count number of set bits (Brian Kernighan's algorithm)'''
        count = 0
        while bitboard:
            bitboard &= bitboard - 1
            count += 1
        return count

    def get_lsb(self, bitboard):
        '''Get least significant bit position'''
        if bitboard == 0:
            return -1
        return (bitboard & -bitboard).bit_length() - 1


class MoveOrderingOptimizer:
    '''
    Advanced move ordering for better alpha-beta pruning
    '''

    def __init__(self):
        # Killer moves: moves that caused cutoffs at same depth
        self.killer_moves = [[None, None] for _ in range(64)]

        # History heuristic: moves that historically caused cutoffs
        self.history_scores = {}

        # Principal variation: best line from previous search
        self.pv_table = {}

    def order_moves(self, moves, depth, board):
        '''
        Order moves for optimal alpha-beta pruning
        Priority:
        1. PV move (from previous iteration)
        2. Hash move (from transposition table)
        3. Winning captures (MVV-LVA)
        4. Killer moves
        5. History heuristic
        6. Other moves
        '''
        scored_moves = []

        for move, pos in moves:
            score = 0

            # PV move gets highest priority
            if self.is_pv_move(move, pos, depth):
                score += 10000000

            # Captures scored by MVV-LVA
            target = board.state[move["to"][0]][move["to"][1]]
            if target:
                piece_values = {
                    "pawn": 100, "knight": 320, "bishop": 330,
                    "rook": 500, "queen": 900, "king": 20000
                }
                attacker = board.state[pos[0]][pos[1]]
                victim_value = piece_values[target.type]
                attacker_value = piece_values[attacker.type]
                score += (victim_value * 10 - attacker_value) * 1000

            # Promotions are valuable
            if move["special"] == "promotion":
                score += 9000

            # Killer moves
            if self.is_killer_move(move, pos, depth):
                score += 8000

            # History heuristic
            history_key = self.get_history_key(move, pos)
            if history_key in self.history_scores:
                score += self.history_scores[history_key]

            scored_moves.append((score, move, pos))

        # Sort by score descending
        scored_moves.sort(key=lambda x: x[0], reverse=True)

        return [(m, p) for _, m, p in scored_moves]

    def update_killer(self, move, pos, depth):
        '''Store killer move at this depth'''
        if depth < 64:
            # Shift and add new killer
            if self.killer_moves[depth][0] != (move, pos):
                self.killer_moves[depth][1] = self.killer_moves[depth][0]
                self.killer_moves[depth][0] = (move, pos)

    def is_killer_move(self, move, pos, depth):
        '''Check if move is a killer move'''
        if depth < 64:
            return (move, pos) in self.killer_moves[depth]
        return False

    def update_history(self, move, pos, depth):
        '''Update history score for this move'''
        key = self.get_history_key(move, pos)
        if key not in self.history_scores:
            self.history_scores[key] = 0
        self.history_scores[key] += depth * depth

    def get_history_key(self, move, pos):
        '''Generate key for history table'''
        return (pos, move["to"])

    def is_pv_move(self, move, pos, depth):
        '''Check if move is from principal variation'''
        key = (depth, pos)
        return key in self.pv_table and self.pv_table[key] == move["to"]

    def store_pv_move(self, move, pos, depth):
        '''Store principal variation move'''
        self.pv_table[(depth, pos)] = move["to"]


class ZobristHashing:
    '''
    Zobrist hashing for fast position comparison
    Used for transposition table and repetition detection
    '''

    def __init__(self):
        import random
        random.seed(42)  # Deterministic for consistency

        # Random numbers for each piece at each square
        self.piece_keys = {}
        pieces = ["pawn", "knight", "bishop", "rook", "queen", "king"]
        colors = ["white", "black"]

        for color in colors:
            for piece in pieces:
                self.piece_keys[(color, piece)] = [
                    random.getrandbits(64) for _ in range(64)
                ]

        # Random numbers for castling rights
        self.castling_keys = {
            ("white", "king"): random.getrandbits(64),
            ("white", "queen"): random.getrandbits(64),
            ("black", "king"): random.getrandbits(64),
            ("black", "queen"): random.getrandbits(64)
        }

        # Random number for side to move
        self.side_to_move_key = random.getrandbits(64)

        # Random numbers for en passant file
        self.en_passant_keys = [random.getrandbits(64) for _ in range(8)]

    def hash_position(self, board):
        '''Generate Zobrist hash for current position'''
        hash_value = 0

        # Hash pieces
        for row in range(8):
            for col in range(8):
                piece = board.state[row][col]
                if piece:
                    square = row * 8 + col
                    hash_value ^= self.piece_keys[(piece.color, piece.type)][square]

        # Hash castling rights
        for color in ["white", "black"]:
            if board.castling[color]["king"]:
                hash_value ^= self.castling_keys[(color, "king")]
            if board.castling[color]["queen"]:
                hash_value ^= self.castling_keys[(color, "queen")]

        # Hash side to move
        if board.to_move == "black":
            hash_value ^= self.side_to_move_key

        return hash_value

    def update_hash_move(self, hash_value, move, piece, captured, color):
        '''Incrementally update hash after a move'''
        # Remove piece from source square
        from_square = move["from"][0] * 8 + move["from"][1]
        hash_value ^= self.piece_keys[(color, piece.type)][from_square]

        # Add piece to destination square
        to_square = move["to"][0] * 8 + move["to"][1]
        hash_value ^= self.piece_keys[(color, piece.type)][to_square]

        # Remove captured piece if any
        if captured:
            hash_value ^= self.piece_keys[(captured.color, captured.type)][to_square]

        # Flip side to move
        hash_value ^= self.side_to_move_key

        return hash_value


class LateMovePruning:
    '''
    Late move reduction and pruning techniques
    '''

    @staticmethod
    def should_reduce(move, pos, move_number, depth, in_check):
        '''
        Determine if move should get reduced search depth

        Late Move Reduction (LMR): moves later in the list are
        less likely to be good, so search them at reduced depth
        '''
        if in_check:
            return False  # Never reduce in check

        if depth < 3:
            return False  # Don't reduce at low depths

        # Don't reduce captures, promotions, or special moves
        if move["special"] is not None:
            return False

        # Reduce moves after the first few
        if move_number > 4:
            return True

        return False

    @staticmethod
    def get_reduction(move_number, depth):
        '''Calculate reduction amount based on move number and depth'''
        if move_number < 4:
            return 0
        elif move_number < 8:
            return 1
        else:
            return min(2, depth - 2)


class NullMovePruning:
    '''
    Null move pruning: skip a move to verify if position is so good
    that even giving opponent a free move doesn't help them
    '''

    @staticmethod
    def can_use_null_move(board, depth, in_check):
        '''Determine if null move pruning is applicable'''
        if in_check:
            return False  # Can't skip move in check

        if depth < 3:
            return False  # Not useful at low depths

        # Count non-pawn material
        material_count = 0
        for row in range(8):
            for col in range(8):
                piece = board.state[row][col]
                if piece and piece.color == board.to_move and piece.type != "pawn":
                    material_count += 1

        # Don't use in endgame (zugzwang risk)
        if material_count < 3:
            return False

        return True

    @staticmethod
    def get_null_move_reduction(depth):
        '''Calculate depth reduction for null move search'''
        return min(3, depth - 1)


class AspirationWindow:
    '''
    Aspiration window for faster alpha-beta search
    Start with narrow window, widen if needed
    '''

    @staticmethod
    def get_initial_window(prev_score, depth):
        '''Get aspiration window based on previous score'''
        if depth <= 2:
            # Use full window for shallow searches
            return (float('-inf'), float('inf'))

        # Narrow window around previous score
        window_size = 50
        alpha = prev_score - window_size
        beta = prev_score + window_size

        return (alpha, beta)

    @staticmethod
    def widen_window(alpha, beta, fail_type):
        '''Widen window after fail-high or fail-low'''
        if fail_type == "high":
            # Failed high: widen beta
            beta = float('inf')
        else:
            # Failed low: widen alpha
            alpha = float('-inf')

        return (alpha, beta)


# Performance monitoring
class PerformanceMonitor:
    '''Track and analyze engine performance'''

    def __init__(self):
        self.nodes_per_second = 0
        self.total_nodes = 0
        self.search_time = 0
        self.branching_factor = 0
        self.cutoff_ratio = 0
        self.cache_hit_ratio = 0

    def update_stats(self, nodes, time_elapsed, cutoffs, total_moves, cache_hits, cache_lookups):
        '''Update performance statistics'''
        self.total_nodes = nodes
        self.search_time = time_elapsed

        if time_elapsed > 0:
            self.nodes_per_second = int(nodes / time_elapsed)

        if total_moves > 0:
            self.cutoff_ratio = cutoffs / total_moves

        if cache_lookups > 0:
            self.cache_hit_ratio = cache_hits / cache_lookups

    def print_stats(self):
        '''Print performance statistics'''
        print(f"Nodes: {self.total_nodes:,}")
        print(f"Time: {self.search_time:.2f}s")
        print(f"NPS: {self.nodes_per_second:,}")
        print(f"Cutoff ratio: {self.cutoff_ratio:.2%}")
        print(f"Cache hit ratio: {self.cache_hit_ratio:.2%}")
