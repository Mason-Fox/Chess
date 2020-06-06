import chess
import AIMoves as ai
import Tree
import ChessMove

#File contains main logic and input/output for player
# TODO : min/max tree

#formats and outputs given move into output file
#move = valid move in san notation added to the board
#notationFile = output file to write notation into
#board = new state of board after move was added
def write_notation(move, notationFile, board):
    
    #add newline or tab depending on previous turn
    if(board.turn is chess.WHITE):
        outString = str(move) + "\n"
    else:
        outString = str(move) + "\t"
    notationFile.write(outString)
    
#Prompts the user to enter move until valid move is chosen and executes move on board
#board = current state of board
#returns san move of move added to the board
def player_move(board):

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

    board.push_uci(str(uciMove))

    return sanMove

#Creates a new board and opens output file
#prompt user for white or black, loops moves until game ends
def new_game():
    #create board and notation file
    board = chess.Board()
    computer_move = ai.highest_val_move
    notationFile = open("notation.txt", "w+")
    notationFile.write("Wite\tBlack\n-------------\n");

    #Prompt for color
    choice = input("W for White, B for Black:")
    while(choice is not "B" and choice is not "W"):
        choice = input("W for White, B for Black:")

    #If black, computer makes first move
    if choice is "B":
        write_notation(computer_move(board), notationFile, board)

    print()
    print(board,"\n")
    #Continue moves until game ends
    while not board.is_game_over():
        #Move player and computer and write to output file
        write_notation(player_move(board), notationFile, board)
        write_notation(computer_move(board), notationFile, board)
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