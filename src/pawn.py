import abc
from typing import TYPE_CHECKING

from src.piece import Piece


if TYPE_CHECKING:
    from board import Board


class Pawn(Piece):
    def __init__(self, starting_coordinates: tuple, color: str):
        super().__init__(starting_coordinates, color)

    @property
    def direction(self) -> int:
        return 1 if self.color == "white" else -1

    def get_coordinates(self) -> tuple:
        return self._coordinates

    def set_coordinates(self, coordinates: tuple) -> None:
        self._coordinates = coordinates

    def can_move(self, board: "Board", new_coordinates: tuple) -> bool:
        coordinates = self.get_coordinates()

        if coordinates == new_coordinates:
            return False

        if new_coordinates not in board.matrix:
            return False

        if new_coordinates[1] != coordinates[1] and new_coordinates[0] == coordinates[0]:
            return False

        if self.move_number == 0:
            if (new_coordinates[0] - coordinates[0] == 2 * self.direction and new_coordinates[1] == coordinates[1]):
                piece_in_between = board.get_piece_at_coordinates((coordinates[0] + self.direction, coordinates[1]))
                if piece_in_between:
                    return False

                piece_at_new_coordinates = board.get_piece_at_coordinates(new_coordinates)
                if not piece_at_new_coordinates:
                    return True

        if new_coordinates[0] - coordinates[0] != self.direction:
            return False

        piece_at_new_coordinates = board.get_piece_at_coordinates(new_coordinates)

        if piece_at_new_coordinates:
            if piece_at_new_coordinates.color == self.color:
                return False

            if new_coordinates[1] != coordinates[1]:
                return True

        if not piece_at_new_coordinates and coordinates[1] == new_coordinates[1]:
            return True

        return False