import graphics
from graphics import *
from board import Board, Direction
from empty_piece import EmptyPiece


length = 500
height = 500

# Divided by 8 since board is of 8 * 8 dimension.

x_box_size = length / 8
y_box_size = height / 8
checker_board = graphics.GraphWin("Checkers", length, height)

# Used to draw the checkers board.It is a square board of 8 * 8 separately filled boxes.
def draw_checker_board():
    color_shade = False
    for x in range(0, 8):
        if x % 2 == 1:
            color_shade = True
        else:
            color_shade = False
        for y in range(0, 8):
            point = Point(x * x_box_size, y * y_box_size)
            board_box = graphics.Rectangle(point, Point(point.x + x_box_size, point.y + y_box_size))
            board_box.setFill("White")
            if color_shade:
                if x % 2 == 0 or y % 2 == 0:
                    board_box.setFill("#0d0d0c")
            elif x % 2 == 1 or y % 2 == 1:
                board_box.setFill("#0d0d0c")
            board_box.draw(checker_board)


def findPiece(click):
    click_x = click.x/62.5
    click_y = click.y/62.5
    for x in range(0, 8):
        for y in range(0, 8):
            if (click_x > x and click_y > y) and (click_x < x+1 and click_y < y+1):
                return (y, x)
    return None

def choosename():
    win = GraphWin("Enter Player Name", 300, 300)
    win.setBackground("white")
    textEntry = Entry(Point(150, 150), 25)
    textEntry.draw(win)
    win.getMouse()
    text = textEntry.getText()
    testText = Text(Point(50, 15),"Player Name : "+text)
    testText.draw(win)
    win.getMouse()
    win.close()
    return  text


def draw_checkers_piece(board_to_print):
    for row in board_to_print.board:
        for piece in row:
            if not type(piece) == EmptyPiece:
                vertices = []
                piece_x = (piece.row * 62.5) + 25
                piece_y = (piece.col * 62.5) + 25
                piece_circle = graphics.Circle(Point(piece_y, piece_x), 15)
                triangle = None
                if piece.symbol == "O":
                    piece_circle.setFill("White")
                elif piece.symbol == "X":
                    piece_circle.setFill("Red")
                elif piece.symbol == "X̂":
                    vertices.append(Point(piece_y, piece_x - 15))
                    vertices.append(Point(piece_y - 10, piece_x + 10))
                    vertices.append(Point(piece_y + 10, piece_x + 10))
                    triangle = Polygon(vertices)
                    triangle.setFill("Red")
                    triangle.draw(checker_board)
                elif piece.symbol == "Ô":
                    vertices.append(Point(piece_y, piece_x - 15))
                    vertices.append(Point(piece_y - 10, piece_x + 10))
                    vertices.append(Point(piece_y + 10, piece_x + 10))
                    triangle = Polygon(vertices)
                    triangle.setFill("White")
                    triangle.draw(checker_board)
                piece_circle.draw(checker_board)







def draw(board_to_print):
    draw_checker_board()
    draw_checkers_piece(board_to_print)
    # checker_board.getMouse()
    # checker_board.close()


def get_pos():
    click1 = checker_board.getMouse()
    cc = findPiece(click1)
    return cc

def redraw(board_to_print):
    for child in checker_board.children:
        child.undraw()
    draw_checker_board()
    draw_checkers_piece(board_to_print)


def winner(name):
    win = GraphWin("Game Over", 300, 300)
    win.setBackground("white")
    testText = Text(Point(50, 15),name+" is the Winner!!")
    testText.draw(win)
    win.getMouse()
    win.close()
    checker_board.close()

