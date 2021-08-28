    def rook_moves(self , row , col , moves):
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        opponent = "B" if self.white_move else "W"
        for direction in directions:
            for i in range(1,8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if self.whithin_range(end_row , end_col):
                    if self.state[end_row][end_col] == "--":
                        moves.append(Move([(row,col) ,(end_row,end_col)] , self.state[row][col] , '--'))
                    elif self.state[end_row][end_col][0] == opponent:
                        moves.append(Move([(row,col) ,(end_row,end_col)] , self.state[row][col] , '--'))
                        break
                    else: 
                        break
                else: 
                    break  
  
    #adds all the bishop moves to the list
    def bishop_moves(self , row , col , moves):
        directions = ((1,1), (1, -1), (-1, 1), (-1, -1))
        opponent = "B" if self.white_move else "W"
        for direction in directions:
            for i in range(1,8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if self.whithin_range(end_row , end_col):
                    if self.state[end_row][end_col] == "--":
                        moves.append(Move([(row,col) ,(end_row,end_col)] , self.state[row][col] , '--'))
                    elif self.state[end_row][end_col][0] == opponent:
                        moves.append(Move([(row,col) ,(end_row,end_col)] , self.state[row][col] , '--'))
                        break
                    else: 
                        break
                else: 
                    break

    #adds all the queen moves to the list
    def queen_moves(self , row , col , moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1),(1,1), (1, -1), (-1, 1), (-1, -1)) 
        opponent = "B" if self.white_move else "W"
        for direction in directions:
            for i in range(1,8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if self.whithin_range(end_row , end_col):
                    if self.state[end_row][end_col] == "--":
                        moves.append(Move([(row,col) ,(end_row,end_col)] , self.state[row][col] , '--'))
                    elif self.state[end_row][end_col][0] == opponent:
                        moves.append(Move([(row,col) ,(end_row,end_col)] , self.state[row][col] , '--'))
                        break
                    else: 
                        break
                else: 
                    break

    def knight_moves(self,row,col,moves):
        opponent = "B" if self.white_move else "W"
        directions = []

