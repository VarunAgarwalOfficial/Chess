'''
Pawn Promotion UI
Shows a dialog to select which piece to promote to
'''

import pygame

class PromotionDialog:
    def __init__(self, screen, color, position):
        '''
        Create promotion dialog
        position: (row, col) where promotion happens
        color: "white" or "black"
        '''
        self.screen = screen
        self.color = color
        self.position = position
        self.pieces = ["queen", "rook", "bishop", "knight"]
        self.selected_piece = None

        # Dialog dimensions
        self.dialog_width = 240
        self.dialog_height = 100
        self.dialog_x = 120
        self.dialog_y = 190

        # Piece selection boxes
        self.piece_boxes = []
        box_size = 50
        spacing = 10
        start_x = self.dialog_x + 10

        for i, piece in enumerate(self.pieces):
            x = start_x + i * (box_size + spacing)
            y = self.dialog_y + 40
            self.piece_boxes.append({
                "rect": pygame.Rect(x, y, box_size, box_size),
                "piece": piece
            })

    def draw(self, images):
        '''Draw the promotion dialog'''
        # Semi-transparent background
        overlay = pygame.Surface((480, 480), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Dialog box
        dialog_rect = pygame.Rect(self.dialog_x, self.dialog_y,
                                  self.dialog_width, self.dialog_height)
        pygame.draw.rect(self.screen, (240, 240, 240), dialog_rect, border_radius=10)
        pygame.draw.rect(self.screen, (50, 50, 50), dialog_rect, 3, border_radius=10)

        # Title
        font = pygame.font.Font(None, 24)
        title_text = "Promote to:"
        title_surface = font.render(title_text, True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(self.dialog_x + self.dialog_width // 2,
                                                     self.dialog_y + 20))
        self.screen.blit(title_surface, title_rect)

        # Draw piece options
        mouse_pos = pygame.mouse.get_pos()
        for box in self.piece_boxes:
            # Highlight on hover
            if box["rect"].collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (200, 220, 240), box["rect"], border_radius=5)
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), box["rect"], border_radius=5)

            pygame.draw.rect(self.screen, (100, 100, 100), box["rect"], 2, border_radius=5)

            # Draw piece image (scaled down)
            piece_img = images[self.color][box["piece"]]
            scaled_img = pygame.transform.scale(piece_img, (45, 45))
            img_rect = scaled_img.get_rect(center=box["rect"].center)
            self.screen.blit(scaled_img, img_rect)

    def handle_click(self, pos):
        '''Handle click on promotion dialog'''
        for box in self.piece_boxes:
            if box["rect"].collidepoint(pos):
                self.selected_piece = box["piece"]
                return self.selected_piece
        return None
