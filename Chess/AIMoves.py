import ChessMove
import random
import Tree
import chess

#File contains implementation of different move techniques for computer

#Follows a min/max aglorithm to determine and execute move
#board = current state of board
#returns san move of move added to the board
def min_max_move(board):
    #create Tree of given depth of baord state and moves
    #NOTE: change tree depth to change how many moves are looked ahead
    treeDepth = 3
    moves_tree = Tree.Tree(treeDepth, board)

    if(board.turn is chess.WHITE and treeDepth%2 == 1):
        color = True
    else:
        color = False

    move = min_max(moves_tree, color, moves_tree.max_depth)
    sanMove = board.san(move)
    board.push_uci(str(move))
    
    return sanMove
    

#Recursivley updates each layer of tree by minimizing or maximizing the value of parent based on child nodes
#tree = tree of moves/values being traversed
#color = True/White or False/Black
#depth = current depth to min/max values of nodes
def min_max(tree, color, depth):
    #if top of tree is reached, return randomly chosen move from children tied with best value
    if depth is 0:
        if (color):
            print(ChessMove.Value_Move(tree.root.children.min_val_moves()[0]).move_val(tree.root.board))
            return random.choice(tree.root.children.min_val_moves())
        else:
            print(ChessMove.Value_Move(tree.root.children.max_val_moves()[0]).move_val(tree.root.board))
            return random.choice(tree.root.children.max_val_moves())

    #find all nodes at a given depth in tree
    nodes_to_update = BFS(tree, depth)

    #If white, update values of nodes at depth to the max of their children
    if(color is False):
        for i in nodes_to_update:
            #only update values if nodes are not the end of the tree
            if(i.children.size is not 0):
                i.val = i.children.max()
       
        return min_max(tree, True, depth-1)
    else:
        #if black, update values of nodes at depth to min of their children
        for i in nodes_to_update:
            #only update values if nodes are not the end of the tree
            if(i.children.size is not 0):
                i.val = i.children.min()
        
        return min_max(tree, False, depth-1)

#Breadth First Search to return a list of all nodes in the tree at a given depth
#tree = tree being traversed
#depth = depth to find nodes for 
def BFS(tree, depth):
    nodes_at_depth = list()
    queue_to_visit = list()
    tempNode = tree.root
    queue_to_visit.append(tree.root)
    nodeDepth = tree.get_depth(tempNode)

    #loop until a node that is greater than desired depth is reached or queue is empty(end of tree is reached)
    while (queue_to_visit and nodeDepth <= depth):

        tempNode = queue_to_visit.pop(0)
        nodeDepth = tree.get_depth(tempNode)
        #If node is at depth, save it
        if(nodeDepth is depth):
            nodes_at_depth.append(tempNode)
        
        #add children to nodes to be visited
        iterator = tempNode.children.head
        while iterator is not None:
            queue_to_visit.append(iterator)
            iterator = iterator.next_node
        #queue_to_visit.extend(tempNode.children)

    return nodes_at_depth

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
