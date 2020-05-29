import chess
import random

# TODO : min/max tree

#piece = piece object containing piece type and color
#returns value of piece
def piece_val(piece):
    #White pos, Black neg
    if(piece.color):
        colorVal = 1
    else:
        colorVal = -1

    if(piece.piece_type is 1):  
        return 1 * colorVal
    elif(piece.piece_type is 2 or piece.piece_type is 3):
        return 3 * colorVal
    elif(piece.piece_type is 4):
        return 5 * colorVal
    elif(piece.piece_type is 5):
        return 9 * colorVal
    else:
        return 10000 * colorVal

#Chooses a random move from list of legal moves, writes choice to output file and executes move
#board = current state of board
#notationFile = file to direct output to
def rand_move(board, notationFile):
    #make random move from list of legal moves
    move = random.choice(list(board.legal_moves))
    #add to notation file
    if(board.turn is chess.WHITE):
        outString = board.san(move) + "\t"
    else:
        outString = board.san(move) + "\n"
    notationFile.write(outString)

    board.push_uci(str(move))
    
#Prompts the user to enter move until valid move is chosen, writes move to output file and exectutes move on board
#board = current state of board
#notationFile = file to direct output to
def player_move(board, notationFile):

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

    #add move to notation file
    if(board.turn is chess.WHITE):
        outString = sanMove + "\t"
    else:
        outString = sanMove + "\n"
    notationFile.write(outString)

    board.push_uci(str(uciMove))

#Creates a new board and opens output file
#prompt user for white or black, loops moves until game ends
def new_game():
   
    #create board and notation file
    board = chess.Board()

    test = chess.Piece(4, True)
    print(piece_val(test))

    notationFile = open("notation.txt", "w+")
    notationFile.write("Wite\tBlack\n-------------\n");

    #Prompt for color
    choice = input("W for White, B for Black:")
    while(choice is not "B" and choice is not "W"):
        choice = input("W for White, B for Black:")

    #If black, computer makes first move
    if choice is "B":
        rand_move(board, notationFile)
          
    print()
    print(board, "\n")
    #Continue moves until game ends
    while not board.is_game_over():
        
        #Move player and computer
        player_move(board, notationFile)
        rand_move(board, notationFile)
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

new_game()