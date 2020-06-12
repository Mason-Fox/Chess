import chess
import copy

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
        val = 0
        #determine if white or black move
        if (board.turn is chess.WHITE):
            colorVal = 1
        else:
            colorVal = -1

        #if pawn promotion, recieve points based on what promoted to 
        if(self.promotion is chess.QUEEN):
            val += 9
        elif(self.promotion is chess.ROOK):
            val += 5
        elif(self.promotion is chess.BISHOP or self.promotion is chess.KNIGHT):
            val += 3

        #If a piece is taken, recieve points based on value of pirce
        pieceTaken = board.piece_at(self.to_square)
        if (pieceTaken is not None):
            if(pieceTaken.piece_type is chess.QUEEN):
                val += 9
            elif(pieceTaken.piece_type is chess.ROOK):
                val += 5
            elif(pieceTaken.piece_type is chess.BISHOP or pieceTaken.piece_type is chess.KNIGHT):
                val += 3
            elif(pieceTaken.piece_type is chess.PAWN):
                val += 1

        #if move results in checkmate, add highest value to move
        newBoard = copy.copy(board)
        newBoard.push_uci(str(self))
        if(newBoard.is_checkmate()):
            val += 100000
        elif(newBoard.is_game_over()):
            #If result is stalemate and in winning possition, lose value
            ####TODO : Calc winning
            print()
        #Add points for castling to prioritize over another random move
        if(board.is_castling(self)):
            val += 0.5
        elif (board.piece_at(self.from_square).piece_type is chess.KING):
        #Priotoitize any other random move over king
            val -= 0.25
            
        return val * colorVal