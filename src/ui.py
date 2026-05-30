import math
import tkinter as tk
from src.utils.symbols import symbols


root = tk.Tk()


class Ui(tk.Canvas):
    def __init__(self, parent, board, **kwargs):
        super().__init__(parent, **kwargs)
        self.board = board
        self.square_size = min(self.winfo_reqwidth(), self.winfo_reqheight())
        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self._click)
        self.selected_piece = None
        self.selected_coordinates = None
        self.legal_moves = []
        
    def _chess_to_canvas(self, coordinates: tuple) -> tuple:
        chess_x, chess_y = coordinates

        canvas_col = chess_y - 1
        canvas_row = 8 - chess_x

        return (canvas_row, canvas_col)


    def _canvas_to_chess(self, x: int, y: int) -> tuple:
        canvas_col = int(x // self.square_size)
        canvas_row = int(y // self.square_size)

        chess_x = 8 - canvas_row
        chess_y = canvas_col + 1

        return (chess_x, chess_y)

    def _click(self, event) -> None:
        click_coordinates = self._get_row_column_from_click_coordinates(event.x, event.y)
        piece = self.board.pieces.get(click_coordinates)
        if not self.selected_piece:
            if piece and piece.color == self.board.turn:
                self.selected_piece = piece
                self.selected_coordinates = click_coordinates
            return
        
        if piece and piece.color == self.board.turn:
            self.selected_piece = piece
            self.selected_coordinates = click_coordinates
            return

        self.board.move_piece(self.selected_piece, click_coordinates)

        self.selected_piece = None
        self.selected_coordinates = None

        self.delete("all")
        self._draw_board()
        self._draw_pieces()

    def _get_row_column_from_click_coordinates(self, x: int, y: int) -> tuple:
        return self._canvas_to_chess(x, y)

    def _draw_board(self) -> None:
        for row in range(8):
            for col in range(8):
                x0 = col * self.square_size
                y0 = row * self.square_size
                x1 = x0 + self.square_size
                y1 = y0 + self.square_size
                color = "grey" if (row + col) % 2 == 0 else "darkgrey"
                self.create_rectangle(x0, y0, x1, y1, fill=color)

    def _draw_pieces(self) -> None:
        font = f"Times {round(self.square_size / 1.5)}"

        for coordinates, piece in self.board.pieces.items():
            canvas_row, canvas_col = self._chess_to_canvas(coordinates)

            text = symbols[type(piece)][piece.color]

            x = canvas_col * self.square_size + self.square_size / 2
            y = canvas_row * self.square_size + self.square_size / 2

            self.create_text(x, y, text=text, font=font, fill=piece.color)

    def on_resize(self, event) -> None:
        width = event.width
        height = event.height
        board_size = min(width, height)
        self.square_size = board_size / 8
        self.delete("all")
        self._draw_board()
        self._draw_pieces()
        