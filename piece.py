from king_piece import KingPiece


class Piece:
    def __init__(self, row, col, player):
        self.row = row
        self.col = col
        self.player = player
        self.symbol = player.symbol

    def move_right(self):
        if self.player.is_bottom:
            if self.row - 1 != 0:
                return Piece(self.row - 1, self.col + 1, self.player)
            else:
                return KingPiece(self.row - 1, self.col + 1, self.player)
        else:
            if self.row + 1 != 7:
                return Piece(self.row + 1, self.col + 1, self.player)
            else:
                return KingPiece(self.row + 1, self.col + 1, self.player)

    def move_left(self):
        if self.player.is_bottom:
            if self.row - 1 != 0:
                return Piece(self.row - 1, self.col - 1, self.player)
            else:
                return KingPiece(self.row - 1, self.col - 1, self.player)
        else:
            if self.row + 1 != 7:
                return Piece(self.row + 1, self.col - 1, self.player)
            else:
                return KingPiece(self.row + 1, self.col - 1, self.player)