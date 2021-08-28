import pygame as p
import sys
from ChessEngine import Game

'''
Declaring Constants
'''




# COLORS 
LIGHT = (241,218,179)
DARK = (182,136,96)


WIDTH = HEIGHT = 480
DIMENSION = 8
PIECE_HEIGHT = 60
FPS = 15
IMAGES = {}




'''
Global Varibals (only change state)
'''
square_selected = (-1,-1)
clicks = []


#loading images once
def load_images():
    pieces = ["Br" , "Bn" , "Bb" , "Bq" , "Bk" , "Bp" , "Wr" , "Wn" , "Wb" , "Wq" , "Wk" , "Wp" ]
    for piece in pieces:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")


#drawing things every time clock tiks
def draw(SCREEN , state ):
    SCREEN.fill((0,0,255))
    COLORS = [LIGHT , DARK]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if(square_selected == (i,j)):
                color = (120,134,107)
            else:
                color = COLORS[(i+j)%2]
            p.draw.rect(SCREEN, color, p.Rect(j*PIECE_HEIGHT, i*PIECE_HEIGHT, PIECE_HEIGHT, PIECE_HEIGHT))
            piece = state[i][j]
            if(piece != "--"):
                SCREEN.blit(IMAGES[piece] ,( j*PIECE_HEIGHT, i*PIECE_HEIGHT))



'''
Handling game logic when clicked
'''



def click_handler(pos , game):
    global square_selected
    global clicks
    global promotion 
    click = (pos[1]// 60 , pos[0]// 60 )
    if(click[0] < 0 or click[1] < 0 or click[0] > 7 or click[1] > 7):
        pass
    else:
        if(len(clicks) == 0 and game.state[click[0]][click[1]] != '--'):
            clicks.append(click)
            square_selected = click
        elif(len(clicks) == 1 and square_selected == click):
            clicks = []
        elif(len(clicks)==1):
            clicks.append(click)
            val = game.validate(clicks)
            if (val == 1):
                print("successfull move")
            elif val == "promotion":
                promotion = True
            else:
                print("please check the move")
            clicks = []
            square_selected = ()


        



def main():
    
    '''
    Initializing Constants
    '''
    p.init()
    game = Game()
    SCREEN = p.display.set_mode((WIDTH , HEIGHT))
    clock = p.time.Clock()
    load_images()
    running = True





    while running:
        for e in p.event.get():
            if e.type == p.MOUSEBUTTONDOWN:
                click_handler(p.mouse.get_pos() , game)
            elif e.type == p.QUIT:
                running = False
                p.quit()
                sys.exit()
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    game.undo()
                    
        clock.tick(FPS)
        p.display.flip()
        draw(SCREEN,game.state)



if __name__ == "__main__":
    main()






