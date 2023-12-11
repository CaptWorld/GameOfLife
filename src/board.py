# from curses import _CursesWindow
from pathlib import Path
from typing import List, Callable, Self, Tuple


class Board:
    @staticmethod
    def return_state_from_initializer(
        width: int, height: int, state_initializer: Callable[[int, int], int]
    ) -> List[List[int]]:
        return [
            [state_initializer(col, row) for col in range(width)]
            for row in range(height)
        ]

    @staticmethod
    def _validate_file_data(data: List[str]) -> Tuple[int, int]:
        height: int = len(data)
        width: int = 0 if height == 0 else len(data[0])
        for row in data:
            assert len(row) == width
            assert all(x in ["0", "1"] for x in row)
        return height, width

    @classmethod
    def from_file(cls, file_path: Path) -> Self:
        with open(file_path) as f:
            file_data: List[str] = f.read().splitlines()
            height, width = Board._validate_file_data(file_data)
            return Board(width, height, lambda col, row: int(file_data[row][col]))

    def __init__(
        self, width: int, height: int, state_initializer: Callable[[int, int], int]
    ):
        self.width: int = width
        self.height: int = height
        self.state: List[List[int]] = Board.return_state_from_initializer(
            width, height, state_initializer
        )

    def render(self, stdscr) -> None:
        common_string: str = "-" * (self.width + 2)
        stdscr.addstr(0, 0, common_string)
        for row in range(self.height):
            stdscr.addch(row + 1, 0, "|")
            stdscr.addstr(
                "".join(
                    [
                        "*" if self.state[row][col] == 1 else " "
                        for col in range(self.width)
                    ]
                )
            )
            stdscr.addch("|")
        stdscr.addstr(self.height + 1, 0, common_string)
        stdscr.refresh()

    def evolve(self) -> None:
        self.state = Board.return_state_from_initializer(
            self.width, self.height, self._next_state_of_cell
        )

    def _next_state_of_cell(self, col: int, row: int) -> int:
        alive_neighbours: int = self._alive_neighbours(col, row)
        return int(alive_neighbours in ([2, 3] if self.state[row][col] else [3]))

    def _alive_neighbours(self, col: int, row: int) -> int:
        min_row: int = max(row - 1, 0)
        max_row: int = min(row + 1, self.height - 1)
        min_col: int = max(col - 1, 0)
        max_col: int = min(col + 1, self.width - 1)

        alive_neighbours: int = 0
        for _row in range(min_row, max_row + 1):
            for _col in range(min_col, max_col + 1):
                if _col != col or _row != row:
                    alive_neighbours += self.state[_row][_col]
        return alive_neighbours

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Board):
            return NotImplemented
        return (
            self.height == __value.height
            and self.width == __value.width
            and self.state == __value.state
        )
