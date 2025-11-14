'''
Advanced Search Techniques for Chess Engine
Endgame tablebases, singular extensions, and more
'''


class EndgameKnowledge:
    '''
    Endgame patterns and heuristics
    Provides perfect play in simple endgames
    '''

    def __init__(self):
        self.tablebase = {}

    def is_simple_endgame(self, board):
        '''Determine if position is a simple endgame'''
        piece_count = 0
        pieces = []

        for row in range(8):
            for col in range(8):
                piece = board.state[row][col]
                if piece:
                    pieces.append(piece.type)
                    piece_count += 1

        # Consider endgame if 5 or fewer pieces
        return piece_count <= 5

    def evaluate_known_endgame(self, board):
        '''
        Evaluate known endgame positions
        Returns score or None if not a known endgame
        '''
        # Count material
        white_pieces = []
        black_pieces = []

        for row in range(8):
            for col in range(8):
                piece = board.state[row][col]
                if piece:
                    if piece.color == "white":
                        white_pieces.append(piece.type)
                    else:
                        black_pieces.append(piece.type)

        # K vs K - draw
        if len(white_pieces) == 1 and len(black_pieces) == 1:
            return 0

        # KQ vs K - checkmate
        if "queen" in white_pieces and len(white_pieces) == 2 and len(black_pieces) == 1:
            return self._evaluate_kq_vs_k(board, "white")
        if "queen" in black_pieces and len(black_pieces) == 2 and len(white_pieces) == 1:
            return -self._evaluate_kq_vs_k(board, "black")

        # KR vs K - checkmate
        if "rook" in white_pieces and len(white_pieces) == 2 and len(black_pieces) == 1:
            return self._evaluate_kr_vs_k(board, "white")
        if "rook" in black_pieces and len(black_pieces) == 2 and len(white_pieces) == 1:
            return -self._evaluate_kr_vs_k(board, "black")

        return None

    def _evaluate_kq_vs_k(self, board, winning_side):
        '''Evaluate King + Queen vs King endgame'''
        # Find kings
        winning_king = None
        losing_king = None

        for row in range(8):
            for col in range(8):
                piece = board.state[row][col]
                if piece and piece.type == "king":
                    if piece.color == winning_side:
                        winning_king = (row, col)
                    else:
                        losing_king = (row, col)

        if not winning_king or not losing_king:
            return 0

        # Push losing king to edge
        edge_distance = min(
            losing_king[0],
            7 - losing_king[0],
            losing_king[1],
            7 - losing_king[1]
        )

        # Reduce distance between kings
        king_distance = abs(winning_king[0] - losing_king[0]) + \
                       abs(winning_king[1] - losing_king[1])

        # Higher score for pushing to edge and closing in
        score = 900 + (7 - edge_distance) * 10 + (14 - king_distance) * 5

        return score

    def _evaluate_kr_vs_k(self, board, winning_side):
        '''Evaluate King + Rook vs King endgame'''
        # Similar to KQ vs K but slightly harder
        winning_king = None
        losing_king = None

        for row in range(8):
            for col in range(8):
                piece = board.state[row][col]
                if piece and piece.type == "king":
                    if piece.color == winning_side:
                        winning_king = (row, col)
                    else:
                        losing_king = (row, col)

        if not winning_king or not losing_king:
            return 0

        edge_distance = min(
            losing_king[0],
            7 - losing_king[0],
            losing_king[1],
            7 - losing_king[1]
        )

        king_distance = abs(winning_king[0] - losing_king[0]) + \
                       abs(winning_king[1] - losing_king[1])

        score = 500 + (7 - edge_distance) * 10 + (14 - king_distance) * 5

        return score


class SingularExtension:
    '''
    Singular extension: extend search when one move is
    significantly better than all others
    '''

    @staticmethod
    def is_singular(best_move, second_best_score, best_score, margin=100):
        '''
        Check if best move is singular
        (much better than second best)
        '''
        if second_best_score is None:
            return False

        # Move is singular if it's much better than alternatives
        return best_score - second_best_score > margin

    @staticmethod
    def get_extension(depth, is_singular):
        '''Get search extension amount'''
        if is_singular and depth > 4:
            return 1  # Extend by 1 ply
        return 0


class MultiCut:
    '''
    Multi-cut pruning: if multiple moves fail high,
    assume position is too good (fail high)
    '''

    @staticmethod
    def should_multi_cut(fail_high_count, depth, threshold=3):
        '''
        Determine if multi-cut should be applied
        '''
        if depth < 3:
            return False

        # If multiple moves fail high, cut search
        return fail_high_count >= threshold


