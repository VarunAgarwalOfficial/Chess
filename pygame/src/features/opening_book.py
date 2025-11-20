'''
Opening Book for Chess Engine
Contains common chess openings with their move sequences
'''

class OpeningBook:
    def __init__(self):
        '''
        Opening book storing common chess openings
        Format: "position_hash": [{"from": (r,c), "to": (r,c), "name": "Opening Name"}, ...]
        '''
        self.openings = {
            # Italian Game
            "e2e4_e7e5_Ng1f3_Nb8c6_Bf1c4": {
                "name": "Italian Game",
                "moves": ["e4", "e5", "Nf3", "Nc6", "Bc4"]
            },

            # Ruy Lopez
            "e2e4_e7e5_Ng1f3_Nb8c6_Bf1b5": {
                "name": "Ruy Lopez",
                "moves": ["e4", "e5", "Nf3", "Nc6", "Bb5"]
            },

            # Sicilian Defense
            "e2e4_c7c5": {
                "name": "Sicilian Defense",
                "moves": ["e4", "c5"]
            },

            # French Defense
            "e2e4_e7e6": {
                "name": "French Defense",
                "moves": ["e4", "e6"]
            },

            # Caro-Kann Defense
            "e2e4_c7c6": {
                "name": "Caro-Kann Defense",
                "moves": ["e4", "c6"]
            },

            # Queen's Gambit
            "d2d4_d7d5_c2c4": {
                "name": "Queen's Gambit",
                "moves": ["d4", "d5", "c4"]
            },

            # King's Indian Defense
            "d2d4_Ng8f6_c2c4_g7g6": {
                "name": "King's Indian Defense",
                "moves": ["d4", "Nf6", "c4", "g6"]
            },

            # English Opening
            "c2c4": {
                "name": "English Opening",
                "moves": ["c4"]
            },
        }

        # Common opening principles (moves that are generally good)
        self.opening_principles = [
            # E4 openings (white)
            {"from": (6, 4), "to": (4, 4)},  # e4

            # D4 openings (white)
            {"from": (6, 3), "to": (4, 3)},  # d4

            # C4 English (white)
            {"from": (6, 2), "to": (4, 2)},  # c4

            # Nf3 (white)
            {"from": (7, 6), "to": (5, 5)},  # Nf3

            # E5 response (black)
            {"from": (1, 4), "to": (3, 4)},  # e5

            # C5 Sicilian (black)
            {"from": (1, 2), "to": (3, 2)},  # c5

            # E6 French (black)
            {"from": (1, 4), "to": (2, 4)},  # e6

            # Nf6 (black)
            {"from": (0, 6), "to": (2, 5)},  # Nf6
        ]

        self.current_opening = None
        self.move_sequence = []

    def add_move(self, from_pos, to_pos):
        '''Add a move to the sequence'''
        move_str = self.position_to_notation(from_pos, to_pos)
        self.move_sequence.append(move_str)
        self.detect_opening()

    def position_to_notation(self, from_pos, to_pos):
        '''Convert position to simplified notation for matching'''
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        from_square = f"{files[from_pos[1]]}{8-from_pos[0]}"
        to_square = f"{files[to_pos[1]]}{8-to_pos[0]}"
        return f"{from_square}{to_square}"

    def detect_opening(self):
        '''Detect which opening is being played'''
        sequence_key = "_".join(self.move_sequence)

        for opening_key, opening_data in self.openings.items():
            if sequence_key == opening_key:
                self.current_opening = opening_data["name"]
                return

        # Check if sequence starts with a known opening
        for opening_key, opening_data in self.openings.items():
            if opening_key.startswith(sequence_key):
                # Might be heading towards this opening
                pass

    def get_opening_move(self, board, move_number):
        '''
        Get a good opening move from the book
        Returns None if no book move is available
        '''
        if move_number > 10:  # Only use book for first 10 moves
            return None

        # Simple heuristic: return a principled opening move
        # In a full implementation, this would match current position to book

        return None  # For now, let AI decide

    def get_current_opening(self):
        '''Return the name of the current opening being played'''
        return self.current_opening if self.current_opening else "Unknown Opening"

    def reset(self):
        '''Reset the opening book for a new game'''
        self.current_opening = None
        self.move_sequence = []
