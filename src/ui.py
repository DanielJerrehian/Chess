import tkinter as tk
from math import ceil

from src.utils.symbols import symbols
from src.board import Board
from src.piece import Piece

root = tk.Tk()


class Ui(tk.Canvas):
    def __init__(self, parent, board: Board, **kwargs):
        super().__init__(parent, **kwargs)
        self.board = board
        self.square_size = min(.9*self.winfo_reqwidth(), .9*self.winfo_reqheight())
        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self._click)
        self.selected_piece = None
        self.selected_coordinates = None
        self.legal_moves = []
        self.highlighted_tags = []
        self.pixels_per_move = 10
        
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
        piece: Piece = self.board.pieces.get(click_coordinates)
        
        if not self.selected_piece:
            if piece and piece.color == self.board.turn:
                self.legal_moves = piece.get_legal_moves(self.board)
                self._highlight_legal_moves(self.legal_moves)
                self.selected_piece = piece
                self.selected_coordinates = click_coordinates
            return
        

        if piece and piece.color == self.board.turn:
            self.selected_piece = piece
            self._delete_previous_legal_move_highlights()
            self.legal_moves = piece.get_legal_moves(self.board)
            self._highlight_legal_moves(self.legal_moves)
            self.selected_coordinates = click_coordinates
            return
        
        if not self.board.would_move_be_legal(piece=self.selected_piece, new_coordinates=click_coordinates):
            return

        if self.board.move_piece(self.selected_piece, click_coordinates):
            self.after(
                5,
                self._animate_move,
                self.selected_piece,
                self.selected_coordinates,
                click_coordinates,
                0
            )
            self.selected_piece = None
            self.selected_coordinates = None
            
            if self.board.is_checkmate(self.board.turn):
                print(f"Team {self.board.turn} is checkmated")
                self._end_game()
            elif self.board.is_stalemate(self.board.turn):
                print("Gameover - Stalemate!")
            elif self.board.verify_king_in_check(self.board.turn):
                print(f"Team {self.board.turn} is in check")

    def _delete_previous_legal_move_highlights(self) -> None:
        for tag in self.highlighted_tags:
            self.delete(tag)
        self.highlighted_tags = []

    def _highlight_legal_moves(self, legal_moves: list[tuple]) -> None:
        self.delete("all")
        self._draw_board()
        for coordinates in legal_moves:
            x, y = self._chess_to_canvas(coordinates)
            center_x = self._get_pixel_of_square_center(y)
            center_y = self._get_pixel_of_square_center(x)
            x0 = center_x - (self.square_size / 5)
            y0 = center_y - (self.square_size / 5)
            x1 = center_x + (self.square_size / 5)
            y1 = center_y + (self.square_size / 5)
            tag = self.create_oval(x0, y0, x1, y1, fill="red")
            self.highlighted_tags.append(tag)
        self._draw_pieces(None)

    def _get_font(self) -> str:
        return f"Times {round(self.square_size / 1.5)}"

    def _get_pixel_of_square_center(self, coordinate: int) -> int:
        return coordinate * self.square_size + self.square_size / 2

    def _animate_move(self, piece, start_coordinates, end_coordinates, current_frame=0) -> None:
        start_canvas_coordinates = self._chess_to_canvas(start_coordinates)
        end_canvas_coordiantes = self._chess_to_canvas(end_coordinates)
        start_location_pixel_x = self._get_pixel_of_square_center(start_canvas_coordinates[1])
        start_location_pixel_y = self._get_pixel_of_square_center(start_canvas_coordinates[0])
        target_location_pixel_x = self._get_pixel_of_square_center(end_canvas_coordiantes[1])
        target_location_pixel_y = self._get_pixel_of_square_center(end_canvas_coordiantes[0])
        dx = target_location_pixel_x - start_location_pixel_x
        dy = target_location_pixel_y - start_location_pixel_y
        frames = int(ceil(max(abs(dx), abs(dy)) / self.pixels_per_move))
        progress = current_frame / frames
        x = start_location_pixel_x + (target_location_pixel_x - start_location_pixel_x) * progress
        y = start_location_pixel_y + (target_location_pixel_y - start_location_pixel_y) * progress
        self.delete("all")
        self._draw_board()
        self._draw_pieces(skip_piece=piece)
        self.create_text(x, y, text=symbols[type(piece)][piece.color], font=self._get_font(), fill=piece.color)
        if current_frame < frames:
            self.after(
                7,
                self._animate_move,
                piece,
                start_coordinates,
                end_coordinates,
                current_frame + 1,
            )
        else:
            self.delete("all")
            self._draw_board()
            self._draw_pieces(skip_piece=None)

    def _get_row_column_from_click_coordinates(self, x: int, y: int) -> tuple:
        return self._canvas_to_chess(x, y)

    def _get_x_y_from_chess_coordinates(self, coordinates: tuple) -> tuple:
        return  self._chess_to_canvas(coordinates)

    def _draw_board(self) -> None:
        for row in range(8):
            for col in range(8):
                x0 = col * self.square_size
                y0 = row * self.square_size
                x1 = x0 + self.square_size
                y1 = y0 + self.square_size
                color = "grey" if (row + col) % 2 == 0 else "darkgrey"
                self.create_rectangle(x0, y0, x1, y1, fill=color)

    def _draw_pieces(self, skip_piece: Piece) -> None:
        for coordinates, piece in self.board.pieces.items():
            if skip_piece and skip_piece.get_coordinates() == coordinates:
                continue
            canvas_row, canvas_col = self._chess_to_canvas(coordinates)
            text = symbols[type(piece)][piece.color]

            x = self._get_pixel_of_square_center(canvas_col)
            y = self._get_pixel_of_square_center(canvas_row)

            self.create_text(x, y, text=text, font=self._get_font(), fill=piece.color)

    def on_resize(self, event) -> None:
        width = event.width
        height = event.height
        board_size = min(width, height)
        self.square_size = board_size / 8
        self.delete("all")
        self._draw_board()
        self._draw_pieces(skip_piece=None)

    def _end_game(self, color: str):
        self.create_text(text=f"Team {color} wins!")