import abc

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board


class Piece(abc.ABC):
    def __init__(self, starting_coordinates: tuple, color: str) -> None:
        self._coordinates = (starting_coordinates)
        self.color = color
        self.move_number = 0
    
    @abc.abstractmethod
    def get_coordinates(self) -> None:
        """Change coordinates of a piece"""

    @abc.abstractmethod
    def set_coordinates(self, coordinates: tuple) -> None:
        """Change coordinates of a piece"""  
    
    @abc.abstractmethod
    def can_move(self, board: "Board", new_coordinates: tuple) -> bool:
        """Whether the piece can legally move to a new set of coordinates"""