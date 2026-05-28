from typing import TYPE_CHECKING

from src.piece import Piece

if TYPE_CHECKING:
    from board import Board


class Knight(Piece):
    def __init__(self, starting_coordinates: tuple, color: str):
        super().__init__(starting_coordinates, color)

    def _can_move(self, board: "Board", new_coordinates: tuple) -> bool:
        coordinates = self.get_coordinates()

        dx = new_coordinates[0] - coordinates[0] 
        dy = new_coordinates[1] - coordinates[1] 

        if dx == 0 or dy == 0:
            return False
        
        if (abs(dx) + abs(dy) != 3):
            return False
        
        piece_at_coordinates = board.get_piece_at_coordinates(coordinates=new_coordinates)
        if not piece_at_coordinates:
            return True
        
        if piece_at_coordinates.color != self.color:
            return True
        
        return False