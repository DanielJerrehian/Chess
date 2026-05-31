import abc

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board


class Piece(abc.ABC):
    def __init__(self, starting_coordinates: tuple, color: str) -> None:
        self._coordinates = starting_coordinates
        self.color = color
        self.move_number = 0

    def get_coordinates(self) -> tuple | None:
        """Get coordinates of a piece"""
        return self._coordinates

    def set_coordinates(self, coordinates: tuple | None) -> None:
        """Change coordinates of a piece"""
        self._coordinates = coordinates
    
    def can_move(self, board: "Board", new_coordinates: tuple) -> bool:
        if self.get_coordinates() == new_coordinates:
            return False

        if new_coordinates not in board.matrix:
            return False
        
        return self._can_move(board, new_coordinates)
    
    def can_attack(self, board: "Board", coordinates: tuple) -> bool:
        return self.can_move(board, coordinates)
    
    def get_legal_moves(self, board: "Board") -> list[tuple]:
        legal_moves = []

        for coordinate in board.matrix:
            if not self.can_move(board, coordinate):
                continue

            if board.would_move_be_legal(self, coordinate):
                legal_moves.append(coordinate)
        return legal_moves

    @abc.abstractmethod
    def _can_move(self, board: "Board", new_coordinates: tuple) -> bool:
        """Whether the piece can legally move to a new set of coordinates"""
