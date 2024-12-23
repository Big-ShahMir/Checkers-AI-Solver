import argparse
import copy
import sys
import time

cache = {}  # you can use this to implement state caching


class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board):

        self.board = board

        self.width = 8
        self.height = 8

    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")


def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']


def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'


def read_from_file(filename):

    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board


def get_king(chara):
    if chara == "r":
        return "R"
    else:
        return "C"


def get_moves(state: State, cha: list[str]):

    brd = state.board
    potential = []
    has_jumps = False
    jump_moves = []
    moves = None

    for row in range(len(brd)):
        for col in range(len(brd[row])):
            if brd[row][col] in cha:
                if brd[row][col].upper() == 'B':
                    moves = check_jump_b(state, col, row, brd[row][col],
                                         brd[row][col] == 'B')
                elif brd[row][col].upper() == 'R':
                    moves = check_jump_r(state, col, row, brd[row][col],
                                         brd[row][col] == 'R')

                if moves:
                    has_jumps = True
                    jump_moves.extend(moves)

    if has_jumps:
        return jump_moves

    for row in range(len(brd)):
        for col in range(len(brd[row])):
            if brd[row][col] in cha:
                if brd[row][col] == "B":
                    potential.extend(basic_king_moves(state, "B", col, row))
                elif brd[row][col] == "r":
                    potential.extend(get_regular_moves(state, "r", col, row,
                                                       forward_direction=-1))
                elif brd[row][col] == "R":
                    potential.extend(basic_king_moves(state, "R", col, row))
                elif brd[row][col] == "b":
                    potential.extend(get_regular_moves(state, "b", col, row,
                                                       forward_direction=1))

    return potential


def get_regular_moves(state: State, cha: str, x: int, y: int,
                      forward_direction: int):

    successors = []
    brd = state.board
    king_row = 0 if cha == 'r' else 7
    king_char = 'R' if cha == 'r' else 'B'

    for dx in [-1, 1]:
        new_x = x + dx
        new_y = y + forward_direction

        if 0 <= new_x < 8 and 0 <= new_y < 8 and brd[new_y][new_x] == ".":
            new_board = copy.deepcopy(brd)
            new_board[y][x] = "."
            # change to king
            new_board[new_y][new_x] = king_char if new_y == king_row else cha
            successors.append(State(new_board))

    return successors


def check_jump_r(state: State, x: int, y: int, cha: str, king: bool):

    potential_successor = []
    ops = get_opp_char(cha)
    brd = state.board

    def attempt_jump(x_dir, y_dir):
        new_x, new_y = x + 2 * x_dir, y + 2 * y_dir
        mid_x, mid_y = x + x_dir, y + y_dir

        if (0 <= new_x < 8 and 0 <= new_y < 8 and
                brd[new_y][new_x] == "." and
                brd[mid_y][mid_x] in ops):

            new_board = copy.deepcopy(brd)
            new_board[y][x] = "."
            new_board[mid_y][mid_x] = "."
            new_board[new_y][new_x] = "R" if new_y == 0 else cha

            new_state = State(new_board)
            #checing for jumps
            further_jumps = check_jump_r(new_state, new_x, new_y, cha, king)
            if further_jumps:
                potential_successor.extend(further_jumps)
            else:
                potential_successor.append(new_state)

    attempt_jump(-1, -1)
    attempt_jump(1, -1)
    if king:
        attempt_jump(-1, 1)
        attempt_jump(1, 1)
    return potential_successor


def check_jump_b(state: State, x: int, y: int, cha: str, king: bool):

    potential_successor = []
    ops = get_opp_char(cha)
    brd = state.board

    def attempt_jump(x_dir, y_dir):
        new_x, new_y = x + 2 * x_dir, y + 2 * y_dir
        mid_x, mid_y = x + x_dir, y + y_dir

        if (0 <= new_x < 8 and 0 <= new_y < 8 and
                brd[new_y][new_x] == "." and
                brd[mid_y][mid_x] in ops):

            new_board = copy.deepcopy(brd)
            new_board[y][x] = "."
            new_board[mid_y][mid_x] = "."
            new_board[new_y][new_x] = "B" if new_y == 7 else cha

            new_state = State(new_board)
            # Check for additional jumps
            further_jumps = check_jump_b(new_state, new_x, new_y, cha, king)
            if further_jumps:
                potential_successor.extend(further_jumps)
            else:
                potential_successor.append(new_state)

    attempt_jump(-1, 1)
    attempt_jump(1, 1)
    if king:
        attempt_jump(-1, -1)
        attempt_jump(1, -1)
    return potential_successor


