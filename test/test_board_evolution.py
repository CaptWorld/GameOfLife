import os
from pathlib import Path

from main import load_board_state, next_board_state, are_two_boards_equal


def test_board_evolution():
    tests_folder: Path = Path("test", "states")
    for test_folder in os.listdir(tests_folder):
        common_path: Path = Path(tests_folder, test_folder)

        test_board = load_board_state(Path(common_path, "before.txt"))
        expected_board = load_board_state(Path(common_path, "after.txt"))

        next_board_state(test_board)

        assert are_two_boards_equal(test_board, expected_board)


if __name__ == "__main__":
    test_board_evolution()
