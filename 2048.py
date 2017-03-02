##########################
# Game graphic interface #
##########################

from Tkinter import *
from random import *
import time
from random import *
from copy import deepcopy

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

WHITE_COLOR = "#ffffff"
BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {   2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", \
                            32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61", \
                            512:"#edc850", 1024:"#edc53f", 2048:"#edc22e", 4096:"#edc22e", 8192:"#edc22e" }
CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2", \
                    32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2", \
                    512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2" , 4096:"#f9f6f2" , 8192:"#f9f6f2" }
FONT = ("Verdana", 40, "bold")
SCORE_FONT=("Verdana", 20, "bold")


class GameGrid(Frame):
    
    def __init__(self, logic):
        Frame.__init__(self)
        self.l = logic
        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)
        self.commands = {   'w': self.l['up'],
                            's': self.l['down'],
                            'a': self.l['left'],
                            'd': self.l['right'] }
        self.AI = False
        self.menubar = Menu(self.master)
        self.menubar.add_command(label="Play", command=self.newgamePlay)
        self.menubar.add_command(label="Watch AI", command = self.newgameAI)
        self.master.configure(menu = self.menubar)
        print(self.grid)
        self.newgame()

    def newgamePlay(self):
        self.AI = False
        self.newgame()

    def newgameAI(self):
        self.AI = True
        self.newgame()

    def newgame(self, AI=False):
        if hasattr(self, 'background'):
            self.background.grid_forget()
            self.score_container.grid_forget()
        self.grid_cells = []
        self.init_grid()
        self.init_score()
        self.game_state = self.l['make_new_game'](GRID_LEN)
        self.update_grid_cells()
        self.mainloop()
        
    def init_grid(self):
        self.background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        self.background.grid()

        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(self.background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/GRID_LEN, height=SIZE/(GRID_LEN))                
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def init_score(self):
        self.score_container = Frame(self, width=SIZE, height=50)
        self.score_container.grid()

        score_label = Frame(self.score_container, bg=WHITE_COLOR, width=SIZE/2, height=20)
        score_label.grid(row=0, column=0, columnspan=1, padx=GRID_PADDING, pady=GRID_PADDING)
        self.score_label = Label(master=score_label, text="Score ", bg=WHITE_COLOR, justify=RIGHT, font=SCORE_FONT, width=10, height=1)
        self.score_label.pack()

        score_text = Frame(self.score_container, bg=WHITE_COLOR, width=SIZE/2, height=20)
        score_text.grid(row=0, column=1, columnspan=1, padx=GRID_PADDING, pady=GRID_PADDING)
        self.score_text = Label(master=score_text, text="0000", bg=WHITE_COLOR, justify=RIGHT, font=SCORE_FONT, width=10, height=1)
        self.score_text.pack()

    def update_grid_cells(self):
        current_score = self.l['get_score'](self.game_state)
        current_matrix = self.l['get_matrix'](self.game_state)
        self.score_text.configure(text=str(current_score))
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = current_matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number], fg=CELL_COLOR_DICT[new_number])
        self.update_idletasks()
       
    def key_down(self, event):
        def display_end_game(word1, word2):
            self.grid_cells[1][1].configure(text=word1, bg=BACKGROUND_COLOR_CELL_EMPTY, fg=WHITE_COLOR)
            self.grid_cells[1][2].configure(text=word2, bg=BACKGROUND_COLOR_CELL_EMPTY, fg=WHITE_COLOR)

        # Press any key to make move
        current_matrix = self.l['get_matrix'](self.game_state)
        if self.AI:
            current_move = self.l['AI'](current_matrix)
        else:
            current_move = event.char
        try:
            self.game_state, is_valid_move = self.commands[current_move](self.game_state)
        except KeyError:
            raise RuntimeError("The solver produced an invalid command!")
        if is_valid_move:
            self.update_grid_cells()
            current_matrix = self.l['get_matrix'](self.game_state)
            current_status = self.l['game_status'](current_matrix)
            if current_status == "win":
                display_end_game('You', 'Win!')
            if current_status == "lose":
                display_end_game('You','Lose!')

####################
# Helper Functions #
####################

def accumulate(fn, initial, seq):
    if not seq:
        return initial
    else:
        return fn(seq[0], 
                  accumulate(fn, initial, seq[1:]))
    
def flatten(mat):
    return [num for row in mat for num in row]

def has_zero(mat):
    return 0 in flatten(mat)

def transpose(mat):
    return list(map(list,zip(*mat)))

def reverse(mat):
    return list(map(lambda row: list(reversed(row)),mat))


###############
# Game Matrix #
###############

def new_game_matrix(n):
    matrix = []
    for i in range(n):
        matrix.append([0] * n)
    return matrix


def add_two(mat):
    if not has_zero(mat):
        return mat
    a = randint(0, len(mat)-1)
    b = randint(0, len(mat)-1)
    while mat[a][b] != 0:
        a = randint(0, len(mat)-1)
        b = randint(0, len(mat)-1)
    mat[a][b] = 2
    return mat

def game_status(mat):
    for row in mat:
        for element in row:
            if element == 2048:
                return 'win'
    if has_zero(mat):
        return 'not over'
    for i in range(len(mat)): #Check horizontally
        for j in range(len(mat[0])-1):
            if mat[i][j] == mat[i][j+1]:
                return 'not over'
    for i in range(len(mat)-1): #Check vertically
        for j in range(len(mat[0])):
            if mat[i][j] == mat[i+1][j]:
                return 'not over'
    return 'lose'

