"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
#TODO: you can import more modules, if needed
import numpy as np
from multiprocessing import Process
import time



class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time, penalty_score) # keep the inheritance of the parent's (AbstractPlayer) __init__()
        #TODO: initialize more fields, if needed, and the Minimax algorithm from SearchAlgos.py
        self.board = None  # and add three more fields to Player
        self.pos = None
        self.en_pos = None
        self.score = 0.0
        self.en_score = 0.0

        self.fruits = {}
        #minimum duration for fruit existance
        self.duration = 0


    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        #TODO: erase the following line and implement this function.
        # This implementation is from SimplePlayer.py, might need to change this ##NOTE THIS COMMENT !!!
        self.board = board
        pos = np.where(board == 1)
        en_pos = np.where(board == 2)
        # convert pos to tuple of ints
        self.pos = tuple(ax[0] for ax in pos)
        self.en_pos = tuple(ax[0] for ax in en_pos)

        self.duration = min(len(self.board), len(self.board[0]))
        #

        """
        #get fruits from map, include ints from 3 to max score on a position on board,
        #fruits is a dictionary of position (tuple of two int indexes) to value (integer)
        # fruits = np.where(board >= 3)
        # self.fruits = tuple(ax[0] for ax in fruits)
        """


    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        #TODO: erase the following line and implement this function.
        # search through first position using maximum

        #gets program start time
        start_time = time.time()  #translates from miliseconds to seconds
        #plays always while time remaining
        lim = 0
        current_time = start_time
        move = self.best_move(0)
        while current_time - start_time < time_limit * .25:
            move, val = self.best_move(lim)
            current_time = time.time()
            time_passed = (current_time - start_time)
            if val == float('inf') or val == -float('inf'):
                break
            lim += 1

        new_pos = self.pos[0] + move[0], self.pos[1] + move[1]
        #print(f"MINIMAX Limit:{lim}")

        self.effect_move(new_pos, 1) #player is always 1, opponent always 2
        return move


    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        #TODO: erase the following line and implement this function.
        self.board[self.en_pos] = -1
        self.en_pos = pos
        self.board[pos] = 2  #might keep our agent number in self, probably not necessary


    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        #TODO: erase the following line and implement this function. In case you choose not to use it, use 'pass' instead of the following line.
        for pos in fruits_on_board_dict.keys():
            if self.board[pos] not in (1, 2):
                self.board[pos] = fruits_on_board_dict[pos]
                self.fruits[pos] = {'value': fruits_on_board_dict[pos], 'duration': self.duration}


    ########## helper functions in class ##########
    #TODO: add here helper functions in class, if needed

    # makes the effect of a player move to given location, does not check validity, return new copy of fruits dictionary
    def effect_move(self, pos, turn):
        old_fruits = self.fruits.copy()
        prev = self.pos if turn == 1 else self.en_pos
        score = self.board[pos]
        if pos in self.fruits.keys():
            self.fruits.pop(pos)
        self.score += score
        self.board[pos] = turn
        self.board[prev] = -1
        if turn == 1:
            self.pos = pos
        else:
            self.en_pos = pos

        to_remove = []
        for pos in self.fruits.keys():
            self.fruits[pos]['duration'] -= 1
            if self.fruits[pos]['duration'] == -1:
                to_remove.append(pos)
        for pos in to_remove:
            self.fruits.pop(pos)

        return old_fruits

    # undo effects of a certain move (move is from prev to pos: prev->pos, and we undo it), gets old fruits and restores it, if score in old location updates it
    def undo_move(self, prev, pos, turn, old_fruits):
        self.fruits = old_fruits
        if turn == 1:
            self.pos = prev
        else:
            self.en_pos = prev
        score = 0
        if pos in self.fruits.keys():
            score = self.fruits[pos]['value']
        self.board[pos] = score
        self.board[prev] = turn
        self.score -= score


    #checks if move to pos is legal
    def is_legal(self, pos):
        return 0 <= pos[0] < len(self.board) and 0 <= pos[1] < len(self.board[0]) and (self.board[pos[0]][pos[1]] not in [-1, 1, 2])

    def best_move(self, lim):
        pos = self.pos
        curr_max = -float('inf')
        best = None
        for d in self.directions:
            p = (pos[0] + d[0], pos[1] + d[1])
            if self.is_legal(p):
                #make player move
                prev = self.pos
                old_fruits = self.effect_move(p, 1)

                #calculate minimax values for move and maximize
                val = self.MiniMax(2, lim)
                curr_max = max(curr_max, val)
                #keep best move
                best = d if curr_max == val else best

                #reset player move
                self.undo_move(prev, p, 1, old_fruits)
        if best is None:
            print(self.pos)
        return best, curr_max


    #TODO: MOVE THIS FUNCTION TO SearchAlgos.py file
    #gets the calling Player, the current turn, the limit of depth and an object that stores time to end, if too low time remaining, stops immediately
    def MiniMax(self, turn, lim): #TODO: add time check in function (might use different way to timeout minimax)
        if self.goal(turn):
            val1, val2 = self.utility()  #tuple of player1, player 2
            return float('inf') if val1 > val2 else -float('inf') if val1 < val2 else 0
        if lim == 0:
            val1, val2 = self.heuristic()  #tuple of player1, player 2
            return val1 - val2
        #turn is Agent
        if turn == 1:
            curr_max = -float('inf')
            for pos in self.succ(self.pos):
                # make player move

                prev_pos = self.pos
                old_fruits = self.effect_move(pos, 1)
                #find minimax value for player

                val = self.MiniMax(2, lim - 1)

                # save maximum of all values
                curr_max = max(val, curr_max)

                # reset player move
                self.undo_move(prev_pos, pos, 1, old_fruits)
            return curr_max  #maximize our player, minimize the other
        #turn is enemy agent
        else:
            curr_min = float('inf')
            for pos in self.succ(self.en_pos):

                #make rival move
                prev = self.en_pos
                old_fruits = self.effect_move(pos, 2)
                #find minimax value for rival
                val = self.MiniMax(1, lim - 1)

                #save minimum of all values
                curr_min = min(val, curr_min)

                #reset rival move
                self.undo_move(prev, pos, 2, old_fruits)
            return curr_min  #maximize our player, minimize the other

    ########## helper functions for MiniMax algorithm ##########
    #TODO: add here the utility, succ, and perform_move functions used in MiniMax algorithm
    #succ function returns all legal next moves
    def succ(self, pos):
        for d in self.directions:
            p = (pos[0] + d[0], pos[1] + d[1])
            if self.is_legal(p):
                yield p

    #goal is when the player to play cant play, turn marks {1,2} for the specific player
    def goal(self, turn):
        #return sum(1 for d in self.directions if 0 <= i < len(board) and 0 <= j < len(board[0]) and (board[pos[0] + d[0]][pos[1] + d[1]] not in [-1, 1, otherTurn])) == 0
        pos = self.pos if turn == 1 else self.en_pos
        for (i, j) in self.succ(pos):
            #checks legal move
            if self.is_legal((i, j)):
                return False
        return True

    #utility function gets state and calculates value (might need to calculate for heuristic as well)
    #calculates for both players
    def utility(self):
        # could do stuck check with reduce, better than two loops

        #check if our player is stuck
        our_stuck = True
        pos = self.pos
        for (i, j) in self.succ(pos):
            # checks legal move
            our_stuck = False
            break

        #check if opponent is stuck
        en_stuck = True
        pos = self.en_pos

        for (i, j) in self.succ(pos):
            # checks legal move
            en_stuck = False
            break

        #returns score for both players, our player is 1st index, other is 2nd
        score = self.score
        en_score = self.en_score
        #adds penalty to stuck player
        if our_stuck:
            score -= self.penalty_score
        if en_stuck:
            en_score -= self.penalty_score

        return score, en_score

    #heuristic function (checked when gets to limit)
    def heuristic(self):
        #TODO: implement this heuristic
        #getting next moves for player and rival
        p_next = [p for p in self.succ(self.pos)]
        en_next = [p for p in self.succ(self.en_pos)]

        #weigths
        w_stuck = 0.1 * self.penalty_score  #weight for penalty of bed moving position, getting stuck and etc.
        w_score = 0.3  #weight for speculative score (score not yet achieved)

        #check waste of space
        stuck = [0.0, 0.0]  #0- player 1, 1- player 2
        nxt = p_next
        stuck[0] = self.stuck_val(nxt) * w_stuck
        nxt = en_next
        stuck[1] = self.stuck_val(nxt) * w_stuck

        ##stuck[0] = 4-len(p_next) if p_next is not [] else -1
        ##stuck[1] = 4-len(en_next) if en_next is not [] else -1

        ##return stuck[0], stuck[1]

        #get fruits on board which are closer to us or to opponent, and distance is lower than duration of fruit
        fruits = [0.0, 0.0]
        for pos in self.fruits.keys():
            d1 = self.distance(self.pos, pos)
            d2 = self.distance(self.en_pos, pos)
            dur = self.fruits[pos]['duration']
            if d1 <= dur or d2 <= dur:
                fruits = [fruits[0] + self.fruits[pos]['value'] * w_score, fruits[1]] if d1 > d2 else [fruits[0], fruits[1] + self.fruits[pos]['value'] * w_score]

        return self.score + fruits[0] - stuck[0], self.en_score + fruits[1] - stuck[1]  # score is the real points taken so far by each player

    @staticmethod
    def stuck_val(nxt):
        if len(nxt) == 0:
            return 10
        elif len(nxt) == 2:
            if (nxt[0][0] == nxt[1][0] and nxt[0][1] != nxt[1][1]) or (nxt[0][1] == nxt[1][1] and nxt[0][0] != nxt[1][0]):
                return 1
            else:
                return 0.1
        elif len(nxt) == 1:
            return 0.25
        else:
            return 0


    @staticmethod
    def distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    @staticmethod
    def count_ones(board):
        counter = len(np.where(board == 2)[0])
        return counter