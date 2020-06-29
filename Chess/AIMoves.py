import ChessMove
import random
import Tree
import chess

#File contains implementation of different move techniques for computer

#Follows a min/max aglorithm to determine and execute move
#board = current state of board
#returns san move of move added to the board
def min_max_move(board):

    import time
    start = time.time()

    #create Tree of given depth of baord state and moves
    #NOTE: change tree depth to change how many moves are looked ahead
    treeDepth = 4
    moves_tree = Tree.Tree(treeDepth, board)

    #Decide whether to start bottom as max or min
    if(board.turn is chess.WHITE and treeDepth%2 == 1):
        color = True
    else:
        color = False
        
    move = min_max(moves_tree.root, color, float('-inf'), float('inf'))
    sanMove = board.san(move)
    board.push_uci(str(move))
    
    end = time.time()
    print(end - start)

    return sanMove
    
#Recursivley updates each layer of tree by minimizing or maximizing the value of parent based on child nodes
#tree = tree of moves/values being traversed
#color = True/White or False/Black
#depth = current depth to min/max values of nodes
def min_max(node, color, alpha, beta):
    #If there are children nodes, get min/max from each child
    if(node.children.size is not 0):
        iterator = node.children.head
        while iterator is not None:
            min_max(iterator, not color, alpha, beta)
            #set alpha to min of children and beta to max
            if(color):
                if (iterator.val > alpha):
                    alpha = iterator.val
            else:
                if (iterator.val < beta):
                    beta = iterator.val
            #If alpha is greater or equal to beta, prune branch
            if(alpha >= beta):
                break
            iterator = iterator.next_node

        #After all children are at min/max value, update value of current node to min/max of children
        if(color):
            node.val = node.children.max()
        else:
            node.val = node.children.min()
            
    #If root node is reached, return move with the best min/max value
    if(node.parent_node is None):
        if(color):
            return random.choice(node.children.max_val_moves())
        else:
            return random.choice(node.children.min_val_moves())

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
