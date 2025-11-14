'''
function to reset check
'''
def reset_check(self):
    self.check = False
    self.checks = []
    self.double_check = False


'''
check if a piece is pined
'''
def is_pinned(self, row , col):
    opponent = "black" if self.to_move == 'white' else "white"
    '''
    diagonal checks
    '''
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for direction in directions:
        found = False
        for i in range(1,8):
            end_row = self.king_positions[self.to_move][0] + direction[0] * i
            end_col = self.king_positions[self.to_move][1] + direction[1] * i
            if(end_row <= 7 and end_row >= 0 and end_col <= 7 and end_col >= 0):
                if self.state[end_row][end_col] != None :
                    if not found:
                        '''
                        Found the piece before opponent
                        '''
                        if(end_row == row and col == end_col):
                            found = True
                        else: 
                            break 
                    else:           
                        if self.state[end_row][end_col].color == opponent:
                            if self.state[end_row][end_col].type == "bishop" or self.state[end_row][end_col].type == "queen":
                                return direction
                        break
            else:
                break
    
    '''
    horizontal and vertical checks
    '''
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for direction in directions:
        found = False
        for i in range(1,8):
            end_row = self.king_positions[self.to_move][0] + direction[0] * i
            end_col = self.king_positions[self.to_move][1] + direction[1] * i
            if(end_row <= 7 and end_row >= 0 and end_col <= 7 and end_col >= 0):
                if self.state[end_row][end_col] != None :
                    if not found:
                        '''Found the piece before opponent'''
                        if(end_row == row and col == end_col):
                            found = True
                        else: 
                            break 
                    else:           
                        if self.state[end_row][end_col].color == opponent:
                            if self.state[end_row][end_col].type == "rook" or self.state[end_row][end_col].type == "queen":
                                return direction
                        break
            else:
                break

'''
checks if the king is in check
'''
def in_check(self , pos = None):
    opponent = "black" if self.to_move == "white" else "white"
    
    king = self.state[self.king_positions[self.to_move][0]][self.king_positions[self.to_move][1]]
    if pos:
        king_pos = pos
        '''
        Remove existing king from the board
        '''
        self.state[self.king_positions[self.to_move][0]][self.king_positions[self.to_move][1]] = None
    else:
        king_pos = self.king_positions[self.to_move]


    '''
    Diagonal checks
    '''
    def diagonal():
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for direction in directions:
            for i in range(1,8):
                end_row = king_pos[0] + direction[0] * i
                end_col = king_pos[1] + direction[1] * i
                if(end_row <= 7 and end_row >= 0 and end_col <= 7 and end_col >= 0):
                    if self.state[end_row][end_col] != None:
                        if self.state[end_row][end_col].color == opponent:
                            if self.state[end_row][end_col].type == "bishop" or self.state[end_row][end_col].type == "queen":
                                return (direction , (end_row, end_col))
                        break
                else:
                    break
        return None
        
    '''
    Horizontal and vertical checks
    '''
    def linear():
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for direction in directions:
            for i in range(1,8):
                end_row = king_pos[0] + direction[0] * i
                end_col = king_pos[1] + direction[1] * i
                if(end_row <= 7 and end_row >= 0 and end_col <= 7 and end_col >= 0):
                    if self.state[end_row][end_col] != None:
                        if self.state[end_row][end_col].color == opponent:
                            if self.state[end_row][end_col].type == "rook" or self.state[end_row][end_col].type == "queen":
                                return (direction , (end_row, end_col))
                        break
                else:
                    break
        return None
    

    
    '''
    Knight checks
    '''
    def knight():
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for direction in directions:
            end_row = king_pos[0] + direction[0]
            end_col = king_pos[1] + direction[1]
            if(end_row <= 7 and end_row >= 0 and end_col <= 7 and end_col >= 0):
                if self.state[end_row][end_col] != None:
                    if self.state[end_row][end_col].color == opponent:
                        if self.state[end_row][end_col].type == "knight":
                            return (direction , (end_row, end_col))
        return None
    
    '''
    Pawn checks
    '''
    def pawn():
        if self.to_move == "white":
            if king_pos[0] - 1 >= 0 and king_pos[1] - 1 >= 0 and (self.state[king_pos[0] - 1][king_pos[1] - 1]):
                if self.state[king_pos[0] - 1][king_pos[1] - 1].color == opponent and self.state[king_pos[0] - 1][king_pos[1] - 1].type == "pawn":
                    return ([-1, -1], (king_pos[0] - 1, king_pos[1] - 1))
            if king_pos[0] - 1 >= 0 and king_pos[1] + 1 <= 7 and (self.state[king_pos[0] - 1][king_pos[1] + 1]):
                if self.state[king_pos[0] - 1][king_pos[1] + 1].color == opponent and self.state[king_pos[0] - 1][king_pos[1] + 1].type == "pawn":
                    return ([-1, 1], (king_pos[0] - 1, king_pos[1] + 1))
        else:
            if king_pos[0] + 1 <= 7 and king_pos[1] - 1 >= 0 and (self.state[king_pos[0] + 1][king_pos[1] - 1]):
                if self.state[king_pos[0] + 1][king_pos[1] - 1].color == opponent and self.state[king_pos[0] + 1][king_pos[1] - 1].type == "pawn":
                    return ([1, -1], (king_pos[0] + 1, king_pos[1] - 1))
            if king_pos[0] + 1 <= 7 and king_pos[1] + 1 <= 7 and (self.state[king_pos[0] + 1][king_pos[1] + 1]):
                if self.state[king_pos[0] + 1][king_pos[1] + 1].color == opponent and self.state[king_pos[0] + 1][king_pos[1] + 1].type == "pawn":
                    return ([1, 1], (king_pos[0] + 1, king_pos[1] + 1))
        return None

    '''
    checks in the format (type , direction, atackers posn)
    '''
    checks = []
    if(diag := diagonal()):
        checks.append({"type" : "diag" , "dirn" : diag[0] , "pos" : diag[1]})
    if(lin := linear()):
        checks.append({ "type" : "lin" , "dirn" : lin[0] , "pos" : lin[1]})
    if(kni := knight()):
        checks.append({ "type" : "knight" , "dirn" : kni[0] , "pos" : kni[1]})
    if(pa := pawn()):
        checks.append({ "type" : "pawn" , "dirn" : pa[0] , "pos" : pa[1]})
    
    
    '''
    Add the king back to the board
    '''
    self.state[self.king_positions[self.to_move][0]][self.king_positions[self.to_move][1]] = king
    return checks 
