import chess
import random

# TODO : Make an output file that holds transcript of moves by each player
# TODO : Structure code for python
# TODO : Values for pieces
# TODO : min/max tree

def compRandMove(board):
    #make random move from list of legal moves
    move = random.choice(list(board.legal_moves))
    board.push_uci(str(move))
    
def getMove(board):

     #Get player move and validate
    notValid = True
    sanMove = input("Enter move: ")
    while(notValid):
        notValid = False
        #Validate that the entry can be parsed and is a valid move
        try:
            uciMove = board.parse_san(sanMove)
            if(chess.Move.from_uci(str(uciMove)) not in board.legal_moves) and notValid:
                notValid = True
                print("Not a valid move!")
                sanMove = input("Enter move: ")
        except:
            notValid = True
            print("Not a valid move!")
            sanMove = input("Enter move: ")

    return uciMove

def newGame():
   
    board = chess.Board()

    #Prompt for color
    choice = input("W for White, B for Black:")
    while(choice is not "B" and choice is not "W"):
        choice = input("W for White, B for Black:")

    #If black, computer makes first move
    if choice is "B":
        compRandMove(board)
    print(board)
    #Continue moves until game ends
    while not board.is_game_over():
        
        #Move player and computer
        board.push_uci(str(getMove(board)))
        compRandMove(board)
        print(board, "\n")

    #Display reason for end of game
    if board.is_checkmate():
        print("Checkmate")
    elif board.is_stalemate():
        print("Stalemate")
    elif board.is_insufficient_material():
        print("Insufficient Material!")
    else:
        print("Game Over")

newGame()
