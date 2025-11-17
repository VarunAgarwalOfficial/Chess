import pygame
import sys
import os
import threading
from game import Board
from ai.ai import AI
from features.opening_book import OpeningBook
from features.tutorial import ChessTutorial
from features.puzzles import ChessPuzzles
from features.settings import Settings


'''
Declaring Constants
'''


# SHARP DESIGN - Black, Pink, White, Baby Pink Theme
# Pink palette
PINK_PRIMARY = (236, 64, 122)     # #EC407A - Main pink
PINK_BABY = (248, 187, 208)       # #F8BBD0 - Baby pink
PINK_DARK = (173, 20, 87)         # #AD1457 - Dark pink
PINK_BRIGHT = (255, 64, 129)      # #FF4081 - Bright accent

# Base colors
BLACK = (0, 0, 0)                 # Pure black
WHITE = (255, 255, 255)           # Pure white
GRAY_DARK = (33, 33, 33)          # Dark gray for surfaces
GRAY_MED = (66, 66, 66)           # Medium gray
GRAY_LIGHT = (158, 158, 158)      # Light gray

# Board colors - high contrast
LIGHT = (245, 245, 245)           # Light squares - almost white
DARK = (90, 90, 90)               # Dark squares - medium gray
LIGHT_SELECTED = PINK_PRIMARY     # Pink for selected light
DARK_SELECTED = PINK_DARK         # Dark pink for selected dark

# Highlight colors
HILIGHT = (236, 64, 122, 120)     # Pink highlight
HILIGHT_CAPTURE = (255, 64, 129, 150)  # Bright pink for captures
LAST_MOVE_HIGHLIGHT = (255, 255, 100, 100)  # Light yellow for last move

# UI colors
BLACK_BG = BLACK
DASHBOARD_BG = GRAY_DARK
SURFACE = GRAY_DARK
SURFACE_ELEVATED = GRAY_MED
EVAL_BAR_WHITE = WHITE
EVAL_BAR_BLACK = GRAY_DARK
TEXT_PRIMARY = WHITE
TEXT_SECONDARY = GRAY_LIGHT
TEXT_DISABLED = (117, 117, 117)
BUTTON_COLOR = PINK_PRIMARY
BUTTON_HOVER = PINK_BRIGHT
BUTTON_DISABLED = GRAY_MED
BUTTON_TEXT = WHITE


COLORS = [LIGHT , DARK , LIGHT_SELECTED , DARK_SELECTED]

BOARD_SIZE = 560
DASHBOARD_WIDTH = 380
WIDTH = BOARD_SIZE + DASHBOARD_WIDTH
HEIGHT = BOARD_SIZE
DIMENSION = 8
PIECE_HEIGHT = 70
FPS = 60  # Smoother animations
IMAGES = {
    "black": {},
    "white": {}
}


CLOCK = pygame.time.Clock()

#loading images once
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")
pieces = ["rook", "knight", "bishop",  "king", "pawn" , "queen"]
for piece in pieces:
    IMAGES["black"][piece] = pygame.image.load(os.path.join(ASSETS_DIR, "images", "black", piece + ".png"))
    IMAGES["white"][piece] = pygame.image.load(os.path.join(ASSETS_DIR, "images", "white", piece + ".png"))


'''
Sharp Design Helper Functions
'''

def draw_card(surface, rect, elevated=False):
    '''Draw a sharp-edged card'''
    # Card surface
    color = SURFACE_ELEVATED if elevated else SURFACE
    pygame.draw.rect(surface, color, rect)

    # Border
    border_color = GRAY_MED if elevated else (50, 50, 50)
    pygame.draw.rect(surface, border_color, rect, 2)

def draw_button(surface, rect, text, font, hover=False, disabled=False):
    '''Draw a sharp-edged button'''
    # Button color based on state
    if disabled:
        color = BUTTON_DISABLED
        text_color = TEXT_DISABLED
    elif hover:
        color = BUTTON_HOVER
        text_color = WHITE
    else:
        color = BUTTON_COLOR
        text_color = WHITE

    # Button surface
    pygame.draw.rect(surface, color, rect)

    # Sharp border
    border_color = PINK_BRIGHT if hover else WHITE
    pygame.draw.rect(surface, border_color, rect, 2)

    # Button text
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_back_button(surface, x, y, font, hover=False):
    '''Draw a back button'''
    button_rect = pygame.Rect(x, y, 140, 45)
    draw_button(surface, button_rect, "← BACK", font, hover)
    return button_rect

def draw_chip(surface, x, y, text, font, color=PINK_PRIMARY):
    '''Draw a sharp chip/tag'''
    text_surface = font.render(text, True, WHITE)
    padding = 10
    chip_width = text_surface.get_width() + padding * 2
    chip_height = text_surface.get_height() + padding

    chip_rect = pygame.Rect(x, y, chip_width, chip_height)
    pygame.draw.rect(surface, color, chip_rect)
    pygame.draw.rect(surface, PINK_BRIGHT, chip_rect, 1)

    text_rect = text_surface.get_rect(center=chip_rect.center)
    surface.blit(text_surface, text_rect)

    return chip_width + 8

def draw_divider(surface, x, y, width):
    '''Draw a divider line'''
    pygame.draw.line(surface, GRAY_MED, (x, y), (x + width, y), 2)



