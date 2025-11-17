#!/usr/bin/env python3
"""
Visualize attack patterns from the pre-computed attack tables.
Shows what squares each piece can attack from various positions.
"""

from src.ai.attack_tables import (
    get_knight_attacks,
    get_king_attacks,
    get_pawn_attacks
)


def visualize_attacks(piece_pos, attacks, piece_name):
    """
    Visualize attack pattern on a chess board.

    Args:
        piece_pos: (row, col) of the piece
        attacks: List of (row, col) tuples showing attacked squares
        piece_name: Name of the piece for display
    """
    print(f"\n{piece_name} on {pos_to_algebraic(piece_pos)}")
    print("=" * 33)

    # Create board representation
    board = [['.' for _ in range(8)] for _ in range(8)]

    # Mark piece position
    board[piece_pos[0]][piece_pos[1]] = 'P'

    # Mark attacked squares
    for row, col in attacks:
        board[row][col] = 'X'

    # Print board with coordinates
    print("   a b c d e f g h")
    print("  " + "-" * 17)
    for row in range(8):
        rank = 8 - row
        print(f"{rank} |", end="")
        for col in range(8):
            print(f" {board[row][col]}", end="")
        print(f" | {rank}")
    print("  " + "-" * 17)
    print("   a b c d e f g h")
    print("\nP = Piece position")
    print("X = Attacked square")


def pos_to_algebraic(pos):
    """Convert (row, col) to algebraic notation (e.g., e4)"""
    files = 'abcdefgh'
    ranks = '87654321'
    return files[pos[1]] + ranks[pos[0]]


def demonstrate_all_pieces():
    """Show attack patterns for all piece types"""
    print("\n" + "=" * 70)
    print("ATTACK PATTERN VISUALIZATIONS")
    print("=" * 70)

    # Knight from center
    knight_pos = (4, 4)  # e4
    knight_attacks = get_knight_attacks(4, 4)
    visualize_attacks(knight_pos, knight_attacks, "KNIGHT")

    # Knight from corner
    knight_pos = (7, 0)  # a1
    knight_attacks = get_knight_attacks(7, 0)
    visualize_attacks(knight_pos, knight_attacks, "KNIGHT (corner)")

    # King from center
    king_pos = (4, 4)  # e4
    king_attacks = get_king_attacks(4, 4)
    visualize_attacks(king_pos, king_attacks, "KING")

    # King from edge
    king_pos = (7, 4)  # e1
    king_attacks = get_king_attacks(7, 4)
    visualize_attacks(king_pos, king_attacks, "KING (edge)")

    # White pawn from center
    pawn_pos = (4, 4)  # e4
    white_pawn_attacks = get_pawn_attacks(4, 4, "white")
    visualize_attacks(pawn_pos, white_pawn_attacks, "WHITE PAWN")

    # Black pawn from center
    pawn_pos = (3, 4)  # e5
    black_pawn_attacks = get_pawn_attacks(3, 4, "black")
    visualize_attacks(pawn_pos, black_pawn_attacks, "BLACK PAWN")

    # Show edge cases
    print("\n" + "=" * 70)
    print("EDGE CASES")
    print("=" * 70)

    # Knight on edge (limited moves)
    knight_pos = (0, 3)  # d8
    knight_attacks = get_knight_attacks(0, 3)
    visualize_attacks(knight_pos, knight_attacks, "KNIGHT (top edge)")

    # King in corner (minimal moves)
    king_pos = (0, 0)  # a8
    king_attacks = get_king_attacks(0, 0)
    visualize_attacks(king_pos, king_attacks, "KING (corner)")

    # White pawn on edge file (only 1 attack)
    pawn_pos = (4, 0)  # a4
    white_pawn_attacks = get_pawn_attacks(4, 0, "white")
    visualize_attacks(pawn_pos, white_pawn_attacks, "WHITE PAWN (edge file)")

    # White pawn on 7th rank (no attacks forward - would promote)
    pawn_pos = (1, 4)  # e7
    white_pawn_attacks = get_pawn_attacks(1, 4, "white")
    visualize_attacks(pawn_pos, white_pawn_attacks, "WHITE PAWN (7th rank)")


def show_statistics():
    """Show attack count statistics for each piece type"""
    print("\n" + "=" * 70)
    print("ATTACK COUNT STATISTICS")
    print("=" * 70)

    # Count attacks for each piece from different positions
    positions = {
        'center': (4, 4),      # e4
        'edge': (4, 0),        # a4
        'corner': (0, 0),      # a8
        'near_corner': (1, 1)  # b7
    }

    print("\nKnight attacks from different positions:")
    for pos_name, pos in positions.items():
        attacks = get_knight_attacks(pos[0], pos[1])
        alg = pos_to_algebraic(pos)
        print(f"  {pos_name:12} ({alg}): {len(attacks)} squares")

    print("\nKing attacks from different positions:")
    for pos_name, pos in positions.items():
        attacks = get_king_attacks(pos[0], pos[1])
        alg = pos_to_algebraic(pos)
        print(f"  {pos_name:12} ({alg}): {len(attacks)} squares")

    print("\nWhite pawn attacks from different positions:")
    for pos_name, pos in positions.items():
        attacks = get_pawn_attacks(pos[0], pos[1], "white")
        alg = pos_to_algebraic(pos)
        print(f"  {pos_name:12} ({alg}): {len(attacks)} squares")

    print("\nBlack pawn attacks from different positions:")
    for pos_name, pos in positions.items():
        attacks = get_pawn_attacks(pos[0], pos[1], "black")
        alg = pos_to_algebraic(pos)
        print(f"  {pos_name:12} ({alg}): {len(attacks)} squares")


if __name__ == "__main__":
    demonstrate_all_pieces()
    show_statistics()

    print("\n" + "=" * 70)
    print("VISUALIZATION COMPLETE")
    print("=" * 70)
    print("\nThese patterns are pre-computed and stored in RAM for instant O(1) lookup.")
    print("No computation needed during move generation or check detection!\n")
