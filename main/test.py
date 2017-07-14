'''
Created on 3 Jul 2017

@author: edward allan florindo

MEGA tic tac toe
sizes from 3x3 to 15x15
'''

from IPython.display import clear_output
import os, math

if __name__ == '__main__':
    pass
size = 7
win_size = 4
char_width = 3
board = []
board_string = ''
move = {}
winner  = None


def reset_game():
    '''
    Reset the global variables
    '''
    global board, move, winner, board_string
    board = list(range(1,(size*size) + 1))
    board_string = ''.join([str(a) for a in board])
    move = {'player': None, 'cell': None}
    winner  = None

def check_winner():
    '''
    Check if there is winner
    Return: True or False
    '''
    global board, winner, win_size, size

    for player in ['X','O']:
        for loc in range(0,len(board)):
            #horizontal
            #x,x+1,x+2 were x+1 is not factor of size
            if loc + (win_size - 1) >= len(board):
                break
            row = math.ceil((loc+1)/size)
            pattern = [board[p] for p in  range(loc, loc + win_size) if math.ceil((p+1)/size) == row]
            if pattern.count(player) == win_size:
                winner = player
                return True

        for slope in [1,0,-1]:
            for loc in range(0,len(board)):
                #check with the row

                #vertical, diagonal + diagonal -
                if loc + ((win_size - 1) * (size + slope)) >=  len(board):
                    break
                pattern = [board[p] for p in range(loc, loc + ((win_size - 1) * (size + slope)) + 1, (size + slope)) if math.ceil((p + 1 + size + slope)/size) - math.ceil((p + 1)/size) == 1 or (p + 1 == len(board) and slope == 1) or (slope == -1 and len(board) - size == p)]
                if pattern.count(player) == win_size:
                    winner = player
                    return True
    return False

def  is_gameover():
    '''
    Check if all cell are filled-out or not
    Return: True or False
    '''
    global board, size
    if(board.count('X') + board.count('O') < size*size):
        return False
    return True

def print_board():
    '''
    Print board 3x3 store the move here X and 0
    the board global, size global
    '''
    global board, size, char_width,move
    clear_output()
    os.system('cls||clear')
    cell = 0
    while cell < len(board):
        row =  [(' ' * (char_width - len(str(x)))) + str(x) for x in board[ cell : (cell + size)]]
        print(str(row).replace(',', '|').replace("'", ''))
        cell += size
    print('Next move: '+ str(move))

def next_move():
    '''
    Determine next move and switch player
    reset cell to None on next move
    the move global
    '''
    global move
    if move['player'] == None:
        move['player'] = 'X'
    elif move['player'] == 'X':
        move['player'] = 'O'
    else:
        move['player'] = 'X'
    move['cell'] = 'None'

def save_move():
    '''
    save the move to board if it is correct
    Return : True or False
    '''
    global move, board, board_string
    try:
        if move['cell'] not in board_string:
            return False
        elif str(board[int(move['cell'])-1]) not in board_string:
            return False
        else:
            board[int(move['cell'])-1] = move['player']
            return True
    except:
        return False

def get_input():
    '''
    Get user input
    global board, move
    '''
    global board, move
    next_move()

    while True:
        print_board()
        move['cell'] = input('Please enter cell number as indicated in board:  ')
        if save_move():
            break
        else:
            move['cell'] = 'Incorrect move!'
    print_board()

def get_size():
    '''
    Get the user chosen size
    '''
    global size, win_size
    while True:
        try:
            input_size = input('Please enter 3 to 15 size: ')
            if int(input_size)  in range(3,16):
                size = int(input_size)
                if size > 7:
                    win_size = 5
                elif size > 4:
                    win_size = 4
                else:
                    win_size = 3
                break
        except:
            pass

#the main flow
cont = True
while cont == True:
    get_size()
    reset_game()
    while  is_gameover() == False:
        get_input()
        if check_winner() == True:
            print('Winner: Player %s!' % winner)
            break
    if (winner == None):
        print('Tie!')
    print('Game ended.')
    toplay = input ('Play again? (y,n)')
    if toplay.lower() == 'y':
        cont = True
    else:
        cont = False
