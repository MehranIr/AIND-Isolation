"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import isolation
from isolation import Board

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    print(str(game.get_legal_moves(player)))
    return float(len(game.get_legal_moves(player)))



def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    print("score is "+ str(float((h - y)**2 + (w - x)**2)))
    return float((h - y)**2 + (w - x)**2)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    raise NotImplementedError


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=2, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


    def min_value(self, game, depth, alpha=float("-inf"), beta=float("inf"), prune=False):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        alpha and beta limit the lower and upper bound of our search and prune determines whether we use alpha beta pruning or not 
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # Check if this is the last possible move
        if game.utility(game.active_player) != 0: 
            return float("inf")  # by Assumption 2
        # If this is the last depth that is supposed to be searched the score in the eyes of player 1 will be returned 
        if (depth == 0):
            return self.score(game, game._player_1)
        # v is the placeholder for the lowest known score among all the available options
        v = float("inf")
        for m in game.get_legal_moves(game.active_player):
            if prune: 
                v = min(v, self.max_value((game.forecast_move(m)), (depth - 1), alpha, beta, prune))
                if v <= alpha :
                    return v
                beta = min(beta, v)
            else:
                v = min(v, self.max_value((game.forecast_move(m)), (depth - 1)))
        return v

    def max_value(self, game, depth, alpha=float("-inf"), beta=float("inf"), prune=False):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        alpha and beta limit the lower and upper bound of our search and prune determines whether we use alpha beta pruning or not
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # if this is the last possible move
        if game.utility(game.active_player) != 0:
            return float("-inf")  # by assumption 2
        # If this is the last depth that is supposed to be searched the score in the eyes of player 1 will be returned 
        if (depth == 0):
            return self.score(game, game._player_1)
        # v is the placeholder for the highest known score among all the available options
        v = float("-inf")
        for m in game.get_legal_moves(game.active_player):
            if prune:
                v = max(v, self.min_value(game.forecast_move(m), (depth - 1), alpha, beta, prune))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            else:
                v = max(v, self.min_value(game.forecast_move(m), (depth - 1)))
        return v



class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """


    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if game.active_player == game._player_1:
#             print(str(game.active_player) + " location is: "+str(game.get_player_location(game.active_player)))
#             print("move list is: "+str(move_list))
            
            # v is the place holder for the highest available score while bestMove is the move that has caused the score
            bestMove = None
            v = float("-inf")
            for m in game.get_legal_moves():
#                 print(str(game.active_player)+ " moved to location: " + str(m))
                move_score = self.min_value(game.forecast_move(m), depth - 1)
                if v < move_score:
                    v = move_score
                    bestMove = m
                else:
                    if bestMove == None and v == move_score:
                        bestMove = m
#             print ("===============================")
#             print("final result is: "+ str(bestMove) + "for depth"+ str(depth)) 
            print ("minimax best score is: " + str(v))
            return bestMove
        else:
            move_list = game.get_legal_moves(game.active_player)
            print(str(game.active_player) + " location is: " + str(game.get_player_location(game.active_player)))
            print("move list is: " + str(move_list))
            
            # v is the place holder for the lowest available score(best move for player2) while bestMove is the move that has caused the score
            bestMove = None
            v = float("inf")
            for m in game.get_legal_moves():
                move_score = self.max_value(game.forecast_move(m), depth - 1)
                if v > move_score:
                    v = move_score
                    bestMove = m
#             print ("===============================")
#             print("final result is: "+ str(bestMove)) 
            print ("minimax best score is: " + str(v))
            return bestMove


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

#         try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
        return self.alphabeta(game, self.search_depth)

#         except SearchTimeout:
#             pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
#         return best_move

#     def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

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

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        bestMove = None
        # TODO: finish this function!
        if game.active_player == game._player_1:
            for m in game.get_legal_moves():
                move_score = self.min_value(game.forecast_move(m), depth - 1, alpha, beta, True)
                # updating our alpha and the best possible move in case the evaluated move was the best move that was evaluated until now...
                if alpha < move_score: 
                    alpha = move_score
                    bestMove = m
            return bestMove
        # if we are player 2
        else:
            for m in game.get_legal_moves():
                move_score = self.max_value(game.forecast_move(m), depth - 1, alpha, beta, True)
                # updating our beta and the best possible move in case the evaluated move was the best move that was evaluated until now...
                if beta > move_score:
                    beta = move_score
                    bestMove = m
            return bestMove