def basic_king_moves(state: State, cha: str, x: int, y: int):

    successors = []
    brd = state.board

    for move_x, move_y in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        new_x = x + move_x
        new_y = y + move_y

        if (0 <= new_x < 8 and 0 <= new_y < 8 and
                brd[new_y][new_x] == "."):

            new_board = copy.deepcopy(brd)
            new_board[y][x] = "."
            new_board[new_y][new_x] = cha
            successors.append(State(new_board))

    return successors


def node_ordering(states: list[State], current_turn: str):
    evaluated_states = [(state, evalu(state, current_turn)) for state in states]
    sorted_states = sorted(evaluated_states, key=lambda x: x[1], reverse=True)
    return [state for state, _ in sorted_states]


def node_ordering_b(states: list[State], current_turn: str):
    evaluated_states = [(state, -evalu(state, current_turn)) for state in
                        states]
    sorted_states = sorted(evaluated_states, key=lambda x: x[1], reverse=True)
    return [state for state, _ in sorted_states]


def utility(state: State, depth: int, cha: str):
    player = cha
    if player == "r":
        return -10000000 + depth
    return 10000000 - depth


def evalu(state: State, cha: str):

    red_pieces = sum(row.count('r') for row in state.board)
    red_kings = sum(row.count('R') for row in state.board)
    black_pieces = sum(row.count('b') for row in state.board)
    black_kings = sum(row.count('B') for row in state.board)

    piece_points = 100
    king_points = 250

    material_score_red = red_pieces * piece_points + red_kings * king_points
    material_score_black = black_pieces * piece_points + black_kings * king_points
    material_score = material_score_red - material_score_black

    piece_point_grid = [
        [0, 5, 5, 0, 0, 5, 5, 0],  # Back
        [5, 10, 10, 5, 5, 10, 10, 5],
        [10, 15, 20, 20, 20, 20, 15, 10],
        [20, 25, 30, 35, 35, 30, 25, 20],
        [20, 25, 30, 35, 35, 30, 25, 20],
        [10, 15, 20, 20, 20, 20, 15, 10],
        [5, 10, 10, 5, 5, 10, 10, 5],
        [0, 5, 5, 0, 0, 5, 5, 0]  # Forward
    ]

    king_point_grid = [
        [20, 20, 20, 20, 20, 20, 20, 20],
        [20, 30, 30, 30, 30, 30, 30, 20],
        [20, 30, 40, 40, 40, 40, 30, 20],
        [20, 30, 40, 50, 50, 40, 30, 20],
        [20, 30, 40, 50, 50, 40, 30, 20],
        [20, 30, 40, 40, 40, 40, 30, 20],
        [20, 30, 30, 30, 30, 30, 30, 20],
        [20, 20, 20, 20, 20, 20, 20, 20]
    ]

    positional_score = 0
    for row in range(8):
        for col in range(8):
            piece = state.board[row][col]
            if piece == 'r':
                positional_score += piece_point_grid[row][col]
            elif piece == 'R':
                positional_score += king_point_grid[row][col]
            elif piece == 'b':
                positional_score -= piece_point_grid[7 - row][col]
            elif piece == 'B':
                positional_score -= king_point_grid[7 - row][col]

    total_score = material_score + positional_score

    return total_score


def check_terminal(state: State):
    red_pieces = sum(row.count('r') + row.count('R') for row in state.board)
    black_pieces = sum(row.count('b') + row.count('B') for row in state.board)

    if red_pieces == 0 or black_pieces == 0:
        return True

    red_moves = get_moves(state, ["r", "R"])
    black_moves = get_moves(state, ["b", "B"])

    if not red_moves or not black_moves:
        return True

    return False


