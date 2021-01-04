"""
MiniMax Player with AlphaBeta pruning with light heuristic
"""
from players.AbstractPlayer import AbstractPlayer
# TODO: you can import more modules, if needed
import players.AlphabetaPlayer
import players.MinimaxPlayer

class Player(players.MinimaxPlayer.Player):
    def __init__(self, game_time, penalty_score):
        players.MinimaxPlayer.Player.__init__(self, game_time, penalty_score)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        # TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py

    def heuristic(self, turn):
        nxt1 = [p for p in self.succ(self.pos)]
        nxt2 = [p for p in self.succ(self.en_pos)]
        val1 = 4 - len(nxt1) * self.penalty_score
        val2 = 4 - len(nxt2) * self.penalty_score
        return self.score - val1, self.en_score - val2

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        # TODO: erase the following line and implement this function.
        move, val = self.best_move(4)  # limit is 3 permanently

        pos = (self.pos[0] + move[0], self.pos[1] + move[1])
        self.effect_move(pos, 1)
        if self.count_ones(self.board) != 1:
            problem = True
        return move



    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed

    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, and perform_move functions used in AlphaBeta algorithm
