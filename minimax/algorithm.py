from copy import deepcopy
import pygame

from checkers.constants import BLACK

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Position -> Current position that we are in (Board Object)
#Depth -> How far the tree extends. As the depth value gets higher algorithm gets better.
#Max Player -> Boolean value that shows us whether we are maximizing or minimizing our value.
#Game -> Game Object
def minimax(position, depth, max_player, game):
    #Checking if the game is over or not 
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    #Maximizing
    if max_player:
        #Starting from -inf for our max evalutaion value because for each position value check we will try to get the better value so that starting from worst possible value.
        maxEval = float('-inf') 
        #Stores the best move we will find
        best_move = None
        #Checking all possible moves for white (Ai) in order to get the best move with max evaluation score
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    #Minimizing
    else:
        minEval = float('inf')
        best_move = None
        #Checking all possible moves for black to get the worse move for it in orde to take advantage for itself(WHITE)
        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move

#This function takes the piece and makes the move for the piece on board
def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board

#Getting the moves of one of the colors in the game and returns it
def get_all_moves(board, color, game):
    moves = [] #Stores moves
    #Getting all of the pieces of that certain color
    for piece in board.get_all_pieces(color):
        #Getting valid moves for each pieces
        valid_moves = board.get_valid_moves(piece)
        #move -> row column possible move topple
        #skip -> Pieces we could skip if we jump on them 
        for move, skip in valid_moves.items():
            #Storing the board in order to determine when the piece makes the move what would the new board looks like 
            #Rather than modifying same board every time creating a new one with the possible move while holdin the board on temp
            temp_board = deepcopy(board)
            #Again for same reasons for board keeping the pieces old position in order to not to lose when tho move happens
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            #Creating new board
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            #Appending the move into moves list in order to use it in our minimax algorithm
            moves.append(new_board)
    return moves
