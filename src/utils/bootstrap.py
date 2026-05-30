from src.rook import Rook
from src.knight import Knight
from src.bishop import Bishop
from src.queen import Queen
from src.king import King
from src.pawn import Pawn


pieces = {
    (1,1): Rook((1, 1), "white"),
    (1,2): Knight((1, 2), "white"),
    (1,3): Bishop((1, 3), "white"),
    (1,4): Queen((1, 4), "white"),
    (1,5): King((1, 5), "white"),
    (1,6): Bishop((1, 6), "white"),
    (1,7): Knight((1, 7), "white"),
    (1,8): Rook((1, 8), "white"),
    (2,1): Pawn((2, 1), "white"),
    (2,2): Pawn((2, 2), "white"),
    (2,3): Pawn((2, 3), "white"),
    (2,4): Pawn((2, 4), "white"),
    (2,5): Pawn((2, 5), "white"),
    (2,6): Pawn((2, 6), "white"),
    (2,7): Pawn((2, 7), "white"),
    (2,8): Pawn((2, 8), "white"),
    (7,1): Pawn((7, 1), "black"),
    (7,2): Pawn((7, 2), "black"),
    (7,3): Pawn((7, 3), "black"),
    (7,4): Pawn((7, 4), "black"),
    (7,5): Pawn((7, 5), "black"),
    (7,6): Pawn((7, 6), "black"),
    (7,7): Pawn((7, 7), "black"),
    (7,8): Pawn((7, 8), "black"),
    (8,1): Rook((8, 1), "black"),
    (8,2): Knight((8, 2), "black"),
    (8,3): Bishop((8, 3), "black"),
    (8,4): Queen((8, 4), "black"),
    (8,5): King((8, 5), "black"),
    (8,6): Bishop((8, 6), "black"),
    (8,7): Knight((8, 7), "black"),
    (8,8): Rook((8, 8), "black")
}