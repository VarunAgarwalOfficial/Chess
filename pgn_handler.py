'''
PGN (Portable Game Notation) Handler
Supports saving and loading chess games in standard PGN format
'''

import datetime

class PGNHandler:
    def __init__(self):
        self.piece_symbols = {
            "pawn": "",
            "knight": "N",
            "bishop": "B",
            "rook": "R",
            "queen": "Q",
            "king": "K"
        }

        self.files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    def move_to_algebraic(self, board, from_pos, move):
        '''Convert a move to algebraic notation'''
        piece = board.state[from_pos[0]][from_pos[1]]
        if not piece:
            return ""

        # Handle special moves
        if move["special"] == "KSC":
            return "O-O"
        elif move["special"] == "QSC":
            return "O-O-O"

        # Get piece symbol
        piece_symbol = self.piece_symbols[piece.type]

        # Get destination square
        to_square = f"{self.files[move['to'][1]]}{8 - move['to'][0]}"

        # Check if capture
        is_capture = board.state[move["to"][0]][move["to"][1]] is not None
        if move["special"] == "EP":
            is_capture = True

        # Build move string
        move_str = piece_symbol

        # For pawns, include file if capture
        if piece.type == "pawn" and is_capture:
            move_str = self.files[from_pos[1]]

        # Add capture symbol
        if is_capture:
            move_str += "x"

        # Add destination
        move_str += to_square

        # Add promotion
        if move["special"] == "promotion":
            move_str += "=Q"  # Default to queen for now

        # TODO: Add check (+) and checkmate (#) symbols

        return move_str

    def save_game(self, board, move_history, result, filename, white_player="Player", black_player="Computer"):
        '''Save game to PGN file'''
        pgn_lines = []

        # Header (Seven Tag Roster)
        pgn_lines.append(f'[Event "Casual Game"]')
        pgn_lines.append(f'[Site "Chess Game"]')
        pgn_lines.append(f'[Date "{datetime.datetime.now().strftime("%Y.%m.%d")}"]')
        pgn_lines.append(f'[Round "1"]')
        pgn_lines.append(f'[White "{white_player}"]')
        pgn_lines.append(f'[Black "{black_player}"]')

        # Result
        if result == "checkmate_white":
            result_str = "1-0"
        elif result == "checkmate_black":
            result_str = "0-1"
        else:
            result_str = "1/2-1/2"

        pgn_lines.append(f'[Result "{result_str}"]')
        pgn_lines.append("")  # Blank line after headers

        # Moves
        move_text = ""
        for i, move in enumerate(move_history):
            if i % 2 == 0:
                move_number = i // 2 + 1
                move_text += f"{move_number}. {move} "
            else:
                move_text += f"{move} "

            # Line break every 8 moves for readability
            if i % 16 == 15:
                move_text += "\n"

        move_text += result_str
        pgn_lines.append(move_text)

        # Write to file
        try:
            with open(filename, 'w') as f:
                f.write('\n'.join(pgn_lines))
            return True
        except Exception as e:
            print(f"Error saving PGN: {e}")
            return False

    def load_game(self, filename):
        '''Load game from PGN file'''
        try:
            with open(filename, 'r') as f:
                content = f.read()

            # Parse PGN (basic implementation)
            lines = content.split('\n')

            # Extract headers
            headers = {}
            moves_section = []
            in_moves = False

            for line in lines:
                line = line.strip()
                if line.startswith('['):
                    # Header
                    tag = line[1:line.index(' ')]
                    value = line[line.index('"')+1:line.rindex('"')]
                    headers[tag] = value
                elif line and not line.startswith('['):
                    in_moves = True
                    moves_section.append(line)

            # Parse moves (simplified - full PGN parsing is complex)
            moves_text = ' '.join(moves_section)

            return {
                'headers': headers,
                'moves': moves_text,
                'success': True
            }

        except Exception as e:
            print(f"Error loading PGN: {e}")
            return {'success': False, 'error': str(e)}

    def export_position_fen(self, board):
        '''Export current position in FEN (Forsyth-Edwards Notation)'''
        fen_parts = []

        # 1. Piece placement
        for row in range(8):
            empty_count = 0
            row_str = ""
            for col in range(8):
                piece = board.state[row][col]
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        row_str += str(empty_count)
                        empty_count = 0

                    # Get piece character
                    piece_char = self.piece_symbols.get(piece.type, "")
                    if piece.type == "pawn":
                        piece_char = "P"
                    elif piece.type == "knight":
                        piece_char = "N"
                    elif piece.type == "bishop":
                        piece_char = "B"
                    elif piece.type == "rook":
                        piece_char = "R"
                    elif piece.type == "queen":
                        piece_char = "Q"
                    elif piece.type == "king":
                        piece_char = "K"

                    if piece.color == "black":
                        piece_char = piece_char.lower()

                    row_str += piece_char

            if empty_count > 0:
                row_str += str(empty_count)

            fen_parts.append(row_str)

        position = "/".join(fen_parts)

        # 2. Active color
        active_color = "w" if board.to_move == "white" else "b"

        # 3. Castling availability
        castling = ""
        if board.castling["white"]["king"]:
            castling += "K"
        if board.castling["white"]["queen"]:
            castling += "Q"
        if board.castling["black"]["king"]:
            castling += "k"
        if board.castling["black"]["queen"]:
            castling += "q"
        if not castling:
            castling = "-"

        # 4. En passant target square (simplified - would need to track this)
        en_passant = "-"

        # 5. Halfmove clock (for fifty-move rule)
        halfmove = "0"

        # 6. Fullmove number
        fullmove = str(len(board.move_log) // 2 + 1)

        fen = f"{position} {active_color} {castling} {en_passant} {halfmove} {fullmove}"
        return fen
