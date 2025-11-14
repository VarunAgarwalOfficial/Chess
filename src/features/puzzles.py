'''
Chess Puzzles System
Collection of chess tactics puzzles
'''

class ChessPuzzles:
    def __init__(self):
        '''Initialize with a collection of tactical puzzles'''
        # Format: {
        #   "id": unique identifier,
        #   "fen": FEN notation of position,
        #   "moves": solution moves in algebraic notation,
        #   "theme": tactical theme (fork, pin, skewer, etc.),
        #   "difficulty": easy/medium/hard
        # }

        self.puzzles = [
            {
                "id": 1,
                "name": "Back Rank Mate",
                "fen": "6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1",
                "solution": ["Re8#"],
                "theme": "Back Rank Mate",
                "difficulty": "easy",
                "description": "White to move and checkmate in 1"
            },
            {
                "id": 2,
                "name": "Knight Fork",
                "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
                "solution": ["Nxe5"],
                "theme": "Fork",
                "difficulty": "easy",
                "description": "Win material with a knight fork"
            },
            {
                "id": 3,
                "name": "Pin Tactics",
                "fen": "r1bqkb1r/pppp1ppp/2n5/4p3/2BnP3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1",
                "solution": ["Nxe5", "Nxe5", "Qf3"],
                "theme": "Pin",
                "difficulty": "medium",
                "description": "Exploit the pin to win material"
            },
            {
                "id": 4,
                "name": "Smothered Mate",
                "fen": "6k1/5p1p/6p1/8/8/8/5q1P/5RKN b - - 0 1",
                "solution": ["Qf1+", "Nxf1", "Ne3#"],
                "theme": "Smothered Mate",
                "difficulty": "hard",
                "description": "Black to deliver smothered mate"
            },
            {
                "id": 5,
                "name": "Discovered Attack",
                "fen": "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 1",
                "solution": ["Bxf7+"],
                "theme": "Discovered Attack",
                "difficulty": "medium",
                "description": "Win material with a discovered attack"
            },
            {
                "id": 6,
                "name": "Remove the Defender",
                "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 1",
                "solution": ["Bxf7+", "Kxf7", "Nxe5+"],
                "theme": "Remove the Defender",
                "difficulty": "medium",
                "description": "Remove the defender and win material"
            },
            {
                "id": 7,
                "name": "Deflection",
                "fen": "r1b1k2r/ppppqppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP1QPPP/RNB1K2R b KQkq - 0 1",
                "solution": ["Qxe4+"],
                "theme": "Deflection",
                "difficulty": "easy",
                "description": "Use deflection to win"
            },
            {
                "id": 8,
                "name": "Double Check",
                "fen": "r1bqkb1r/pppp1ppp/2n5/4p3/2BnP3/5N2/PPPP1PPP/RNBQ1RK1 b kq - 0 1",
                "solution": ["Nf3+"],
                "theme": "Double Check",
                "difficulty": "hard",
                "description": "Find the double check"
            },
            {
                "id": 9,
                "name": "Legal's Mate",
                "fen": "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 1",
                "solution": ["Nxe5", "Nxe5", "Qf3", "Nxf3", "Bxf7#"],
                "theme": "Legal's Mate",
                "difficulty": "hard",
                "description": "Classic Legal's Mate pattern"
            },
            {
                "id": 10,
                "name": "Skewer",
                "fen": "6k1/5ppp/8/8/8/8/r4PPP/3R2K1 w - - 0 1",
                "solution": ["Rd8+"],
                "theme": "Skewer",
                "difficulty": "easy",
                "description": "Use a skewer to win the rook"
            },
            {
                "id": 11,
                "name": "Greco Sacrifice",
                "fen": "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1",
                "solution": ["Bxf7+", "Kxf7", "Ng5+"],
                "theme": "Greco Sacrifice",
                "difficulty": "medium",
                "description": "Classic bishop sacrifice on f7"
            },
            {
                "id": 12,
                "name": "Windmill",
                "fen": "r3k2r/pbpnn1pp/1p2pq2/3p4/2PP4/1P2B3/PB1NQPPP/R4RK1 w kq - 0 1",
                "solution": ["Bxh7+", "Kxh7", "Ng5+"],
                "theme": "Windmill",
                "difficulty": "hard",
                "description": "Execute a windmill attack"
            },
            {
                "id": 13,
                "name": "Arabian Mate",
                "fen": "5rk1/6pp/8/8/8/8/8/4RNK1 w - - 0 1",
                "solution": ["Re8+", "Rxe8", "Nf7#"],
                "theme": "Arabian Mate",
                "difficulty": "medium",
                "description": "Deliver Arabian mate with rook and knight"
            },
            {
                "id": 14,
                "name": "Anastasia's Mate",
                "fen": "r2qkb1r/ppp2ppp/2np1n2/8/2BPP1b1/2N2N2/PPP2PPP/R1BQK2R w KQkq - 0 1",
                "solution": ["Bxf7+", "Kf8", "Ng5"],
                "theme": "Anastasia's Mate",
                "difficulty": "hard",
                "description": "Set up Anastasia's mate pattern"
            },
            {
                "id": 15,
                "name": "X-Ray Attack",
                "fen": "r1bq1rk1/ppp2ppp/2np1n2/2b1p3/2B1P3/2NP1N2/PPP2PPP/R1BQ1RK1 w - - 0 1",
                "solution": ["Bxf7+"],
                "theme": "X-Ray",
                "difficulty": "medium",
                "description": "Use x-ray attack to win material"
            },
            {
                "id": 16,
                "name": "Clearance Sacrifice",
                "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1",
                "solution": ["Ng5"],
                "theme": "Clearance",
                "difficulty": "easy",
                "description": "Clear a square for your attack"
            },
            {
                "id": 17,
                "name": "Zugzwang",
                "fen": "8/8/p7/P7/8/2k5/8/2K5 w - - 0 1",
                "solution": ["Kb1"],
                "theme": "Zugzwang",
                "difficulty": "medium",
                "description": "Put opponent in zugzwang"
            },
            {
                "id": 18,
                "name": "Boden's Mate",
                "fen": "r1b2rk1/ppp2ppp/8/4Bb2/8/8/PPP2PPP/2KR3R w - - 0 1",
                "solution": ["Rd8+", "Bxd8", "Bf6#"],
                "theme": "Boden's Mate",
                "difficulty": "hard",
                "description": "Execute Boden's mate with crossed bishops"
            },
            {
                "id": 19,
                "name": "Epaulette Mate",
                "fen": "5rk1/6pp/8/8/8/8/6PP/4RRK1 w - - 0 1",
                "solution": ["Re8#"],
                "theme": "Epaulette Mate",
                "difficulty": "easy",
                "description": "Checkmate with rooks on both sides of king"
            },
            {
                "id": 20,
                "name": "Interference",
                "fen": "r4rk1/ppp1qppp/2n5/3n4/3P4/2N1B3/PPP1QPPP/R4RK1 w - - 0 1",
                "solution": ["Nd5"],
                "theme": "Interference",
                "difficulty": "medium",
                "description": "Use interference to disrupt opponent's defense"
            },
            {
                "id": 21,
                "name": "Perpetual Check",
                "fen": "r5k1/5ppp/8/8/8/8/5PPP/4Q1K1 w - - 0 1",
                "solution": ["Qa8+", "Kh7", "Qh1+"],
                "theme": "Perpetual Check",
                "difficulty": "easy",
                "description": "Force a draw with perpetual check"
            },
            {
                "id": 22,
                "name": "Overloading",
                "fen": "r4rk1/1ppq1ppp/p1np1n2/4p1B1/2B1P3/2NP1N2/PPP2PPP/R2Q1RK1 w - - 0 1",
                "solution": ["Bxf7+"],
                "theme": "Overloading",
                "difficulty": "medium",
                "description": "Exploit an overloaded defender"
            },
            {
                "id": 23,
                "name": "Trapped Piece",
                "fen": "rnbqk2r/pppp1ppp/5n2/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1",
                "solution": ["Qb3"],
                "theme": "Trapped Piece",
                "difficulty": "easy",
                "description": "Trap the opponent's piece"
            },
            {
                "id": 24,
                "name": "Decoy Sacrifice",
                "fen": "r1bq1rk1/ppp2ppp/2np1n2/2b1p3/2B1P3/2NP1N2/PPP2PPP/R1BQK2R w KQ - 0 1",
                "solution": ["Bxf7+", "Kxf7", "Ng5+"],
                "theme": "Decoy",
                "difficulty": "medium",
                "description": "Sacrifice to lure the king out"
            },
            {
                "id": 25,
                "name": "Desperado",
                "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1",
                "solution": ["Bxf7+"],
                "theme": "Desperado",
                "difficulty": "medium",
                "description": "Make the most of a doomed piece"
            },
            {
                "id": 26,
                "name": "Damiano's Defense Refutation",
                "fen": "rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1",
                "solution": ["Nxe5", "Nxe4", "Qe2"],
                "theme": "Tactical Refutation",
                "difficulty": "hard",
                "description": "Punish Damiano's defense"
            },
            {
                "id": 27,
                "name": "Stalemate Trick",
                "fen": "7k/8/6Q1/8/8/8/8/7K b - - 0 1",
                "solution": [],
                "theme": "Stalemate",
                "difficulty": "easy",
                "description": "Black is stalemated - draw"
            },
            {
                "id": 28,
                "name": "Queen Sacrifice for Mate",
                "fen": "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 w kq - 0 1",
                "solution": ["Qd5", "Qe7", "Qxf7+", "Kd8", "Qf8#"],
                "theme": "Queen Sacrifice",
                "difficulty": "hard",
                "description": "Sacrifice the queen for checkmate"
            },
            {
                "id": 29,
                "name": "Rook Endgame",
                "fen": "8/8/8/4k3/8/3K4/8/1R6 w - - 0 1",
                "solution": ["Rb5+"],
                "theme": "Endgame",
                "difficulty": "easy",
                "description": "Cut off the king in rook endgame"
            },
            {
                "id": 30,
                "name": "Bishop Pair",
                "fen": "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/2NP1N2/PPP2PPP/R1BQK2R w KQkq - 0 1",
                "solution": ["d4"],
                "theme": "Bishop Pair",
                "difficulty": "medium",
                "description": "Activate your bishop pair"
            },
            {
                "id": 31,
                "name": "Passed Pawn",
                "fen": "8/2k5/8/2P5/8/2K5/8/8 w - - 0 1",
                "solution": ["c6+", "Kd6", "Kb4"],
                "theme": "Passed Pawn",
                "difficulty": "medium",
                "description": "Push the passed pawn to promotion"
            },
            {
                "id": 32,
                "name": "Mayet's Mate",
                "fen": "r3k3/ppp2p1p/3p4/4nBp1/2B5/8/PPP2PPP/R3K2R w KQ - 0 1",
                "solution": ["Rh8+", "Kf7", "Bh5#"],
                "theme": "Mayet's Mate",
                "difficulty": "hard",
                "description": "Execute Mayet's mating pattern"
            },
            {
                "id": 33,
                "name": "Morphy's Brilliancy",
                "fen": "r2qkb1r/ppp2ppp/2n5/3n4/3P4/2N5/PPP2PPP/R1BQKB1R w KQkq - 0 1",
                "solution": ["Nxd5"],
                "theme": "Combination",
                "difficulty": "medium",
                "description": "Win material with a combination"
            },
            {
                "id": 34,
                "name": "Zwischenzug",
                "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1",
                "solution": ["Bxf7+"],
                "theme": "Zwischenzug",
                "difficulty": "medium",
                "description": "Make an in-between move"
            },
            {
                "id": 35,
                "name": "Philidor's Legacy",
                "fen": "5rk1/6pp/8/8/8/8/5PPP/3QR1K1 w - - 0 1",
                "solution": ["Qd8+", "Kh7", "Qh8#"],
                "theme": "Smothered Mate",
                "difficulty": "easy",
                "description": "Classic smothered mate pattern"
            },
            {
                "id": 36,
                "name": "Petrov's Defense Trap",
                "fen": "rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1",
                "solution": ["Nxe5", "d6", "Nf3"],
                "theme": "Opening Trap",
                "difficulty": "medium",
                "description": "Avoid Petrov's defense trap"
            },
            {
                "id": 37,
                "name": "Blackburne's Mate",
                "fen": "r3k2r/ppp2ppp/2n5/2b5/2Bn4/8/PPP2PPP/R1BQK2R w KQkq - 0 1",
                "solution": ["Qd5"],
                "theme": "Blackburne's Mate",
                "difficulty": "hard",
                "description": "Set up Blackburne's mating attack"
            },
            {
                "id": 38,
                "name": "Hook Mate",
                "fen": "r4rk1/ppp2ppp/3p1n2/8/1b1P4/5N2/PPP2PPP/RNBQR1K1 w - - 0 1",
                "solution": ["Re8+", "Rxe8", "Nf7#"],
                "theme": "Hook Mate",
                "difficulty": "medium",
                "description": "Deliver hook mate with knight and rook"
            },
            {
                "id": 39,
                "name": "Lolli's Mate",
                "fen": "r3k2r/ppp2ppp/2n2n2/2b5/2B5/2N2N2/PPP2PPP/R1BQK2R w KQkq - 0 1",
                "solution": ["Nd5"],
                "theme": "Lolli's Mate",
                "difficulty": "hard",
                "description": "Execute Lolli's mating pattern"
            },
            {
                "id": 40,
                "name": "Pawn Breakthrough",
                "fen": "8/2k2p2/3p4/3P1PPP/8/2K5/8/8 w - - 0 1",
                "solution": ["f6", "gxf6", "g6"],
                "theme": "Pawn Breakthrough",
                "difficulty": "hard",
                "description": "Execute a pawn breakthrough"
            },
        ]

        self.current_puzzle_index = 0
        self.user_moves = []
        self.hints_used = 0

    def get_puzzle(self, puzzle_id=None):
        '''Get a specific puzzle or the current one'''
        if puzzle_id is not None:
            for puzzle in self.puzzles:
                if puzzle["id"] == puzzle_id:
                    return puzzle
            return None
        return self.puzzles[self.current_puzzle_index]

    def get_puzzles_by_difficulty(self, difficulty):
        '''Get all puzzles of a specific difficulty'''
        return [p for p in self.puzzles if p["difficulty"] == difficulty]

    def get_puzzles_by_theme(self, theme):
        '''Get all puzzles of a specific theme'''
        return [p for p in self.puzzles if p["theme"] == theme]

    def check_solution(self, user_moves):
        '''Check if user's moves match the solution'''
        puzzle = self.get_puzzle()
        if not puzzle:
            return False

        # Convert both to lowercase for comparison
        user_moves_lower = [m.lower() for m in user_moves]
        solution_lower = [m.lower() for m in puzzle["solution"]]

        return user_moves_lower == solution_lower

    def get_hint(self):
        '''Get a hint for the current puzzle'''
        puzzle = self.get_puzzle()
        if not puzzle:
            return None

        self.hints_used += 1

        # Return first move of solution
        if len(puzzle["solution"]) > 0:
            return puzzle["solution"][0]

        return None

    def next_puzzle(self):
        '''Move to next puzzle'''
        self.current_puzzle_index = (self.current_puzzle_index + 1) % len(self.puzzles)
        self.user_moves = []
        self.hints_used = 0

    def previous_puzzle(self):
        '''Move to previous puzzle'''
        self.current_puzzle_index = (self.current_puzzle_index - 1) % len(self.puzzles)
        self.user_moves = []
        self.hints_used = 0

    def reset_puzzle(self):
        '''Reset current puzzle'''
        self.user_moves = []
        self.hints_used = 0

    def get_progress(self):
        '''Get puzzle solving progress'''
        return {
            "current": self.current_puzzle_index + 1,
            "total": len(self.puzzles),
            "percentage": ((self.current_puzzle_index + 1) / len(self.puzzles)) * 100
        }
