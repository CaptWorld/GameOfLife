from pathlib import Path
from random import randint
import time

from board import Board


def dead_state(width: int, height: int) -> Board:
    return Board(width, height, lambda col, row: 0)


def random_state(width: int, height: int) -> Board:
    return Board(width, height, lambda col, row: randint(0, 1))


def load_board_state(file_path: Path) -> Board:
    return Board.from_file(file_path)


def next_board_state(board: Board):
    board.evolve()


def render(board: Board) -> None:
    board.render()


def are_two_boards_equal(board1: Board, board2: Board) -> bool:
    return board1 == board2


def play_game_of_life(board: Board) -> None:
    while True:
        render(board)
        next_board_state(board)
        time.sleep(0.5)


if __name__ == "__main__":
    # board: Board = random_state(10, 10)
    board: Board = load_board_state(Path("soups", "random1.txt"))
    play_game_of_life(board)