def alpha_beta(state: State, alpha: float, beta: float, r_move: bool,
               depth: int = 0):
    state_key = hash(str(state.board))
    if state_key in cache:
        cache_util = cache[state_key]["utility"]
        cache_depth = cache[state_key]["depth"]
        cache_player = cache[state_key]["player"]
        cache_alpha = cache[state_key]["alpha"]
        cache_beta = cache[state_key]["beta"]
        player = "r" if r_move else "b"
        # if depth >= cache_depth and alpha <= cache_alpha and \
        #         beta >= cache_beta:
        if depth >= cache_depth:
            if player == "r":
                return state, cache_util
            else:
                return state, -cache_util
        # if depth >= cache_depth and player == cache_player and player == "r":
        #     return state, cache_util
        # elif depth >= cache_depth and player == cache_player and player == "b":
        #     return state, -cache_util
    # Check if it is a terminal state: winning or losing game
    if check_terminal(state):
        if r_move:
            cache[state_key] = {"depth": depth,
                                "utility": utility(state, depth, "r"), "alpha":
                                    alpha, "beta": beta, "player": "r"}
            return state, utility(state, depth, "r")
        else:
            cache[state_key] = {"depth": depth,
                                "utility": utility(state, depth, "b"), "alpha":
                                    alpha, "beta": beta, "player": "b"}
            return state, utility(state, depth, "b")

    if depth == 12:
        cha = "r" if r_move else "b"
        if cha == "r":
            return state, evalu(state, cha)
        else:
            return state, -evalu(state, cha)
        # return state, endgame_evalu(state, cha)

    if r_move:
        # return max_value(state, alpha, beta, depth)
        ret = max_value(state, alpha, beta, depth)
        cache[state_key] = {"depth": depth, "utility": ret[1], "alpha":
            alpha, "beta": beta, "player": "r"}
        return ret
    else:
        # return min_value(state, alpha, beta, depth)
        ret = min_value(state, alpha, beta, depth)
        cache[state_key] = {"depth": depth, "utility": -ret[1], "alpha":
            alpha, "beta": beta, "player": "b"}
        return ret


def max_value(state: State, alpha: float, beta: float, depth: int):
    key = hash(state)
    max_v = -float("inf")
    best_move = None
    moves = get_moves(state, ["r", "R"])
    moves = node_ordering(moves, "r")
    # moves.sort(key=lambda s: evalu(s, "r"), reverse=True)
    # moves = endgame_node_ordering(moves, "r")
    # moves.reverse()
    for move in moves:
        next_value = alpha_beta(move, alpha, beta, False, depth + 1)
        if next_value[1] > max_v:
            max_v = next_value[1]
            best_move = move
        alpha = max(alpha, max_v)
        if beta <= alpha:
            break
    # cache[key] = {"depth": depth, "utility": max_v, "alpha": alpha, "beta":
    #     beta, "player": "r"}
    return best_move, max_v


def min_value(state: State, alpha: float, beta: float, depth: int):
    key = hash(state)
    min_v = float("inf")
    best_move = None
    moves = get_moves(state, ["b", "B"])
    moves = node_ordering_b(moves, "b")
    # moves.reverse()
    # moves.sort(key=lambda s: evalu(s, "r"), reverse=False)
    # moves = endgame_node_ordering(moves, "b")
    for move in moves:
        next_value = alpha_beta(move, alpha, beta, True, depth + 1)
        if next_value[1] < min_v:
            min_v = next_value[1]
            best_move = move
        beta = min(beta, min_v)
        if alpha >= beta:
            break
    # cache[key] = {"depth": depth, "utility": min_v, "alpha": alpha, "beta":
    #     beta, "player": "b"}
    return best_move, min_v


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    initial_board = read_from_file(args.inputfile)
    state = State(initial_board)
    # turn = 'r'
    # ctr = 0
    #
    # sys.stdout = open(args.outputfile, 'w')
    #
    #
    # sys.stdout = sys.__stdout__
    initial_state = State(initial_board)

    # Set the initial parameters for alpha-beta pruning
    alpha = -float('inf')
    beta = float('inf')
    red_player_turn = True  # Assuming red player moves first
    depth = 0

    # Start alpha-beta pruning to find the best move
    # best_move, _ = alpha_beta(initial_state, (alpha), (beta), red_player_turn,
    #                           depth)

    best_move = initial_state
    # best_move.display()
    # count = 1
    # while not check_terminal(best_move):
    #     print(count)
    #     count += 1
    #     best_move, p = alpha_beta(best_move, (alpha), (beta),
    #                               red_player_turn, depth)
    #     best_move.display()
    #     print(p)
    #     if red_player_turn:
    #         red_player_turn = False
    #     else:
    #         red_player_turn = True

    # cha = ["r", "R"]
    # # cha = ["b", "B"]
    # move = get_moves(initial_state, cha)
    # move = node_ordering(move, "r")
    # for moves in move:
    #     print("------------")
    #     moves.display()
    #     print(evalu(moves, cha[0]))
    #
    #     a, b = alpha_beta(moves, alpha, beta, False, depth)
    #     # a.display()
    #     print(b)
    #     print("------------")

    with open(args.outputfile, 'w') as f:
        sys.stdout = f
        best_move.display()
        while not check_terminal(best_move):
            # print(count)
            # count += 1
            best_move, p = alpha_beta(best_move, (alpha), (beta),
                                      red_player_turn, depth)
            best_move.display()
            # print(p)
            if red_player_turn:
                red_player_turn = False
            else:
                red_player_turn = True
