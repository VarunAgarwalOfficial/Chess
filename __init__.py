import pygame
import sys
from Game import Board


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


COLORS = [LIGHT , DARK , LIGHT_SELECTED , DARK_SELECTED]

WIDTH = HEIGHT = 480
DIMENSION = 8
PIECE_HEIGHT = 60
FPS = 15
IMAGES = {
    "black": {},
    "white": {}
}





CLOCK = pygame.time.Clock()

#loading images once
pieces = ["rook", "knight", "bishop",  "king", "pawn" , "queen"]
for piece in pieces:
    IMAGES["black"][piece] = pygame.image.load("images/black/" + piece + ".png")
    IMAGES["white"][piece] = pygame.image.load("images/white/" + piece + ".png")





class Game:
    def __init__(self):
        pygame.init()
        self.legal_moves = []
        self.board = Board()
        self.screen = pygame.display.set_mode((WIDTH , HEIGHT))        
        self.running = True
        self.square_selected = (-1,-1)

    #drawing things
    def draw(self):
        pygame.display.flip()
        self.screen.fill((0,0,255))
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
                self.click_handler()
            elif event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    self.board.undo()


    '''
    Handling game logic when clicked
    '''
    def click_handler(self):
        click =  pygame.mouse.get_pos()
        pos = (click[1]// 60 , click[0]// 60 )

        if(pos[0] < 0 or pos[1] < 0 or pos[0] > 7 or pos[1] > 7):
            return
        else:

            '''
            No piece selected
            '''
            if(self.square_selected == (-1,-1)):
                if(self.board.state[pos[0]][pos[1]]):
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
                        if(self.board.move(self.square_selected, move)):
                            pass
                            '''
                            TODO PROMOTION > CHECK
                            '''
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
                        self.square_selected = pos
                        self.legal_moves = self.board.get_legal_moves(pos)
                    else:
                        self.square_selected = (-1,-1)
                        self.legal_moves = []

                    

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

