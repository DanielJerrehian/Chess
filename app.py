from src.board import Board
from src.bishop import Bishop


board = Board()
# print(board._format_matrix(board.matrix))


bishop = Bishop(starting_coordinates=(1,1), color="black")
bishop.can_move(board=board, new_coordinates=(2,2))
# print(is_straight)