import pprint

from src.board import Board
from src.piece import Pawn


board = Board()
print(board._format_matrix(board.matrix))
