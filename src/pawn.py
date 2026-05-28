from typing import TYPE_CHECKING, override

from src.piece import Piece


if TYPE_CHECKING:
    from board import Board


class Pawn(Piece):
    def __init__(self, starting_coordinates: tuple, color: str):
        super().__init__(starting_coordinates, color)

    @property
    def direction(self) -> int:
        return 1 if self.color == "white" else -1

    def _can_move(self, board: "Board", new_coordinates: tuple) -> bool:
        coordinates = self.get_coordinates()

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
    
    @override
    def can_attack(self, board: "Board", new_coordinates: tuple) -> bool:
        coordinates = self.get_coordinates()

        dx = new_coordinates[0] - coordinates[0]
        dy = new_coordinates[1] - coordinates[1]

        if dx != self.direction:
            return False

        if abs(dy) != 1:
            return False

        return True