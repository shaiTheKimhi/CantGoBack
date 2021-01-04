"""
MiniMax Player with AlphaBeta pruning and global time
"""
from players.AbstractPlayer import AbstractPlayer
#TODO: you can import more modules, if needed
import players.AlphabetaPlayer
import numpy as np

class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time, penalty_score) # keep the inheritance of the parent's (AbstractPlayer) __init__()
        #TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py
        self.alpha_beta_player = players.AlphabetaPlayer.Player(game_time, penalty_score)
        self.max_nr_turns = 0  #indicates the number of free turns
        self.turn_number = 1  #indicates the current turn number
        self.average_turn_time = 0.0

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        #TODO: erase the following line and implement this function.
        self.alpha_beta_player.set_game_params(board)
        free_blocks = self.free_blocks(board)
        self.max_nr_turns = free_blocks / 2 + 1  #maximum number of turns until finish is number of free blocks, our player will perform maximum of half + 1 of that
        self.average_turn_time = self.game_time / self.max_nr_turns



    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        #TODO: erase the following line and implement this function.
        turn_time = 0.0
        #turns 0 - n/5, gets 2/5 of average time
        #turns n/5 - 3n/5, gets 1/5 of average time
        #turns 3n/5 - 4n/5, gets 3/25 of average time
        #turns 4n/5 - 1, gets 2/25 of average time
        factors = [2, 1, 1, 0.6, 0.4]
        turn_time = self.average_turn_time * factors[int(self.turn_number / self.max_nr_turns)]
        turn_time = time_limit if time_limit < turn_time else turn_time

        self.turn_number += 1
        return self.alpha_beta_player.make_move(turn_time, players_score)


    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        #TODO: erase the following line and implement this function.
        self.alpha_beta_player.set_rival_move(pos)


    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        #TODO: erase the following line and implement this function. In case you choose not to use this function, 
        # use 'pass' instead of the following line.
        self.alpha_beta_player.update_fruits(fruits_on_board_dict)


    ########## helper functions in class ##########
    #TODO: add here helper functions in class, if needed

    @staticmethod
    def free_blocks(board):
        return len(np.where(board == 0)[0]) + len(np.where(board >= 3)[0])

    ########## helper functions for AlphaBeta algorithm ##########
    #TODO: add here the utility, succ, and perform_move functions used in AlphaBeta algorithm