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


# COLORS
LIGHT = (241,218,179)
DARK = (182,136,96)
LIGHT_SELECTED = "#00BCD4"
DARK_SELECTED = "#08a8c6"

HILIGHT = (0,188,212 , 50)
HILIGHT_CAPTURE = (173,238,126 , 150)

# Dashboard colors
DASHBOARD_BG = (40, 40, 40)
EVAL_BAR_WHITE = (220, 220, 220)
EVAL_BAR_BLACK = (60, 60, 60)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)


COLORS = [LIGHT , DARK , LIGHT_SELECTED , DARK_SELECTED]

BOARD_SIZE = 480
DASHBOARD_WIDTH = 320
WIDTH = BOARD_SIZE + DASHBOARD_WIDTH
HEIGHT = BOARD_SIZE
DIMENSION = 8
PIECE_HEIGHT = 60
FPS = 30
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





class Game:
    def __init__(self):
        pygame.init()
        self.legal_moves = []
        self.board = Board()
        self.screen = pygame.display.set_mode((WIDTH , HEIGHT))
        pygame.display.set_caption("Chess - Python Edition")
        self.running = True
        self.square_selected = (-1,-1)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 18)

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

        # Settings
        self.settings = Settings()
        self.show_settings = False

        # Help screen
        self.show_help = False

        # Analysis mode
        self.analysis_mode = False
        self.show_hint = False
        self.hint_move = None

        # Evaluation
        self.current_eval = 0

        # Move history
        self.move_history_display = []

        # Captured pieces
        self.captured_pieces = {"white": [], "black": []}

        # AI thinking
        self.ai_thinking = False
        self.ai_thread = None

        # Menu state
        self.show_menu = True
        self.menu_buttons = []
        self.create_menu()

    def create_menu(self):
        '''Create main menu buttons'''
        button_width = 280
        button_height = 45
        start_x = WIDTH // 2 - button_width // 2
        start_y = 100
        spacing = 55

        self.menu_buttons = [
            {"rect": pygame.Rect(start_x, start_y, button_width, button_height),
             "text": "Player vs Player", "action": "pvp"},
            {"rect": pygame.Rect(start_x, start_y + spacing, button_width, button_height),
             "text": "Player vs AI (Easy)", "action": "pva_easy"},
            {"rect": pygame.Rect(start_x, start_y + spacing * 2, button_width, button_height),
             "text": "Player vs AI (Medium)", "action": "pva_medium"},
            {"rect": pygame.Rect(start_x, start_y + spacing * 3, button_width, button_height),
             "text": "Player vs AI (Hard)", "action": "pva_hard"},
            {"rect": pygame.Rect(start_x, start_y + spacing * 4, button_width, button_height),
             "text": "Player vs AI (Expert)", "action": "pva_expert"},
            {"rect": pygame.Rect(start_x, start_y + spacing * 5, button_width, button_height),
             "text": "Learn Chess (Tutorial)", "action": "tutorial"},
            {"rect": pygame.Rect(start_x, start_y + spacing * 6, button_width, button_height),
             "text": "Solve Puzzles (40 Tactics)", "action": "puzzles"},
            {"rect": pygame.Rect(start_x, start_y + spacing * 7, button_width, button_height),
             "text": "Help & Instructions", "action": "help"},
        ]

    def draw_menu(self):
        '''Draw the main menu'''
        self.screen.fill(DASHBOARD_BG)

        # Title
        title_font = pygame.font.Font(None, 56)
        title_text = "Chess Master"
        title_surface = title_font.render(title_text, True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 50))
        self.screen.blit(title_surface, title_rect)

        # Subtitle
        subtitle_text = "Professional Chess Engine with AI & Learning Tools"
        subtitle_surface = self.tiny_font.render(subtitle_text, True, (180, 180, 180))
        subtitle_rect = subtitle_surface.get_rect(center=(WIDTH // 2, 78))
        self.screen.blit(subtitle_surface, subtitle_rect)

        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.menu_buttons:
            color = BUTTON_HOVER if button["rect"].collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(self.screen, color, button["rect"], border_radius=10)
            pygame.draw.rect(self.screen, TEXT_COLOR, button["rect"], 2, border_radius=10)

            text_surface = self.small_font.render(button["text"], True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)

        # Footer
        footer_text = "40 Puzzles | 20 Tutorials | Advanced AI with Optimizations"
        footer_surface = self.tiny_font.render(footer_text, True, (140, 140, 140))
        footer_rect = footer_surface.get_rect(center=(WIDTH // 2, HEIGHT - 20))
        self.screen.blit(footer_surface, footer_rect)

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

        # Check back button
        back_rect = pygame.Rect(20, btn_y, btn_width, btn_height)
        if back_rect.collidepoint(pos):
            self.show_puzzles = False
            self.show_menu = True
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

        if mode == "pva":
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
                piece = self.board.state[i][j]

                # hilight the possible moves
                if((i,j) in [move["to"] for move in self.legal_moves]):
                    if(self.board.state[i][j] and (i,j) != self.square_selected):
                        draw_rect_alpha(self.screen, HILIGHT_CAPTURE, pygame.Rect(j*PIECE_HEIGHT, i*PIECE_HEIGHT, PIECE_HEIGHT, PIECE_HEIGHT))
                    else:
                        draw_rect_alpha(self.screen, HILIGHT, pygame.Rect(j*PIECE_HEIGHT, i*PIECE_HEIGHT, PIECE_HEIGHT, PIECE_HEIGHT))


                if(piece):
                    self.screen.blit(IMAGES[piece.color][piece.type] ,( j*PIECE_HEIGHT, i*PIECE_HEIGHT))

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

        # Draw AI thinking indicator
        if self.ai_thinking:
            thinking_text = "AI is thinking..."
            thinking_surface = self.small_font.render(thinking_text, True, (255, 255, 0))
            self.screen.blit(thinking_surface, (BOARD_SIZE // 2 - 80, HEIGHT - 30))

    def draw_dashboard(self):
        '''Draw the right-side dashboard'''
        dashboard_x = BOARD_SIZE
        dashboard_y = 0

        # Background
        pygame.draw.rect(self.screen, DASHBOARD_BG,
                        pygame.Rect(dashboard_x, dashboard_y, DASHBOARD_WIDTH, HEIGHT))

        y_offset = 10

        # Game mode
        mode_text = f"Mode: {self.game_mode.upper()}"
        if self.game_mode == "pva":
            mode_text += f" ({self.difficulty.capitalize()})"
        mode_surface = self.small_font.render(mode_text, True, TEXT_COLOR)
        self.screen.blit(mode_surface, (dashboard_x + 10, y_offset))
        y_offset += 35

        # Current turn
        turn_text = f"Turn: {self.board.to_move.capitalize()}"
        turn_surface = self.small_font.render(turn_text, True, TEXT_COLOR)
        self.screen.blit(turn_surface, (dashboard_x + 10, y_offset))
        y_offset += 35

        # Current opening
        opening_text = f"Opening: {self.opening_book.get_current_opening()}"
        opening_surface = self.tiny_font.render(opening_text, True, (200, 200, 200))
        self.screen.blit(opening_surface, (dashboard_x + 10, y_offset))
        y_offset += 25

        # Evaluation bar
        y_offset = self.draw_evaluation_bar(dashboard_x, y_offset)

        # Captured pieces
        y_offset = self.draw_captured_pieces(dashboard_x, y_offset)

        # Move history
        y_offset = self.draw_move_history(dashboard_x, y_offset)

    def draw_evaluation_bar(self, x, y):
        '''Draw the evaluation bar showing position advantage'''
        bar_width = DASHBOARD_WIDTH - 20
        bar_height = 30
        margin = 10

        # Calculate evaluation if AI exists
        if self.ai and not self.board.game_over:
            self.current_eval = self.ai.evaluate_board() / 100.0  # Convert centipawns to pawns

        # Clamp evaluation between -10 and +10 for display
        display_eval = max(-10, min(10, self.current_eval))

        # Calculate bar fill (0 = all black, 1 = all white)
        white_percentage = (display_eval + 10) / 20.0

        # Draw bar background
        pygame.draw.rect(self.screen, EVAL_BAR_BLACK,
                        pygame.Rect(x + margin, y, bar_width, bar_height))

        # Draw white portion
        white_width = int(bar_width * white_percentage)
        pygame.draw.rect(self.screen, EVAL_BAR_WHITE,
                        pygame.Rect(x + margin, y, white_width, bar_height))

        # Draw border
        pygame.draw.rect(self.screen, TEXT_COLOR,
                        pygame.Rect(x + margin, y, bar_width, bar_height), 2)

        # Draw evaluation text
        eval_text = f"Eval: {self.current_eval:+.2f}"
        eval_surface = self.tiny_font.render(eval_text, True, TEXT_COLOR)
        self.screen.blit(eval_surface, (x + margin + bar_width // 2 - 30, y + 7))

        return y + bar_height + 20

    def draw_captured_pieces(self, x, y):
        '''Draw captured pieces'''
        margin = 10

        # Title
        title_surface = self.tiny_font.render("Captured Pieces:", True, TEXT_COLOR)
        self.screen.blit(title_surface, (x + margin, y))
        y += 25

        # White's captures (black pieces)
        white_captures_text = "White: "
        for piece_type in self.captured_pieces["black"]:
            white_captures_text += f"{piece_type[0].upper()} "
        white_surface = self.tiny_font.render(white_captures_text, True, TEXT_COLOR)
        self.screen.blit(white_surface, (x + margin, y))
        y += 20

        # Black's captures (white pieces)
        black_captures_text = "Black: "
        for piece_type in self.captured_pieces["white"]:
            black_captures_text += f"{piece_type[0].upper()} "
        black_surface = self.tiny_font.render(black_captures_text, True, TEXT_COLOR)
        self.screen.blit(black_surface, (x + margin, y))
        y += 30

        return y

    def draw_move_history(self, x, y):
        '''Draw move history'''
        margin = 10

        # Title
        title_surface = self.tiny_font.render("Move History:", True, TEXT_COLOR)
        self.screen.blit(title_surface, (x + margin, y))
        y += 25

        # Display last 15 moves
        start_index = max(0, len(self.move_history_display) - 15)
        for i in range(start_index, len(self.move_history_display)):
            move_text = self.move_history_display[i]
            move_surface = self.tiny_font.render(move_text, True, (200, 200, 200))
            self.screen.blit(move_surface, (x + margin, y))
            y += 18

            if y > HEIGHT - 30:
                break

        return y

    def run(self):
        while self.running:
            self.events()
            # self.update()
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

    def ai_make_move(self):
        '''Make AI move in a separate thread'''
        if self.ai_thread and self.ai_thread.is_alive():
            return

        self.ai_thinking = True

        def ai_move_thread():
            move, pos = self.ai.get_best_move()
            if move and pos:
                # Record captured piece
                if self.board.state[move["to"][0]][move["to"][1]]:
                    captured = self.board.state[move["to"][0]][move["to"][1]]
                    opponent = "white" if self.ai_color == "black" else "black"
                    self.captured_pieces[opponent].append(captured.type)

                # Make the move
                self.board.move(pos, move)

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
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Determine message based on result
        if self.board.game_result == "checkmate_white":
            message = "Checkmate! White Wins!"
            color = (255, 255, 255)
        elif self.board.game_result == "checkmate_black":
            message = "Checkmate! Black Wins!"
            color = (50, 50, 50)
        elif self.board.game_result == "stalemate":
            message = "Stalemate! Draw!"
            color = (200, 200, 0)
        elif self.board.game_result == "insufficient_material":
            message = "Draw by Insufficient Material!"
            color = (200, 200, 0)
        elif self.board.game_result == "fifty_move_rule":
            message = "Draw by Fifty Move Rule!"
            color = (200, 200, 0)
        elif self.board.game_result == "threefold_repetition":
            message = "Draw by Threefold Repetition!"
            color = (200, 200, 0)
        else:
            message = "Game Over!"
            color = (255, 255, 255)

        # Render main message
        text_surface = self.font.render(message, True, color)
        text_rect = text_surface.get_rect(center=(BOARD_SIZE // 2, HEIGHT // 2 - 20))
        self.screen.blit(text_surface, text_rect)

        # Render instruction
        instruction = "Press R to return to menu"
        instruction_surface = self.small_font.render(instruction, True, (255, 255, 255))
        instruction_rect = instruction_surface.get_rect(center=(BOARD_SIZE // 2, HEIGHT // 2 + 20))
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

        pos = (click[1]// 60 , click[0]// 60 )

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
        '''Draw tutorial screen'''
        self.screen.fill(DASHBOARD_BG)

        lesson = self.tutorial.get_lesson()
        if not lesson:
            return

        # Header
        header_font = pygame.font.Font(None, 40)
        title = f"Lesson {lesson['id']}: {lesson['title']}"
        title_surface = header_font.render(title, True, TEXT_COLOR)
        self.screen.blit(title_surface, (20, 20))

        # Category and difficulty
        info = f"{lesson['category'].replace('_', ' ').title()} | {lesson['difficulty'].title()}"
        info_surface = self.tiny_font.render(info, True, (180, 180, 180))
        self.screen.blit(info_surface, (20, 60))

        # Content
        y_pos = 100
        for line in lesson['content']:
            if y_pos > HEIGHT - 150:
                break
            text_surface = self.tiny_font.render(line, True, TEXT_COLOR)
            self.screen.blit(text_surface, (20, y_pos))
            y_pos += 25

        # Key points
        y_pos += 10
        points_title = self.small_font.render("Key Points:", True, (100, 200, 255))
        self.screen.blit(points_title, (20, y_pos))
        y_pos += 30

        for point in lesson['key_points']:
            if y_pos > HEIGHT - 100:
                break
            text_surface = self.tiny_font.render(f"- {point}", True, (150, 220, 150))
            self.screen.blit(text_surface, (30, y_pos))
            y_pos += 22

        # Navigation buttons
        btn_width = 120
        btn_height = 35
        btn_y = HEIGHT - 50

        # Back to menu
        back_rect = pygame.Rect(20, btn_y, btn_width, btn_height)
        pygame.draw.rect(self.screen, BUTTON_COLOR, back_rect, border_radius=8)
        back_text = self.tiny_font.render("Back to Menu", True, TEXT_COLOR)
        self.screen.blit(back_text, (back_rect.centerx - back_text.get_width()//2, back_rect.centery - back_text.get_height()//2))

        # Previous
        if self.tutorial.current_lesson_index > 0:
            prev_rect = pygame.Rect(WIDTH//2 - 130, btn_y, btn_width, btn_height)
            pygame.draw.rect(self.screen, BUTTON_COLOR, prev_rect, border_radius=8)
            prev_text = self.tiny_font.render("< Previous", True, TEXT_COLOR)
            self.screen.blit(prev_text, (prev_rect.centerx - prev_text.get_width()//2, prev_rect.centery - prev_text.get_height()//2))

        # Progress
        progress = self.tutorial.get_progress()
        progress_text = f"Lesson {progress['current']} / {progress['total']}"
        progress_surface = self.tiny_font.render(progress_text, True, (180, 180, 180))
        self.screen.blit(progress_surface, (WIDTH//2 - progress_surface.get_width()//2, btn_y + 10))

        # Next
        if self.tutorial.current_lesson_index < len(self.tutorial.lessons) - 1:
            next_rect = pygame.Rect(WIDTH//2 + 10, btn_y, btn_width, btn_height)
            pygame.draw.rect(self.screen, BUTTON_COLOR, next_rect, border_radius=8)
            next_text = self.tiny_font.render("Next >", True, TEXT_COLOR)
            self.screen.blit(next_text, (next_rect.centerx - next_text.get_width()//2, next_rect.centery - next_text.get_height()//2))

    def draw_puzzles(self):
        '''Draw puzzle screen'''
        self.screen.fill(DASHBOARD_BG)

        puzzle = self.puzzles.get_puzzle()
        if not puzzle:
            return

        # Header
        header_font = pygame.font.Font(None, 40)
        title = f"Puzzle {puzzle['id']}: {puzzle['name']}"
        title_surface = header_font.render(title, True, TEXT_COLOR)
        self.screen.blit(title_surface, (20, 20))

        # Theme and difficulty
        info = f"{puzzle['theme']} | {puzzle['difficulty'].title()}"
        info_surface = self.tiny_font.render(info, True, (180, 180, 180))
        self.screen.blit(info_surface, (20, 60))

        # Description
        desc_surface = self.small_font.render(puzzle['description'], True, (255, 200, 100))
        self.screen.blit(desc_surface, (20, 90))

        # FEN position
        fen_label = self.tiny_font.render("Position (FEN):", True, (150, 150, 150))
        self.screen.blit(fen_label, (20, 130))
        fen_surface = self.tiny_font.render(puzzle['fen'], True, TEXT_COLOR)
        self.screen.blit(fen_surface, (20, 155))

        # Solution moves
        sol_label = self.small_font.render("Solution:", True, (100, 255, 100))
        self.screen.blit(sol_label, (20, 190))

        y_pos = 220
        for i, move in enumerate(puzzle['solution'], 1):
            move_text = f"{i}. {move}"
            move_surface = self.tiny_font.render(move_text, True, TEXT_COLOR)
            self.screen.blit(move_surface, (30, y_pos))
            y_pos += 22

        # Instructions
        inst_y = 320
        instructions = [
            "Set up this position on a real board or online chess site.",
            "Try to find the best move sequence.",
            "Check the solution when ready.",
            "Study the tactical pattern to improve your chess vision."
        ]

        inst_label = self.small_font.render("How to solve:", True, (255, 255, 100))
        self.screen.blit(inst_label, (20, inst_y))
        inst_y += 30

        for line in instructions:
            text_surface = self.tiny_font.render(line, True, (200, 200, 200))
            self.screen.blit(text_surface, (30, inst_y))
            inst_y += 22

        # Navigation buttons
        btn_width = 120
        btn_height = 35
        btn_y = HEIGHT - 50

        # Back to menu
        back_rect = pygame.Rect(20, btn_y, btn_width, btn_height)
        pygame.draw.rect(self.screen, BUTTON_COLOR, back_rect, border_radius=8)
        back_text = self.tiny_font.render("Back to Menu", True, TEXT_COLOR)
        self.screen.blit(back_text, (back_rect.centerx - back_text.get_width()//2, back_rect.centery - back_text.get_height()//2))

        # Previous
        if self.puzzles.current_puzzle_index > 0:
            prev_rect = pygame.Rect(WIDTH//2 - 130, btn_y, btn_width, btn_height)
            pygame.draw.rect(self.screen, BUTTON_COLOR, prev_rect, border_radius=8)
            prev_text = self.tiny_font.render("< Previous", True, TEXT_COLOR)
            self.screen.blit(prev_text, (prev_rect.centerx - prev_text.get_width()//2, prev_rect.centery - prev_text.get_height()//2))

        # Progress
        progress = self.puzzles.get_progress()
        progress_text = f"Puzzle {progress['current']} / {progress['total']}"
        progress_surface = self.tiny_font.render(progress_text, True, (180, 180, 180))
        self.screen.blit(progress_surface, (WIDTH//2 - progress_surface.get_width()//2, btn_y + 10))

        # Next
        if self.puzzles.current_puzzle_index < len(self.puzzles.puzzles) - 1:
            next_rect = pygame.Rect(WIDTH//2 + 10, btn_y, btn_width, btn_height)
            pygame.draw.rect(self.screen, BUTTON_COLOR, next_rect, border_radius=8)
            next_text = self.tiny_font.render("Next >", True, TEXT_COLOR)
            self.screen.blit(next_text, (next_rect.centerx - next_text.get_width()//2, next_rect.centery - next_text.get_height()//2))

    def draw_help(self):
        '''Draw help screen'''
        self.screen.fill(DASHBOARD_BG)

        # Header
        header_font = pygame.font.Font(None, 48)
        title_surface = header_font.render("Help & Instructions", True, TEXT_COLOR)
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
            section_surface = self.small_font.render(section_title, True, (100, 200, 255))
            self.screen.blit(section_surface, (20, y_pos))
            y_pos += 28

            # Section content
            for line in section_lines:
                if y_pos > HEIGHT - 100:
                    break
                text_surface = self.tiny_font.render(line, True, TEXT_COLOR)
                self.screen.blit(text_surface, (30, y_pos))
                y_pos += 20

            y_pos += 10

        # Back button
        btn_width = 120
        btn_height = 35
        back_rect = pygame.Rect(20, HEIGHT - 50, btn_width, btn_height)
        pygame.draw.rect(self.screen, BUTTON_COLOR, back_rect, border_radius=8)
        back_text = self.tiny_font.render("Back to Menu", True, TEXT_COLOR)
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
