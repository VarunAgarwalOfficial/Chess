import numpy as np

"""
Every legal move is an dictionary in the format
move = {
    to : (row,col),
    special : None (default) or "EP" or "KSC" or "QSC" or "promotion",
    special_info : None (default) or (row,col) for EP or (piece) for promotion}

Every Check is a dictionary in the format
check = {
    type : "diag" or "lin" or "pawn" or "knight",
    dirn : (mag,mag),
    pos : (row,col)
}


"""


'''
Squared Magnitude of two points to avoid precision
'''
def mag(a):
    return a[0]**2 + a[1]**2



def get_legal_moves(self, pos):
    moves = []
    if self.state[pos[0]][pos[1]] == None:
        return []
    piece = self.state[pos[0]][pos[1]]
    if piece.color == self.to_move:
        if(piece.type == "pawn"):
            moves =  self.pawn_moves(pos[0] , pos[1])
        if(piece.type == "rook"):
            moves =  self.rook_moves(pos[0] , pos[1])
        if(piece.type == "knight"):
            moves =  self.knight_moves(pos[0] , pos[1])
        if(piece.type == "bishop"):
            moves =  self.bishop_moves(pos[0] , pos[1])
        if(piece.type == "queen"):
            moves =  self.queen_moves(pos[0] , pos[1])
        if(piece.type == "king"):
            '''
            King dont need to check Legal moves
            '''
            return self.king_moves(pos[0] , pos[1])




    '''
    Filter Legal Moves from Pseudo Legal Moves
    '''
    if(self.check):
        if(self.double_check):
            '''
            Only king can move if it is in double check
            '''
            return []

        '''
        if opponents knights and pawns checks the king , you can move any piece that can take the checking piece 
        '''
        if (self.checks[0]["type"] == "knight" or self.checks[0]["type"] == "pawn"):
            return [move for move in moves if move["to"] == self.checks[0]["pos"]]

        else:
            '''
            The check comes from a diagnoal or horizontal line
            '''
            '''
            Find the vector from the king to the checker and the vector from the king to every pseudo legal move
            if the directions of the vectors are the same, the move is legal if the magnitude of the move is smaller or equal to the magnitude of the check
            This implies the move either blocks the check or captures the checker
            '''
            legal_moves = []
            
            king_to_attacker = np.array(self.king_positions[self.to_move]) -  np.array(self.checks[0]["pos"])
            k_t_a_mag = mag(king_to_attacker)
            for move in moves:
                '''
                find the vector from the king to the move
                '''
                king_to_move = np.array(self.king_positions[self.to_move]) - np.array(move["to"])
                k_t_m_mag = mag(king_to_move)

                if(k_t_m_mag <= k_t_a_mag and (king_to_move**2*np.sign(king_to_move)/k_t_m_mag == king_to_attacker**2*np.sign(king_to_attacker)/k_t_a_mag).all()):
                    '''
                    The piece blocks or captures the check
                    '''
                    legal_moves.append(move)

            return legal_moves            
    return moves




