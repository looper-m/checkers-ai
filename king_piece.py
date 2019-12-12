class KingPiece:
    def __init__(self, row, col, player):
        self.row = row
        self.col = col
        self.player = player
        self.center = [row, col]
        self.symbol = player.king_symbol

    def move_right(self):
        if self.player.is_bottom:
            return KingPiece(self.row - 1, self.col + 1, self.player)
        else:
            return KingPiece(self.row + 1, self.col + 1, self.player)

    def move_left(self):
        if self.player.is_bottom:
            return KingPiece(self.row - 1, self.col - 1, self.player)
        else:
            return KingPiece(self.row + 1, self.col - 1, self.player)

    def move_right_backwards(self):
        if self.player.is_bottom:
            return KingPiece(self.row + 1, self.col + 1, self.player)
        else:
            return KingPiece(self.row - 1, self.col + 1, self.player)

    def move_left_backwards(self):
        if self.player.is_bottom:
            return KingPiece(self.row + 1, self.col - 1, self.player)
        else:
            return KingPiece(self.row - 1, self.col - 1, self.player)