import numpy as np


def read_input(fn):
    with open(fn) as fh:
        blocks = fh.read().split('\n\n')

        nums = [int(x) for x in blocks[0].split(',')]

        boards = []
        for block in blocks[1:]:
            board = []
            # boards.append([])
            for row in block.split('\n'):
                board.append([int(x) for x in row.split()])
            boards.append(np.array(board))
    return nums, np.array(boards)


def check_board(board):
    dim = board.shape[0]
    for x in range(dim):
        # print(board[x, :])
        if sum(np.isnan(board[x, :])) == dim:
            return True
        if sum(np.isnan(board[:, x])) == dim:
            return True
    return False


def first_winner(boards, nums):
    for num in nums:
        boards = np.where(boards == num, np.nan, boards)
        for board in boards:
            if check_board(board):
                return board, num


def last_winner(boards, num):
    winning_boards = set()
    for num in nums:
        boards = np.where(boards == num, np.nan, boards)
        for b_ind, board in enumerate(boards):
            if b_ind in winning_boards:
                continue
            if check_board(board):
                winning_boards.add(b_ind)
                if len(winning_boards) == len(boards):
                    return board, num


def calc_score(board, num):
    return np.nansum(board) * num


fn = '04.txt'
nums, boards = read_input(fn)
board, num = first_winner(boards, nums)
print(calc_score(board, num))

board, num = last_winner(boards, nums)
print(calc_score(board, num))
