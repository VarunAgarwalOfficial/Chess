'''
FEN (Forsyth-Edwards Notation) Parser for Chess
Loads chess positions from FEN strings
'''

from .Piece import Piece


def parse_fen(board, fen_string):
    '''
    Parse FEN notation and set up the board

    FEN format: "pieces side castling en_passant halfmove fullmove"
    Example: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    '''
    parts = fen_string.split()

    if len(parts) < 1:
        raise ValueError("Invalid FEN string")

    # Parse board position
    ranks = parts[0].split('/')
    if len(ranks) != 8:
        raise ValueError("FEN must have 8 ranks")

    # Clear the board
    board.state = [[None for _ in range(8)] for _ in range(8)]

    # Piece mapping
    piece_map = {
        'p': ('black', 'pawn'), 'n': ('black', 'knight'), 'b': ('black', 'bishop'),
        'r': ('black', 'rook'), 'q': ('black', 'queen'), 'k': ('black', 'king'),
        'P': ('white', 'pawn'), 'N': ('white', 'knight'), 'B': ('white', 'bishop'),
        'R': ('white', 'rook'), 'Q': ('white', 'queen'), 'K': ('white', 'king')
    }

    # Place pieces on board
    for rank_idx, rank in enumerate(ranks):
        file_idx = 0
        for char in rank:
            if char.isdigit():
                # Empty squares
                file_idx += int(char)
            elif char in piece_map:
                # Place piece
                color, piece_type = piece_map[char]
                board.state[rank_idx][file_idx] = Piece(color, piece_type)

                # Track king positions
                if piece_type == 'king':
                    board.king_positions[color] = (rank_idx, file_idx)

                file_idx += 1
            else:
                raise ValueError(f"Invalid character in FEN: {char}")

    # Parse side to move
    if len(parts) >= 2:
        board.to_move = "white" if parts[1] == 'w' else "black"
    else:
        board.to_move = "white"

    # Parse castling rights
    if len(parts) >= 3:
        castling_str = parts[2]
        board.castling = {
            "white": {
                "allowed": 'K' in castling_str or 'Q' in castling_str,
                "king": 'K' in castling_str,
                "queen": 'Q' in castling_str
            },
            "black": {
                "allowed": 'k' in castling_str or 'q' in castling_str,
                "king": 'k' in castling_str,
                "queen": 'q' in castling_str
            }
        }
    else:
        # Default castling rights
        board.castling = {
            "white": {"allowed": True, "king": True, "queen": True},
            "black": {"allowed": True, "king": True, "queen": True}
        }

    # Reset game state
    board.check = False
    board.checks = []
    board.double_check = False
    board.game_over = False
    board.game_result = None
    board.move_log = []

    # Update position hash
    board.position_hash = board.zobrist.hash_position(board)

    return board


def fen_to_board(fen_string):
    '''
    Create a new Board instance from FEN notation
    Returns a Board object set up according to the FEN
    '''
    from game import Board
    board = Board()
    return parse_fen(board, fen_string)
