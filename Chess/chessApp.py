import chess
import random

# TODO : min/max tree

#Chooses a random move from legal moves that gain value, writes choice to output file and executes move
#board = current state of board
#notationFile = file to direct output  
def highest_val_move(board, notationFile):
    #loop through legal moves list, keeping moves with highest value
    highestVals = []
    highestVals.append(list(board.legal_moves)[0])
    high = move_val(board, highestVals[0])
    for i in list(board.legal_moves)[1:]:
        moveVal = move_val(board, i)
        if (moveVal is high):
            highestVals.append(i)
        elif (moveVal > high):
            highestVals.clear()
            highestVals.append(i)
            high = move_val(board, highestVals[0])
    
    #Randomly pick move from those tied with same value
    move = random.choice(highestVals)

    #add to notation file
    if(board.turn is chess.WHITE):
        outString = board.san(move) + "\t"
    else:
        outString = board.san(move) + "\n"
    notationFile.write(outString)

    board.push_uci(str(move))

#Chooses a random move from list of legal moves, writes choice to output file and executes move
#board = current state of board
#notationFile = file to direct output  
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
    
#board = current state of board
#move = potential move made onto board in san format
#returns value of move
def move_val(board, move):

    #final square coords are always last 2 chars
    moveString = str(move)
    fileIndex = (moveString[moveString.__len__()-2])
    rankIndex = (moveString[moveString.__len__()-1])
    
    #if pawn promotion
    if(fileIndex is "="):
        #determine if white or black 
        if(moveString[moveString.__len__()-3] == 7):
            colorVal = 1
        else:
            colorVal = -1
        #points based on what promoted to 
        if(rankIndex is "Q"):
            return 9 * colorVal
        elif(rankIndex is "R"):
            return 5 * colorVal
        else:
            return 3 * colorVal

    #convert strings to integer values and determine piece at that square
    piece = board.piece_at(chess.square(ord(fileIndex) - 97, int(rankIndex)-1))

    #If blank square, no value gained or lost
    if(piece is None):
        return 0

    #White pos, Black neg
    if(piece.color):
        colorVal = 1
    else:
        colorVal = -1

    #Value for each piece: pawn 1, knight/bishop 3, rook 5, queen 9
    if(piece.piece_type is 1):  
        return colorVal
    elif(piece.piece_type is 2 or piece.piece_type is 3):
        return 3 * colorVal
    elif(piece.piece_type is 4):
        return 5 * colorVal
    elif(piece.piece_type is 5):
        return 9 * colorVal
    else:
        return 10000 * colorVal

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
    computer_move = highest_val_move
    notationFile = open("notation.txt", "w+")
    notationFile.write("Wite\tBlack\n-------------\n");

    #Prompt for color
    choice = input("W for White, B for Black:")
    while(choice is not "B" and choice is not "W"):
        choice = input("W for White, B for Black:")

    #If black, computer makes first move
    if choice is "B":
        computer_move(board, notationFile)

    print()
    print(board,"\n")
    #Continue moves until game ends
    while not board.is_game_over():
        
        #Move player and computer
        player_move(board, notationFile)
        computer_move(board, notationFile)
        #rand_move(board, notationFile)
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