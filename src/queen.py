from typing import TYPE_CHECKING

from src.piece import Piece

if TYPE_CHECKING:
    from board import Board


class Queen(Piece):
    def __init__(self, starting_coordinates: tuple, color: str):
        super().__init__(starting_coordinates, color)
    
    def _can_move(self, board: "Board", new_coordinates: tuple) -> bool:
        coordinates = self.get_coordinates()

        dx = new_coordinates[0] - coordinates[0]
        dy = new_coordinates[1] - coordinates[1]

        is_straight = dx == 0 or dy == 0
        is_diagonal = abs(dx) == abs(dy)

        if not is_straight and not is_diagonal:
            return False

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
            