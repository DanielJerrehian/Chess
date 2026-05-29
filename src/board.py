from __future__ import annotations
from typing import TYPE_CHECKING

from src.king import King
from src.pawn import Pawn
from src.queen import Queen
from src.rook import Rook
from src.bishop import Bishop
from src.knight import Knight
from src.utils.states import MoveState


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

        if isinstance(piece, King):
            piece_coordinates = piece.get_coordinates()
            if abs(piece_coordinates[1] - new_coordinates[1]) == 2:
                side = "king" if new_coordinates[1] == 7 else "queen"
                castle_success = self.castle(color=piece.color, side=side)
                if not castle_success:
                    return False
                return True

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

    def can_castle_kingside(self, color: str) -> bool:
        castle_coordinates = self._get_king_and_rook_coordinates_for_castling(color=color, side="king")
        if not self._verify_king_and_rook_move_numbers_equal_zero(king_coordinates=castle_coordinates["king_coordinates"], rook_coordinates=castle_coordinates["rook_coordinates"], color=color):
            return False
        if not self._verify_squares_between_king_and_rook_are_empty(king_coordinates=castle_coordinates["king_coordinates"], rook_coordinates=castle_coordinates["rook_coordinates"], side="king"):
            return False
        if self.verify_king_in_check(color=color):
            return False

        king = self.get_piece_at_coordinates(castle_coordinates["king_coordinates"])
        king_coordinate_x = castle_coordinates["king_coordinates"][0]

        if not king:
            raise ValueError(f"King not found on board for color '{color}")

        for coordinate_y in range(6, 8):
            if not self.would_move_be_legal(piece=king, new_coordinates=(king_coordinate_x, coordinate_y)):
                return False
            
        return True

    def can_castle_queenside(self, color: str) -> bool:
        castle_coordinates = self._get_king_and_rook_coordinates_for_castling(color=color, side="queen")
        if not self._verify_king_and_rook_move_numbers_equal_zero(king_coordinates=castle_coordinates["king_coordinates"],rook_coordinates=castle_coordinates["rook_coordinates"], color=color):
            return False
        if not self._verify_squares_between_king_and_rook_are_empty(king_coordinates=castle_coordinates["king_coordinates"], rook_coordinates=castle_coordinates["rook_coordinates"], side="queen"):
            return False
        if self.verify_king_in_check(color=color):
            return False
        
        king = self.get_piece_at_coordinates(castle_coordinates["king_coordinates"])
        king_coordinate_x = castle_coordinates["king_coordinates"][0]

        if not king:
            raise ValueError(f"King not found on board for color '{color}")

        for coordinate_y in range(3, 5):
            if not self.would_move_be_legal(piece=king, new_coordinates=(king_coordinate_x, coordinate_y)):
                return False
            
        return True

    def _get_king_and_rook_coordinates_for_castling(self, color: str, side: str) -> dict:
        king_coordinates = None
        rook_coordinates = None
        if color == "white":
            king_coordinates = (1, 5)
            if side == "queen":
                rook_coordinates = (1, 1)
            elif side == "king":
                rook_coordinates = (1, 8)
        elif color == "black":
            king_coordinates = (8, 5)
            if side == "queen":
                rook_coordinates = (8, 1)
            elif side == "king":
                rook_coordinates = (8, 8)

        return {"king_coordinates": king_coordinates, "rook_coordinates": rook_coordinates}

    def _verify_king_and_rook_move_numbers_equal_zero(self, king_coordinates: tuple, rook_coordinates: tuple, color: str) -> bool:
        if not king_coordinates:
            raise ValueError("King coordinates are None")

        if not rook_coordinates: 
            raise ValueError("Rook coordinates are None")
        
        king = self.get_piece_at_coordinates(coordinates=king_coordinates)
        king_move_number = king.move_number if king else None

        rook = self.get_piece_at_coordinates(coordinates=rook_coordinates)
        rook_move_number = rook.move_number if rook else None
        
        if king_move_number == None:
            raise ValueError(f"No king found for color {color}")

        if rook_move_number == None:
            raise ValueError(f"No rook found for color {color}")
        
        if king_move_number != 0 or rook_move_number != 0:
            return False
        
        return True

    def _verify_squares_between_king_and_rook_are_empty(self, king_coordinates: tuple, rook_coordinates: tuple, side: str) -> bool:
        coordinate_x = king_coordinates[0]
        
        lower_bound = king_coordinates[1] + 1 if side == "king" else rook_coordinates[1] + 1
        upper_bound = rook_coordinates[1] if side == "king" else king_coordinates[1]
        
        for coordinate_y in range(lower_bound, upper_bound):
            if self.get_piece_at_coordinates((coordinate_x, coordinate_y)):
                return False
            
        return True

    def castle(self, color: str, side: str) -> bool:
        castle_coordinates = self._get_king_and_rook_coordinates_for_castling(color=color, side=side)

        king = self.get_piece_at_coordinates(castle_coordinates["king_coordinates"])
        king_coordinate_x = castle_coordinates["king_coordinates"][0]

        rook = self.get_piece_at_coordinates(coordinates=castle_coordinates["rook_coordinates"])
        rook_coordinate_x = castle_coordinates["rook_coordinates"][0]
        
        rook_target = None
        king_target = None

        if side == "king":
            if not self.can_castle_kingside(color=color):
                return False
            rook_target = (rook_coordinate_x, 6)
            king_target = (king_coordinate_x, 7)
        
        elif side == "queen":
            if not self.can_castle_queenside(color=color):
                return False
            rook_target = (rook_coordinate_x, 4)
            king_target = (king_coordinate_x, 3)

        if not rook_target or not king_target:
            raise ValueError(f"Invalid value for side: '{side}' - value must be either 'king' or 'queen'")

        king_move_state = self._create_move_state(king, king_target)
        rook_move_state = self._create_move_state(rook, rook_target)

        self._apply_move(king_move_state)
        self._apply_move(rook_move_state)

        self.turn = "black" if self.turn == "white" else "white"

        return True

