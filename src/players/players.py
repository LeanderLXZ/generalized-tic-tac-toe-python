import numpy as np
from strategies.get_initial_moves import null_im
from strategies.get_limited_moves import null_lm
from board import Board, GameError


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


class Player(object):
    
    TIMER_THRESHOLD = 100
    BLANK_SPACE = '-'
    PLAYER_1 = 'O'
    PLAYER_2 = 'X'
    
    def __init__(self):
        self.player_mark = None
        self.opponent_mark = None
        self.initial_moves_fn = null_im
        self.limited_moves_fn = null_lm
        
    def assign_player_mark(self, player_mark):
        self.player_mark = player_mark
        self.opponent_mark = self.get_opponent(player_mark)
        
    def get_move(self, board, time_left, n_step):
        raise NotImplementedError
    
    def get_opponent(self, player_mark):
        if player_mark == self.PLAYER_1:
            return self.PLAYER_2
        elif player_mark == self.PLAYER_2:
            return self.PLAYER_1
        else:
            return None


class HumanPlayer(Player):

    def get_move(self, board, time_left, n_step):
        input_move = input('Input a move (format: tuple): ')
        try:
           input_move = tuple([int(s) for s in input_move.split(' ')]) 
        except:
            try:
                input_move = eval(input_move)
                if type(input_move) is not tuple:
                    raise GameError('Illegal input! Please input a tuple!')
            except:
                raise GameError('Illegal input! Please input a tuple!')
        return input_move
