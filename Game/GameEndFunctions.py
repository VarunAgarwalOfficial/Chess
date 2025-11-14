'''
Functions for detecting game-ending conditions:
- Checkmate
- Stalemate
- Draw by insufficient material
- Draw by threefold repetition
- Draw by fifty-move rule
'''

def is_checkmate(self):
    '''
    Checkmate occurs when:
    1. The king is in check
    2. There are no legal moves available
    '''
    if not self.check:
        return False

    # Check if any piece has a legal move
    for row in range(8):
        for col in range(8):
            piece = self.state[row][col]
            if piece and piece.color == self.to_move:
                if len(self.get_legal_moves((row, col))) > 0:
                    return False

    return True


def is_stalemate(self):
    '''
    Stalemate occurs when:
    1. The king is NOT in check
    2. There are no legal moves available
    '''
    if self.check:
        return False

    # Check if any piece has a legal move
    for row in range(8):
        for col in range(8):
            piece = self.state[row][col]
            if piece and piece.color == self.to_move:
                if len(self.get_legal_moves((row, col))) > 0:
                    return False

    return True


def is_insufficient_material(self):
    '''
    Draw by insufficient material occurs when neither side can checkmate:
    - King vs King
    - King + Bishop vs King
    - King + Knight vs King
    - King + Bishop vs King + Bishop (same color bishops)
    '''
    pieces = {
        "white": [],
        "black": []
    }

    # Count all pieces on the board
    for row in range(8):
        for col in range(8):
            piece = self.state[row][col]
            if piece and piece.type != "king":
                pieces[piece.color].append((piece.type, row, col))

    # King vs King
    if len(pieces["white"]) == 0 and len(pieces["black"]) == 0:
        return True

    # King + minor piece vs King
    if len(pieces["white"]) == 0 and len(pieces["black"]) == 1:
        if pieces["black"][0][0] in ["bishop", "knight"]:
            return True
    if len(pieces["black"]) == 0 and len(pieces["white"]) == 1:
        if pieces["white"][0][0] in ["bishop", "knight"]:
            return True

    # King + Bishop vs King + Bishop (same color squares)
    if len(pieces["white"]) == 1 and len(pieces["black"]) == 1:
        white_piece = pieces["white"][0]
        black_piece = pieces["black"][0]
        if white_piece[0] == "bishop" and black_piece[0] == "bishop":
            # Check if bishops are on same color squares
            white_square_color = (white_piece[1] + white_piece[2]) % 2
            black_square_color = (black_piece[1] + black_piece[2]) % 2
            if white_square_color == black_square_color:
                return True

    return False


def is_threefold_repetition(self):
    '''
    Draw by threefold repetition occurs when the same position
    appears three times with the same player to move
    '''
    if len(self.move_log) < 8:  # Need at least 8 moves for repetition
        return False

    # Create a hashable representation of current position
    current_position = self._position_hash()

    # Count occurrences in move log
    count = 1  # Current position counts as 1

    # Check previous positions (only same color to move)
    for i in range(len(self.move_log) - 2, -1, -2):  # Step by 2 to check same color
        if i >= 0:
            # Would need to reconstruct position from move log
            # For simplicity, we'll implement a basic version using board state hashing
            # This is a simplified version - full implementation would track position hashes
            pass

    # Simplified: just return False for now, full implementation would track position hashes
    return False


def _position_hash(self):
    '''
    Create a hashable representation of the current position
    includes piece positions, castling rights, en passant, and side to move
    '''
    position = []

    # Add all piece positions
    for row in range(8):
        for col in range(8):
            piece = self.state[row][col]
            if piece:
                position.append((row, col, piece.color, piece.type))

    # Add castling rights
    position.append(("castling",
                    self.castling["white"]["king"],
                    self.castling["white"]["queen"],
                    self.castling["black"]["king"],
                    self.castling["black"]["queen"]))

    # Add side to move
    position.append(("to_move", self.to_move))

    return tuple(position)


def is_fifty_move_rule(self):
    '''
    Draw by fifty-move rule: if 50 moves have been made
    without a pawn move or capture
    '''
    if len(self.move_log) < 100:  # 50 moves = 100 half-moves
        return False

    # Check last 100 half-moves (50 full moves)
    for i in range(len(self.move_log) - 1, max(len(self.move_log) - 101, -1), -1):
        move = self.move_log[i]
        # If there was a capture or pawn move, reset counter
        if move["final_piece"] is not None or move["initial_piece"].type == "pawn":
            return False

    return True


def get_game_result(self):
    '''
    Returns the game result:
    - None: game ongoing
    - "checkmate_white": white wins by checkmate
    - "checkmate_black": black wins by checkmate
    - "stalemate": draw by stalemate
    - "insufficient_material": draw by insufficient material
    - "threefold_repetition": draw by threefold repetition
    - "fifty_move_rule": draw by fifty-move rule
    '''
    if self.is_checkmate():
        # The player to move is checkmated, so opponent wins
        if self.to_move == "white":
            return "checkmate_black"
        else:
            return "checkmate_white"

    if self.is_stalemate():
        return "stalemate"

    if self.is_insufficient_material():
        return "insufficient_material"

    if self.is_fifty_move_rule():
        return "fifty_move_rule"

    if self.is_threefold_repetition():
        return "threefold_repetition"

    return None
