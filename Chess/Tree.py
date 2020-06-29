import ChessMove
import chess
import copy 

class LinkedList():
    def __init__(self):
        self.head = None
        self.size = 0

    #node = node to be added to list
    def add(self, node):
        #if list is empty, make head point to first node
        if (self.size is 0):
            self.head = node
        else:
            #point new node to previous first node and update head
            temp = self.head
            node.next_node = temp
            self.head = node
        self.size += 1

    #returns highest val of any nodes in list
    def max(self):
        temp = self.head
        high = temp.val
        while temp is not None:
            if temp.val > high:
                high = temp.val
            temp = temp.next_node
        return high

    #returns highest val of any nodes in list
    def min(self):
        temp = self.head
        low = temp.val
        while temp is not None:
            if temp.val < low:
                low = temp.val
            temp = temp.next_node
        return low

    #retuns list holding all moves in list tied at max value
    def max_val_moves(self):
        temp = self.head
        moves = list()
        moves.append(temp.next_move)
        high = -1000000
        while temp is not None:
            #If a node with higher value is found, clear list and save new node
            if(temp.val > high):
                high = temp.val
                moves.clear()
                moves.append(temp.next_move)
            elif(temp.val is high):
                moves.append(temp.next_move)
            temp = temp.next_node
        return moves

    #retuns list holding all moves in list tied at min value
    def min_val_moves(self):
        temp = self.head
        moves = list()
        moves.append(temp.next_move)
        low = 1000000
        while temp is not None:
            #If a node with lower value is found, clear list and save new node
            if(temp.val < low):
                low = temp.val
                moves.clear()
                moves.append(temp.next_move)
            elif(temp.val is low):
                moves.append(temp.next_move)
            temp = temp.next_node
        return moves

    #print all values stored in nodes in list (Used for testing)
    def print_list(self):
        
        temp = self.head
        high = temp.val
        while temp is not None:
            if temp.val > high:
                high = temp.val
            temp = temp.next_node
        print(high)
        
class Node():
    def __init__(self, board, next_move, parent_node = None, depth = None, max_depth = None, prev_node = None, next_node = None):
        
        self.board = board
        self.parent_node = parent_node
        self.next_move = next_move
        self.next_node = next_node
        self.children = LinkedList()
        self.val = self.value(depth, max_depth)

    #Calculates the value of a node based on net gain or loss of given move and parent moves
    def value(self, depth, max_depth):
        #If the node is meant to have value (not head or root), do not calc
        if(self.next_move is not None):
            val = ChessMove.Value_Move(self.next_move).move_val(self.board)
            #If at max depth, calculate net value of parents rather than static value
            if(depth == max_depth):
                temp = self
                while temp.parent_node.parent_node is not None:
                    temp = temp.parent_node
                    val += temp.val
            #update board after move to pass to children
            tempBoard = copy.copy(self.board)
            tempBoard.push_uci(str(self.next_move))
            self.board = tempBoard

            return val

class Tree():
    def __init__(self, max_depth, board):
        self.root = Node(board, None, None, 0, max_depth)
        self.max_depth = max_depth
        self.board = board
        self.construct_tree(self.root)
    
    #Constructs tree by adding children to given node
    def construct_tree(self, node):
        need_children = LinkedList()

        #Add the layer if the max depth is not reached
        if self.get_depth(node) < self.max_depth:
            for i in node.board.legal_moves:
                #For each legal move, create a new node
                newNode = Node(node.board, i, node, self.get_depth(node)+1, self.max_depth)
                node.children.add(newNode)
                need_children.add(newNode)
                
            #loop through all nodes that need children and add layer
            iterator = need_children.head
            while(iterator is not None):
                self.construct_tree(iterator)
                iterator = iterator.next_node
        
    #Returns depth of a given node (distance from root)
    def get_depth(self, node):
        depth = 0
        temp = node
        while temp is not self.root:
            temp = temp.parent_node
            depth += 1
        return depth

    