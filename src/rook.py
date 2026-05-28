from typing import TYPE_CHECKING

from src.piece import Piece

if TYPE_CHECKING:
    from board import Board


class Rook(Piece):
    def __init__(self, starting_coordinates: tuple, color: str):
        super().__init__(starting_coordinates, color)

    def _can_move(self, board: "Board", new_coordinates: tuple) -> bool:
        coordinates = self.get_coordinates()

        dx = coordinates[0] == new_coordinates[0]
        dy = coordinates[1] == new_coordinates[1]

        is_straight = dx or dy

        if not is_straight:
            return False # Can't move diagonal, either dX or dY needs to stay the same
        
        dx_step = 0
        if coordinates[0] < new_coordinates[0]:
            dx_step = 1
        elif coordinates[0] > new_coordinates[0]:
            dx_step = -1

        dy_step = 0
        if coordinates[1] < new_coordinates[1]:
            dy_step = 1
        elif coordinates[1] > new_coordinates[1]:
            dy_step = -1

        check_dx = coordinates[0] + dx_step
        check_dy = coordinates[1] + dy_step

        while (check_dx, check_dy) != new_coordinates:
            piece_in_path = board.get_piece_at_coordinates(coordinates=(check_dx, check_dy))
            if piece_in_path:
                return False
            
            check_dx += dx_step
            check_dy += dy_step
        
        piece_at_new_coordinates = board.get_piece_at_coordinates(new_coordinates)
        if piece_at_new_coordinates and piece_at_new_coordinates.color == self.color:
            return False
        
        return True
            

        