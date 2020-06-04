import ChessMove
import random

#File contains implementation of different move techniques for computer

#TODO : ADD DESC
#board = current state of board
#returns san move of move added to the board
def min_max_move(board):
    print()
    #TODO

#Chooses a random move from legal moves of highest value gain and executes move
#board = current state of board
#returns san move of move added to the board
def highest_val_move(board):
    
    highestVals = []
    highestVals.append(ChessMove.Value_Move(list(board.legal_moves)[0]))
    high = abs(highestVals[0].move_val(board))
    #loop through legal moves list, keeping moves with highest value
    for i in list(board.legal_moves)[1:]:
        move_val = abs(ChessMove.Value_Move(i).move_val(board))
        #if ties with highest val move add to list, if greater clear old values and add
        if (move_val is high):
            highestVals.append(i)
        elif (move_val > high):
            highestVals.clear()
            highestVals.append(i)
            high = move_val
    
    #Randomly pick move from those tied with same value
    move = random.choice(highestVals)
    sanMove = board.san(move)
    print("Chose ", str(move))
    board.push_uci(str(move))
    
    return sanMove

#Chooses a random move from list of legal moves and executes move
#board = current state of board
#returns san move of move added to the board
def rand_move(board):
    #make random move from list of legal moves
    move = random.choice(list(board.legal_moves))
    sanMove = board.san(move)
    board.push_uci(str(move))

    return sanMove