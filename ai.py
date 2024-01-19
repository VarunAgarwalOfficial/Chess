class AI:
    def __init__(self, board):
        self.board = board
        self.map = {
            "pawn": [
                [],       
            ]
        }
    
    def get_moves(self):
        moves = []
        for i in range(8):
            for j in range(8):
                moves += self.board.get_legal_moves(i, j)
        return moves

    def get_score(self):
        score = 0
        for i in range(8):
            for j in range(8):
                if self.board.state[i][j]:
                    if self.board.state[i][j].color == "white":
                        score += self.map[self.board.state[i][j].type][i][j]
                    else:
                        score -= self.map[self.board.state[i][j].type][i][j]
        return score 