def merge_left(matrix):
    def merge_row(row):
        merged_row, prev_tile, score_increment = [], 0, 0
        # performance increase
        merged_row_append = merged_row.append
        # pack element by element left-wards
        for tile in row:
            if tile == 0: continue
            if prev_tile == 0:
                prev_tile = tile
            elif prev_tile != tile:
                merged_row_append(prev_tile)
                prev_tile = tile
            else:
                merged_row_append(prev_tile*2)
                score_increment += prev_tile*2
                prev_tile = 0
        merged_row_append(prev_tile) # valid regardless whether there are merges or not
        # top up zeros
        while len(merged_row) != len(row):
            merged_row_append(0)
        return (merged_row, merged_row != row, score_increment)

    return accumulate(lambda first, rest: ([first[0]] + rest[0], 
                                            first[1] or rest[1], 
                                            first[2] + rest[2]),
                      ([], False, 0),
                      list(map(merge_row, matrix)))

def merge_right(mat):
    mat, valid, score = merge_left(reverse(mat))
    return (reverse(mat), valid, score)

def merge_up(mat):
    mat, valid, score = merge_left(transpose(mat))
    return (transpose(mat), valid, score)

def merge_down(mat):
    mat, valid, score = merge_left(reverse(transpose(mat)))
    return (transpose(reverse(mat)), valid, score)


###############
# Game Record #
###############
                
def make_new_record(mat, score):
    return (mat, score)
def get_record_matrix(record):
    return record[0]
def get_record_score(record):
    return record[1]


################
# Game Records #
################

def new_records():
    return []
def add_record(new_record, records):
    NUM_OF_UNDOS = 3
    records.append(new_record)
    if num_of_records(records) > NUM_OF_UNDOS:
        records = records[-NUM_OF_UNDOS:]
    return records
def num_of_records(records):
    return len(records)
def is_empty(records):
    return num_of_records(records) <= 0
def pop_last_record(records):
    if not is_empty(records):
        last_record = records.pop()
        return (get_record_matrix(last_record),
                get_record_score(last_record),
                records)
    else:
        return (None, None, records)

##############
# Game State #
##############

def make_state(matrix, total_score, history):
    return (matrix, total_score, history)
def get_matrix(state):
    return state[0]
def get_score(state):
    return state[1]
def get_history(state):
    return state[2]
def make_new_game(n):
    starting_matrix = add_two(add_two(new_game_matrix(n)))
    return make_state(starting_matrix, 0, new_records())

def execute_move(state, matrix_updater):   
    current_score = get_score(state)
    next_matrix, valid_move, score_increment = matrix_updater(get_matrix(state))
    if not valid_move:
        return (state, False)
    else:
        updated_history = add_record(state, get_history(state))
        updated_state = make_state(add_two(next_matrix),
                                   current_score + score_increment,
                                   updated_history)
        return (updated_state, True)
def left(state):
    return execute_move(state, merge_left)
def right(state):
    return execute_move(state, merge_right)
def up(state):
    return execute_move(state, merge_up)
def down(state):
    return execute_move(state, merge_down)

def undo(state):
    records = get_history(state)
    matrix, score, records = pop_last_record(records)
    if matrix:
        return (make_state(matrix, score, records), True)
    else:
        return (state, False)    

game_logic = {
    'make_new_game': make_new_game,
    'game_status': game_status,
    'get_score': get_score,
    'get_matrix': get_matrix,
    'up': up,
    'down': down,
    'left': left,
    'right': right,
    'undo': undo
}

#################
# AI Assessment #
#################

def get_AI_score(AI_funct, custom_mat = []):
    GRID_SIZE = 4
    MAX_FALSE_MOVES = 80
    false_moves_counter = MAX_FALSE_MOVES
    score = 0
    mat = add_two(add_two(new_game_matrix(GRID_SIZE))) if not custom_mat else custom_mat
    while True:
        move_funct = {'w': merge_up,
                      'a': merge_left,
                      's': merge_down,
                      'd': merge_right}[AI_funct(mat)]
        mat, valid, score_increment = move_funct(mat)
        if not valid:
            MAX_FALSE_MOVES -= 1
            if MAX_FALSE_MOVES <= 0:
                raise RuntimeError("Max number of consecutive false move reached!")
            continue
        false_moves_counter = MAX_FALSE_MOVES
        score += score_increment
        mat = add_two(mat)
        status = game_status(mat)
        if status == "win":
            return score, mat, True
        elif status == "lose":
            return score, mat, False
        
def get_average_AI_score(AI_funct, print_final_states = False):
    def print_game(mat, score):
        if not print_final_states: return
        for row in mat:
            print(''.join(map(lambda x: str(x).rjust(5), row)))
        print('score: ' + str(score))
        
    SAMPLE_SIZE = 10
    total = 0
    win_count = 0
    for i in range(SAMPLE_SIZE):
        try:
            score, mat, is_won = get_AI_score(AI_funct)
            print_game(mat, score)
            total += score
            win_count += 1 if is_won else 0
        except RuntimeError:
            print("The solver seems to have problem finding valid moves!")
            return
    average_score = total / SAMPLE_SIZE
    percent_wins = win_count * 100 / SAMPLE_SIZE
    print("Average score = " + str(average_score))
    print("Percentage wins = " + str(percent_wins) + "%")
    return (average_score, percent_wins)



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
# get_average_AI_score(AI, True)
