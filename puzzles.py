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