'''
Returns a list of all possible PAWN moves
Includes en passant and promotion
'''
def pawn_moves(self , row , col):
    dirn =  self.is_pinned(row,col)
    moves = []
    if(self.to_move == "white"):

        '''
        moving the pawn forward
        '''
        if not dirn or dirn == (-1 , 0):
            if(row >= 1 and self.state[row-1][col] == None):
                if(row == 1):
                    moves.append({"to" : (row-1,col), "special" : "promotion"})
                else:
                    moves.append({"to": (row-1,col) , "special" : None})

                '''
                if the pawn is on the first row, it can move two spaces forward
                '''
                if(self.state[row-2][col] == None and row == 6):
                    moves.append({"to": (row-2,col) , "special" : None})


        '''
        the pawn can take a piece diagonally
        '''
        if (not dirn or dirn == (-1,1)) and (col <= 6 and self.state[row-1][col+1] and self.state[row-1][col+1].color == "black"):
            if row == 1:
                moves.append({"to": (row-1,col+1), "special" : "promotion"})
            else:
                moves.append({"to": (row-1,col+1) , "special" : None})
        if(not dirn or dirn == (-1,-1)) and (col >= 1 and self.state[row-1][col-1] and self.state[row-1][col-1].color == "black"):
            if row == 1:
                moves.append({"to": (row-1,col-1) , "special" : "promotion"})
            else:
                moves.append({"to": (row-1,col-1) , "special" : None})

        '''
        en passant
        '''
        if(not dirn or dirn == (-1,1)) and (col<=6 and self.state[row][col+1] and self.state[row][col+1].type == "pawn" and self.state[row][col+1].color == "black" and self.state[row][col+1].en_passant):
            moves.append({"to": (row-1,col+1) , "special" : "EP" , "special_info" :(row,col+1)})

        if(not dirn or dirn == (-1,-1)) and (col>= 1 and self.state[row][col-1] and self.state[row][col-1].type == "pawn" and self.state[row][col-1].color == "black" and self.state[row][col-1].en_passant):
            moves.append({"to": (row-1,col-1) , "special" : "EP" , "special_info" :(row,col-1)})
    
    else:
        '''
        Black Pawn
        '''
        '''
        moving the pawn forward
        '''
        if not dirn or dirn == (1 , 0):
            if(row <= 6 and self.state[row+1][col] == None):
                if row == 6:
                    moves.append({"to" : (row+1,col), "special" : "promotion"})
                else:
                    moves.append({"to": (row+1,col) , "special" : None})
                '''
                if the pawn is on the second last row, it can move two spaces forward
                '''
                if(self.state[row+2][col] == None and row == 1):
                    moves.append({"to": (row+2,col) , "special" : None})

        '''
        the pawn can take a piece diagonally
        '''
        if(not dirn or dirn == (1,1)) and (col <= 6 and self.state[row+1][col+1] and self.state[row+1][col+1].color == "white"):
            if row == 6:
                moves.append({"to": (row+1,col+1), "special" : "promotion"})
            else:
                moves.append({"to": (row+1,col+1) , "special" : None})
        if(not dirn or dirn == (1,-1)) and (col >= 1 and self.state[row+1][col-1] and self.state[row+1][col-1].color == "white"):
            if row == 6:
                moves.append({"to": (row+1,col-1), "special" : "promotion"})
            else:
                moves.append({"to": (row+1,col-1) , "special" : None})
        
        '''
        en passant
        '''
        if (not dirn or dirn == (1,1)) and (col<= 6 and self.state[row][col+1] and self.state[row][col+1].type == "pawn" and self.state[row][col+1].color == "white" and self.state[row][col+1].en_passant):
            moves.append({"to": (row+1,col+1) , "special" : "EP" , "special_info" :(row,col+1)})
        if(not dirn or dirn == (1,-1)) and (col >= 1 and self.state[row][col-1] and self.state[row][col-1].type == "pawn" and self.state[row][col-1].color == "white" and self.state[row][col-1].en_passant):
            moves.append({"to": (row+1,col-1) , "special" : "EP" , "special_info" :(row,col-1)})

    return moves

'''
Returns a list of all possible ROOK moves
'''
def rook_moves(self , row , col):
    moves = []
    '''
    directions in which a rook can move
    '''
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]


    '''
    check if the rook is pinned
    '''
    if dirn := self.is_pinned(row,col):
        if dirn in directions:
            directions = [dirn]
        else:
            return []

    opponent = "black" if self.to_move == 'white' else "white"
    for direction in directions:
        '''
        a rook can move a maximum of 7 spaces in any direction
        '''
        for i in range(1,8):
            end_row = row + direction[0] * i
            end_col = col + direction[1] * i
            if(end_row <= 7 and end_row >= 0 and end_col <= 7 and end_col >= 0):
                if self.state[end_row][end_col] == None:
                    '''
                    move is valid if the space is empty
                    '''
                    moves.append({"to": (end_row,end_col) , "special" : None})
                elif self.state[end_row][end_col].color == opponent:
                    moves.append({"to": (end_row,end_col) , "special" : None})
                    '''
                    stop when you hit an opponent piece
                    '''
                    break
                else: 
                    '''
                    stop when you hit your own piece
                    '''
                    break
            else: 
                '''
                stop when you hit the edge of the board
                '''
                break

    return moves

'''
Returns a list of all possible BISHOP moves
'''
def bishop_moves(self , row , col):
    moves = []
    '''
    directions in which a bishop can move
    '''
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


    '''
    Check if the bishop is pinned
    '''
    if dirn := self.is_pinned(row,col):
        if dirn in directions:
            directions = [dirn]
        else:
            return []


    opponent = "black" if self.to_move == 'white' else "white"
    for direction in directions:
        '''
        a bishop can move a maximum of 7 spaces in any direction
        '''
        for i in range(1,8):
            end_row = row + direction[0] * i
            end_col = col + direction[1] * i
            if(end_row <= 7 and end_row >= 0 and end_col <= 7 and end_col >= 0):
                if self.state[end_row][end_col] == None:
                    '''
                    move is valid if the space is empty
                    '''
                    moves.append({"to": (end_row,end_col) , "special" : None})
                elif self.state[end_row][end_col].color == opponent:
                    moves.append({"to": (end_row,end_col) , "special" : None})
                    '''
                    stop when you hit an opponent piece
                    '''
                    break
                else: 
                    '''
                    stop when you hit your own piece
                    '''
                    break
            else: 
                '''
                stop when you hit the edge of the board
                '''
                break

    return moves

