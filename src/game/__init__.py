'''
The Game module which holds all the Baord information
'''

from .Piece import Piece
from ai.optimizations import ZobristHashing

class Board:
    def __init__(self):

        '''
        Variables:
            - state: The current state of the board
            - to_move: The color of the player to move
            - move_log: The list of moves made
            - king_positions: The positions of the kings
            - castling: The castling rights
            - check: Whether the king is in check
            - checks: The array of all the current checks [(type , direction , position)]
            - double_check: Whether the king is in double check

        '''


        self.state = [
                [Piece("black", "rook"), Piece("black", "knight"), Piece("black", "bishop"), Piece("black", "queen"), Piece("black", "king"), Piece("black", "bishop"), Piece("black", "knight"), Piece("black", "rook")],
                [Piece("black", "pawn"), Piece("black", "pawn"), Piece("black", "pawn"), Piece("black", "pawn"), Piece("black", "pawn"), Piece("black", "pawn"), Piece("black", "pawn"), Piece("black", "pawn")],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [Piece("white", "pawn"), Piece("white", "pawn"), Piece("white", "pawn"), Piece("white", "pawn"), Piece("white", "pawn"), Piece("white", "pawn"), Piece("white", "pawn"),Piece("white", "pawn")],
                [Piece("white", "rook"), Piece("white", "knight"), Piece("white", "bishop"),Piece("white", "queen"), Piece("white", "king"),Piece("white", "bishop"),Piece("white", "knight"), Piece("white", "rook")]]
                # [Piece("white", "rook"), None,None,None, Piece("white", "king"),None,None, Piece("white", "rook")]]

        self.to_move = "white"
        self.move_log = []
        self.king_positions = {
            "white": (7, 4),
            "black": (0, 4)
        }

        self.castling = {
            "white": {
                "allowed": True,
                "king": True,
                "queen": True
            },
            "black": {
                "allowed": True,
                "king": True,
                "queen": True
            }
        }




        self.check = False
        self.checks = []
        self.double_check = False

        self.game_over = False
        self.game_result = None

        # Zobrist hashing for fast position comparison
        self.zobrist = ZobristHashing()
        self.position_hash = self.zobrist.hash_position(self)


    '''
    Moving a piece
    '''
    def move(self,initial,move):
        self.reset_check()
        final = move["to"]
        '''
        Add move to the move_log
        '''
        self.move_log.append({
            "initial": initial,
            "final": final,
            "special": move["special"],
            "initial_piece": self.state[initial[0]][initial[1]],
            "final_piece": self.state[final[0]][final[1]],
            "castling" : self.castling[self.to_move].copy(),
            "special_info": None if "special_info" not in move else move["special_info"]
        })

        '''
        Check for catling moves
        '''
        if (move["special"] == "KSC" or move["special"] == "QSC"):
            self.castling[self.to_move]["allowed"] = False            
            if(move["special"] == "KSC"):
                self.state[final[0]][final[1]] , self.state[initial[0]][initial[1]] = self.state[initial[0]][initial[1]] , None
                self.state[initial[0]][5] , self.state[initial[0]][7]= self.state[initial[0]][7],None
                self.castling[self.to_move]["king"] = False
            else:
                self.castling[self.to_move]["queen"] = False
                self.state[final[0]][final[1]] , self.state[initial[0]][initial[1]] = self.state[initial[0]][initial[1]] , None
                self.state[initial[0]][3] , self.state[initial[0]][0]= self.state[initial[0]][0],None
            
        elif(move["special"] == "EP"):
            self.state[final[0]][final[1]] , self.state[initial[0]][initial[1]] = self.state[initial[0]][initial[1]] , None
            self.state[initial[0]][final[1]] , self.state[move["special_info"][0]][move["special_info"][1]] = None,None
        

        elif(move["special"] == "promotion"):
            self.state[final[0]][final[1]] = Piece(self.to_move,"queen")
            self.state[initial[0]][initial[1]] = None
        else:

            '''
            Checking if the king moved
            '''
            if(self.state[initial[0]][initial[1]].type == "king"):
                self.king_positions[self.to_move] = final
                '''
                Remove castling rights
                '''
                self.castling[self.to_move]["allowed"] = False




            '''
            Checking if the rook moved
            '''
            if(self.state[initial[0]][initial[1]].type == "rook"):
                if(initial[1] == 0 and self.castling[self.to_move]["king"]):
                    self.castling[self.to_move]["king"] = False
                if(initial[1] == 7 and self.castling[self.to_move]["queen"]):
                    self.castling[self.to_move]["queen"] = False



            '''
            Checking if the pawn moved
            '''
            if(self.state[initial[0]][initial[1]].type == "pawn"):
                if(abs(initial[0] - final[0]) == 2):
                    self.state[initial[0]][initial[1]].en_passant = True
                else:
                    self.state[initial[0]][initial[1]].en_passant = False

            self.state[final[0]][final[1]] = self.state[initial[0]][initial[1]]
            self.state[initial[0]][initial[1]] = None






        if(self.to_move == "white"):
            self.to_move = "black"
        else:
            self.to_move = "white"
        if(len(checks := self.in_check()) > 0):
            self.check = True
            self.checks = checks
            # print("Check")
            if(len(checks) == 2):
                print("Double Check")
                self.double_check = True
            if(len(checks) > 2):
                print("Something is Wrong")
        else:
            self.reset_check()

        # Check for game-ending conditions
        result = self.get_game_result()
        if result:
            self.game_over = True
            self.game_result = result
            print(f"Game Over: {result}")

        # Update position hash after move
        self.position_hash = self.zobrist.hash_position(self)




    '''
    Function to undo the move
    '''
    def undo(self):
        
        move = self.move_log.pop()
        initial = move["initial"]
        final = move["final"]

        if(move["special"] == "KSC" or move["special"] == "QSC"):
            if(move["special"] == "KSC"):
                self.state[initial[0]][4] , self.state[initial[0]][7] = self.state[initial[0]][6] , self.state[initial[0]][5]
                self.state[initial[0]][5] , self.state[initial[0]][6] = None , None
            else:
                self.state[initial[0]][4] , self.state[initial[0]][0] = self.state[initial[0]][2] , self.state[initial[0]][3]
                self.state[initial[0]][3] , self.state[initial[0]][2] = None , None
        
        
        elif(move["special"] == "EP"):
            self.state[initial[0]][initial[1]] , self.state[final[0]][final[1]] = self.state[final[0]][final[1]] , self.state[initial[0]][initial[1]]
            self.state[final[0]][final[1]] , self.state[move["special_info"][0]][move["special_info"][1]] = None,Piece(self.to_move , "pawn" , True)


        else:
            self.state[initial[0]][initial[1]] = move["initial_piece"]
            self.state[final[0]][final[1]] = move["final_piece"]
        

        self.to_move = "black" if self.to_move == "white" else "white"
        if(move["initial_piece"].type == "king"):
            self.king_positions[self.to_move] = initial

        self.castling[self.to_move] = move["castling"]



        if(len(checks := self.in_check()) > 0):
            self.check = True
            self.checks = checks
            # print("Check")
            if(len(checks) == 2):
                print("Double Check")
                self.double_check = True
            if(len(checks) > 2):
                print("Something is Wrong")
        else:
            self.reset_check()

    from .MoveGenerator import get_legal_moves
    from .CheckFunctions import reset_check
    from .CheckFunctions import is_pinned
    from .CheckFunctions import in_check

    from .GameEndFunctions import is_checkmate
    from .GameEndFunctions import is_stalemate
    from .GameEndFunctions import is_insufficient_material
    from .GameEndFunctions import is_threefold_repetition
    from .GameEndFunctions import is_fifty_move_rule
    from .GameEndFunctions import get_game_result
    from .GameEndFunctions import _position_hash

    from .MoveGenerator import pawn_moves
    from .MoveGenerator import knight_moves
    from .MoveGenerator import bishop_moves
    from .MoveGenerator import rook_moves
    from .MoveGenerator import queen_moves
    from .MoveGenerator import king_moves


