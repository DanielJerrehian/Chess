from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from piece import Piece


class Board:
    width: int = 8
    height: int = 8

    def __init__(self) -> None:
        self.matrix: tuple = self._create_matrix()
        self.pieces: dict = {}

    def _create_matrix(self) -> tuple:
        matrix = []
        for x in range(1, Board.width + 1):
            for y in range(1, Board.width + 1):
                coordinate = (x, y)
                matrix.append(coordinate)
        return tuple(matrix)
    
    def _format_matrix(self, matrix: tuple) -> str:
        matrix = str(matrix).replace(" ", "")[1:-1]
        pretty = []
        row = []
        for coordinate in matrix.split("),"):
            if not coordinate.endswith(")"):
                coordinate += ")"
            row.append(coordinate)
            if coordinate.endswith(",8)"):
                pretty.append(",".join(row))
                row = []
        return "\n".join(pretty[::-1])
    
    def add_piece(self, piece: "Piece") -> None:
        self.pieces[piece.get_coordinates()] = piece

    def are_valid_coordinates(self, coordinates: tuple) -> bool:
        if coordinates in self.matrix:
            return True
        return False
    
    def get_piece_at_coordinates(self, coordinates: tuple) -> "Piece" | None:
        return self.pieces.get(coordinates)

    def move_piece(self, piece: "Piece", new_coordinates: tuple) -> None:
        old_coordinates = piece.get_coordinates()

        if piece.can_move(self, new_coordinates):
            # pass
            piece.move_number += 1