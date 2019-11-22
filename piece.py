class Piece:
    def __init__(self, row, col, player, is_king=False):
        self.row = row
        self.col = col
        self.player = player
        if not is_king:
            self.symbol = player.symbol
        else:
            self.symbol = player.king_symbol

    def move_right(self):
        if self.player.is_bottom:
            if self.row - 1 != 0:
                return Piece(self.row - 1, self.col + 1, self.player)
            else:
                return Piece(self.row - 1, self.col + 1, self.player, True)
        else:
            if self.row + 1 != 7:
                return Piece(self.row + 1, self.col + 1, self.player)
            else:
                return Piece(self.row + 1, self.col + 1, self.player, True)

    def move_left(self):
        if self.player.is_bottom:
            if self.row - 1 != 0:
                return Piece(self.row - 1, self.col - 1, self.player)
            else:
                return Piece(self.row - 1, self.col - 1, self.player, True)
        else:
            if self.row + 1 != 7:
                return Piece(self.row + 1, self.col - 1, self.player)
            else:
                return Piece(self.row + 1, self.col - 1, self.player, True)