from typing import TYPE_CHECKING

from src.piece import Piece

if TYPE_CHECKING:
    from board import Board


class King(Piece):
    def __init__(self, starting_coordinates: tuple, color: str):
        super().__init__(starting_coordinates, color)
    
    def _can_move(self, board: "Board", new_coordinates: tuple) -> bool:
        coordinates = self.get_coordinates()
        
        dx = new_coordinates[0] - coordinates[0]
        dy = new_coordinates[1] - coordinates[1]
        
        if abs(dx) > 1 or abs(dy) > 1:
            return False
        
        piece_at_new_coordinates = board.get_piece_at_coordinates(new_coordinates)
        if piece_at_new_coordinates and piece_at_new_coordinates.color == self.color:
            return False

        return True