from Game import Board
import copy
total = 0
board = Board()


def temp(b , depth):
    total = 0
    if depth == 6:
        
        for i in range(8):
            for j in range(8):
                total += len(b.get_legal_moves((i,j))) 
        return total
    

    for i in range(8):
        for j in range(8):
            for move in b.get_legal_moves((i,j)):
                b.move((i,j), move)
                total += temp(b, depth+1)
                b.undo()
    if (depth == 1):
        print(total)
    return total

print(temp(board, 0))
