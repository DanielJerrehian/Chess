from dataclasses import dataclass

from src.piece import Piece


@dataclass
class MoveState:
    piece: "Piece"
    old_coordinates: tuple
    new_coordinates: tuple
    captured_piece: Piece | None
    captured_coordinates: tuple | None
    en_passant_captured_piece: Piece | None = None