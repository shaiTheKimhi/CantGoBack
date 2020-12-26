"""
MiniMax Player with AlphaBeta pruning
"""
from players.AbstractPlayer import AbstractPlayer
#TODO: you can import more modules, if needed
from players.MinimaxPlayer import Player as MinimaxPlayer
import time
import numpy as np

class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time, penalty_score)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        self.minimax = MinimaxPlayer(game_time, penalty_score)   # keeps the shell of the Minimax player



    #finds best move to act
    def best_move(self, lim):
        pos = self.minimax.pos
        curr_max = -float('inf')
        best = None
        for d in self.minimax.directions:
            p = (pos[0] + d[0], pos[1] + d[1])
            if self.minimax.is_legal(p):
                # make player move
                prev = self.minimax.pos
                old_fruits = self.minimax.effect_move(p, 1)

                # calculate minimax values for move and maximize
                val = self.MiniMaxAB(2, lim, -float('inf'), float('inf'))
                curr_max = max(curr_max, val)
                # keep best move
                best = d if curr_max == val else best

                # reset player move
                self.minimax.undo_move(prev, p, 1, old_fruits)
        if best is None:
            print(self.minimax.pos)
        return best, curr_max


    #alpha beta function search, similar to Minimax
    def MinimaxAB(self, turn, lim, alpha, beta):
        if self.minimax.goal(turn):
            val1, val2 = self.minimax.utility() #tuple of player1, player 2
            return float('inf') if val1 > val2 else -float('inf') if val1 < val2 else 0
        if lim == 0:
            val1, val2 = self.minimax.heuristic()  # tuple of player1, player 2
            return val1 - val2
        # turn is Agent
        if turn == 1:
            curr_max = -float('inf')
            for pos in self.minimax.succ(self.minimax.pos):
                # make player move

                prev_pos = self.minimax.pos
                old_fruits = self.minimax.effect_move(pos, 1)
                # find minimax value for player

                val = self.minimax.MiniMax(2, lim - 1)

                # save maximum of all values
                curr_max = max(val, curr_max)

                alpha = max(curr_max, alpha)
                if curr_max >= beta:
                    return float('inf')  #cut branch, minimizing caller will not be taken

                # reset player move
                self.minimax.undo_move(prev_pos, pos, 1, old_fruits)
            return curr_max  # maximize our player, minimize the other
        # turn is enemy agent
        else:
            curr_min = float('inf')
            for pos in self.minimax.succ(self.minimax.en_pos):
                # make rival move
                prev = self.minimax.en_pos
                old_fruits = self.minimax.effect_move(pos, 2)
                # find minimax value for rival
                val = self.minimax.MiniMax(1, lim - 1)

                # save minimum of all values
                curr_min = min(val, curr_min)

                beta = min(curr_min, beta)
                if curr_min <= beta:
                    return -float('inf')  #cut branch, maximizing caller will not be taken

                # reset rival move
                self.minimax.undo_move(prev, pos, 2, old_fruits)
            return curr_min  # maximize our player, minimize the other


    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        self.minimax.set_game_params(board)
    

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        ##gets program start time
        start_time = time.time()  #translates from miliseconds to seconds
        #plays always while time remaining
        lim = 0
        current_time = start_time
        move = self.minimax.best_move(0)
        while current_time - start_time < time_limit * .25:
            move, val = self.minimax.best_move(lim)
            current_time = time.time()
            time_passed = (current_time - start_time)
            if val == float('inf'):
                break
            lim += 1

        new_pos = self.minimax.pos[0] + move[0], self.minimax.pos[1] + move[1]
        #print(f"Limit:{lim}")
        #should use new function to make a move, and to undo the same move

        self.minimax.effect_move(new_pos, 1)  #player is always 1, opponent always 2
        return move


    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        #TODO: erase the following line and implement this function.
        self.minimax.set_rival_move(pos)


    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        self.minimax.update_fruits(fruits_on_board_dict)


    ########## helper functions in class ##########
    #TODO: add here helper functions in class, if needed


    ########## helper functions for AlphaBeta algorithm ##########
    #TODO: add here the utility, succ, and perform_move functions used in AlphaBeta algorithm
