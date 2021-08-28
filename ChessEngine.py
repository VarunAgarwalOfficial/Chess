class Game():
    def __init__(self , state = [['Br', 'Bn', 'Bb', 'Bq', 'Bk', 'Bb', 'Bn', 'Br'],
            ["Bp", "Bp", "Bp", "Bp", "Bp", "Bp", "Bp", "Bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["Wp", "Wp", "Wp", "Wp", "Wp", "Wp", "Wp", "Wp"],
            ['Wr', 'Wn', 'Wb','Wq', 'Wk', 'Wb', 'Wn', 'Wr']] ):
        self.state = state
        self.white_move = True
        self.move_log = []
        self.valid_moves = []
        self.castle_rights = ["wk","wq","bq","bk"]


        self.get_valid_moves()

    #validate the move which was done and does them
    def validate(self , clicks):
        
        #validate code here
        if((self.white_move and (self.state[clicks[0][0]][clicks[0][1]])[0] != 'W') or (not self.white_move and (self.state[clicks[0][0]][clicks[0][1]])[0] != 'B')):
            return 0

        move = Move(clicks , self.state[clicks[0][0]][clicks[0][1]] , self.state[clicks[1][0]][clicks[1][1]])
        if move in self.valid_moves:

            #Checking For Promotions
    
            if(self.state[clicks[0][0]][clicks[0][1]] == "Wp" and clicks[1][0] == 0):
                self.state[clicks[0][0]][clicks[0][1]] = "Wq"
            if(self.state[clicks[0][0]][clicks[0][1]] == "Bp" and clicks[1][0] == 7):
                self.state[clicks[0][0]][clicks[0][1]] = "Bq"   
            #Pushing it in the move log
            self.move_log.append(move)
            #Moving the piece
            self.state[clicks[1][0]][clicks[1][1]] = self.state[clicks[0][0]][clicks[0][1]]
            self.state[clicks[0][0]][clicks[0][1]] = "--"
            self.white_move = not self.white_move

            self.get_valid_moves()
            return  1
        else:
            return 0


    #undos the last move
    def undo(self):
        if(len(self.move_log)>= 1):
            move = self.move_log.pop()
            clicks = move.clicks
            self.state[clicks[1][0]][clicks[1][1]] = move.end_piece
            self.state[clicks[0][0]][clicks[0][1]] = move.start_piece
            self.white_move = not self.white_move
            self.get_valid_moves()
        else:
            print("Please make a move first")






    def get_valid_moves(self):
        moves =  self.get_all_moves()
        self.valid_moves = moves
        print(len(moves))
    #returns the pseudo legal moves
    def get_all_moves(self):
        moves = []
        # print("func called")
        for row in range(len(self.state)):
            for col in range(len(self.state[row])): 
                if((self.white_move and self.state[row][col][0] == 'W') or (not self.white_move and self.state[row][col][0] == 'B')):
                    #only getting moves for the plyaer whose turn it is
                    #calls respected functions for all pieces
                    if(self.state[row][col][1] == 'p'):
                        self.pawn_moves(row, col, moves)
                    elif(self.state[row][col][1] == 'r'):
                        self.rook_moves(row, col, moves)
                    elif(self.state[row][col][1] == 'b'):
                        self.bishop_moves(row, col, moves)
                    elif(self.state[row][col][1] == 'q'):
                        self.queen_moves(row, col, moves)
                    elif(self.state[row][col][1] == 'n'):
                        self.knight_moves(row, col, moves)
                    elif(self.state[row][col][1] == 'k'):
                        self.king_moves(row, col, moves)
        return moves


    '''
    Pseudo Legal moves
    '''

    # Adds all the possible pawn moves to the list
    def pawn_moves(self , row , col , moves):
        if(self.white_move and self.state[row][col][0] == 'W'):
            if(self.state[row-1][col] == "--"):
                moves.append(Move([(row,col) ,(row-1,col)] ,"Wp" , "--"))
                if(self.state[row-2][col] == "--" and row == 6):
                    moves.append(Move([(row,col) ,(row-2,col)] ,"Wp" , "--"))
            if(col <= 6 and self.state[row-1][col+1][0] == "B" ):
                 moves.append(Move([(row,col) ,(row-1,col+1)] ,"Wp" , "--"))
            if(col >= 1 and self.state[row-1][col-1][0] == "B" ):
                 moves.append(Move([(row,col) ,(row-1,col-1)] ,"Wp" , "--"))
            
            
        
        if(not self.white_move and self.state[row][col][0] == 'B'):
            if(self.state[row+1][col] == "--"):
                moves.append(Move([(row,col) ,(row+1,col)] ,"Bp" , "--"))
                if(self.state[row+2][col] == "--" and row == 1):
                    moves.append(Move([(row,col) ,(row+2,col)] ,"Bp" , "--"))
            if(col <= 6 and self.state[row+1][col+1][0] == "W" ):
                 moves.append(Move([(row,col) ,(row+1,col+1)] ,"Bp" , "--"))
            if(col >= 1 and self.state[row+1][col-1][0] == "W" ):
                 moves.append(Move([(row,col) ,(row+1,col-1)] ,"Bp" , "--"))


        #pawn promotion and en peasant is left to code

    # Adds all the possible rook moves to the list

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
        directions = [(1,1), (1, -1), (-1, 1), (-1, -1)]
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
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1),(1,1), (1, -1), (-1, 1), (-1, -1)]
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
        directions = [(1,2), (1,-2) , (-1,2) , (-1,-2),(2,1), (2,-1) , (-2,1) , (-2,-1)]
        for direction in directions:
            end_row = row + direction[0]
            end_col = col + direction[1]
            if self.whithin_range(end_row , end_col):
                if self.state[end_row][end_col] == "--":
                    moves.append(Move([(row,col) ,(end_row,end_col)] , self.state[row][col] , '--'))
                elif self.state[end_row][end_col][0] == opponent:
                    moves.append(Move([(row,col) ,(end_row,end_col)] , self.state[row][col] , '--'))


    #defines all the king moves
    def king_moves(self,row,col,moves):
        opponent = "B" if self.white_move else "W"
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1),(1,1), (1, -1), (-1, 1), (-1, -1)]
        for direction in directions:
            end_row = row + direction[0]
            end_col = col + direction[1]
            if self.whithin_range(end_row , end_col):
                if self.state[end_row][end_col] == "--":
                    moves.append(Move([(row,col) ,(end_row,end_col)] , self.state[row][col] , '--'))
                elif self.state[end_row][end_col][0] == opponent:
                    moves.append(Move([(row,col) ,(end_row,end_col)] , self.state[row][col] , '--'))

        



    def whithin_range(self, row , col):
        if(row>7 or row < 0 or col>7 or col < 0):
            return 0
        return 1


class Move:
    def __init__(self , clicks , start_piece,end_piece):
        self.clicks = clicks
        self.start_piece = start_piece
        self.end_piece = end_piece

    def __eq__(self, other): 
        if not isinstance(other, Move):
            # don't attempt to compare against unrelated types
            return 0

        return self.clicks == other.clicks
    
    def __repr__(self): 
        return f"Moved {self.start_piece} in {self.clicks}"