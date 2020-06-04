import chess

#File contains inheritence of chess.Move class to add method

class Value_Move(chess.Move):
    def __init__(self, from_square, to_square, promotion=None, drop=None):
        super().__init__(from_square, to_square, promotion=promotion, drop=drop)

    #constructor to convert parent to child class
    def __init__(self, move):
        super().__init__(move.from_square, move.to_square, move.promotion, move.drop)
    
    #board = current state of board
    #self = potential move made onto board
    #returns value of move
    def move_val(self, board):
        #determine if white or black move
        if (board.turn is chess.WHITE):
            colorVal = 1
        else:
            colorVal = -1

        #if pawn promotion, recieve points based on what promoted to 
        if(self.promotion is chess.QUEEN):
            return 9 * colorVal
        elif(self.promotion is chess.ROOK):
            return 5 * colorVal
        elif(self.promotion is chess.BISHOP or self.promotion is chess.KNIGHT):
            return 3 * colorVal
       
        #If blank square, no value gained or lost, else gain points based on what piece is taken
        pieceTaken = board.piece_at(self.to_square)
        if(pieceTaken is None):
            return 0
        elif(pieceTaken.piece_type is chess.QUEEN):
            return 9 * colorVal
        elif(pieceTaken.piece_type is chess.ROOK):
            return 5 * colorVal
        elif(pieceTaken.piece_type is chess.BISHOP or pieceTaken.piece_type is chess.KNIGHT):
            return 3 * colorVal
        elif(pieceTaken.piece_type is chess.PAWN):
            return 1 * colorVal