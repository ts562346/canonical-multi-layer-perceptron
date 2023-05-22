import time
from two_d_set import two_d_set
import random

NUM_POINTS = 6


class backgammon:

    def gen_moves(self):
        self.moves = two_d_set()
        if self.dice1 != self.dice2:
            for i in range(0, 6):
                first_board = self.move_check(i, self.dice1, self.board)
                if first_board == None:
                    continue
                jx = 0
                for j in range(0, 6):
                    final_board = self.move_check(j, self.dice2, first_board)
                    if final_board == None:
                        jx += 1
                        if jx == 6:
                            self.moves.add_array(first_board)
                        continue
                    else:
                        self.moves.add_array(final_board)

            for i in range(0, 6):
                first_board = self.move_check(i, self.dice2, self.board)
                if first_board == None:
                    continue
                jx = 0
                for j in range(0, 6):
                    final_board = self.move_check(j, self.dice1, first_board)
                    if final_board == None:
                        jx += 1
                        if jx == 6:
                            self.moves.add_array(first_board)
                        continue
                    else:
                        self.moves.add_array(final_board)

        else:
            for i in range(0, 6):
                first_board = self.move_check(i, self.dice1, self.board)
                if first_board == None:
                    continue
                jx = 0
                for j in range(0, 6):
                    second_board = self.move_check(j, self.dice1, first_board)
                    if second_board == None:
                        jx += 1
                        if jx == 6:
                            self.moves.add_array(first_board)
                        continue
                    kx = 0
                    for k in range(0, 6):
                        third_board = self.move_check(k, self.dice1, second_board)
                        if third_board == None:
                            kx += 1
                            if kx == 6:
                                self.moves.add_array(second_board)
                            continue
                        lx = 0
                        for l in range(0, 6):
                            final_board = self.move_check(l, self.dice1, third_board)
                            if final_board == None:
                                lx += 1
                                if lx == 6:
                                    self.moves.add_array(third_board)
                                continue
                            else:
                                self.moves.add_array(final_board)
        if len(self.moves) == 0:  # PASS turn
            self.moves.add_array(self.board)
        return self.moves

    def __init__(self):
        self.moves_info = []
        self.genarateBoard()
        self.dice1 = self.roll()
        self.dice2 = self.roll()
        self.winner = None
        self.moves = self.gen_moves()

    def random_board(self):
        board = [0] * NUM_POINTS
        checkers = 15
        length = len(board)
        arr = [0, 1, 2, 3, 4, 5]

        # Shuffle the array
        random.shuffle(arr)

        for idx, point in enumerate(arr):
            if idx == 0:
                board[point] = self.rng(0, 8)
            elif idx == length - 1:
                board[point] = abs(sum(board) - 15)
                continue
            else:
                board[point] = self.rng(0, checkers)
            checkers = checkers - board[point]
        return board

    def flip_coin(self):
        black = self.rng(0, 1)
        if black == 0:
            return [0, 1]
        if black == 1:
            return [1, 0]

    def genarateBoard(self):
        off = [0, 0]
        turn = self.flip_coin()
        white = self.random_board()
        black = self.random_board()
        self.board = white + black + off + turn

    def check_winner(self):
        self.winner = None
        if self.board[12] == 15:
            self.winner = "WHITE"
        elif self.board[13] == 15:
            self.winner = "BLACK"

    def get_winner(self):
        return self.winner

    def get_moves(self):
        return self.moves

    def get_board(self):
        return self.board

    def move_check(self, point, roll, board):
        player = board.copy()
        if player[14] == 1:
            min = 0
            max = 6
            new_move = player[min:max]
            off_idx = 12
        else:
            min = 6
            max = 12
            new_move = player[min:max]
            off_idx = 13

        highest_point = next((i for i, x in enumerate(new_move) if x != 0), None)
        if highest_point == None or new_move[point] == 0:
            return None
        if point < highest_point:
            return None
        if (point == highest_point) and (point + roll >= 6):
            new_move[point] -= 1
            player[off_idx] += 1
        elif (point + roll == 6):
            new_move[point] -= 1
            player[off_idx] += 1
        elif (point + roll < 6):
            new_move[point] -= 1
            new_move[point + roll] += 1
        else:
            return None

        player[min:max] = new_move

        return player

    def make_move(self, new_board):
        self.board = new_board
        self.moves_info = []
        self.dice1 = self.roll()
        self.dice2 = self.roll()
        self.check_winner()
        self.gen_moves()

    def roll(self):
        return self.rng(1, 6)

    def rng(self, min, max):
        return random.randint(min, max)

    def get_next_move(moves):
        for move in moves:
            yield move

    def score_move(self, move_array, scalar_value):
        move_info = {
            "move": move_array,
            "score": scalar_value
        }
        self.moves_info.append(move_info)
        if len(self.moves_info) == len(self.moves):
            if self.board[14] == 1:
                self.make_move(self.get_best_move())
            else:
                self.make_move(self.get_best_move(highest_score=False))

    def get_best_move(self, highest_score=True):
        if len(self.moves_info) == 0:
            return None

        best_move = None
        if highest_score:
            best_move = max(self.moves_info, key=lambda x: x["score"])
            print(best_move)
        else:
            best_move = min(self.moves_info, key=lambda x: x["score"])
            print(best_move)

        return best_move["move"]