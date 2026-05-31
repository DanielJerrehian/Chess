import tkinter as tk

from src.board import Board
from src.utils.bootstrap import pieces
from src.ui import Ui, root


board = Board()
board.pieces = pieces
distance_per_move = 10

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
ui = Ui(root, board, width=900, height=900)
ui.grid()
root.mainloop()