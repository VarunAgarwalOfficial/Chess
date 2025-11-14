'''
Comprehensive tests for Chess game
Tests checkmate, stalemate, AI, and game mechanics
'''

from Game import Board
from Game.Piece import Piece
from ai import AI

def test_checkmate():
    '''Test checkmate detection'''
    print("\n=== Testing Checkmate Detection ===")

    # Fool's Mate (fastest checkmate)
    board = Board()

    # f3
    board.move((6, 5), {"to": (5, 5), "special": None})
    # e5
    board.move((1, 4), {"to": (3, 4), "special": None})
    # g4
    board.move((6, 6), {"to": (4, 6), "special": None})
    # Qh4# (checkmate)
    board.move((0, 3), {"to": (4, 7), "special": None})

    print(f"Board in check: {board.check}")
    print(f"Board checkmate: {board.is_checkmate()}")
    print(f"Game over: {board.game_over}")
    print(f"Game result: {board.game_result}")

    assert board.is_checkmate(), "Failed: Fool's Mate should be checkmate!"
    assert board.game_result == "checkmate_black", "Failed: Black should win!"
    print("✓ Fool's Mate checkmate detected correctly")

    return True

def test_stalemate():
    '''Test stalemate detection'''
    print("\n=== Testing Stalemate Detection ===")

    # Create a stalemate position manually
    board = Board()

    # Clear the board
    for i in range(8):
        for j in range(8):
            board.state[i][j] = None

    # Set up stalemate position: black king in corner with white king and queen blocking
    # Black king on a8, white king on c7, white queen on b6
    board.state[0][0] = Piece("black", "king")  # a8
    board.state[1][2] = Piece("white", "king")  # c7
    board.state[2][1] = Piece("white", "queen")  # b6

    board.king_positions["white"] = (1, 2)
    board.king_positions["black"] = (0, 0)
    board.to_move = "black"

    # Check for stalemate
    is_stale = board.is_stalemate()
    print(f"Board in check: {board.check}")
    print(f"Board stalemate: {is_stale}")

    # Get legal moves for black king
    legal_moves = board.get_legal_moves((0, 0))
    print(f"Legal moves for black king: {len(legal_moves)}")

    assert is_stale, "Failed: Should be stalemate!"
    print("✓ Stalemate detected correctly")

    return True

def test_insufficient_material():
    '''Test draw by insufficient material'''
    print("\n=== Testing Insufficient Material ===")

    # King vs King
    board = Board()
    for i in range(8):
        for j in range(8):
            board.state[i][j] = None

    board.state[7][4] = Piece("white", "king")
    board.state[0][4] = Piece("black", "king")
    board.king_positions["white"] = (7, 4)
    board.king_positions["black"] = (0, 4)

    assert board.is_insufficient_material(), "Failed: K vs K should be insufficient material!"
    print("✓ K vs K insufficient material detected")

    # King + Bishop vs King
    board.state[7][5] = Piece("white", "bishop")
    assert board.is_insufficient_material(), "Failed: K+B vs K should be insufficient material!"
    print("✓ K+B vs K insufficient material detected")

    return True

def test_ai_evaluation():
    '''Test AI evaluation function'''
    print("\n=== Testing AI Evaluation ===")

    board = Board()
    ai = AI(board, color="black", difficulty="easy")

    # Starting position should be roughly equal (around 0)
    eval_score = ai.evaluate_board()
    print(f"Starting position evaluation: {eval_score}")
    assert abs(eval_score) < 200, f"Starting position should be roughly equal, got {eval_score}"
    print("✓ Starting position evaluated correctly")

    # Position with white ahead (white has extra queen)
    board.state[0][3] = None  # Remove black queen
    eval_score = ai.evaluate_board()
    print(f"White ahead by queen evaluation: {eval_score}")
    assert eval_score > 700, f"White should be ahead by ~900, got {eval_score}"
    print("✓ Material advantage evaluated correctly")

    return True

def test_ai_move_generation():
    '''Test AI can generate valid moves'''
    print("\n=== Testing AI Move Generation ===")

    board = Board()
    ai = AI(board, color="white", difficulty="easy")

    # Get best move
    print("AI thinking...")
    move, pos = ai.get_best_move()

    print(f"AI chose to move from {pos} to {move['to']}")
    assert move is not None, "AI should find a move!"
    assert pos is not None, "AI should provide starting position!"
    print("✓ AI generated a valid move")

    # Verify the move is legal
    legal_moves = board.get_legal_moves(pos)
    assert move in legal_moves, "AI move should be legal!"
    print("✓ AI move is legal")

    return True

def test_special_moves():
    '''Test special moves: castling, en passant, promotion'''
    print("\n=== Testing Special Moves ===")

    # Test En Passant
    board = Board()

    # Set up en passant position
    # Move white pawn from e2 to e4
    board.move((6, 4), {"to": (4, 4), "special": None})
    # Move black pawn from a7 to a6
    board.move((1, 0), {"to": (2, 0), "special": None})
    # Move white pawn from e4 to e5
    board.move((4, 4), {"to": (3, 4), "special": None})
    # Move black pawn from d7 to d5 (two squares)
    board.move((1, 3), {"to": (3, 3), "special": None})

    # Check if en passant is available
    white_pawn_moves = board.get_legal_moves((3, 4))
    en_passant_moves = [m for m in white_pawn_moves if m["special"] == "EP"]

    print(f"En passant moves available: {len(en_passant_moves)}")
    assert len(en_passant_moves) > 0, "En passant should be available!"
    print("✓ En passant detected correctly")

    # Test Castling
    board2 = Board()

    # Clear pieces between king and rook
    board2.state[7][1] = None  # Clear knight
    board2.state[7][2] = None  # Clear bishop
    board2.state[7][3] = None  # Clear queen

    king_moves = board2.get_legal_moves((7, 4))
    castling_moves = [m for m in king_moves if m["special"] in ["KSC", "QSC"]]

    print(f"Castling moves available: {len(castling_moves)}")
    assert len(castling_moves) > 0, "Queen-side castling should be available!"
    print("✓ Castling detected correctly")

    return True

def test_move_undo():
    '''Test move undo functionality'''
    print("\n=== Testing Move Undo ===")

    board = Board()

    # Save initial state
    initial_state = str(board.state)

    # Make a move
    board.move((6, 4), {"to": (4, 4), "special": None})

    # Verify state changed
    assert str(board.state) != initial_state, "State should change after move!"

    # Undo move
    board.undo()

    # Verify state restored
    assert str(board.state) == initial_state, "State should be restored after undo!"
    print("✓ Move undo works correctly")

    return True

def run_all_tests():
    '''Run all tests'''
    print("="*50)
    print("RUNNING COMPREHENSIVE CHESS TESTS")
    print("="*50)

    tests = [
        test_checkmate,
        test_stalemate,
        test_insufficient_material,
        test_ai_evaluation,
        test_ai_move_generation,
        test_special_moves,
        test_move_undo
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1

    print("\n" + "="*50)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*50)

    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
