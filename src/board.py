from __future__ import annotations
from typing import TYPE_CHECKING

from king import King
from pawn import Pawn
from queen import Queen
from rook import Rook
from bishop import Bishop
from knight import Knight
from utils.states import MoveState

if TYPE_CHECKING:
    from piece import Piece


class Board:
    width: int = 8
    height: int = 8

    def __init__(self) -> None:
        self.matrix: tuple = self._create_matrix()
        self.pieces: dict = {}
        self.turn = "white"

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
        return coordinates in self.matrix
    
    def get_piece_at_coordinates(self, coordinates: tuple) -> "Piece" | None:
        return self.pieces.get(coordinates)

    def capture_piece(self, piece: "Piece") -> None:
        old_coordinates = piece.get_coordinates()
        del self.pieces[old_coordinates]
        piece.set_coordinates(None)

    def verify_king_in_check(self, color: str) -> bool:
        kings_coordinates = None
        for coordinates, piece in self.pieces.items():
            if piece.color != color:
                continue
            if isinstance(piece, King):
                kings_coordinates = coordinates
                break

        if kings_coordinates is None:
            raise ValueError(f"No king found for color {color}")

        for coordinates, piece in self.pieces.items():
            if piece.color == color:
                continue
            if piece.can_attack(self, kings_coordinates):
                return True
        return False

    def move_piece(self, piece: "Piece", new_coordinates: tuple) -> bool:
        if piece.color != self.turn:
            return False

        if not piece.can_move(self, new_coordinates):
            return False

        if not self.would_move_be_legal(piece=piece, new_coordinates=new_coordinates):
            return False

        move_state = self._create_move_state(piece=piece, new_coordinates=new_coordinates)

        self._apply_move(move_state=move_state)

        if isinstance(move_state.piece, Pawn):
            final_row_dx = move_state.new_coordinates[0]
            if move_state.piece.color == "white" and final_row_dx == 8:
                self.upgrade_pawn(piece)
            elif move_state.piece.color == "black" and final_row_dx == 1:
                self.upgrade_pawn(piece)

        self.turn = "black" if self.turn == "white" else "white"

        if self.verify_king_in_check(self.turn):
            print(f"Color {self.turn} is in check!")

        return True

    def _undo_move(self, move_state: MoveState) -> None:
        del self.pieces[move_state.new_coordinates]
        move_state.piece.set_coordinates(move_state.old_coordinates)
        move_state.piece.move_number -= 1
        self.pieces[move_state.old_coordinates] = move_state.piece

        if move_state.captured_piece:
            move_state.captured_piece.set_coordinates(move_state.captured_coordinates)
            self.pieces[move_state.captured_coordinates] = move_state.captured_piece

    def would_move_be_legal(self, piece: "Piece", new_coordinates: tuple) -> bool:
        moving_color = self.turn
        move_state = self._create_move_state(piece=piece, new_coordinates=new_coordinates)
        
        self._apply_move(move_state=move_state)

        king_in_check = self.verify_king_in_check(color=moving_color)
        
        self._undo_move(move_state=move_state)

        return not king_in_check

    def _apply_move(self, move_state: MoveState) -> None:
        if move_state.captured_piece:
            self.capture_piece(move_state.captured_piece)

        del self.pieces[move_state.old_coordinates]
        
        move_state.piece.set_coordinates(move_state.new_coordinates)
        self.pieces[move_state.new_coordinates] = move_state.piece
        move_state.piece.move_number += 1

    def _create_move_state(self, piece: "Piece", new_coordinates: tuple) -> MoveState:
        captured_piece = self.get_piece_at_coordinates(new_coordinates)
        captured_coordinates = captured_piece.get_coordinates() if captured_piece else None

        return MoveState(
            piece=piece,
            old_coordinates=piece.get_coordinates(),
            new_coordinates=new_coordinates,
            captured_piece=captured_piece,
            captured_coordinates=captured_coordinates
        )
    
    def check_player_has_any_legal_moves(self, color: str) -> bool:
        for piece in self.pieces.values():
            if piece.color != color:
                continue
            if len(piece.get_legal_moves(self)) >= 1:
                return True
        return False
    
    def is_checkmate(self, color: str) -> bool:
        if not self.verify_king_in_check(color=color):
            return False
        
        if self.check_player_has_any_legal_moves(color=color):
            return False
        
        return True
    
    def is_stalemate(self, color: str) -> bool:
        check = self.verify_king_in_check(color=color)
        legal_moves = self.check_player_has_any_legal_moves(color=color)

        return True if not check and not legal_moves else False
    
    def upgrade_pawn(self, pawn_piece: "Piece") -> None:
        coordinates = pawn_piece.get_coordinates()
        self.pieces[coordinates] = self.get_desired_upgrade_piece(pawn_piece=pawn_piece)
        pawn_piece.set_coordinates(None)

    def get_desired_upgrade_piece(self, pawn_piece: "Piece", desired_piece: str = "queen") -> "Piece":
        options = {
            "queen": Queen(starting_coordinates=pawn_piece.get_coordinates(), color=pawn_piece.color),
            "rook": Rook(starting_coordinates=pawn_piece.get_coordinates(), color=pawn_piece.color),
            "bishop": Bishop(starting_coordinates=pawn_piece.get_coordinates(), color=pawn_piece.color),
            "knight": Knight(starting_coordinates=pawn_piece.get_coordinates(), color=pawn_piece.color)
        }
        return options[desired_piece]
        

#         Kingside castling:

# White: king e1 -> g1, rook h1 -> f1
# Black: king e8 -> g8, rook h8 -> f8

# Queenside castling:

# White: king e1 -> c1, rook a1 -> d1
# Black: king e8 -> c8, rook a8 -> d8

# Conditions checklist:

# King has never moved
# Rook involved has never moved
# Squares between king and rook are empty
# King is NOT currently in check
# King does NOT pass through check
# King does NOT end in check

# Important:

# The rook may pass through attacked squares.
# Only the king matters.

# For implementation architecture:

# You probably want:

# board.can_castle_kingside(color)
# board.can_castle_queenside(color)

# Then inside King._can_move():

# if move is 2 squares horizontally:
#     ask board if castling is legal

# Then board handles:

# rook lookup
# empty path
# attack checks
# moving rook during castle

# Your existing:

# would_move_be_legal()
# verify_king_in_check()

# already solves a huge part of this.