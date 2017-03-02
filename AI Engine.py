from random import *
from puzzle_AI import *
from copy import deepcopy
from math import log

def AI(mat):

    #Some variables that many functions will want, lets only calculate them once
    dim = len(mat)
    merge_choices = ['left', 'right', 'up', 'down']
    ai_param = {'left': 'a', 'right' : 'd','up':'w', 'down': 's'}
    merge_function = {'left': merge_left, 'right' : merge_right,'up':merge_up, 'down': merge_down}

    def zeros(mat):
        # Count the number of zeros in the matrix
        return flatten(mat).count(0)

    def sorted_mat(mat):
        return sorted(flatten(mat))


    def monotonicity(mat):
        score = [0,0,0,0]
        for i in range(4):
            for j in range(4):
                score[0] += (40 - (i+j)**2) * mat[i][j]
                score[1] += (40 - (3-i+j)**2) * mat[3-i][j]
                score[2] += (40 - (3-i+j)**2) * mat[i][3-j]
                score[3] += (40 - (6-i+j)**2) * mat[3-i][3-j]
        return max(score)

    def rotate(mat):
        return zip(*mat[::-1])
   
    def prefer_corner(mat):
        score = [0,0,0,0]
        weighting = 50

        for rotation in range(4):
            for i in range(4):
                score[rotation] += (weighting - (i)**2) * (mat[i][0] + mat[0][i])
            mat = rotate(mat)

        return max(score)

    def zero_positions(mat):
        return [i for i, x in enumerate(flatten(mat)) if x == 0]

    def score(mat):
        z = zeros(mat)
        k = 4
        if z <= k:
            return z * prefer_corner(mat)
        else:
            return k * prefer_corner(mat)

    def minimax_player(mat,depth, return_move = False):

        # this is an index of all available moves and how good they are
        valid_moves = []
        valid_moves_append = valid_moves.append #performance enhancement
        # iterate through all possible moves
        for move in merge_choices:
            (possible_move, eligible) = merge_function[move](mat)[:2]
            # only do something if the move is legal
            if eligible:
                # now it is the computer's turn
                move_score = minimax_computer(possible_move, depth)
                valid_moves_append((move_score,move))
        valid_moves = sorted(valid_moves, key = lambda entry: entry[0], reverse=True)
        if return_move == True:
            return valid_moves[0][1]
        elif len(valid_moves) > 0:
            return valid_moves[0][0]
        else:
            return 0

    def minimax_computer(possible_move, depth):
        if depth == 1:
            return score(possible_move)

        # now it is the computer's turn
        # find out where the computer may play
        indices = zero_positions(possible_move)
        # record the scores the computer may get
        valid_moves = []
        valid_moves_append = valid_moves.append #performance enhancement
        # iterate through computer's  legal moves
        if len(indices) >= 4:
            indices= sample(indices,4)
        for i in indices:
            possible_outcome = deepcopy(possible_move)
            row,col = i//dim, i%dim
            possible_outcome[row][col]= 2
            # now find out how good the computer's response is
            valid_moves_append(minimax_player(possible_outcome,depth-1))

        # this is the computer's best move
        valid_moves = sorted(valid_moves)
        min_score = valid_moves[0]
        return min_score

    return ai_param[minimax_player(mat,3, return_move=True)]


# LEAVE THE FOLLOWING LINES UNCOMMENTED AND RUN TO WATCH THE SOLVER AT WORK
game_logic['AI'] = AI
gamegrid = GameGrid(game_logic)

# UNCOMMENT THE FOLLOWING LINE AND RUN TO SEE THE PERFORMANCE OF THE SOLVER OVER MANY ATTEMPTS
# Note: Your solver is expected to produce only valid moves.
get_average_AI_score(AI, True)
