'''
Chess Tutorial System
Interactive lessons for learning chess basics and advanced concepts
'''

class ChessTutorial:
    def __init__(self):
        '''Initialize tutorial system with lessons'''
        self.lessons = [
            {
                "id": 1,
                "title": "The Pawn",
                "category": "basics",
                "difficulty": "beginner",
                "content": [
                    "Pawns move straight forward, one square at a time.",
                    "",
                    "When a pawn hasn't moved yet, it can jump two squares forward",
                    "if it wants to. After that, it's back to one square at a time.",
                    "",
                    "To capture an enemy piece, pawns move diagonally forward -",
                    "one square to the left or right. They can't capture forward.",
                    "",
                    "Pawns never move backward. Once they move, there's no going back!"
                ],
                "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                "key_points": [
                    "Move forward, capture diagonally",
                    "First move can be two squares",
                    "Never goes backward"
                ]
            },
            {
                "id": 2,
                "title": "The Knight",
                "category": "basics",
                "difficulty": "beginner",
                "content": [
                    "Knights are the trickiest piece to learn. They move in an L-shape:",
                    "go two squares in one direction, then one square to the side.",
                    "",
                    "Here's the cool part: knights can hop over other pieces!",
                    "They're the only piece that can do this.",
                    "",
                    "Knights are strongest when they're in the center of the board,",
                    "where they can reach up to 8 different squares.",
                    "",
                    "Tip: Knights on the edge have fewer options, so keep them central!"
                ],
                "fen": "8/8/8/3N4/8/8/8/8 w - - 0 1",
                "key_points": [
                    "L-shaped jumps",
                    "Can hop over other pieces",
                    "Best in the center"
                ]
            },
            {
                "id": 3,
                "title": "The Bishop",
                "category": "basics",
                "difficulty": "beginner",
                "content": [
                    "Bishops glide diagonally across the board. They can go as far",
                    "as they want in one move, but can't jump over other pieces.",
                    "",
                    "Here's something interesting: each bishop is stuck on either",
                    "light or dark squares for the entire game. A bishop that starts",
                    "on a light square will never touch a dark square!",
                    "",
                    "Having both bishops (one light, one dark) is usually good",
                    "because together they cover all the squares."
                ],
                "fen": "8/8/8/3B4/8/8/8/8 w - - 0 1",
                "key_points": [
                    "Moves diagonally, any distance",
                    "Stuck on one color forever",
                    "Bishop pair is powerful"
                ]
            },
            {
                "id": 4,
                "title": "The Rook",
                "category": "basics",
                "difficulty": "beginner",
                "content": [
                    "Rooks move straight: horizontally or vertically. Like bishops,",
                    "they can slide as far as they want, but can't jump over pieces.",
                    "",
                    "Rooks love open files - that's a column with no pawns in the way.",
                    "When a rook has an open file, it can really dominate the board.",
                    "",
                    "Two rooks working together are incredibly strong. They can",
                    "trap the enemy king and deliver checkmate pretty easily."
                ],
                "fen": "8/8/8/3R4/8/8/8/8 w - - 0 1",
                "key_points": [
                    "Straight lines: horizontal or vertical",
                    "Love open files",
                    "Two rooks are very powerful"
                ]
            },
            {
                "id": 5,
                "title": "How the Queen Moves",
                "category": "basics",
                "difficulty": "beginner",
                "content": [
                    "Queens combine the power of rooks and bishops.",
                    "Queens can move horizontally, vertically, or diagonally any number of squares.",
                    "The queen is the most powerful piece on the board.",
                    "Be careful not to lose your queen early in the game."
                ],
                "fen": "8/8/8/3Q4/8/8/8/8 w - - 0 1",
                "key_points": [
                    "Most powerful piece",
                    "Combines rook + bishop movement",
                    "Protect it carefully"
                ]
            },
            {
                "id": 6,
                "title": "How the King Moves",
                "category": "basics",
                "difficulty": "beginner",
                "content": [
                    "Kings move one square in any direction.",
                    "The king is the most important piece - if it's checkmated, you lose.",
                    "Kings cannot move into check.",
                    "Kings can castle with a rook under certain conditions."
                ],
                "fen": "8/8/8/3K4/8/8/8/8 w - - 0 1",
                "key_points": [
                    "One square movement",
                    "Most important piece",
                    "Cannot move into check"
                ]
            },
            {
                "id": 7,
                "title": "Castling",
                "category": "special_moves",
                "difficulty": "beginner",
                "content": [
                    "Castling is a special move involving the king and a rook.",
                    "The king moves two squares toward the rook, and the rook jumps over the king.",
                    "You can only castle if: king hasn't moved, rook hasn't moved, no pieces between them.",
                    "You cannot castle out of, through, or into check.",
                    "Kingside castling (O-O) is more common than queenside (O-O-O)."
                ],
                "fen": "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1",
                "key_points": [
                    "King safety move",
                    "Activates the rook",
                    "Can only do once per game"
                ]
            },
            {
                "id": 8,
                "title": "En Passant",
                "category": "special_moves",
                "difficulty": "intermediate",
                "content": [
                    "En passant is a special pawn capture.",
                    "If an enemy pawn moves two squares forward from its starting position...",
                    "...and lands beside your pawn, you can capture it as if it moved one square.",
                    "You must capture en passant immediately or lose the opportunity.",
                    "This prevents pawns from avoiding capture by moving two squares."
                ],
                "fen": "8/8/8/3pP3/8/8/8/8 w - d6 0 1",
                "key_points": [
                    "Special pawn capture",
                    "Must be done immediately",
                    "Captures sideways pawn"
                ]
            },
            {
                "id": 9,
                "title": "Pawn Promotion",
                "category": "special_moves",
                "difficulty": "beginner",
                "content": [
                    "When a pawn reaches the opposite end of the board, it promotes.",
                    "You can promote to a queen, rook, bishop, or knight.",
                    "Almost always promote to a queen (most powerful piece).",
                    "You can have multiple queens through promotion.",
                    "Pawn promotion can completely change the game."
                ],
                "fen": "8/4P3/8/8/8/8/8/8 w - - 0 1",
                "key_points": [
                    "Pawn reaches end rank",
                    "Usually promote to queen",
                    "Game-changing move"
                ]
            },
            {
                "id": 10,
                "title": "Check and Checkmate",
                "category": "basics",
                "difficulty": "beginner",
                "content": [
                    "Check: when the king is under attack.",
                    "When in check, you must: move the king, block the attack, or capture the attacker.",
                    "Checkmate: when the king is in check and has no legal moves to escape.",
                    "Checkmate ends the game immediately - you win!",
                    "Stalemate: when not in check but have no legal moves - it's a draw."
                ],
                "fen": "6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1",
                "key_points": [
                    "Check = king under attack",
                    "Checkmate = game over",
                    "Stalemate = draw"
                ]
            },
            {
                "id": 11,
                "title": "Opening Principles",
                "category": "strategy",
                "difficulty": "intermediate",
                "content": [
                    "Control the center with pawns (e4, d4, e5, d5).",
                    "Develop your knights and bishops early.",
                    "Castle early to protect your king.",
                    "Don't move the same piece twice in the opening.",
                    "Don't bring your queen out too early - it can be attacked.",
                    "Connect your rooks by developing all pieces."
                ],
                "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                "key_points": [
                    "Control center",
                    "Develop pieces",
                    "Castle early",
                    "Don't waste moves"
                ]
            },
            {
                "id": 12,
                "title": "Material Value",
                "category": "strategy",
                "difficulty": "beginner",
                "content": [
                    "Pawn = 1 point",
                    "Knight = 3 points",
                    "Bishop = 3 points (slightly more than knight)",
                    "Rook = 5 points",
                    "Queen = 9 points",
                    "Don't trade a rook for a knight (you lose 2 points).",
                    "Material advantage usually leads to victory."
                ],
                "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                "key_points": [
                    "Know piece values",
                    "Avoid losing material",
                    "Trade when ahead in material"
                ]
            },
            {
                "id": 13,
                "title": "Pin Tactic",
                "category": "tactics",
                "difficulty": "intermediate",
                "content": [
                    "A pin is when a piece cannot move without exposing a more valuable piece behind it.",
                    "Absolute pin: piece pinned to the king (cannot legally move).",
                    "Relative pin: piece pinned to another valuable piece (can move but loses material).",
                    "Bishops and rooks create pins along their lines of attack.",
                    "Breaking a pin can be a strong defensive resource."
                ],
                "fen": "r1bqkb1r/pppp1ppp/2n5/4p3/2BnP3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1",
                "key_points": [
                    "Piece cannot move safely",
                    "Absolute vs relative pins",
                    "Powerful attacking tool"
                ]
            },
            {
                "id": 14,
                "title": "Fork Tactic",
                "category": "tactics",
                "difficulty": "beginner",
                "content": [
                    "A fork attacks two or more pieces at once.",
                    "Knights are excellent at forking because of their unique movement.",
                    "The enemy can only save one piece, so you win material.",
                    "Look for fork opportunities with all pieces, not just knights.",
                    "The royal fork attacks king and queen simultaneously."
                ],
                "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1",
                "key_points": [
                    "Attack two pieces at once",
                    "Knights excel at forks",
                    "Forces material gain"
                ]
            },
            {
                "id": 15,
                "title": "Skewer Tactic",
                "category": "tactics",
                "difficulty": "intermediate",
                "content": [
                    "A skewer is the opposite of a pin.",
                    "A more valuable piece is in front and must move, exposing a less valuable piece.",
                    "Bishops, rooks, and queens can create skewers.",
                    "Skewering the king is especially powerful.",
                    "Similar to a pin but the valuable piece is in front, not behind."
                ],
                "fen": "6k1/5ppp/8/8/8/8/r4PPP/3R2K1 w - - 0 1",
                "key_points": [
                    "Reverse pin",
                    "Valuable piece in front",
                    "Forces piece to move"
                ]
            },
            {
                "id": 16,
                "title": "Discovered Attack",
                "category": "tactics",
                "difficulty": "intermediate",
                "content": [
                    "When you move a piece and reveal an attack from a piece behind it.",
                    "Very powerful because you make two threats at once.",
                    "The moving piece can attack one target while the revealed piece attacks another.",
                    "Discovered check (revealing check on the king) is especially strong.",
                    "Double check (both pieces give check) forces the king to move."
                ],
                "fen": "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 1",
                "key_points": [
                    "Moving reveals attack",
                    "Two threats at once",
                    "Very powerful tactic"
                ]
            },
            {
                "id": 17,
                "title": "Remove the Defender",
                "category": "tactics",
                "difficulty": "intermediate",
                "content": [
                    "Capture or deflect a piece that's defending something important.",
                    "Once the defender is gone, you can win the undefended piece or deliver checkmate.",
                    "Look for overworked pieces defending multiple things.",
                    "This tactic often involves a sacrifice to remove the key defender.",
                    "Common in attacking the king when a piece defends a mating square."
                ],
                "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 1",
                "key_points": [
                    "Eliminate key defender",
                    "Win undefended material",
                    "Often involves sacrifice"
                ]
            },
            {
                "id": 18,
                "title": "Endgame: King Activity",
                "category": "endgame",
                "difficulty": "intermediate",
                "content": [
                    "In the endgame, the king becomes a strong piece.",
                    "Centralize your king to support pawns and attack enemy pawns.",
                    "The king can help escort passed pawns to promotion.",
                    "Opposition: kings facing each other with one square between them.",
                    "Having the opposition is often the key to winning pawn endgames."
                ],
                "fen": "8/8/3k4/8/8/3K4/8/8 w - - 0 1",
                "key_points": [
                    "King is strong in endgame",
                    "Centralize your king",
                    "Opposition is important"
                ]
            },
            {
                "id": 19,
                "title": "Endgame: Passed Pawns",
                "category": "endgame",
                "difficulty": "intermediate",
                "content": [
                    "A passed pawn has no enemy pawns to stop it from promoting.",
                    "Passed pawns are very valuable in the endgame.",
                    "Push passed pawns toward promotion.",
                    "Support passed pawns with your king.",
                    "Create passed pawns by advancing and trading pawns."
                ],
                "fen": "8/2k5/8/2P5/8/2K5/8/8 w - - 0 1",
                "key_points": [
                    "No enemy pawns blocking",
                    "Very powerful",
                    "Push toward promotion"
                ]
            },
            {
                "id": 20,
                "title": "Endgame: Rook vs Pawn",
                "category": "endgame",
                "difficulty": "advanced",
                "content": [
                    "Rook can usually stop a lone pawn from promoting.",
                    "Cut off the enemy king with your rook.",
                    "Attack the pawn from behind (not in front).",
                    "Philidor position: defend from the side, check when king advances.",
                    "Lucena position: winning technique when king is in front of pawn."
                ],
                "fen": "8/8/8/4k3/8/3K4/8/1R6 w - - 0 1",
                "key_points": [
                    "Cut off enemy king",
                    "Attack pawn from behind",
                    "Learn key positions"
                ]
            }
        ]

        self.current_lesson_index = 0
        self.completed_lessons = set()
        self.lesson_progress = {}

    def get_lesson(self, lesson_id=None):
        '''Get a specific lesson or the current one'''
        if lesson_id is not None:
            for lesson in self.lessons:
                if lesson["id"] == lesson_id:
                    return lesson
            return None
        if self.current_lesson_index < len(self.lessons):
            return self.lessons[self.current_lesson_index]
        return None

    def get_lessons_by_category(self, category):
        '''Get all lessons in a category'''
        return [l for l in self.lessons if l["category"] == category]

    def get_lessons_by_difficulty(self, difficulty):
        '''Get all lessons by difficulty level'''
        return [l for l in self.lessons if l["difficulty"] == difficulty]

    def next_lesson(self):
        '''Move to next lesson'''
        if self.current_lesson_index < len(self.lessons) - 1:
            self.current_lesson_index += 1
            return self.get_lesson()
        return None

    def previous_lesson(self):
        '''Move to previous lesson'''
        if self.current_lesson_index > 0:
            self.current_lesson_index -= 1
            return self.get_lesson()
        return None

    def mark_completed(self, lesson_id=None):
        '''Mark a lesson as completed'''
        if lesson_id is None:
            lesson_id = self.lessons[self.current_lesson_index]["id"]
        self.completed_lessons.add(lesson_id)

    def get_progress(self):
        '''Get tutorial completion progress'''
        return {
            "completed": len(self.completed_lessons),
            "total": len(self.lessons),
            "percentage": (len(self.completed_lessons) / len(self.lessons)) * 100,
            "current_lesson": self.current_lesson_index + 1
        }

    def get_categories(self):
        '''Get all unique categories'''
        return list(set(l["category"] for l in self.lessons))

    def get_category_info(self):
        '''Get lesson count by category'''
        categories = {}
        for lesson in self.lessons:
            cat = lesson["category"]
            if cat not in categories:
                categories[cat] = {
                    "count": 0,
                    "completed": 0
                }
            categories[cat]["count"] += 1
            if lesson["id"] in self.completed_lessons:
                categories[cat]["completed"] += 1
        return categories

    def reset_progress(self):
        '''Reset all tutorial progress'''
        self.current_lesson_index = 0
        self.completed_lessons = set()
        self.lesson_progress = {}

    def jump_to_lesson(self, lesson_id):
        '''Jump to a specific lesson by ID'''
        for i, lesson in enumerate(self.lessons):
            if lesson["id"] == lesson_id:
                self.current_lesson_index = i
                return lesson
        return None

    def get_next_incomplete_lesson(self):
        '''Get the next lesson that hasn't been completed'''
        for i, lesson in enumerate(self.lessons):
            if lesson["id"] not in self.completed_lessons:
                self.current_lesson_index = i
                return lesson
        return None

    def print_lesson(self, lesson_id=None):
        '''Print a formatted lesson to console'''
        lesson = self.get_lesson(lesson_id)
        if not lesson:
            return

        print(f"\n{'='*60}")
        print(f"Lesson {lesson['id']}: {lesson['title']}")
        print(f"Category: {lesson['category'].replace('_', ' ').title()}")
        print(f"Difficulty: {lesson['difficulty'].title()}")
        print(f"{'='*60}\n")

        for line in lesson["content"]:
            print(f"  {line}")

        print(f"\nKey Points:")
        for point in lesson["key_points"]:
            print(f"  - {point}")

        print(f"\nFEN: {lesson['fen']}")
        print(f"\n{'='*60}\n")