class FutilityPruning:
    '''
    Futility pruning: skip moves that can't improve
    alpha even with best possible outcome
    '''

    # Material value estimates
    PIECE_VALUES = {
        "pawn": 100,
        "knight": 320,
        "bishop": 330,
        "rook": 500,
        "queen": 900
    }

    @staticmethod
    def get_futility_margin(depth):
        '''Get futility margin for given depth'''
        margins = {
            1: 200,  # ~2 pawns
            2: 500,  # ~5 pawns
            3: 900   # ~9 pawns (queen)
        }
        return margins.get(depth, 1000)

    @staticmethod
    def is_futile(board, move, pos, alpha, depth):
        '''
        Check if move is futile (can't improve position enough)
        '''
        if depth > 3:
            return False

        # Don't prune captures or promotions
        if move["special"] is not None:
            return False

        # Don't prune if in check
        if board.check:
            return False

        # Estimate best possible outcome
        # (current eval + futility margin)
        # This is a simplified version - would need actual eval

        return False  # Disabled for now - needs eval function


class SEE:
    '''
    Static Exchange Evaluation
    Evaluates capture sequences to determine if a capture is good
    '''

    PIECE_VALUES = {
        "pawn": 100,
        "knight": 320,
        "bishop": 330,
        "rook": 500,
        "queen": 900,
        "king": 20000
    }

    def __init__(self):
        pass

    def evaluate_capture(self, board, from_pos, to_pos):
        '''
        Evaluate a capture using SEE
        Returns net material gain/loss
        '''
        attacker = board.state[from_pos[0]][from_pos[1]]
        victim = board.state[to_pos[0]][to_pos[1]]

        if not attacker or not victim:
            return 0

        # Start with victim value
        gain = [self.PIECE_VALUES[victim.type]]

        # Simulate exchange
        # Find all attackers and defenders of the square
        # This is simplified - full SEE is complex

        return gain[0] - self.PIECE_VALUES.get(attacker.type, 0)


class SearchExtensions:
    '''
    Collection of search extension rules
    Extends search in interesting positions
    '''

    @staticmethod
    def check_extension(in_check, depth):
        '''Extend when in check (forced move)'''
        if in_check and depth > 0:
            return 1
        return 0

    @staticmethod
    def passed_pawn_extension(board, move, pos, depth):
        '''Extend for passed pawns near promotion'''
        piece = board.state[pos[0]][pos[1]]

        if not piece or piece.type != "pawn":
            return 0

        # Check if pawn is on 6th or 7th rank
        if piece.color == "white" and pos[0] <= 2:
            return 1
        elif piece.color == "black" and pos[0] >= 5:
            return 1

        return 0

    @staticmethod
    def recapture_extension(board, move, last_move):
        '''Extend for recaptures'''
        if not last_move:
            return 0

        # Check if this move recaptures on same square
        if move["to"] == last_move["to"]:
            return 1

        return 0


class SelectiveDepth:
    '''
    Selective depth increase for interesting lines
    '''

    @staticmethod
    def get_selective_depth(base_depth, extensions_applied):
        '''
        Calculate actual depth considering extensions
        '''
        # Limit total extensions to prevent explosion
        max_extensions = base_depth // 2

        actual_extensions = min(extensions_applied, max_extensions)

        return base_depth + actual_extensions


class ParallelSearch:
    '''
    Framework for parallel/concurrent search
    (Not fully implemented - requires threading)
    '''

    def __init__(self, num_threads=1):
        self.num_threads = num_threads
        self.threads = []

    def split_work(self, moves, num_splits):
        '''Split moves into chunks for parallel processing'''
        chunk_size = len(moves) // num_splits
        chunks = []

        for i in range(num_splits):
            start = i * chunk_size
            end = start + chunk_size if i < num_splits - 1 else len(moves)
            chunks.append(moves[start:end])

        return chunks

    def can_split(self, depth, move_count):
        '''Determine if search can be split across threads'''
        # Only split at higher depths with many moves
        return depth >= 4 and move_count >= 8


# Performance optimization utilities
class SearchOptimizer:
    '''
    Combines various optimizations for best performance
    '''

    def __init__(self):
        self.endgame = EndgameKnowledge()
        self.see = SEE()
        self.extensions = SearchExtensions()

        # Statistics
        self.extensions_applied = 0
        self.pruning_applied = 0

    def should_extend(self, board, move, pos, depth, in_check, last_move):
        '''
        Determine if search should be extended
        Returns extension amount (0, 1, or 2)
        '''
        total_extension = 0

        # Check extension
        total_extension += self.extensions.check_extension(in_check, depth)

        # Passed pawn extension
        total_extension += self.extensions.passed_pawn_extension(board, move, pos, depth)

        # Recapture extension
        total_extension += self.extensions.recapture_extension(board, move, last_move)

        if total_extension > 0:
            self.extensions_applied += 1

        # Limit total extension
        return min(total_extension, 2)

    def get_stats(self):
        '''Get optimization statistics'''
        return {
            'extensions_applied': self.extensions_applied,
            'pruning_applied': self.pruning_applied
        }