'''
Returns a list of all possible KNIGHT moves
'''
def knight_moves(self , row , col):
    
    moves = []
    '''
    directions in which a knight can move
    '''
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    


    '''
    Check if the knight is pinned
    '''
    if dirn := self.is_pinned(row,col):
        if dirn in directions:
            directions = [dirn]
        else:
            return []
    
    
    opponent = "black" if self.to_move == 'white' else "white"
    for direction in directions:
        end_row = row + direction[0]
        end_col = col + direction[1]
        if(end_row <= 7 and end_row >= 0 and end_col <= 7 and end_col >= 0):
            if self.state[end_row][end_col] == None:
                '''
                move is valid if the space is empty
                '''
                moves.append({"to": (end_row,end_col) , "special" : None})
            elif self.state[end_row][end_col].color == opponent:
                '''
                move is valid if the space is occupied by an opponent piece
                '''
                moves.append({"to": (end_row,end_col) , "special" : None})


    return moves

'''
Returns a list of all possible QUEEN moves
'''
def queen_moves(self , row , col):
    moves = []
    '''
    directions in which a queen can move
    '''
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (0, 1), (1, 0)]
    
    '''
    Check if the queen is pinned
    '''
    if dirn := self.is_pinned(row,col):
        if dirn in directions:
            directions = [dirn]
        else:
            return []
    
    opponent = "black" if self.to_move == 'white' else "white"
    for direction in directions:
        '''
        a queen can move a maximum of 7 spaces in any direction
        '''
        for i in range(1,8):
            end_row = row + direction[0] * i
            end_col = col + direction[1] * i
            if(end_row <= 7 and end_row >= 0 and end_col <= 7 and end_col >= 0):
                if self.state[end_row][end_col] == None:
                    '''
                    move is valid if the space is empty
                    '''
                    moves.append({"to": (end_row,end_col) , "special" : None})
                elif self.state[end_row][end_col].color == opponent:
                    moves.append({"to": (end_row,end_col) , "special" : None})
                    '''
                    stop when you hit an opponent piece
                    '''
                    break
                else: 
                    '''
                    stop when you hit your own piece
                    '''
                    break
            else: 
                '''
                stop when you hit the edge of the board
                '''
                break

    return moves


'''
returns a list of all possible KING moves
'''

def king_moves(self , row , col):
    moves = []
    '''
    Check Castling
    '''
    if not self.check:

        '''
        King Side Castling
        '''
        if  self.castling[self.to_move]["allowed"] and self.castling[self.to_move]["king"]:
            if self.state[row][col+1] == None and self.state[row][col+2] == None and self.state[row][col+3] and self.state[row][col+3].type == "rook":
                if  len(self.in_check((row,col+1))) == 0 and len(self.in_check((row,col+2))) == 0 and len(self.in_check((row,col+3))) == 0:
                    moves.append({"to": (row,col+2) , "special" : "KSC"})
                    print("KSC")
        
        if  self.castling[self.to_move]["allowed"] and self.castling[self.to_move]["queen"]:
            if self.state[row][col-1] == None and self.state[row][col-2] == None and self.state[row][col-3] == None and self.state[row][col-4] and self.state[row][col-4].type == "rook":
                if  len(self.in_check((row,col-1))) == 0 and len(self.in_check((row,col-2))) == 0 and len(self.in_check((row,col-3))) == 0 and len(self.in_check((row,col-4))) == 0:
                    moves.append({"to": (row,col-2) , "special" : "QSC"})
                    print("QSC")


    '''
    directions in which a king can move
    '''
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    opponent = "black" if self.to_move == 'white' else "white"
    for direction in directions:
        end_row = row + direction[0]
        end_col = col + direction[1]
        if(end_row <= 7 and end_row >= 0 and end_col <= 7 and end_col >= 0):
            if self.state[end_row][end_col] == None and len(self.in_check((end_row, end_col))) == 0:
                '''
                move is valid if the space is empty and not in check
                '''
                moves.append({"to": (end_row,end_col) , "special" : None})
            elif self.state[end_row][end_col] and self.state[end_row][end_col].color == opponent and len(self.in_check((end_row, end_col))) == 0:
                '''
                move is valid if the space is occupied by an opponent piece
                '''
                moves.append({"to": (end_row,end_col) , "special" : None})

    return moves