class Game:
    def __init__(self):
        pygame.init()
        self.legal_moves = []
        self.board = Board()
        self.screen = pygame.display.set_mode((WIDTH , HEIGHT))
        pygame.display.set_caption("Chess - Python Edition")
        self.running = True
        self.square_selected = (-1,-1)

        # Material UI Typography
        self.font_h1 = pygame.font.Font(None, 64)  # Large titles
        self.font_h2 = pygame.font.Font(None, 48)  # Section headers
        self.font_h3 = pygame.font.Font(None, 32)  # Subsection headers
        self.font = pygame.font.Font(None, 28)     # Body text
        self.small_font = pygame.font.Font(None, 22)  # Small text
        self.tiny_font = pygame.font.Font(None, 18)   # Caption text

        # Game mode settings
        self.game_mode = "pvp"  # "pvp", "pva" (player vs AI), "ava" (AI vs AI)
        self.ai_color = "black"
        self.difficulty = "medium"
        self.ai = None

        # Opening book
        self.opening_book = OpeningBook()

        # Tutorial system
        self.tutorial = ChessTutorial()
        self.show_tutorial = False
        self.tutorial_scroll = 0

        # Puzzle system
        self.puzzles = ChessPuzzles()
        self.show_puzzles = False
        self.puzzle_mode = False
        self.puzzle_board = None
        self.puzzle_feedback = ""
        self.puzzle_solved = False
        self.puzzle_selected_square = (-1, -1)
        self.puzzle_legal_moves = []

        # Settings
        self.settings = Settings()
        self.show_settings = False

        # Help screen
        self.show_help = False

        # Analysis mode
        self.analysis_mode = False
        self.show_hint = False
        self.hint_move = None

        # Evaluation (cached to avoid recalculating every frame)
        self.current_eval = 0
        self.last_move_count = 0  # Track when to update eval

        # Move history
        self.move_history_display = []

        # Captured pieces
        self.captured_pieces = {"white": [], "black": []}

        # AI thinking
        self.ai_thinking = False
        self.ai_thread = None
        self.ai_thinking_dots = 0  # For animated thinking indicator
        self.ai_thinking_timer = 0

        # Last move highlighting
        self.last_move_from = None
        self.last_move_to = None

        # Move animation
        self.animating_move = False
        self.animation_piece = None
        self.animation_from = None
        self.animation_to = None
        self.animation_progress = 0
        self.animation_duration = 250  # milliseconds

        # Menu state
        self.show_menu = True
        self.menu_buttons = []
        self.create_menu()

    def create_menu(self):
        '''Create main menu with better layout'''
        # Two columns of buttons
        col_width = 280
        col_height = 52
        col_spacing = 30
        row_spacing = 20

        # Left column - Game modes
        left_x = WIDTH // 2 - col_width - col_spacing // 2
        left_y = 180

        # Right column - Other features
        right_x = WIDTH // 2 + col_spacing // 2
        right_y = 180

        self.menu_buttons = [
            # Left column - Game modes
            {"rect": pygame.Rect(left_x, left_y, col_width, col_height),
             "text": "PLAYER VS PLAYER", "action": "pvp", "icon": "⚔"},
            {"rect": pygame.Rect(left_x, left_y + col_height + row_spacing, col_width, col_height),
             "text": "VS AI - EASY", "action": "pva_easy", "icon": "🤖"},
            {"rect": pygame.Rect(left_x, left_y + (col_height + row_spacing) * 2, col_width, col_height),
             "text": "VS AI - MEDIUM", "action": "pva_medium", "icon": "🤖"},
            {"rect": pygame.Rect(left_x, left_y + (col_height + row_spacing) * 3, col_width, col_height),
             "text": "VS AI - HARD", "action": "pva_hard", "icon": "🤖"},
            {"rect": pygame.Rect(left_x, left_y + (col_height + row_spacing) * 4, col_width, col_height),
             "text": "VS AI - EXPERT", "action": "pva_expert", "icon": "👑"},

            # Right column - Features
            {"rect": pygame.Rect(right_x, right_y, col_width, col_height),
             "text": "LEARN CHESS", "action": "tutorial", "icon": "📖"},
            {"rect": pygame.Rect(right_x, right_y + col_height + row_spacing, col_width, col_height),
             "text": "SOLVE PUZZLES", "action": "puzzles", "icon": "🧩"},
            {"rect": pygame.Rect(right_x, right_y + (col_height + row_spacing) * 2, col_width, col_height),
             "text": "HELP", "action": "help", "icon": "❓"},
        ]

    def draw_menu(self):
        '''Draw the redesigned main menu'''
        self.screen.fill(BLACK_BG)

        # Header section
        title_text = "CHESS"
        title_surface = self.font_h1.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 60))
        self.screen.blit(title_surface, title_rect)

        subtitle_text = "Master the Game"
        subtitle_surface = self.font_h3.render(subtitle_text, True, PINK_PRIMARY)
        subtitle_rect = subtitle_surface.get_rect(center=(WIDTH // 2, 105))
        self.screen.blit(subtitle_surface, subtitle_rect)

        # Section labels
        left_label_x = WIDTH // 2 - 280 - 15
        right_label_x = WIDTH // 2 + 15
        label_y = 145

        play_label = self.small_font.render("PLAY", True, PINK_BABY)
        self.screen.blit(play_label, (left_label_x, label_y))

        learn_label = self.small_font.render("LEARN", True, PINK_BABY)
        self.screen.blit(learn_label, (right_label_x, label_y))

        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.menu_buttons:
            hover = button["rect"].collidepoint(mouse_pos)
            draw_button(self.screen, button["rect"], button["text"], self.small_font, hover)

    def handle_menu_click(self, pos):
        '''Handle clicks on menu buttons'''
        for button in self.menu_buttons:
            if button["rect"].collidepoint(pos):
                action = button["action"]
                if action == "pvp":
                    self.start_game("pvp", "medium")
                elif action.startswith("pva_"):
                    difficulty = action.split("_")[1]
                    self.start_game("pva", difficulty)
                elif action == "tutorial":
                    self.show_menu = False
                    self.show_tutorial = True
                    self.tutorial.current_lesson_index = 0
                elif action == "puzzles":
                    self.show_menu = False
                    self.show_puzzles = True
                    self.puzzles.current_puzzle_index = 0
                elif action == "help":
                    self.show_menu = False
                    self.show_help = True
                break

    def handle_tutorial_click(self, pos):
        '''Handle clicks in tutorial screen'''
        btn_width = 120
        btn_height = 35
        btn_y = HEIGHT - 50

        # Check back button
        back_rect = pygame.Rect(20, btn_y, btn_width, btn_height)
        if back_rect.collidepoint(pos):
            self.show_tutorial = False
            self.show_menu = True
            return

        # Check previous button
        if self.tutorial.current_lesson_index > 0:
            prev_rect = pygame.Rect(WIDTH//2 - 130, btn_y, btn_width, btn_height)
            if prev_rect.collidepoint(pos):
                self.tutorial.previous_lesson()
                return

        # Check next button
        if self.tutorial.current_lesson_index < len(self.tutorial.lessons) - 1:
            next_rect = pygame.Rect(WIDTH//2 + 10, btn_y, btn_width, btn_height)
            if next_rect.collidepoint(pos):
                self.tutorial.next_lesson()
                return

    def handle_puzzle_click(self, pos):
        '''Handle clicks in puzzle screen'''
        btn_width = 120
        btn_height = 35
        btn_y = HEIGHT - 50

        # Check back button (always visible)
        back_rect = pygame.Rect(20, btn_y, btn_width, btn_height)
        if back_rect.collidepoint(pos):
            self.show_puzzles = False
            self.show_menu = True
            self.puzzle_mode = False
            self.puzzle_board = None
            self.puzzle_feedback = ""
            self.puzzle_solved = False
            self.puzzle_selected_square = (-1, -1)
            self.puzzle_legal_moves = []
            return

        # If in puzzle mode (trying to solve), handle special buttons
        if self.puzzle_mode:
            # "Back to View" button
            back_to_view_rect = pygame.Rect(WIDTH - 160, 20, 140, 40)
            if back_to_view_rect.collidepoint(pos):
                self.puzzle_mode = False
                self.puzzle_board = None
                self.puzzle_feedback = ""
                self.puzzle_solved = False
                self.puzzle_selected_square = (-1, -1)
                self.puzzle_legal_moves = []
                self.puzzles.reset_puzzle()
                return

            # "Hint" button
            hint_rect = pygame.Rect(WIDTH - 160, 70, 140, 40)
            if hint_rect.collidepoint(pos):
                hint = self.puzzles.get_hint()
                self.puzzle_feedback = hint
                return

            # "Reset" button
            reset_rect = pygame.Rect(WIDTH - 160, 120, 140, 40)
            if reset_rect.collidepoint(pos):
                self.reset_puzzle()
                return

            # Handle board clicks
            board_x = 40
            board_y = 80
            board_size = 480
            if (board_x <= pos[0] <= board_x + board_size and
                board_y <= pos[1] <= board_y + board_size):
                # Convert screen position to board position
                square_size = board_size // 8
                col = (pos[0] - board_x) // square_size
                row = (pos[1] - board_y) // square_size
                if 0 <= row < 8 and 0 <= col < 8:
                    self.handle_puzzle_board_click((row, col))
            return

        # Not in puzzle mode - show navigation and "Try Puzzle" button
        # Check "Try Puzzle" button
        try_rect = pygame.Rect(40, HEIGHT - 100, 200, 45)
        if try_rect.collidepoint(pos):
            self.start_puzzle()
            return

        # Check previous button
        if self.puzzles.current_puzzle_index > 0:
            prev_rect = pygame.Rect(WIDTH//2 - 130, btn_y, btn_width, btn_height)
            if prev_rect.collidepoint(pos):
                self.puzzles.previous_puzzle()
                return

        # Check next button
        if self.puzzles.current_puzzle_index < len(self.puzzles.puzzles) - 1:
            next_rect = pygame.Rect(WIDTH//2 + 10, btn_y, btn_width, btn_height)
            if next_rect.collidepoint(pos):
                self.puzzles.next_puzzle()
                return

    def handle_help_click(self, pos):
        '''Handle clicks in help screen'''
        btn_width = 120
        btn_height = 35
        back_rect = pygame.Rect(20, HEIGHT - 50, btn_width, btn_height)
        if back_rect.collidepoint(pos):
            self.show_help = False
            self.show_menu = True

    def start_puzzle(self):
        '''Start the puzzle - load FEN and enter interactive mode'''
        from game.fen_parser import parse_fen

        puzzle = self.puzzles.get_puzzle()
        if not puzzle:
            return

        # Create a new board for the puzzle
        self.puzzle_board = Board()

        # Load the FEN position
        try:
            parse_fen(self.puzzle_board, puzzle['fen'])
            self.puzzle_mode = True
            self.puzzle_feedback = "Your turn! Make the best move."
            self.puzzle_solved = False
            self.puzzle_selected_square = (-1, -1)
            self.puzzle_legal_moves = []
            self.puzzles.reset_puzzle()
        except Exception as e:
            self.puzzle_feedback = f"Error loading puzzle: {str(e)}"
            self.puzzle_mode = False

    def reset_puzzle(self):
        '''Reset the current puzzle to initial position'''
        from game.fen_parser import parse_fen

        puzzle = self.puzzles.get_puzzle()
        if not puzzle:
            return

        # Reset the board
        self.puzzle_board = Board()

        try:
            parse_fen(self.puzzle_board, puzzle['fen'])
            self.puzzle_feedback = "Puzzle reset. Try again!"
            self.puzzle_solved = False
            self.puzzle_selected_square = (-1, -1)
            self.puzzle_legal_moves = []
            self.puzzles.reset_puzzle()
        except Exception as e:
            self.puzzle_feedback = f"Error resetting puzzle: {str(e)}"

    def handle_puzzle_board_click(self, pos):
        '''Handle clicks on the puzzle board'''
        if not self.puzzle_board or self.puzzle_solved:
            return

        # If no piece selected
        if self.puzzle_selected_square == (-1, -1):
            piece = self.puzzle_board.state[pos[0]][pos[1]]
            if piece and piece.color == self.puzzle_board.to_move:
                self.puzzle_selected_square = pos
                self.puzzle_legal_moves = self.puzzle_board.get_legal_moves(pos)
        else:
            # Check if clicked on a legal move
            move_found = None
            for move in self.puzzle_legal_moves:
                if move["to"] == pos:
                    move_found = move
                    break

            if move_found:
                # Make the move
                from_pos = self.puzzle_selected_square
                to_pos = move_found["to"]
                piece = self.puzzle_board.state[from_pos[0]][from_pos[1]]

                # Check if it's a capture BEFORE making the move
                is_capture = self.puzzle_board.state[to_pos[0]][to_pos[1]] is not None

                # Execute the move
                self.puzzle_board.move(from_pos, move_found)

                # Convert to SAN notation
                move_san = self._move_to_san(piece, from_pos, to_pos, move_found, is_capture)

                # Check if the move is correct
                is_correct, is_complete, message = self.puzzles.check_move(move_san)

                if is_correct:
                    if is_complete:
                        self.puzzle_feedback = "Puzzle Solved! Well done!"
                        self.puzzle_solved = True
                    else:
                        self.puzzle_feedback = f"Correct! {message}"
                        # Auto-play opponent's response if there is one
                        self._make_opponent_move()
                else:
                    self.puzzle_feedback = f"Incorrect! {message}"

                self.puzzle_selected_square = (-1, -1)
                self.puzzle_legal_moves = []
            elif pos == self.puzzle_selected_square:
                # Deselect
                self.puzzle_selected_square = (-1, -1)
                self.puzzle_legal_moves = []
            else:
                # Select different piece
                piece = self.puzzle_board.state[pos[0]][pos[1]]
                if piece and piece.color == self.puzzle_board.to_move:
                    self.puzzle_selected_square = pos
                    self.puzzle_legal_moves = self.puzzle_board.get_legal_moves(pos)
                else:
                    self.puzzle_selected_square = (-1, -1)
                    self.puzzle_legal_moves = []

    def _make_opponent_move(self):
        '''Make the opponent's move in puzzle (if solution has opponent moves)'''
        puzzle = self.puzzles.get_puzzle()
        if not puzzle:
            return

        solution = puzzle['solution']
        move_index = len(self.puzzles.user_moves)

        # If there's an opponent move in the solution (odd-indexed moves)
        if move_index < len(solution):
            # For now, just mark that we're waiting for next player move
            # In a full implementation, we'd parse and execute the opponent's move
            pass

    def _move_to_san(self, piece, from_pos, to_pos, move, is_capture):
        '''Convert a move to Standard Algebraic Notation (SAN)'''
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # Handle castling
        if move.get("special") == "KSC":
            return "O-O"
        elif move.get("special") == "QSC":
            return "O-O-O"

        # Build SAN notation
        san = ""

        # Piece symbol (K, Q, R, B, N) - pawns have no symbol
        if piece.type != "pawn":
            san += piece.type[0].upper()

        # Starting square (for disambiguation or pawn captures)
        from_file = files[from_pos[1]]
        from_rank = str(8 - from_pos[0])

        # Capture notation
        if is_capture:
            if piece.type == "pawn":
                san += from_file  # Pawn captures include starting file
            san += "x"

        # Destination square
        to_file = files[to_pos[1]]
        to_rank = str(8 - to_pos[0])
        san += to_file + to_rank

        # Check for promotion
        if move.get("special") == "promotion":
            san += "=Q"  # Assume queen promotion for simplicity

        # Check/checkmate notation (would need to check if move gives check)
        # For simplicity, we'll skip this for now

        return san

    def start_game(self, mode, difficulty):
        '''Start a new game with specified mode and difficulty'''
        self.game_mode = mode
        self.difficulty = difficulty
        self.show_menu = False
        self.show_tutorial = False
        self.show_puzzles = False
        self.show_help = False
        self.board = Board()
        self.square_selected = (-1,-1)
        self.legal_moves = []
        self.opening_book.reset()
        self.move_history_display = []
        self.captured_pieces = {"white": [], "black": []}

        # Reset last move highlighting
        self.last_move_from = None
        self.last_move_to = None

        # Reset animations
        self.animating_move = False
        self.animation_piece = None
        self.animation_from = None
        self.animation_to = None
        self.animation_progress = 0

        # Always create AI for evaluation (even in PvP mode)
        # In PvP, AI is used only for position evaluation, not for making moves
        self.ai = AI(self.board, color=self.ai_color, difficulty=difficulty)

    #drawing things
    def draw(self):
        pygame.display.flip()

        if self.show_menu:
            self.draw_menu()
            return

        if self.show_tutorial:
            self.draw_tutorial()
            return

        if self.show_puzzles:
            self.draw_puzzles()
            return

        if self.show_help:
            self.draw_help()
            return

        self.screen.fill(DASHBOARD_BG)

        # Draw board
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if(self.square_selected == (i,j)):
                    color = COLORS[(i+j)%2 + 2]
                else:
                    color = COLORS[(i+j)%2]

                pygame.draw.rect(self.screen, color, pygame.Rect(j*PIECE_HEIGHT, i*PIECE_HEIGHT, PIECE_HEIGHT, PIECE_HEIGHT))

                # Highlight last move
                if self.last_move_from and (i, j) == self.last_move_from:
                    draw_rect_alpha(self.screen, LAST_MOVE_HIGHLIGHT, pygame.Rect(j*PIECE_HEIGHT, i*PIECE_HEIGHT, PIECE_HEIGHT, PIECE_HEIGHT))
                if self.last_move_to and (i, j) == self.last_move_to:
                    draw_rect_alpha(self.screen, LAST_MOVE_HIGHLIGHT, pygame.Rect(j*PIECE_HEIGHT, i*PIECE_HEIGHT, PIECE_HEIGHT, PIECE_HEIGHT))

                piece = self.board.state[i][j]

                # hilight the possible moves
                if((i,j) in [move["to"] for move in self.legal_moves]):
                    if(self.board.state[i][j] and (i,j) != self.square_selected):
                        draw_rect_alpha(self.screen, HILIGHT_CAPTURE, pygame.Rect(j*PIECE_HEIGHT, i*PIECE_HEIGHT, PIECE_HEIGHT, PIECE_HEIGHT))
                    else:
                        draw_rect_alpha(self.screen, HILIGHT, pygame.Rect(j*PIECE_HEIGHT, i*PIECE_HEIGHT, PIECE_HEIGHT, PIECE_HEIGHT))

                # Draw piece (skip if it's being animated)
                if piece and not (self.animating_move and (i, j) == self.animation_from):
                    self.screen.blit(IMAGES[piece.color][piece.type] ,( j*PIECE_HEIGHT, i*PIECE_HEIGHT))

        # Draw animated piece on top
        if self.animating_move and self.animation_piece:
            self.draw_animated_piece()

        # Draw dashboard
        self.draw_dashboard()

        # Draw check indicator on board
        if self.board.check and not self.board.game_over:
            check_text = "CHECK!" if not self.board.double_check else "DOUBLE CHECK!"
            check_surface = self.font.render(check_text, True, (255, 0, 0))
            self.screen.blit(check_surface, (BOARD_SIZE // 2 - 80, 10))

        # Draw game over message
        if self.board.game_over:
            self.draw_game_over()

        # Draw AI thinking indicator (animated)
        if self.ai_thinking:
            self.draw_ai_thinking_indicator()

        # Draw back button in dashboard area (right side)
        mouse_pos = pygame.mouse.get_pos()
        back_btn_rect = pygame.Rect(BOARD_SIZE + 20, HEIGHT - 55, 140, 45)
        back_hover = back_btn_rect.collidepoint(mouse_pos)
        draw_button(self.screen, back_btn_rect, "← MENU", self.small_font, back_hover)
        self.back_button_rect = back_btn_rect

    def draw_dashboard(self):
        '''Draw the right-side dashboard with Material UI design'''
        dashboard_x = BOARD_SIZE
        dashboard_y = 0

        # Background
        pygame.draw.rect(self.screen, BLACK_BG,
                        pygame.Rect(dashboard_x, dashboard_y, DASHBOARD_WIDTH, HEIGHT))

        margin = 16
        y_offset = margin

        # Game Info Card (increased height to fit opening name properly)
        card_rect = pygame.Rect(dashboard_x + margin, y_offset, DASHBOARD_WIDTH - margin * 2, 170)
        draw_card(self.screen, card_rect, elevated=True)

        # Card content
        card_y = y_offset + 16

        # Game mode with chip
        mode_text = self.game_mode.upper()
        if self.game_mode == "pva":
            mode_text += f" - {self.difficulty.capitalize()}"
        draw_chip(self.screen, dashboard_x + margin + 16, card_y, mode_text, self.tiny_font, PINK_PRIMARY)
        card_y += 40

        # Current turn with pink indicator
        turn_text = f"Turn: {self.board.to_move.capitalize()}"
        turn_color = PINK_BRIGHT if self.board.to_move == "white" else PINK_BABY
        turn_surface = self.small_font.render(turn_text, True, turn_color)
        self.screen.blit(turn_surface, (dashboard_x + margin + 16, card_y))
        card_y += 32

        # Current opening (now with proper spacing)
        opening_text = self.opening_book.get_current_opening()
        if len(opening_text) > 30:
            opening_text = opening_text[:27] + "..."
        opening_label = self.tiny_font.render("Opening:", True, TEXT_DISABLED)
        self.screen.blit(opening_label, (dashboard_x + margin + 16, card_y))
        card_y += 18
        opening_surface = self.tiny_font.render(opening_text, True, TEXT_SECONDARY)
        self.screen.blit(opening_surface, (dashboard_x + margin + 16, card_y))
        card_y += 22  # Add bottom padding

        y_offset += 186

        # Evaluation bar
        y_offset = self.draw_evaluation_bar(dashboard_x, y_offset, margin)

        # Captured pieces
        y_offset = self.draw_captured_pieces(dashboard_x, y_offset, margin)

        # Move history
        y_offset = self.draw_move_history(dashboard_x, y_offset, margin)

    def draw_evaluation_bar(self, x, y, margin):
        '''Draw the evaluation bar'''
        # Evaluation Card
        card_height = 110
        card_rect = pygame.Rect(x + margin, y, DASHBOARD_WIDTH - margin * 2, card_height)
        draw_card(self.screen, card_rect)

        # Calculate evaluation ONLY when position changes (not every frame!)
        # This is a MASSIVE performance improvement - from 3600 evals/min to 2-5/min
        if self.ai and not self.board.game_over and not self.ai_thinking:
            current_move_count = len(self.board.move_log)
            if current_move_count != self.last_move_count:
                self.current_eval = self.ai.evaluate_board() / 100.0  # Convert centipawns to pawns
                self.last_move_count = current_move_count

        # Clamp evaluation between -10 and +10 for display
        display_eval = max(-10, min(10, self.current_eval))

        # Card title
        title_surface = self.small_font.render("Position Evaluation", True, TEXT_PRIMARY)
        self.screen.blit(title_surface, (x + margin + 16, y + 12))

        # Evaluation bar
        bar_y = y + 45
        bar_width = DASHBOARD_WIDTH - margin * 2 - 32
        bar_height = 32

        # Calculate bar fill (0 = all black, 1 = all white)
        white_percentage = (display_eval + 10) / 20.0

        # Bar background
        bar_rect = pygame.Rect(x + margin + 16, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, GRAY_MED, bar_rect)

        # White portion (advantage for white)
        white_width = int(bar_width * white_percentage)
        if white_width > 0:
            white_rect = pygame.Rect(x + margin + 16, bar_y, white_width, bar_height)
            pygame.draw.rect(self.screen, PINK_BABY, white_rect)

        # Black portion (advantage for black)
        black_width = bar_width - white_width
        if black_width > 0:
            black_rect = pygame.Rect(x + margin + 16 + white_width, bar_y, black_width, bar_height)
            pygame.draw.rect(self.screen, GRAY_DARK, black_rect)

        # Center line
        center_x = x + margin + 16 + bar_width // 2
        pygame.draw.line(self.screen, WHITE,
                        (center_x, bar_y), (center_x, bar_y + bar_height), 2)

        # Border
        pygame.draw.rect(self.screen, WHITE, bar_rect, 2)

        # Evaluation text
        eval_text = f"{self.current_eval:+.2f}"
        eval_color = PINK_PRIMARY if self.current_eval > 0 else WHITE
        eval_surface = self.font.render(eval_text, True, eval_color)
        eval_rect = eval_surface.get_rect(center=(center_x, bar_y + bar_height + 18))
        self.screen.blit(eval_surface, eval_rect)

        return y + card_height + margin

    def draw_captured_pieces(self, x, y, margin):
        '''Draw captured pieces'''
        # Captured Pieces Card
        card_height = 90
        card_rect = pygame.Rect(x + margin, y, DASHBOARD_WIDTH - margin * 2, card_height)
        draw_card(self.screen, card_rect)

        # Card title
        title_surface = self.small_font.render("Captured", True, TEXT_PRIMARY)
        self.screen.blit(title_surface, (x + margin + 16, y + 12))

        card_y = y + 42

        # White's captures (black pieces)
        white_label = self.tiny_font.render("White:", True, PINK_BABY)
        self.screen.blit(white_label, (x + margin + 16, card_y))

        white_captures_text = ""
        for piece_type in self.captured_pieces["black"]:
            white_captures_text += f"{piece_type[0].upper()} "
        if not white_captures_text:
            white_captures_text = "None"
        white_surface = self.tiny_font.render(white_captures_text, True, WHITE)
        self.screen.blit(white_surface, (x + margin + 80, card_y))
        card_y += 22

        # Black's captures (white pieces)
        black_label = self.tiny_font.render("Black:", True, TEXT_SECONDARY)
        self.screen.blit(black_label, (x + margin + 16, card_y))

        black_captures_text = ""
        for piece_type in self.captured_pieces["white"]:
            black_captures_text += f"{piece_type[0].upper()} "
        if not black_captures_text:
            black_captures_text = "None"
        black_surface = self.tiny_font.render(black_captures_text, True, WHITE)
        self.screen.blit(black_surface, (x + margin + 80, card_y))

        return y + card_height + margin

    def draw_move_history(self, x, y, margin):
        '''Draw move history with Material UI design'''
        # Calculate available height
        available_height = HEIGHT - y - margin

        # Move History Card
        card_rect = pygame.Rect(x + margin, y, DASHBOARD_WIDTH - margin * 2, available_height)
        draw_card(self.screen, card_rect)

        # Card title
        title_surface = self.small_font.render("Move History", True, TEXT_PRIMARY)
        self.screen.blit(title_surface, (x + margin + 16, y + 12))

        draw_divider(self.screen, x + margin + 16, y + 40, DASHBOARD_WIDTH - margin * 2 - 32)

        # Display moves
        move_y = y + 50
        max_moves = int((available_height - 60) / 20)
        start_index = max(0, len(self.move_history_display) - max_moves)

        for i in range(start_index, len(self.move_history_display)):
            move_text = self.move_history_display[i]
            # Alternate colors for readability
            color = TEXT_PRIMARY if i == len(self.move_history_display) - 1 else TEXT_SECONDARY
            move_surface = self.tiny_font.render(move_text, True, color)
            self.screen.blit(move_surface, (x + margin + 16, move_y))
            move_y += 20

            if move_y > HEIGHT - margin - 20:
                break

        return HEIGHT

    def draw_ai_thinking_indicator(self):
        '''Draw animated AI thinking indicator in dashboard area'''
        # Update animation timer
        current_time = pygame.time.get_ticks()
        if current_time - self.ai_thinking_timer > 400:  # Update every 400ms
            self.ai_thinking_timer = current_time
            self.ai_thinking_dots = (self.ai_thinking_dots + 1) % 4

        # Create text with animated dots
        dots = "." * self.ai_thinking_dots
        thinking_text = f"AI is thinking{dots}"

        # Draw in game info card area (dashboard)
        dashboard_x = BOARD_SIZE
        card_y = 140  # Below the game mode chip

        thinking_surface = self.small_font.render(thinking_text, True, PINK_BRIGHT)
        self.screen.blit(thinking_surface, (dashboard_x + 32, card_y))

    def draw_animated_piece(self):
        '''Draw a piece being animated from one square to another'''
        if not self.animation_piece or self.animation_from is None or self.animation_to is None:
            return

        # Calculate current position using linear interpolation
        from_x = self.animation_from[1] * PIECE_HEIGHT
        from_y = self.animation_from[0] * PIECE_HEIGHT
        to_x = self.animation_to[1] * PIECE_HEIGHT
        to_y = self.animation_to[0] * PIECE_HEIGHT

        # Linear interpolation
        t = self.animation_progress
        current_x = from_x + (to_x - from_x) * t
        current_y = from_y + (to_y - from_y) * t

        # Draw the piece at interpolated position
        piece_img = IMAGES[self.animation_piece.color][self.animation_piece.type]
        self.screen.blit(piece_img, (int(current_x), int(current_y)))

    def update(self):
        '''Update game state and animations'''
        if self.show_menu or self.show_tutorial or self.show_puzzles or self.show_help:
            return

        # Update move animation
        if self.animating_move:
            # Calculate progress based on time elapsed
            delta_time = CLOCK.get_time()  # Time since last frame in ms
            progress_increment = delta_time / self.animation_duration

            self.animation_progress += progress_increment

            if self.animation_progress >= 1.0:
                # Animation complete
                self.animating_move = False
                self.animation_progress = 0
                self.animation_piece = None
                self.animation_from = None
                self.animation_to = None

    def start_move_animation(self, from_pos, to_pos, piece):
        '''Start animating a piece move'''
        self.animating_move = True
        self.animation_from = from_pos
        self.animation_to = to_pos
        self.animation_piece = piece
        self.animation_progress = 0

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            pygame.display.update()
            CLOCK.tick(FPS)

    '''
    Handling events
    '''
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_menu:
                    self.handle_menu_click(event.pos)
                elif self.show_tutorial:
                    self.handle_tutorial_click(event.pos)
                elif self.show_puzzles:
                    self.handle_puzzle_click(event.pos)
                elif self.show_help:
                    self.handle_help_click(event.pos)
                else:
                    # Check back button first
                    if hasattr(self, 'back_button_rect') and self.back_button_rect.collidepoint(event.pos):
                        self.show_menu = True
                        self.square_selected = (-1,-1)
                        self.legal_moves = []
                    else:
                        self.click_handler()
            elif event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and not self.show_menu and not self.show_tutorial and not self.show_puzzles and not self.show_help:
                    self.undo_move()
                elif event.key == pygame.K_r or event.key == pygame.K_ESCAPE:
                    # Return to menu
                    self.show_menu = True
                    self.show_tutorial = False
                    self.show_puzzles = False
                    self.show_help = False
                    self.square_selected = (-1,-1)
                    self.legal_moves = []
                    # Reset puzzle mode
                    self.puzzle_mode = False
                    self.puzzle_board = None
                    self.puzzle_feedback = ""
                    self.puzzle_solved = False
                    self.puzzle_selected_square = (-1, -1)
                    self.puzzle_legal_moves = []

        # Check if AI should make a move
        if (not self.show_menu and
            self.game_mode == "pva" and
            self.board.to_move == self.ai_color and
            not self.board.game_over and
            not self.ai_thinking):
            self.ai_make_move()

    def undo_move(self):
        '''Undo the last move(s)'''
        if len(self.board.move_log) > 0:
            self.board.undo()
            if self.move_history_display:
                self.move_history_display.pop()
            if self.game_mode == "pva" and len(self.board.move_log) > 0:
                # Undo AI move too
                self.board.undo()
                if self.move_history_display:
                    self.move_history_display.pop()

            # Clear last move highlighting after undo
            self.last_move_from = None
            self.last_move_to = None

    def ai_make_move(self):
        '''Make AI move in a separate thread'''
        if self.ai_thread and self.ai_thread.is_alive():
            return

        self.ai_thinking = True

        def ai_move_thread():
            move, pos = self.ai.get_best_move()
            if move and pos:
                # Store the piece for animation (before moving it)
                piece_to_animate = self.board.state[pos[0]][pos[1]]

                # Record captured piece
                if self.board.state[move["to"][0]][move["to"][1]]:
                    captured = self.board.state[move["to"][0]][move["to"][1]]
                    opponent = "white" if self.ai_color == "black" else "black"
                    self.captured_pieces[opponent].append(captured.type)

                # Start animation before making the move
                if piece_to_animate:
                    self.start_move_animation(pos, move["to"], piece_to_animate)

                # Make the move
                self.board.move(pos, move)

                # Update last move highlighting
                self.last_move_from = pos
                self.last_move_to = move["to"]

                # Add to opening book
                self.opening_book.add_move(pos, move["to"])

                # Add to move history
                move_text = self.format_move(pos, move)
                self.move_history_display.append(move_text)

            self.ai_thinking = False

        self.ai_thread = threading.Thread(target=ai_move_thread, daemon=True)
        self.ai_thread.start()

    def format_move(self, from_pos, move):
        '''Format a move for display'''
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        from_square = f"{files[from_pos[1]]}{8-from_pos[0]}"
        to_square = f"{files[move['to'][1]]}{8-move['to'][0]}"

        piece = self.board.state[move["to"][0]][move["to"][1]]
        piece_symbol = piece.type[0].upper() if piece and piece.type != "pawn" else ""

        move_number = len(self.move_history_display) // 2 + 1
        color_indicator = f"{move_number}." if len(self.move_history_display) % 2 == 0 else "..."

        if move["special"] == "KSC":
            return f"{color_indicator} O-O"
        elif move["special"] == "QSC":
            return f"{color_indicator} O-O-O"
        else:
            return f"{color_indicator} {piece_symbol}{from_square}-{to_square}"

    '''
    Draw game over screen
    '''
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((BOARD_SIZE, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # Material UI Card for game result
        card_width = 420
        card_height = 180
        card_x = (BOARD_SIZE - card_width) // 2
        card_y = (HEIGHT - card_height) // 2
        card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
        draw_card(self.screen, card_rect, elevated=True)

        # Determine message and color based on result
        if self.board.game_result == "checkmate_white":
            title = "Checkmate!"
            subtitle = "White Wins"
            color = PINK_BRIGHT
        elif self.board.game_result == "checkmate_black":
            title = "Checkmate!"
            subtitle = "Black Wins"
            color = PINK_BABY
        elif self.board.game_result == "stalemate":
            title = "Draw!"
            subtitle = "Stalemate"
            color = TEXT_SECONDARY
        elif self.board.game_result == "insufficient_material":
            title = "Draw!"
            subtitle = "Insufficient Material"
            color = TEXT_SECONDARY
        elif self.board.game_result == "fifty_move_rule":
            title = "Draw!"
            subtitle = "Fifty Move Rule"
            color = TEXT_SECONDARY
        elif self.board.game_result == "threefold_repetition":
            title = "Draw!"
            subtitle = "Threefold Repetition"
            color = TEXT_SECONDARY
        else:
            title = "Game Over!"
            subtitle = ""
            color = TEXT_PRIMARY

        # Render title
        title_surface = self.font_h2.render(title, True, color)
        title_rect = title_surface.get_rect(center=(BOARD_SIZE // 2, card_y + 50))
        self.screen.blit(title_surface, title_rect)

        # Render subtitle
        if subtitle:
            subtitle_surface = self.font.render(subtitle, True, TEXT_SECONDARY)
            subtitle_rect = subtitle_surface.get_rect(center=(BOARD_SIZE // 2, card_y + 95))
            self.screen.blit(subtitle_surface, subtitle_rect)

        # Render instruction with chip-like styling
        instruction = "Press R to return to menu"
        instruction_surface = self.small_font.render(instruction, True, TEXT_DISABLED)
        instruction_rect = instruction_surface.get_rect(center=(BOARD_SIZE // 2, card_y + 140))
        self.screen.blit(instruction_surface, instruction_rect)

    '''
    Handling game logic when clicked
    '''
    def click_handler(self):
        # Ignore clicks if game is over or AI is thinking
        if self.board.game_over or self.ai_thinking:
            return

        # Ignore clicks outside the board
        click =  pygame.mouse.get_pos()
        if click[0] >= BOARD_SIZE:
            return

        pos = (click[1]// (BOARD_SIZE // 8) , click[0]// (BOARD_SIZE // 8) )

        if(pos[0] < 0 or pos[1] < 0 or pos[0] > 7 or pos[1] > 7):
            return

        # In AI mode, only allow human player to move
        if self.game_mode == "pva" and self.board.to_move == self.ai_color:
            return

        '''
        No piece selected
        '''
        if(self.square_selected == (-1,-1)):
            if(self.board.state[pos[0]][pos[1]]):
                # Only select pieces of the current player
                if self.board.state[pos[0]][pos[1]].color == self.board.to_move:
                    self.square_selected = pos
                    self.legal_moves = self.board.get_legal_moves(pos)
        else:
            '''
            Piece selected
            '''
            found = False
            for move in self.legal_moves:
                if(move["to"] == pos and not found):
                    found = True
                    '''
                    Move is legal
                    '''
                    # Record captured piece
                    if self.board.state[move["to"][0]][move["to"][1]]:
                        captured = self.board.state[move["to"][0]][move["to"][1]]
                        self.captured_pieces[self.board.to_move].append(captured.type)

                    # Make the move
                    self.board.move(self.square_selected, move)

                    # Update last move highlighting
                    self.last_move_from = self.square_selected
                    self.last_move_to = move["to"]

                    # Add to opening book
                    self.opening_book.add_move(self.square_selected, move["to"])

                    # Add to move history
                    move_text = self.format_move(self.square_selected, move)
                    self.move_history_display.append(move_text)

                    self.square_selected = (-1,-1)
                    self.legal_moves = []

            if(pos == self.square_selected and not found):
                '''
                Deselecting the piece
                '''
                self.square_selected = (-1,-1)
                self.legal_moves = []
            elif(not found):
                '''
                Selecting a different piece
                '''
                if(self.board.state[pos[0]][pos[1]]):
                    if self.board.state[pos[0]][pos[1]].color == self.board.to_move:
                        self.square_selected = pos
                        self.legal_moves = self.board.get_legal_moves(pos)
                    else:
                        self.square_selected = (-1,-1)
                        self.legal_moves = []
                else:
                    self.square_selected = (-1,-1)
                    self.legal_moves = []




    def draw_tutorial(self):
        '''Draw tutorial screen with visual board'''
        self.screen.fill(BLACK_BG)

        lesson = self.tutorial.get_lesson()
        if not lesson:
            return

        # Split screen: text on left, board on right
        text_width = WIDTH // 2 - 50
        board_x = WIDTH // 2 + 50
        board_size = 320

        # Header
        title = f"Lesson {lesson['id']}: {lesson['title']}"
        title_surface = self.font_h2.render(title, True, PINK_PRIMARY)
        self.screen.blit(title_surface, (30, 30))

        # Category
        info = f"{lesson['category'].replace('_', ' ').title()}"
        info_surface = self.tiny_font.render(info, True, PINK_BABY)
        self.screen.blit(info_surface, (30, 75))

        # Content with arrows and clean formatting
        y_pos = 120
        for line in lesson['content']:
            if y_pos > HEIGHT - 180:
                break
            text_surface = self.small_font.render(line, True, WHITE)
            self.screen.blit(text_surface, (30, y_pos))
            y_pos += 35

        # Key points section
        y_pos += 20
        points_title = self.small_font.render("Quick Summary:", True, PINK_BABY)
        self.screen.blit(points_title, (30, y_pos))
        y_pos += 30

        for point in lesson['key_points']:
            if y_pos > HEIGHT - 110:
                break
            text_surface = self.tiny_font.render(f"✓ {point}", True, PINK_BABY)
            self.screen.blit(text_surface, (35, y_pos))
            y_pos += 22

        # Draw visual chessboard on right side
        self.draw_lesson_board(board_x, 100, board_size, lesson['fen'])

        # Navigation buttons
        btn_width = 120
        btn_height = 35
        btn_y = HEIGHT - 50

        # Back to menu
        back_rect = pygame.Rect(20, btn_y, btn_width, btn_height)
        pygame.draw.rect(self.screen, BUTTON_COLOR, back_rect)
        pygame.draw.rect(self.screen, WHITE, back_rect, 2)
        back_text = self.tiny_font.render("Back to Menu", True, TEXT_PRIMARY)
        self.screen.blit(back_text, (back_rect.centerx - back_text.get_width()//2, back_rect.centery - back_text.get_height()//2))

        # Previous
        if self.tutorial.current_lesson_index > 0:
            prev_rect = pygame.Rect(WIDTH//2 - 130, btn_y, btn_width, btn_height)
            pygame.draw.rect(self.screen, BUTTON_COLOR, prev_rect)
            pygame.draw.rect(self.screen, WHITE, prev_rect, 2)
            prev_text = self.tiny_font.render("< Previous", True, TEXT_PRIMARY)
            self.screen.blit(prev_text, (prev_rect.centerx - prev_text.get_width()//2, prev_rect.centery - prev_text.get_height()//2))

        # Progress
        progress = self.tutorial.get_progress()
        progress_text = f"Lesson {progress['current_lesson']} / {progress['total']}"
        progress_surface = self.tiny_font.render(progress_text, True, TEXT_SECONDARY)
        self.screen.blit(progress_surface, (WIDTH//2 - progress_surface.get_width()//2, btn_y + 10))

        # Next
        if self.tutorial.current_lesson_index < len(self.tutorial.lessons) - 1:
            next_rect = pygame.Rect(WIDTH//2 + 10, btn_y, btn_width, btn_height)
            pygame.draw.rect(self.screen, BUTTON_COLOR, next_rect)
            pygame.draw.rect(self.screen, WHITE, next_rect, 2)
            next_text = self.tiny_font.render("Next >", True, TEXT_PRIMARY)
            self.screen.blit(next_text, (next_rect.centerx - next_text.get_width()//2, next_rect.centery - next_text.get_height()//2))

    def draw_lesson_board(self, x, y, size, fen):
        '''Draw a chessboard from FEN notation for tutorial lessons'''
        if not fen:
            return

        square_size = size // 8

        # Parse FEN to get piece positions (first part before space)
        fen_parts = fen.split(' ')
        board_fen = fen_parts[0]
        rows = board_fen.split('/')

        # Draw board squares and pieces
        for row_idx, row in enumerate(rows):
            col_idx = 0
            for char in row:
                if char.isdigit():
                    # Empty squares
                    for _ in range(int(char)):
                        color = LIGHT if (row_idx + col_idx) % 2 == 0 else DARK
                        square_rect = pygame.Rect(x + col_idx * square_size,
                                                 y + row_idx * square_size,
                                                 square_size, square_size)
                        pygame.draw.rect(self.screen, color, square_rect)
                        col_idx += 1
                else:
                    # Draw square
                    color = LIGHT if (row_idx + col_idx) % 2 == 0 else DARK
                    square_rect = pygame.Rect(x + col_idx * square_size,
                                             y + row_idx * square_size,
                                             square_size, square_size)
                    pygame.draw.rect(self.screen, color, square_rect)

                    # Draw piece
                    piece_color = "white" if char.isupper() else "black"
                    piece_type_map = {
                        'p': 'pawn', 'n': 'knight', 'b': 'bishop',
                        'r': 'rook', 'q': 'queen', 'k': 'king'
                    }
                    piece_type = piece_type_map[char.lower()]

                    piece_img = IMAGES[piece_color][piece_type]
                    scaled_img = pygame.transform.scale(piece_img, (square_size - 4, square_size - 4))
                    img_rect = scaled_img.get_rect(center=square_rect.center)
                    self.screen.blit(scaled_img, img_rect)

                    col_idx += 1

        # Draw border around the board
        border_rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(self.screen, WHITE, border_rect, 2)

    def draw_puzzles(self):
        '''Draw puzzle screen'''
        self.screen.fill(BLACK_BG)

        puzzle = self.puzzles.get_puzzle()
        if not puzzle:
            return

        # If in puzzle mode, draw interactive board
        if self.puzzle_mode and self.puzzle_board:
            self.draw_puzzle_board()
            return

        # Not in puzzle mode - show puzzle information
        # Header
        header_font = pygame.font.Font(None, 40)
        title = f"Puzzle {puzzle['id']}: {puzzle['name']}"
        title_surface = header_font.render(title, True, PINK_PRIMARY)
        self.screen.blit(title_surface, (20, 20))

        # Theme and difficulty
        info = f"{puzzle['theme']} | {puzzle['difficulty'].title()}"
        info_surface = self.tiny_font.render(info, True, PINK_BABY)
        self.screen.blit(info_surface, (20, 60))

        # Description
        desc_surface = self.small_font.render(puzzle['description'], True, PINK_BRIGHT)
        self.screen.blit(desc_surface, (20, 90))

        # FEN position
        fen_label = self.tiny_font.render("Position (FEN):", True, TEXT_DISABLED)
        self.screen.blit(fen_label, (20, 130))
        fen_surface = self.tiny_font.render(puzzle['fen'], True, TEXT_SECONDARY)
        self.screen.blit(fen_surface, (20, 155))

        # Solution moves
        sol_label = self.small_font.render("Solution:", True, PINK_PRIMARY)
        self.screen.blit(sol_label, (20, 190))

        y_pos = 220
        for i, move in enumerate(puzzle['solution'], 1):
            move_text = f"{i}. {move}"
            move_surface = self.tiny_font.render(move_text, True, TEXT_PRIMARY)
            self.screen.blit(move_surface, (30, y_pos))
            y_pos += 22

        # Instructions
        inst_y = 320
        instructions = [
            "Click 'Try Puzzle' to solve interactively on the board.",
            "Or study the solution and try it on an external board.",
            "Use navigation buttons to browse other puzzles."
        ]

        inst_label = self.small_font.render("How to solve:", True, PINK_BABY)
        self.screen.blit(inst_label, (20, inst_y))
        inst_y += 30

        for line in instructions:
            text_surface = self.tiny_font.render(line, True, TEXT_SECONDARY)
            self.screen.blit(text_surface, (30, inst_y))
            inst_y += 22

        # "Try Puzzle" button (big and prominent)
        mouse_pos = pygame.mouse.get_pos()
        try_rect = pygame.Rect(40, HEIGHT - 100, 200, 45)
        try_hover = try_rect.collidepoint(mouse_pos)
        draw_button(self.screen, try_rect, "Try Puzzle", self.small_font, try_hover)

        # Navigation buttons
        btn_width = 120
        btn_height = 35
        btn_y = HEIGHT - 50

        # Back to menu
        back_rect = pygame.Rect(20, btn_y, btn_width, btn_height)
        back_hover = back_rect.collidepoint(mouse_pos)
        draw_button(self.screen, back_rect, "Back to Menu", self.tiny_font, back_hover)

        # Previous
        if self.puzzles.current_puzzle_index > 0:
            prev_rect = pygame.Rect(WIDTH//2 - 130, btn_y, btn_width, btn_height)
            prev_hover = prev_rect.collidepoint(mouse_pos)
            draw_button(self.screen, prev_rect, "< Previous", self.tiny_font, prev_hover)

        # Progress
        progress = self.puzzles.get_progress()
        progress_text = f"Puzzle {progress['current']} / {progress['total']}"
        progress_surface = self.tiny_font.render(progress_text, True, TEXT_SECONDARY)
        self.screen.blit(progress_surface, (WIDTH//2 - progress_surface.get_width()//2, btn_y + 10))

        # Next
        if self.puzzles.current_puzzle_index < len(self.puzzles.puzzles) - 1:
            next_rect = pygame.Rect(WIDTH//2 + 10, btn_y, btn_width, btn_height)
            next_hover = next_rect.collidepoint(mouse_pos)
            draw_button(self.screen, next_rect, "Next >", self.tiny_font, next_hover)

    def draw_puzzle_board(self):
        '''Draw the interactive puzzle board when in puzzle mode'''
        self.screen.fill(BLACK_BG)

        puzzle = self.puzzles.get_puzzle()
        if not puzzle or not self.puzzle_board:
            return

        board_x = 40
        board_y = 80
        board_size = 480
        square_size = board_size // 8

        # Header
        title = f"Puzzle {puzzle['id']}: {puzzle['name']}"
        title_surface = self.font_h3.render(title, True, PINK_PRIMARY)
        self.screen.blit(title_surface, (board_x, 20))

        # Draw the board
        for i in range(8):
            for j in range(8):
                # Determine square color
                if self.puzzle_selected_square == (i, j):
                    color = LIGHT_SELECTED if (i + j) % 2 == 0 else DARK_SELECTED
                else:
                    color = LIGHT if (i + j) % 2 == 0 else DARK

                square_rect = pygame.Rect(board_x + j * square_size,
                                         board_y + i * square_size,
                                         square_size, square_size)
                pygame.draw.rect(self.screen, color, square_rect)

                # Highlight legal moves
                if (i, j) in [move["to"] for move in self.puzzle_legal_moves]:
                    target_piece = self.puzzle_board.state[i][j]
                    if target_piece:
                        draw_rect_alpha(self.screen, HILIGHT_CAPTURE, square_rect)
                    else:
                        draw_rect_alpha(self.screen, HILIGHT, square_rect)

                # Draw piece
                piece = self.puzzle_board.state[i][j]
                if piece:
                    piece_img = IMAGES[piece.color][piece.type]
                    scaled_img = pygame.transform.scale(piece_img, (square_size - 8, square_size - 8))
                    img_rect = scaled_img.get_rect(center=square_rect.center)
                    self.screen.blit(scaled_img, img_rect)

        # Draw border around board
        border_rect = pygame.Rect(board_x, board_y, board_size, board_size)
        pygame.draw.rect(self.screen, WHITE, border_rect, 3)

        # Right side panel with controls and feedback
        panel_x = board_x + board_size + 40
        panel_y = 80

        # Turn indicator
        turn_text = f"Turn: {self.puzzle_board.to_move.capitalize()}"
        turn_color = PINK_BRIGHT if self.puzzle_board.to_move == "white" else PINK_BABY
        turn_surface = self.small_font.render(turn_text, True, turn_color)
        self.screen.blit(turn_surface, (panel_x, panel_y))
        panel_y += 40

        # Puzzle info
        theme_text = f"Theme: {puzzle['theme']}"
        theme_surface = self.tiny_font.render(theme_text, True, TEXT_SECONDARY)
        self.screen.blit(theme_surface, (panel_x, panel_y))
        panel_y += 25

        diff_text = f"Difficulty: {puzzle['difficulty'].title()}"
        diff_surface = self.tiny_font.render(diff_text, True, TEXT_SECONDARY)
        self.screen.blit(diff_surface, (panel_x, panel_y))
        panel_y += 40

        # Feedback message (colored based on content)
        if self.puzzle_feedback:
            if "Solved" in self.puzzle_feedback or "Correct" in self.puzzle_feedback:
                feedback_color = (100, 255, 100)  # Green
            elif "Incorrect" in self.puzzle_feedback:
                feedback_color = (255, 100, 100)  # Red
            else:
                feedback_color = PINK_BABY

            # Wrap feedback text if too long
            max_width = 350
            words = self.puzzle_feedback.split()
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                test_surface = self.tiny_font.render(test_line, True, feedback_color)
                if test_surface.get_width() <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

            for line in lines:
                feedback_surface = self.tiny_font.render(line, True, feedback_color)
                self.screen.blit(feedback_surface, (panel_x, panel_y))
                panel_y += 22

        panel_y += 30

        # Control buttons on the right
        mouse_pos = pygame.mouse.get_pos()

        # "Back to View" button
        back_to_view_rect = pygame.Rect(WIDTH - 160, 20, 140, 40)
        back_to_view_hover = back_to_view_rect.collidepoint(mouse_pos)
        draw_button(self.screen, back_to_view_rect, "Back to View", self.tiny_font, back_to_view_hover)

        # "Hint" button
        hint_rect = pygame.Rect(WIDTH - 160, 70, 140, 40)
        hint_hover = hint_rect.collidepoint(mouse_pos)
        hint_disabled = self.puzzle_solved
        draw_button(self.screen, hint_rect, "Hint", self.tiny_font, hint_hover, hint_disabled)

        # "Reset" button
        reset_rect = pygame.Rect(WIDTH - 160, 120, 140, 40)
        reset_hover = reset_rect.collidepoint(mouse_pos)
        draw_button(self.screen, reset_rect, "Reset", self.tiny_font, reset_hover)

        # Show move count
        moves_made = len(self.puzzles.user_moves)
        total_moves = len(puzzle['solution'])
        progress_text = f"Moves: {moves_made}/{total_moves}"
        progress_surface = self.tiny_font.render(progress_text, True, TEXT_SECONDARY)
        self.screen.blit(progress_surface, (WIDTH - 160, 180))

        # Navigation buttons at bottom
        btn_width = 120
        btn_height = 35
        btn_y = HEIGHT - 50

        # Back to menu
        back_rect = pygame.Rect(20, btn_y, btn_width, btn_height)
        back_hover = back_rect.collidepoint(mouse_pos)
        draw_button(self.screen, back_rect, "Back to Menu", self.tiny_font, back_hover)

    def draw_help(self):
        '''Draw help screen'''
        self.screen.fill(DASHBOARD_BG)

        # Header
        header_font = pygame.font.Font(None, 48)
        title_surface = header_font.render("Help & Instructions", True, TEXT_PRIMARY)
        self.screen.blit(title_surface, (20, 20))

        help_sections = [
            ("How to Play:", [
                "- Click on a piece to see its legal moves",
                "- Click on a highlighted square to move there",
                "- Special moves: castling, en passant, promotion are automatic",
                "- Game ends with checkmate, stalemate, or draw conditions"
            ]),
            ("Game Modes:", [
                "- Player vs Player: Play against a friend",
                "- Player vs AI: Play against computer (Easy/Medium/Hard/Expert)",
                "- Tutorial: Learn chess basics with 20 structured lessons",
                "- Puzzles: Solve 40 tactical puzzles to improve your skills"
            ]),
            ("AI Difficulty Levels:", [
                "- Easy: Depth 2 search (~1K nodes, beginner level)",
                "- Medium: Depth 3 search (~10K nodes, intermediate)",
                "- Hard: Depth 4 search (~50K nodes, advanced)",
                "- Expert: Depth 5 search (~250K nodes, expert level)"
            ]),
            ("Features:", [
                "- Advanced AI with optimizations (LMR, null move, aspiration)",
                "- Opening book recognition",
                "- Move history and captured pieces display",
                "- Evaluation bar showing position advantage",
                "- 40 tactical puzzles covering all major themes",
                "- 20 comprehensive tutorial lessons"
            ]),
            ("Controls:", [
                "- Left Click: Select piece / Make move",
                "- ESC: Return to main menu (during game)",
                "- Mouse Hover: See button highlights in menus"
            ])
        ]

        y_pos = 80
        for section_title, section_lines in help_sections:
            if y_pos > HEIGHT - 100:
                break

            # Section title
            section_surface = self.small_font.render(section_title, True, PINK_PRIMARY)
            self.screen.blit(section_surface, (20, y_pos))
            y_pos += 28

            # Section content
            for line in section_lines:
                if y_pos > HEIGHT - 100:
                    break
                text_surface = self.tiny_font.render(line, True, TEXT_PRIMARY)
                self.screen.blit(text_surface, (30, y_pos))
                y_pos += 20

            y_pos += 10

        # Back button
        btn_width = 120
        btn_height = 35
        back_rect = pygame.Rect(20, HEIGHT - 50, btn_width, btn_height)
        pygame.draw.rect(self.screen, BUTTON_COLOR, back_rect)
        pygame.draw.rect(self.screen, WHITE, back_rect, 2)
        back_text = self.tiny_font.render("Back to Menu", True, TEXT_PRIMARY)
        self.screen.blit(back_text, (back_rect.centerx - back_text.get_width()//2, back_rect.centery - back_text.get_height()//2))

        # Credits
        credits_text = "Chess Master - Advanced AI with Educational Tools"
        credits_surface = self.tiny_font.render(credits_text, True, (100, 100, 100))
        self.screen.blit(credits_surface, (WIDTH - credits_surface.get_width() - 20, HEIGHT - 25))


'''
Drawing Functions
'''
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)



'''
Main Function
'''


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
