class Piece:
    def __init__(self , color  , type , en_passant = False):
        self.color = color
        self.type = type
        self.en_passant = en_passant

    def __str__(self):
        return self.color + " " + self.type + " "
    
    def __repr__(self):
        return self.color + " " + self.type + " "