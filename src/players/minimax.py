import numpy as np
from strategies.scores import null_score
from strategies.get_initial_moves import null_im
from strategies.get_limited_moves import null_lm
from players.players import Player, SearchTimeout


class MinimaxPlayer(Player):
    """Class for minimax agents.

    Parameters
    ----------
    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, 
                 score_fn=null_score,
                 initial_moves_fn = null_im,
                 limited_moves_fn = null_lm,
                 timeout=10.):
        self.score_fn = score_fn
        self.initial_moves_fn = initial_moves_fn
        self.limited_moves_fn = limited_moves_fn
        self.time_left = None
        self.timer_threshold = timeout
        self.player_mark = None

    def get_move(self, board, time_left, n_step):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Parameters
        ----------
        board : board.Board
            A instance of the generalized TIC-TAC-TOE board `Board` class 
            representing the current board state.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
            
        n_step : int
            the index number of step

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        initial_move = self.initial_moves_fn(board, n_step)
        if initial_move:
            return initial_move
        
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = board.legal_moves[np.random.choice(len(board.legal_moves))]

        try:
            search_depth = 1
            while search_depth <= len(board.legal_moves):
                print('Now searching depth:', search_depth)
                best_move = self.minimax(board, search_depth)
                search_depth += 1
        except SearchTimeout:
            print('[W] Search timeout!')
        
        return best_move
    
    def minimax(self, board, depth):
        """Depth-limited minimax search algorithm.

        Parameters
        ----------
        board : board.Board
            An instance of the generalized TIC-TAC-TOE board `Board` class 
            representing the current board state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = float("-inf")
        best_move = (-1, -1)
        
        candidate_moves = self.limited_moves_fn(board, self.player_mark)
        for m in candidate_moves:
            # print('me first do', m)
            moved_board = board.get_moved_board(m, self.player_mark)
            v = self.min_value(moved_board, depth - 1)
            # print(v, m)
            if v > best_score:
                best_score = v
                best_move = m
                
        if best_move == (-1, -1):
            print('Randomly get a best_move')
            best_move = candidate_moves[np.random.choice(len(candidate_moves))]
        return best_move

    def min_value(self, board, depth):
        """ Return the value for a win (+1) if the board is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if board.is_winner(self.player_mark):
            return float("inf")
        
        if depth <= 0:
            # print('s', self.score_fn(board, self.player_mark))
            return self.score_fn(board, self.player_mark)
        
        v = float("inf")
        candidate_moves = self.limited_moves_fn(board, self.opponent_mark)
        for m in candidate_moves:
            # print('op do', m)
            moved_board = board.get_moved_board(m, self.opponent_mark)
            v = min(v, self.max_value(moved_board, depth - 1))
        return v

    def max_value(self, board, depth):
        """ Return the value for a loss (-1) if the board is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if board.is_loser(self.player_mark):
            return float("-inf")
        
        if depth <= 0:
            # print('s', self.score_fn(board, self.player_mark))
            return self.score_fn(board, self.player_mark)
        
        v = float("-inf")
        candidate_moves = self.limited_moves_fn(board, self.player_mark)
        for m in candidate_moves:
            # print('me do', m)
            moved_board = board.get_moved_board(m, self.player_mark)
            v = max(v, self.min_value(moved_board, depth - 1))
        return v


class AlphaBetaPlayer(MinimaxPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, board, time_left, n_step):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Parameters
        ----------
        board : board.Board
            An instance of the generalized TIC-TAC-TOE board `Board` class 
            representing the current board state

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
            
        n_step : int
            the index number of step

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        initial_move = self.initial_moves_fn(board, n_step)
        if initial_move:
            return initial_move
        
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = board.legal_moves[np.random.choice(len(board.legal_moves))]
    
        try:
            search_depth = 1
            while search_depth <= len(board.legal_moves):
                print('Now searching depth:', search_depth)
                best_move = self.alphabeta(board, search_depth)
                search_depth += 1
        except KeyboardInterrupt:
            print('-======')
            return
        except SearchTimeout:
            print('[W] Search timeout!')
        finally:
            return best_move

    def alphabeta(self, board, depth, alpha=float("-inf"), beta=float("inf")):
        """Depth-limited minimax search with alpha-beta pruning.
        
        Parameters
        ----------
        board : board.Board
            An instance of the generalized TIC-TAC-TOE board `Board` class 
            representing the current board state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = float("-inf")
        best_move = (-1, -1)
        
        candidate_moves = self.limited_moves_fn(board, self.player_mark)
        for m in candidate_moves:
            # print('me first do', m)
            moved_board = board.get_moved_board(m, self.player_mark)
            v = self.min_value(moved_board, alpha, beta, depth - 1)
            print(v, m)
            if v > best_score:
                best_score = v
                best_move = m
            alpha = max(alpha, v)
            
        if best_move == (-1, -1):
            print('Randomly get a best_move')
            best_move = candidate_moves[np.random.choice(len(candidate_moves))]
        return best_move

    def min_value(self, board, alpha, beta, depth):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if board.is_winner(self.player_mark):
            return float("inf")
        
        if depth <= 0:
            # print('s', self.score_fn(board, self.player_mark))
            return self.score_fn(board, self.player_mark)
        
        v = float("inf")
        
        candidate_moves = self.limited_moves_fn(board, self.opponent_mark)
        for m in candidate_moves:
            # print('op do', m)
            moved_board = board.get_moved_board(m, self.opponent_mark)
            v = min(v, self.max_value(moved_board, alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def max_value(self, board, alpha, beta, depth):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if board.is_loser(self.player_mark):
            return float("-inf")
        
        if depth <= 0:
            # print('s', self.score_fn(board, self.player_mark))
            return self.score_fn(board, self.player_mark)
        
        v = float("-inf")
        
        candidate_moves = self.limited_moves_fn(board, self.player_mark)
        for m in candidate_moves:
            # print('me do', m)
            moved_board = board.get_moved_board(m, self.player_mark)
            v = max(v, self.min_value(moved_board, alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v